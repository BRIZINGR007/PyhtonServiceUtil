import itertools
import asyncio
import botocore.exceptions
from aiobotocore.session import get_session
from typing import final, Dict, Any, List

from .message_handler import MessageHandler
from ...logging.base_logger import APP_LOGGER


@final
class AsyncQueueClient:
    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_region_name: str,
        queue_url: str,
        queue_name: str,
    ) -> None:
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region_name = aws_region_name
        self.queue_url = queue_url
        self.queue_name = queue_name

    async def poll_messages(
        self, batch_size_of_messages: int, max_polling_duration: int
    ) -> None:

        session = get_session()
        async with session.create_client(
            "sqs",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region_name,
        ) as async_sqs_client:
            APP_LOGGER.info(f"POLLING TO --> {self.queue_url}")
            print(f"POLLING TO --> {self.queue_url} QUEUE")
            for _ in itertools.repeat(None):
                try:
                    task = asyncio.create_task(
                        async_sqs_client.receive_message(
                            QueueUrl=self.queue_url,
                            MaxNumberOfMessages=batch_size_of_messages,
                            WaitTimeSeconds=max_polling_duration,
                        )
                    )
                    response: Dict[str, Any] = await task
                except botocore.exceptions.ClientError as e:
                    APP_LOGGER.error(f"SQS Error while receiving messages: {e}")
                    continue

                messages: List[Dict[str, Any]] = response.get("Messages", [])

                if messages:
                    entries_to_delete = await MessageHandler(
                        queue_name=self.queue_name
                    ).handle_messages_in_batch(messages_batch_payload=messages)

                    if entries_to_delete:
                        message_entries = [
                            {"Id": item["Id"], "ReceiptHandle": item["ReceiptHandle"]}
                            for item in entries_to_delete
                        ]
                        correlationids = [
                            {"correlationid": item["correlationid"]}
                            for item in entries_to_delete
                        ]
                        try:
                            delete_batch_messages_response = asyncio.create_task(
                                async_sqs_client.delete_message_batch(
                                    QueueUrl=self.queue_url, Entries=message_entries
                                )
                            )
                            delete_batch_messages_response = (
                                await delete_batch_messages_response
                            )
                            APP_LOGGER.info(
                                f"Messages Deleted From SQS with {correlationids}: {str(delete_batch_messages_response)}"
                            )

                        except botocore.exceptions.ClientError as e:
                            APP_LOGGER.error(f"SQS Error while deleting messages: {e}")


@final
class SQS_Manager:
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region_name: str

    __instances: Dict[str, "SQS_Manager"] = {}

    def __new__(cls, queue_name: str, **kwargs):
        if queue_name not in cls.__instances:
            queue_url: str = str(kwargs.get("queue_url"))
            instance = super().__new__(cls)
            instance.__init__(queue_name=queue_name, queue_url=queue_url)
            cls.__instances[queue_name] = instance
        return cls.__instances[queue_name]

    def __init__(self, queue_name: str, **kwargs):
        if not hasattr(self, "initialized"):
            self.queue_name = queue_name
            self.queue_url: str = str(kwargs.get("queue_url"))
            self.async_client = AsyncQueueClient(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_region_name=self.aws_region_name,
                queue_url=self.queue_url,
                queue_name=self.queue_name,
            )
            self.initialized: bool = True
