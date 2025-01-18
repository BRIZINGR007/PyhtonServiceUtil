from abc import ABC, abstractmethod
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import json
from typing import Any, Dict, Generic, Type, TypeVar
from fastapi import FastAPI
from pydantic import BaseModel

from ..interfaces.interfaces_th import (
    Headers_TH,
    SQSClientCallBackResponse_TH,
)
from ..middlewares.message_middlewares import (
    MessageMiddleware,
    ExceptionLogger,
)


T = TypeVar("T", bound=BaseModel)


class ProcessActionHandler(ABC, Generic[T]):
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

    async def handle_with_process_pool(
        self, payload: Dict[str, Any], headers: Headers_TH
    ) -> str:
        process_pool: ProcessPoolExecutor = self.app.state.process_pool
        correlation_id = headers["correlationid"]
        try:
            future = process_pool.submit(
                self.context_setter_and_execute_payload,
                payload=payload,
                headers=headers,
            )
            await asyncio.wrap_future(future)
            response = SQSClientCallBackResponse_TH(
                allSuccess=True, correlationid=correlation_id
            )

        except Exception:
            ExceptionLogger.log_exception(self, correlation_id=correlation_id)
            response = SQSClientCallBackResponse_TH(
                allSuccess=False, correlationid=correlation_id
            )
        return json.dumps(response)

    async def handle_with_thread_pool(
        self, payload: Dict[str, Any], headers: Headers_TH
    ) -> str:
        thread_pool: ThreadPoolExecutor = self.app.state.thread_pool
        correlation_id = headers["correlationid"]
        try:
            future = thread_pool.submit(
                self.context_setter_and_execute_payload,
                payload=payload,
                headers=headers,
            )
            await asyncio.wrap_future(future)
            response = SQSClientCallBackResponse_TH(
                allSuccess=True, correlationid=correlation_id
            )

        except Exception:
            ExceptionLogger.log_exception(self, correlation_id=correlation_id)
            response = SQSClientCallBackResponse_TH(
                allSuccess=False, correlationid=correlation_id
            )
        return json.dumps(response)
