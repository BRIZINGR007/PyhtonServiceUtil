import sys
import traceback
from typing import Any, Dict, Type, cast
from pydantic import BaseModel

from ..utils.env_initlializer import EnvStore

from ..context.vars import headers_context, payload_context
from ..interfaces.interfaces_pd import Headers_PM
from ..interfaces.interfaces_th import Headers_TH
from ..utils.jwt_validation import JwtValdationUtils
from ..logging.base_logger import APP_LOGGER


class MessageMiddleware:
    @staticmethod
    def validate_set_context(
        payload: Dict[str, Any],
        headers: Headers_TH,
        payload_pydantic_model: Type[BaseModel],
    ):
        if headers.get("authorization"):
            JwtValdationUtils.validate_token(
                token=cast(str, headers.get("authorization")),
                verify_aud=False,
                verify_exp=False,
            )
        pydantic_payload = payload_pydantic_model(**payload)
        payload_context.set(pydantic_payload)
        headers_context.set(Headers_PM(**headers))


class ExceptionLogger:
    @staticmethod
    def log_exception(instance, correlation_id: str) -> None:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_type is not None:
            traceback_info = traceback.extract_tb(exc_traceback)
            relevant_traceback = next(
                (
                    trace
                    for trace in reversed(traceback_info)
                    if EnvStore().servicename in trace.filename
                ),
                None,
            )
            error_data = {
                "exception_type": str(exc_type.__name__),
                "exception_value": str(exc_value),
                "correlationid": correlation_id,
            }
            if relevant_traceback:
                pathname, lineno, func_name, code_line = relevant_traceback
                error_data.update(
                    {
                        "pathname": pathname,
                        "lineno": lineno,
                        "funcName": func_name,
                        "code_line": code_line,
                    }
                )
            APP_LOGGER.error(error_data)
