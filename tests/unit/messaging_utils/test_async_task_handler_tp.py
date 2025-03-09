import pytest
from unittest.mock import MagicMock, patch
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
import json
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from app.zoldics_service_utils.messaging_utils.async_task_handler import (
    AsyncTaskHandler,
)


class SampleModel_PM(BaseModel):
    field1: str
    field2: str


class SampleTaskRouter(AsyncTaskHandler[SampleModel_PM]):
    pydantic_model_class = SampleModel_PM

    @classmethod
    def execute_business_logic(cls, payload: SampleModel_PM) -> None:
        print("Exceuting Very Importamnt Busainess Logic  .")
        pass
