from app.utils.hashing import Hasher
from fastapi import HTTPException, Response
from sqlalchemy import select

from app.base.logic import BaseLogic
from app.modules.users import schemas
from app.modules.users.filters import UserFilter
from app.modules.users.models import (
    User,
)
from app.modules.users.schemas import AuthCredentials
from app.config import settings
from app.utils.jwt_utils import auth


class UserBusinessLogic(BaseLogic, UserFilter):
    Model = User

    async def get_user_by_email(self, email: str):
        return await self.repository.session.scalar(select(self.Model).where(self.Model.email == email))

    async def create(
            self,
            user: schemas.UserBase,
    ):
        is_user_exist = await self.get_user_by_email(email=user.email)
        if is_user_exist:
            raise HTTPException(
                status_code=400,
                detail={"status": "False", "message": "Email already registered"},
            )
        user = await self.create_user(user)
        return {
            "status": "True",
            "data": schemas.UserOut(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
            ),
        }

    async def create_user(self, user_data: schemas.UserBase) -> User:
        hashed_password = Hasher.get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone_number=user_data.phone_number,
        )
        self.repository.session.add(user)
        return user

    async def login_user(self, credentials: AuthCredentials, response: Response):
        user = await self.get_user_by_email(credentials.email)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        if Hasher.verify_password(credentials.password, user.hashed_password):
            token = auth.create_access_token(uid=str(user.id))
            response.set_cookie(key=settings.JWT_ACCESS_COOKIE_NAME, value=token, samesite="lax", secure=False, httponly=True)
            return {"access_token": token}
        raise HTTPException(status_code=403, detail="Username or password incorrect")
