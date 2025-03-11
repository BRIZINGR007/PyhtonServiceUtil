from abc import ABC, abstractmethod
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import json
from typing import Any, Dict, Generic, Type, TypeVar, Union
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError

from ..utils.exceptions import JwtValidationError, UserRateLimitReachedError
from ..interfaces.interfaces_th import (
    Headers_TH,
    SQSClientCallBackResponse_TH,
)
from ..middlewares.message_middlewares import (
    MessageMiddleware,
    ExceptionLogger,
)

T = TypeVar("T", bound=BaseModel)


class AsyncTaskHandler(ABC, Generic[T]):
    pydantic_model_class: Type[T]

    def __init__(self, app: FastAPI) -> None:
        self.app = app

    @classmethod
    @abstractmethod
    def execute_business_logic(cls, payload: T) -> None:
        """Execute the specific business logic for the action."""
        raise NotImplementedError("Subclasses must implement execute_business_logic")

    @classmethod
    def context_setter_and_execute_payload(
        cls, payload: Dict[str, Any], headers: Headers_TH
    ) -> None:
        """Set the context and execute the business logic."""
        MessageMiddleware.validate_set_context(
            payload=payload,
            headers=headers,
            payload_pydantic_model=cls.pydantic_model_class,
        )
        cls.execute_business_logic(payload=cls.pydantic_model_class(**payload))

    async def _handle_with_executor(
        self,
        payload: Dict[str, Any],
        headers: Headers_TH,
        executor: Union[ProcessPoolExecutor, ThreadPoolExecutor],
    ) -> str:
        """Common handler logic for both process and thread pools."""
        correlation_id = headers["correlationid"]
        try:
            future = executor.submit(
                self.context_setter_and_execute_payload,
                payload=payload,
                headers=headers,
            )
            await asyncio.wrap_future(future)
            success = True
        except (JwtValidationError, ValidationError, UserRateLimitReachedError):
            # In case of JwtValidationError ,Pydantic ValidationError and  UserRateLimitReached Error   we  delete the message from the queue .
            ExceptionLogger.log_exception(self, correlation_id=correlation_id)
            success = True
        except Exception:
            # For other exceptions, we consider the task failed and do not  delte the message from  the queue . Note  : It will keep on retrying  .
            ExceptionLogger.log_exception(self, correlation_id=correlation_id)
            success = False
        response = SQSClientCallBackResponse_TH(
            allSuccess=success, correlationid=correlation_id
        )
        return json.dumps(response)

    async def handle_with_process_pool(
        self, payload: Dict[str, Any], headers: Headers_TH
    ) -> str:
        """Handle the task using a process pool executor."""
        process_pool: ProcessPoolExecutor = self.app.state.process_pool
        return await self._handle_with_executor(payload, headers, process_pool)

    async def handle_with_thread_pool(
        self, payload: Dict[str, Any], headers: Headers_TH
    ) -> str:
        """Handle the task using a thread pool executor."""
        thread_pool: ThreadPoolExecutor = self.app.state.thread_pool
        return await self._handle_with_executor(payload, headers, thread_pool)
