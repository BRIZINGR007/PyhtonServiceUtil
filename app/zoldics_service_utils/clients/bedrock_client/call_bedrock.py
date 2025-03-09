import boto3
import json
from typing import Dict, Union

from ...utils.env_initlializer import EnvStore


class BedrockClient_Sync:

    def __init__(self) -> None:
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=EnvStore().aws_region_name,
            aws_access_key_id=EnvStore().aws_access_key_id,
            aws_secret_access_key=EnvStore().aws_secret_access_key,
        )

    def no_stream_bedrock_response(
        self, payload: dict, modelId: str
    ) -> Dict[str, Union[str, int]]:
        try:
            response = self.client.invoke_model(
                body=json.dumps(payload),
                modelId=modelId,
                accept="application/json",
                contentType="application/json",
            )
            body = response.get("body").read().decode("utf-8")
            response_body = json.loads(body)
            result = (
                response_body.get("generation")
                or response_body.get("outputs")[0]["text"]
            )
            tokens_count = response_body.get("generation_token_count") or None
            if tokens_count:
                return dict(llm_response=result, tokens=tokens_count)
            return dict(llm_response=result)
        except (
            self.client.exceptions.AccessDeniedException,
            self.client.exceptions.ResourceNotFoundException,
            self.client.exceptions.ThrottlingException,
            self.client.exceptions.ModelTimeoutException,
            self.client.exceptions.InternalServerException,
            self.client.exceptions.ModelStreamErrorException,
            self.client.exceptions.ValidationException,
            self.client.exceptions.ModelNotReadyException,
            self.client.exceptions.ServiceQuotaExceededException,
            self.client.exceptions.ModelErrorException,
        ) as e:
            raise e

    def stream_bedrock_response(self, payload=None, modelId=None):
        try:
            response_stream = self.client.invoke_model_with_response_stream(
                body=json.dumps(payload),
                modelId=modelId,
                accept="application/json",
                contentType="application/json",
            )
            return response_stream
        except (
            self.client.exceptions.AccessDeniedException,
            self.client.exceptions.ResourceNotFoundException,
            self.client.exceptions.ThrottlingException,
            self.client.exceptions.ModelTimeoutException,
            self.client.exceptions.InternalServerException,
            self.client.exceptions.ModelStreamErrorException,
            self.client.exceptions.ValidationException,
            self.client.exceptions.ModelNotReadyException,
            self.client.exceptions.ServiceQuotaExceededException,
            self.client.exceptions.ModelErrorException,
        ) as e:
            raise e
