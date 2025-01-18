import boto3
import json
from typing import final, Dict
from decouple import config
from typing import TypedDict, Required, Any, cast
import uuid

from .helpers import Helpers
from .queue_config import QUEUE_CONFIG
from ...logging.base_logger import APP_LOGGER
from ...context.vars import headers_context


class Message_Payload_TypeHinter(TypedDict, total=False):
    action: Required[str]
    payload: Dict[str, Any]
    context: Dict[str, Any]


DefaultContext = {
    "instanceid": "not-applicable",
    "organizationid": "Embedding-Service",
    "caller": "not-applicable",
    "ipaddress": "not-applicable",
    "origin": "not-applicable",
    "origintype": "not-applicable",
    "userid": "not-applicable",
    "sessionid": "not-applicable",
    "usertype": "not-applicable",
    "correlationid": str(uuid.uuid4()),
}


@final
class SyncSQSPusher:
    aws_access_key_id: str = cast(str, config("AWS_ACCESS_KEY_ID", default=False))
    aws_secret_access_key: str = cast(
        str, config("AWS_SECRET_ACCESS_KEY", default=False)
    )
    aws_region_name: str = cast(str, config("AWS_REGION_NAME", default=False))
    queue_config: Dict[str, Dict[str, bool]] = QUEUE_CONFIG

    def __construct_message_body(
        self, action: str, payload: Dict[str, Any]
    ) -> Message_Payload_TypeHinter:
        message_context = (
            headers_context.get().model_dump(mode="json") or DefaultContext
        )
        message_payload = Message_Payload_TypeHinter(
            action=action, context=message_context, payload=payload
        )
        return message_payload

    def __init__(self, queue_name: str, action: str, payload: Dict[str, Any]) -> None:
        self.sqs_client = boto3.client(
            "sqs",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region_name,
        )
        self.aws_account_id = boto3.client(
            "sts",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        ).get_caller_identity()["Account"]
        self.queue_name = queue_name
        self.queue_url = Helpers.construct_queue_url(
            queue_name=queue_name,
            region_name=self.aws_region_name,
            params=self.queue_config[queue_name],
            aws_account_id=self.aws_account_id,
        )
        self.message_payload = self.__construct_message_body(
            action=action, payload=payload
        )

    def post_message(self) -> None:
        try:
            response = self.sqs_client.send_message(
                QueueUrl=self.queue_url, MessageBody=json.dumps(self.message_payload)
            )
            APP_LOGGER.info(
                f"Message sent successfully to queue '{self.queue_name}' with Message ID: { response['MessageId']} and  ->  message payload : {self.message_payload}"
            )
        except Exception as e:
            APP_LOGGER.error("Error sending message:" + str(e))
            raise e
