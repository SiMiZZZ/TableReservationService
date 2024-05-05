from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.user import User as UserModel
from models.restautant import Restaurant as RestaurantModel
from models.table import Table as TableModel
from models.table import Table
from models.restaurant_image import RestaurantImage
from schemas.restaurant import RestaurantCreate, RestaurantUpdate, CreatedRestaurant, RestaurantImageCreate


class TableRepository:

    async def create_table(self, restaurant_id: int,
                                db: AsyncSession) -> RestaurantModel:
        table = TableModel(restaurant_id=restaurant_id)
        db.add(table)
        await db.commit()
        await db.refresh(table)
        return table
