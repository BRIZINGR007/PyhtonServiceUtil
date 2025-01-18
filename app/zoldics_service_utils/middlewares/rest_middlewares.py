from typing import FrozenSet
import uuid
import json
import sys
import traceback
from decouple import config
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from decouple import config

# modules

from interfaces.interfaces_pd import Headers_PM, RequestContext_PM
from utils.jwt_validation import JwtValdationUtils
from logging.base_logger import APP_LOGGER
from context.vars import (
    headers_context,
    request_context,
    request_params_context,
    payload_context,
)


class HeaderValidationMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        excluded_paths: FrozenSet[str] = frozenset(),
        authexpiryignore_paths: FrozenSet[str] = frozenset(),
    ):
        super().__init__(app)
        self.excluded_paths: FrozenSet[str] = frozenset(
            {"/docs", "/openapi.json", *excluded_paths}
        )

        self.authexpiryignore_paths: FrozenSet[str] = frozenset(authexpiryignore_paths)

    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)
        headers = request.headers
        access_token = None
        verify_exp = True
        should_ignore_expiry = any(
            request.url.path.startswith(path) for path in self.authexpiryignore_paths
        )
        if "access_token" in request.cookies:
            access_token = request.cookies.get("access_token")
            verify_exp = not should_ignore_expiry
        elif "authorization" in headers:
            access_token = headers.get("authorization")
            verify_exp = not should_ignore_expiry
        access_token = request.cookies.get("access_token") or headers.get(
            "authorization"
        )
        try:
            if access_token:
                payload = JwtValdationUtils.validate_token(
                    access_token, verify_exp=verify_exp
                )
                headers_model = Headers_PM(
                    **dict(
                        correlationid=headers.get("correlationid", str(uuid.uuid4())),
                        username=payload["username"],
                        authorization=access_token,
                    )
                )
                headers_context.set(headers_model)
                return await call_next(request)

            if headers.get("x-api-key-2") == config(
                "X_API_KEY_PUBSUB-SERVICE_2"
            ) or headers.get("x-api-key-1") == config("X_API_KEY_PUBSUB-SERVICE_1"):
                headers_model = Headers_PM(
                    **dict(
                        correlationid=headers.get("correlationid", str(uuid.uuid4())),
                        username=headers.get("username", ""),
                        authorization=headers.get("authorization", ""),
                    )
                )
                headers_context.set(headers_model)
                return await call_next(request)

            return JSONResponse(
                {"detail": "Unauthorized: Missing or invalid credentials."},
                status_code=401,
            )

        except HTTPException as e:
            raise e
        except Exception as e:
            APP_LOGGER.error(f"Unexpected error in token validation: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")


class ExceptionMiddleware:
    def __init__(self, app):
        self.app = app

    def log_exception(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_type is not None:
            traceback_info = traceback.extract_tb(exc_traceback)
            relevant_traceback = next(
                (
                    trace
                    for trace in reversed(traceback_info)
                    if str(config("SERVICENAME")) in trace.filename
                ),
                None,
            )
            if relevant_traceback:
                pathname, lineno, funcName, code_line = relevant_traceback
                error_data = {
                    "exception_type": str(exc_type.__name__),
                    "exception_value": str(exc_value),
                    "pathname": str(pathname),
                    "lineno": str(lineno),
                    "funcName": funcName,
                    "code_line": str(code_line),
                }
                APP_LOGGER.error(json.dumps(error_data))

    async def __call__(self, scope, receive, send):
        try:
            await self.app(scope, receive, send)
        except HTTPException as http_exception:
            self.log_exception()
            await self.handle_http_exception(http_exception, scope, receive, send)
        except Exception as e:
            self.log_exception()
            await self.handle_internal_server_error(e, scope, receive, send)

    async def handle_http_exception(self, http_exception, scope, receive, send):
        await http_exception(scope, receive, send)

    async def handle_internal_server_error(self, exception, scope, receive, send):
        error_message = dict(
            detail="Internal Server Error", error_message=str(exception)
        )
        response = JSONResponse(status_code=500, content=error_message)
        await response(scope, receive, send)


class ContextSetter:
    async def __call__(self, request: Request):
        if request.query_params:
            query_params = dict(request.query_params)
            request_params_context.set(query_params)
        try:
            body = await request.json()
            payload_context.set(body)
        except (json.JSONDecodeError, ValueError):
            pass

        request_path_method: RequestContext_PM = RequestContext_PM(
            request_trace_id=str(uuid.uuid4()),
            url_path=request.url.path,
            method=request.method,
        )
        request_context.set(request_path_method)
