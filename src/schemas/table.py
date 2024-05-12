from typing import Optional, List

from pydantic import BaseModel, EmailStr, ConfigDict


class TableInfo(BaseModel):
    id: int
    restaurant_id: int
    people_count: int
    tags: List[str]

class TablesCreate(BaseModel):
    tables_count: int
    people_count: int
    tags: List[str]


class TableCreate(BaseModel):
    people_count: int
    tags: List[str]

