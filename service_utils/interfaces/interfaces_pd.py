from typing import Any, Dict
import uuid
from pydantic import BaseModel, Field


class Headers_PM(BaseModel):
    correlationid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str = "not_applicable"
    authorization: str = Field(default="")

    def model_dump(self, exclude_fields={}, **kwargs) -> Dict[str, Any]:
        return super().model_dump(**kwargs, exclude=exclude_fields)
