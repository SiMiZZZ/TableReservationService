from typing import Optional, List

from pydantic import BaseModel, EmailStr, ConfigDict


class TableInfo(BaseModel):
    id: int
    restaurant_id: int
    tags: List[str]