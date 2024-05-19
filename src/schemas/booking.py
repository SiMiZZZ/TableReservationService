from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class BookingInfo(BaseModel):
    id: int
    table_id: int
    people_count: int
    time_from: Optional[datetime]
    time_to: Optional[datetime]
    comment: str
    user_id: int


class BookingCreate(BaseModel):
    people_count: int
    time_from: Optional[datetime]
    duration: int # minutes
    comment: str


class TableExistsByTag(BaseModel):
    tags: List[str]

