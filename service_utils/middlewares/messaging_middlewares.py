from typing import Any, Dict, Type, cast

from pydantic import BaseModel
from websockets import Headers
from app.interfaces.pd_interfaces import Headers_PM
from service_utils.context.vars import headers_context, payload_context
from service_utils.interfaces.interfaces_th import Headers_TH
from service_utils.utils.jwt_validation import JwtValdationUtls


class BrokerMiddleware:
    @staticmethod
    def validate_set_context(
        payload: Dict[str, Any],
        headers: Headers_TH,
        payload_pydantic_model: Type[BaseModel],
    ):
        try:
            if headers.get("authorization"):
                JwtValdationUtls.validate_token(
                    token=cast(str, headers.get("authorization")),
                    verify_aud=False,
                    verify_exp=False,
                )
                pydantic_payload = payload_pydantic_model(**payload)
                payload_context.set(pydantic_payload)
                headers_context.set(Headers_PM(**headers))
        except Exception as e:
            raise ValueError(f"Validation or context setting failed: {e}")
