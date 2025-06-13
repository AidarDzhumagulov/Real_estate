from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.users.models import User


class ListingCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    price: float
    property_type: str
    address: str
    city: str
    attachment_ids: list[UUID]


class ListingUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    price: float
    property_type: str

class Attachment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

class GetUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_name: str

class ListingGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    price: float
    property_type: str
    address: str
    city: str
    creator: Optional[GetUser] = None

    attachment_ids: Optional[list[Attachment]] = Field(default=None, alias="attachments")
