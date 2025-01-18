from contextvars import ContextVar
from typing import Any

headers_context: Any = ContextVar("headers_context", default=None)
payload_context: Any = ContextVar("request_body", default=None)
request_context: Any = ContextVar("request_context", default=None)
request_params_context: Any = ContextVar("request_params", default=None)
