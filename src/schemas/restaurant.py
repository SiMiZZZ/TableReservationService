from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class RestaurantCreate(BaseModel):
    name: str
    city: str
    description: str | None = None
    latitude: str | None = None
    longitude: str | None = None



class RestaurantCreateFromAPI(RestaurantCreate):
    admin_email: str

class CreatedRestaurant(RestaurantCreate):
    admin_password: str | None = None
    id: int

    model_config = ConfigDict(from_attributes=True)

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None

class RestaurantInfo(BaseModel):
    id: int
    name: str
    description: str | None
    city: str | None
    latitude: str | None
    longitude: str | None
    account_id: int | None
