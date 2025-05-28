from typing import AsyncIterable, Optional

from fastapi import HTTPException, Request
from fastapi.requests import HTTPConnection
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database.session import AsyncSessionMaker
from app.modules.users.models import User
from app.utils.jwt_utils import auth


async def get_session(request: HTTPConnection) -> AsyncIterable[AsyncSession]:
    if "db_session" not in request.scope:
        msg = "Database session is not initialized"
        raise ValueError(msg)
    return request.scope["db_session"]


async def get_socket_id(request: Request) -> Optional[str]:
    cookie = request.cookies
    sid = cookie.get("sid")
    return sid


async def get_current_user(
    request: Request,
):
    token = await auth.get_access_token_from_request(request)
    payload = token.verify(key=settings.SECRET_KEY, verify_csrf=False)
    uid = payload.sub
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid token")
    async with AsyncSessionMaker() as session:
        stmt = select(User).where(User.id == uid)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
