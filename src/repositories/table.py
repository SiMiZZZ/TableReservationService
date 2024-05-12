from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from models.user import User as UserModel
from models.restautant import Restaurant as RestaurantModel
from models.table import Table as TableModel
from models.table import Table
from models.restaurant_image import RestaurantImage
from schemas.table import TableCreate


class TableRepository:

    async def create_table(self, table: TableCreate,
                           restaurant_id: int,
                           db: AsyncSession) -> RestaurantModel:
        table = TableModel(restaurant_id=restaurant_id, **table.dict())
        db.add(table)
        await db.commit()
        await db.refresh(table)
        return table

    async def delete_table(self, table_id: int, db: AsyncSession) -> None:
        q = delete(TableModel).where(TableModel.id == table_id)
        await db.execute(q)
        await db.commit()
