import json
import datetime
import logging
import pytz

from ..utils.env_initlializer import EnvStore

# modules
from ..context.vars import (
    headers_context,
    request_context,
    payload_context,
    request_params_context,
)
from typing import Any, Dict, Optional


class ContextManager:

    @staticmethod
    def _get_model_dump(obj):
        if hasattr(obj, "model_dump"):
            return obj.model_dump(mode="json")
        elif isinstance(obj, dict):
            return obj
        return None

    @classmethod
    def get_current_context(cls) -> Dict[str, Any]:
        """
        Retrieve the current request-specific contexts
        """
        return {
            "headers_context": cls._get_model_dump(headers_context.get()),
            "payload_context": cls._get_model_dump(payload_context.get()),
            "request_context": cls._get_model_dump(request_context.get()),
            "request_params_context": cls._get_model_dump(request_params_context.get()),
        }


class RecordFormatter:
    DATE_FORMAT_TIMEZONE = "%a %b %d %Y %H:%M:%S (%Z)"

    @staticmethod
    def format_record(record: logging.LogRecord) -> str:
        record_items = dict(record.__dict__)
        try:
            message_dict = json.loads(str(record_items.get("message")))
            record_items.update(message_dict)
            record_items["message"] = json.dumps(
                {
                    key: value
                    for key, value in message_dict.items()
                    if key not in ["pathname", "lineno", "funcName"]
                }
            )
        except (ValueError, TypeError):
            pass

        output = {
            "levelname": record_items["levelname"],
            "epoch": record_items["created"],
            "timestamp": datetime.datetime.fromtimestamp(
                record_items["created"], tz=pytz.timezone("Asia/Kolkata")
            ).strftime(RecordFormatter.DATE_FORMAT_TIMEZONE),
            "message": record_items["message"],
            "serviceName": EnvStore().servicename,
            "env": EnvStore().environment,
            "funcName": record_items["funcName"],
            "pathname": record_items["pathname"],
            "lineno": record_items["lineno"],
        }
        context = ContextManager.get_current_context()
        output.update(context)
        return json.dumps(output)


class CustomJsonFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        super().format(record)
        return RecordFormatter.format_record(record)


class LoggerFactory:
    _logger: Optional[logging.Logger] = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Get or create a logger instance
        """
        if cls._logger is None:
            cls._logger = logging.getLogger("fastapi_app")
            cls._logger.setLevel(logging.DEBUG)
            cls._logger.handlers.clear()

            # File handler
            file_handler = logging.FileHandler("service.log")
            file_handler.setFormatter(CustomJsonFormatter())
            cls._logger.addHandler(file_handler)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(CustomJsonFormatter())
            cls._logger.addHandler(console_handler)

        return cls._logger


APP_LOGGER = LoggerFactory.get_logger()
