import re
from fastapi.responses import StreamingResponse
from abc import ABC, abstractmethod
import json
from typing import Generic, Mapping, Optional, Dict, List, Any, TypeVar


from ...clients.bedrock_client.local_interfaces_typehinter import (
    LLM_ClientPayload_TH,
)

from .bedrock_client import GenerateBedrockResponse
from ...interfaces.interfaces_th import (
    LLM_HyperParameters_TH,
    LLM_PromptTemplates_TH,
)
from .foundation_models import FoundationModels
from ...logging.base_logger import APP_LOGGER


T = TypeVar("T", bound=Mapping)


class LLMOperation(ABC, Generic[T]):

    def get_json_response(self, string: str):
        json_match = re.search(r"{.*}", string, re.DOTALL)
        if json_match:
            json_string = json_match.group(0)
            try:
                json_object = json.loads(json_string)
                return json_object
            except json.JSONDecodeError as e:
                APP_LOGGER.error(f"Error decoding JSON: {e}")
                return None
        APP_LOGGER.warning("No JSON object found in the string.")
        return None

    def __add_roles_to_prompts(
        self,
        user_prompt: str,
        system_prompt: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """Constructs a list of message dictionaries for LLM input."""
        messages = (
            [{"role": "system", "content": system_prompt}] if system_prompt else []
        )
        messages.append(dict(role="user", content=user_prompt))
        return messages

    def construct_llmclient_payload(
        self,
        system_prompt: Optional[str],
        user_prompt: str,
        model_hyperparameters: LLM_HyperParameters_TH,
        modelId: FoundationModels,
    ) -> LLM_ClientPayload_TH:
        messages = self.__add_roles_to_prompts(
            user_prompt=user_prompt, system_prompt=system_prompt
        )
        return LLM_ClientPayload_TH(
            messages=messages,
            model_hyperparameters=model_hyperparameters,
            modelId=modelId,
        )

    def call_llmclient(
        self, payload: LLM_ClientPayload_TH, streaming: bool = False
    ) -> str:

        llm_response = GenerateBedrockResponse(
            payload=payload, streaming=streaming
        ).execute()
        if llm_response is not None and not isinstance(llm_response, StreamingResponse):
            summary: str = str(llm_response.get("llm_response")).strip()
            return summary
        else:
            raise ValueError(
                "Expected a non-streaming response and received either None or a StreamingResponse"
            )

    def call_llmclient_with_retries(
        self,
        payload: LLM_ClientPayload_TH,
        max_retries: int = 3,
    ):
        for attempt in range(max_retries):
            llm_response = self.call_llmclient(payload=payload).strip()
            APP_LOGGER.info(llm_response)
            json_response = self.get_json_response(llm_response)
            APP_LOGGER.info(json_response)
            if json_response is not None:
                return json_response
            APP_LOGGER.warning(f"Attempt {attempt + 1}: Failed to extract JSON.")
        raise ValueError(f"Failed to extract JSON after {max_retries} attempts.")

    @abstractmethod
    def execute_llm_operation(self, payload: T, modelId: FoundationModels) -> Any:
        raise NotImplementedError("Subclasses must implement execute_llm_operation.")


class BaseAIEventsConfig(ABC):
    """Abstract base class for all AI event configurations subtypes."""

    @staticmethod
    @abstractmethod
    def MODEL_HYPERPARAMETERS(
        *args, **kwargs
    ) -> Dict[FoundationModels, LLM_HyperParameters_TH]:
        """Abstract property for model parameters. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement MODEL_HYPERPARAMETERS")

    @staticmethod
    @abstractmethod
    def MODEL_PROMPTS(
        *args, **kwargs
    ) -> Dict[FoundationModels, LLM_PromptTemplates_TH]:
        """Abstract property for prompts. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement MODEL_PROMPTS")

    @staticmethod
    @abstractmethod
    def BASE_OUTPUT_TOKENS() -> int:
        """Abstract property for output tokens. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement BASE_OUTPUT_TOKENS")
