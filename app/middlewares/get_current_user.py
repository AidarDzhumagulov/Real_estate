import typing

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.authentication import (
    AuthenticationBackend,
)


class OAuth2Backend(AuthenticationBackend):
    SKIP_IP_VALIDATION_PATHS: typing.ClassVar = [
        "/api/users/fingerprint/refresh/"
    ]  # Сюда можно добавить апи, которые не надо валидировать по ip

    @staticmethod
    def handle_error(_request: Request, exc: Exception):
        message = getattr(exc, "message", "Internal server error")
        code = getattr(exc, "code", 500)
        return JSONResponse(
            content={"detail": message},
            status_code=code,
        )
