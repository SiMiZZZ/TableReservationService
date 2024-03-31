from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User as UserModel
from models.restautant import Restaurant as RestaurantModel
from schemas.restaurant import RestaurantCreate, RestaurantUpdate, CreatedRestaurant


class RestaurantRepository:

    async def create_restaurant(self, restaurant: RestaurantCreate,
                                db: AsyncSession) -> RestaurantModel:
        restaurant = RestaurantModel(**restaurant.dict())
        db.add(restaurant)
        await db.commit()
        await db.refresh(restaurant)
        return restaurant

    async def update_restaurant(self, restaurant_model: RestaurantModel, restaurant: RestaurantUpdate,
                                db: AsyncSession) -> RestaurantModel:
        for name, value in restaurant.model_dump(exclude_unset=True).items():
            setattr(restaurant_model, name, value)
        await db.commit()
        await db.refresh(restaurant_model)
        return restaurant_model

    async def get_restaurant_by_id_or_none(self, id: int,
                                   db: AsyncSession) -> RestaurantModel | None:
        q = select(RestaurantModel).where(RestaurantModel.id == id)
        exec = await db.execute(q)
        user = exec.scalar()
        return user

    async def get_all_restaurants(self, db: AsyncSession) -> List[RestaurantModel]:
        q = select(RestaurantModel)
        exec = await db.execute(q)
        restaurants = exec.scalars().all()
        return restaurants

    async def get_restaurant_by_owner_id(self, owner_id: int, db: AsyncSession) -> RestaurantModel:
        q = select(RestaurantModel).where(RestaurantModel.account_id == owner_id)
        exec = await db.execute(q)
        restaurant = exec.scalar()
        return restaurant