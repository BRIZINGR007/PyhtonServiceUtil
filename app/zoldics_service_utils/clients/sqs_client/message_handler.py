import json
import asyncio
from functools import partial
from typing import Dict, final, List, Union, Callable, Awaitable
from types import MethodType

from ...logging.base_logger import APP_LOGGER
from ...interfaces.interfaces_th import SQSClientCallBackResponse_TH
from ...ioc.singleton import Para_SingletonMeta


@final
class MessageHandler(metaclass=Para_SingletonMeta):
    QUEUE_TO_MESSAGE_HANDLER_MAP: Dict[str, Dict[str, Callable[[], Awaitable[str]]]]
    QUEUE_CONFIG: Dict[str, Dict[str, bool]]

    def __init__(self, queue_name: str) -> None:
        self.message_handler_map = self.QUEUE_TO_MESSAGE_HANDLER_MAP[queue_name]
        if self.message_handler_map is None:
            raise ValueError(f"No Message Handler for: {queue_name}")

    def task_callback(self, task, message_entry):
        if task.done() and task.exception():
            APP_LOGGER.error(
                f"'SQS Action Handler' Callback Response : {task.exception()} || {message_entry} "
            )

        else:
            callback_response: SQSClientCallBackResponse_TH = json.loads(task.result())
            allSuccess = callback_response["allSuccess"]
            if allSuccess:
                self.entries_to_delete.append(message_entry)
            APP_LOGGER.info(
                f"'SQS Action Handler' CallBack Response: {callback_response} || {message_entry}"
            )

    async def handle_messages_in_batch(
        self, messages_batch_payload: List[Dict[str, str]]
    ):
        self.entries_to_delete = []
        awaitables = []
        for message in messages_batch_payload:
            try:
                message_body = json.loads(message["Body"])
                message_context: Dict[str, str] = message_body["context"]
                message_metadata: Dict[str, Union[dict, str]] = dict(
                    message_entry=dict(
                        Id=message["MessageId"],
                        ReceiptHandle=message["ReceiptHandle"],
                        correlationid=message_context["correlationid"],
                    ),
                    action=message_body["action"],
                    payload=message_body["payload"],
                )
                action: str = str(message_metadata.get("action"))

                message_handler = self.message_handler_map.get(action)

                # NOTE : Enable to verify message_context of all messages if they are comming from valid sources .ignore_expiry=False if you want to validate jwt token.
                # try:
                #     await asyncio.to_thread(
                #         lambda payload, model: model(**payload, ignore_expiry=True),
                #         message_context,
                #         HeaderModel,
                #     )
                # except ValidationError as e:
                #     APP_LOGGER.error(f"{message_metadata} || Error: {e}")
                #     self.entries_to_delete.append(message_metadata.get("message_entry"))
                #     continue

                APP_LOGGER.info(message_metadata)

                if isinstance(message_handler, MethodType):
                    task = asyncio.create_task(
                        message_handler(
                            payload=message_metadata["payload"], headers=message_context
                        )
                    )
                    callback_with_args = partial(
                        self.task_callback,
                        message_entry=message_metadata["message_entry"],
                    )
                    task.add_done_callback(callback_with_args)
                    awaitables.append(task)
                else:
                    APP_LOGGER.warning(
                        f"{message_metadata} || No 'SQS Action Handler' found ."
                    )
            except Exception as e:
                APP_LOGGER.error(f"Error processing message: {e}")
                # self.entries_to_delete.append(message_metadata.get("message_entry"))
                continue

        if awaitables:
            await asyncio.gather(*awaitables, return_exceptions=True)

        return self.entries_to_delete
