from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user import UserRepository
from repositories.restaurant import RestaurantRepository
from schemas.restaurant import RestaurantCreate, RestaurantInfo, CreatedRestaurant, RestaurantCreateFromAPI, \
    RestaurantUpdate
from auth.utils import *
from models.user import UserRole


class RestaurantService:
    def __init__(self):
        self.restaurant_repository = RestaurantRepository()
        self.user_repository = UserRepository()

    async def create_restaurant(self, user_role: str,
                                restaurant: RestaurantCreateFromAPI, db: AsyncSession) -> CreatedRestaurant:
        if user_role != UserRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You dont have permission to this action"
            )
        has_user = await self.user_repository.get_user_by_email_or_none(restaurant.admin_email, db)
        if has_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with current email is already registered"
            )

        # Создание пользователя админа ресторана
        password = generate_password()
        hashed_password = hash_password(password)
        admin_account = await self.user_repository.create_user(restaurant.admin_email, hashed_password, db,
                                                               role=UserRole.ADMIN)

        restaurant_info = RestaurantCreate(
            name=restaurant.name,
            city=restaurant.city,
            description=restaurant.description,
            latitude=restaurant.latitude,
            longitude=restaurant.longitude,
            account_id=admin_account.id
        )

        restaurant = await self.restaurant_repository.create_restaurant(restaurant_info, db)
        restaurant_schema = CreatedRestaurant.from_orm(restaurant).dict()
        restaurant_schema.update(admin_password=password)

        created_restaurant = CreatedRestaurant(**restaurant_schema)

        return created_restaurant

    async def get_list_of_restaurants(self, user_role: str, db: AsyncSession) -> List[RestaurantInfo]:
        if user_role != UserRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You dont have permission to this action"
            )
        restaurants = await self.restaurant_repository.get_all_restaurants(db)
        return restaurants

    async def get_restaurant_by_id(self, user_role, restaurant_id: int, db: AsyncSession) -> RestaurantInfo:
        if user_role != UserRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You dont have permission to this action"
            )

        restaurant = await self.restaurant_repository.get_restaurant_by_id_or_none(restaurant_id, db)
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Restaurant with id {restaurant_id} not found"
            )
        return restaurant

    async def get_admin_restaurant(self, payload: dict, db: AsyncSession) -> RestaurantInfo:
        user_role = payload.get("role")
        if user_role not in UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You dont have permission to this action"
            )

        user_id = payload.get("id")
        restaurant = await self.restaurant_repository.get_restaurant_by_owner_id(user_id, db)
        return restaurant

    async def update_restaurant_data(self, restaurant: RestaurantUpdate, payload: dict, db: AsyncSession):
        user_role = payload.get("role")
        if user_role not in UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You dont have permission to this action"
            )

        user_id = payload.get("id")
        founded_restaurant = await self.restaurant_repository.get_restaurant_by_owner_id(user_id, db)

        updated_restaurant = await self.restaurant_repository.update_restaurant(founded_restaurant, restaurant, db)
        return updated_restaurant
