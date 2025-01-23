import json
from typing import Dict, List, Optional, Union
from fastapi.responses import StreamingResponse

from ..bedrock_client.local_interfaces_typehinter import (
    LLM_ClientPayload_TH,
)

from ..bedrock_client.call_bedrock import BedrockClient_Sync
from ..bedrock_client.fm_config import FMS_BEDROCK
from ...interfaces.interfaces_th import (
    LLM_HyperParameters_TH,
    LLM_SpecialTokens_TH,
)
from ...logging.base_logger import APP_LOGGER


class GenerateBedrockResponse:

    def __init__(
        self,
        payload: LLM_ClientPayload_TH,
        streaming: bool,
    ) -> None:
        self.bedrock_client = BedrockClient_Sync()
        self.streaming: bool = streaming
        self.messages: List[Dict[str, str]] = payload["messages"]
        self.hyper_parameters: LLM_HyperParameters_TH = payload["model_hyperparameters"]
        self.model_id = payload["modelId"].value

    def __construct_prompt_template(self, modelId: str, messages: List[dict]):
        special_tokens: LLM_SpecialTokens_TH = FMS_BEDROCK.get(modelId, {}).get(
            "special_tokens", {}
        )
        bos_token: str = str(special_tokens.get("bos_token"))
        content_start_token: str = str(special_tokens.get("content_start_token"))
        content_end_token: str = str(special_tokens.get("content_end_token"))
        provider_name = FMS_BEDROCK.get(modelId, {}).get("providerName")

        def get_start_token(role):
            if provider_name == "Meta":
                return content_start_token.format(role=role)
            elif provider_name == "Mistral AI":
                return content_start_token
            return ""

        structured_prompt = f"{bos_token}" + "\n"

        for msg in messages:
            role: str = str(msg.get("role"))
            content: str = str(msg.get("content"))
            if role in {"system", "user"}:
                structured_prompt += get_start_token(role) + "\n"
                structured_prompt += content + "\n" + content_end_token + "\n"
        if provider_name == "Meta":
            structured_prompt += "<|start_header_id|>assistant<|end_header_id|>"
        return structured_prompt

    def payload_streaming(self, provider_name: str, response_stream: dict):
        if provider_name == "Meta":
            for event in response_stream.get("body", []):
                response = json.loads(event["chunk"]["bytes"]).get("generation")
                yield json.dumps({"chunk": response}) + "\n"

        elif provider_name == "Mistral AI":
            for event in response_stream.get("body", []):
                response = (
                    json.loads(event["chunk"]["bytes"]).get("outputs")[0].get("text")
                )
                yield json.dumps({"chunk": response}) + "\n"

    def execute(self) -> Optional[Union[StreamingResponse, Dict[str, Union[str, int]]]]:
        try:
            constructed_prompt: str = self.__construct_prompt_template(
                modelId=self.model_id, messages=self.messages
            )
            payload = dict(prompt=constructed_prompt, **self.hyper_parameters)
            if self.streaming:
                provider_name: str = str(
                    FMS_BEDROCK.get(self.model_id, {}).get("providerName")
                )
                response_stream = self.bedrock_client.stream_bedrock_response(
                    payload=payload, modelId=self.model_id
                )
                return StreamingResponse(
                    self.payload_streaming(
                        provider_name, response_stream=response_stream
                    ),
                    media_type="text/event-stream",
                )
            else:
                llm_response: Dict[str, Union[str, int]] = (
                    self.bedrock_client.no_stream_bedrock_response(
                        payload=payload, modelId=self.model_id
                    )
                )
                return llm_response

        except Exception as exception:
            APP_LOGGER.error(str(exception))
        return {}
