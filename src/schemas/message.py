from pydantic import BaseModel, EmailStr, ConfigDict
from models.message import OwnerEnum

class MessageCreate(BaseModel):
    restaurant_id: int
    user_id: int
    owner: OwnerEnum
    data: str

