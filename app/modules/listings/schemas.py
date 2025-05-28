from pydantic import BaseModel, ConfigDict


class ListingCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    price: float
    property_type: str
    address: str
    city: str
