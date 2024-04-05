from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class RestaurantCreate(BaseModel):
    name: str
    city: str | None = None
    description: str | None = None
    latitude: str | None = None
    longitude: str | None = None
    account_id: int | None = None



class RestaurantCreateFromAPI(BaseModel):
    name: str
    admin_email: str


class CreatedRestaurant(BaseModel):
    name: str
    admin_password: str | None = None
    id: int

    model_config = ConfigDict(from_attributes=True)

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    address: Optional[str] = None
    site: Optional[str] = None
    tags: Optional[list[str]] = None
    phone_number: Optional[str] = None
    active: Optional[bool] = None
    open_from: Optional[str] = None
    open_to: Optional[str] = None


class RestaurantInfo(BaseModel):
    id: int
    name: str
    description: str | None
    city: str | None
    latitude: str | None
    longitude: str | None
    address: str | None
    site: str | None
    tags: list[str] | None
    phone_number: str | None
    active: bool | None
    account_id: int | None
    open_from: str | None
    open_to: str | None
