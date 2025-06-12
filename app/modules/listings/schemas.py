from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


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

class ListingGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    price: float
    property_type: str
    address: str
    city: str

    attachment_ids: Optional[list[Attachment]] = Field(default=None, alias="attachments")
