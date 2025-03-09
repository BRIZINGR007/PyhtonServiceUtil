import boto3
import json
from typing import List, cast

from ...utils.env_initlializer import EnvStore
from ...ioc.singleton import SingletonMeta


class EmbeddingGenerator(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.__client = boto3.client(
            "bedrock-runtime",
            region_name=EnvStore().aws_region_name,
            aws_access_key_id=EnvStore().aws_access_key_id,
            aws_secret_access_key=EnvStore().aws_secret_access_key,
        )
        self.__model_id = "amazon.titan-embed-text-v2:0"
        self.__dimensions = 256
        self.__normalize = True

    def generate_embedding(self, input_text: str) -> List[float]:
        native_request = dict(
            inputText=input_text,
            dimensions=self.__dimensions,
            normalize=self.__normalize,
        )
        response = self.__client.invoke_model(
            modelId=self.__model_id, body=json.dumps(native_request)
        )
        bedrock_response = json.loads(response["body"].read())
        embedding = bedrock_response["embedding"]
        return cast(List[float], embedding)
