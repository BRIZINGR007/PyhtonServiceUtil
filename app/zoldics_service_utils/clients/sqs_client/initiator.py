import boto3
from typing import List, Callable, Awaitable
from typing import Dict

from .helpers import Helpers
from .message_handler import MessageHandler
from .polling import SQS_Manager
from ...ioc.singleton import SingletonMeta

# modules


class SQSInitiator(metaclass=SingletonMeta):

    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        queue_names: List[str],
        aws_region_name: str,
        queue_config: Dict[str, Dict[str, bool]],
        queue_to_message_handler_map: Dict[
            str, Dict[str, Callable[[], Awaitable[str]]]
        ],
    ) -> None:
        SQS_Manager.aws_access_key_id = aws_access_key_id
        SQS_Manager.aws_secret_access_key = aws_secret_access_key
        SQS_Manager.aws_region_name = aws_region_name

        MessageHandler.QUEUE_TO_MESSAGE_HANDLER_MAP = queue_to_message_handler_map

        self.__aws_account_id = boto3.client(
            "sts",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        ).get_caller_identity()["Account"]

        for queue_name in queue_names:
            queue_url = Helpers.construct_queue_url(
                queue_name=queue_name,
                region_name=aws_region_name,
                params=queue_config.get(queue_name, {}),
                aws_account_id=self.__aws_account_id,
            )
            SQS_Manager(queue_name=queue_name, queue_url=queue_url)
            MessageHandler(queue_name=queue_name)
