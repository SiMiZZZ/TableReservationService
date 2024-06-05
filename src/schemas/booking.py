from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
import typing
class StatusEnum(str, Enum):
    AWAIT_CONFIRM = "await_confirm"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    COMPLETED = "completed"

class BookingInfo(BaseModel):
    id: int
    table_id: int
    people_count: int
    time_from: Optional[datetime]
    time_to: Optional[datetime]
    comment: str
    user_id: int
    status: StatusEnum


class BookingCreate(BaseModel):
    people_count: int
    time_from: Optional[datetime]
    duration: int
    comment: str


class TableExistsByData(BaseModel):
    tags: List[str]
    people_count: int


class BookingUpdate(BaseModel):
    status: Optional[StatusEnum]
