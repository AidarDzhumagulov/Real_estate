from __future__ import annotations

import enum
import uuid
from datetime import datetime  # noqa.
from enum import Enum
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, RootModel, field_validator


if TYPE_CHECKING:
    from datetime import datetime


class UserTransitionPoint(enum.Enum):
    LANDING = "landing"
    INVITE = "invite"
    OTHER = "other"


class UserDateFormat(enum.Enum):
    INTERNATIONAL = "international"
    USA = "usa"


class InviteType(str, Enum):
    master = "master"
    common = "common"


class AuthCredentials(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class UserBase(BaseModel):
    email: str
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    language: Optional[str] = "en"
    description: Optional[str]
    date_format: Optional[UserDateFormat]


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    email: str


class UserShort(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            Optional[UUID]: lambda v: str(v),
        },
    )

    id: Optional[UUID]
    user_name: Optional[str] = Field(serialization_alias="name")
    email: Optional[str]


class Token(BaseModel):
    access_token: str
    refresh_token: str


class UserExists(BaseModel):
    email: EmailStr


class UserExistsOut(BaseModel):
    user_exists: bool


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    description: Optional[str] = None
    date_format: Optional[UserDateFormat] = None
    language: Optional[str] = None
    pincode: Optional[str] = None


class UserGroupShort(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID


class UserGroupList(RootModel):
    model_config = ConfigDict(
        json_encoders={List[UserGroupShort]: lambda fields: [str(field.id) for field in fields]}
    )

    root: List[UserGroupShort]


class UsersWithGroups(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: uuid.UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    created_at: Optional[datetime] = Field(serialization_alias="entered_at")
    phone_number: Optional[str] = None
    groups: UserGroupList = Field(serialization_alias="group")
    role: Optional[str] = None


class UserWithGroupsList(RootModel):
    root: List[UsersWithGroups]


class ListOfUsersWithGroups(BaseModel):
    users: List[UsersWithGroups]


class UserRoomStatusChoice(int, Enum):
    PUBLIC = 0
    WAITING_FOR_APPROVE = 1
    APPROVED = 2
    DENIED = 3


class UpdateUserRoomStatus(BaseModel):
    room_id: uuid.UUID
    status: UserRoomStatusChoice


class UserLogout(BaseModel):
    access_token: str
    refresh_token: str
