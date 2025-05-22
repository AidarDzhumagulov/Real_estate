from typing import AsyncIterable, Optional

from fastapi import HTTPException, Request
from fastapi.requests import HTTPConnection
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User


async def get_session(request: HTTPConnection) -> AsyncIterable[AsyncSession]:
    if "db_session" not in request.scope:
        msg = "Database session is not initialized"
        raise ValueError(msg)
    return request.scope["db_session"]


async def get_socket_id(request: Request) -> Optional[str]:
    cookie = request.cookies
    sid = cookie.get("sid")
    return sid


async def get_current_user(request: Request) -> Optional[User]:
    skip_params = ["is_temp_links", "is_user"]  # skip
    request_data = request.query_params

    if any(request_data.get(param) for param in skip_params):
        return None
    if not hasattr(request.state, "user"):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )
    return request.state.user


async def get_log_context(request: Request):
    if not hasattr(request.state, "log_context"):
        request.state.log_context = {
            "details": {},
        }
    return request.state.log_context


def generate_request_context(request: Request):
    return {"request": request}
