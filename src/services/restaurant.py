from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user import UserRepository
from repositories.restaurant import RestaurantRepository
from repositories.table import TableRepository
from schemas.restaurant import RestaurantCreate, RestaurantInfo, CreatedRestaurant, RestaurantCreateFromAPI, \
    RestaurantUpdate
from schemas.user import UserCreate, NewUserReturn
from schemas.restaurant import RestaurantImageCreate
from schemas.table import TableInfo, TablesCreate, TableCreate
from auth.utils import *
from models.user import UserRole
from consts import restaurant_tags
from fastapi import File
from config import settings
import os
from .database import sessionmanager


class RestaurantService:
    def __init__(self):
        self.restaurant_repository = RestaurantRepository()
        self.user_repository = UserRepository()
        self.table_repository = TableRepository()

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
            account_id=admin_account.id
        )

        restaurant = await self.restaurant_repository.create_restaurant(restaurant_info, db)
        restaurant_schema = CreatedRestaurant.from_orm(restaurant).dict()
        restaurant_schema.update(admin_password=password)

        created_restaurant = CreatedRestaurant(**restaurant_schema)

        return created_restaurant

    async def get_list_of_restaurants(self, db: AsyncSession) -> List[RestaurantInfo]:
        restaurants = await self.restaurant_repository.get_all_restaurants(db)
        restaurant_schemas = []
        for restaurant in restaurants:
            restaurant_image = await self.get_restaurants_image("00", restaurant.id, db)
            restaurant.image = restaurant_image[0] if restaurant_image else None
        return restaurants

    async def get_restaurant_by_id(self, restaurant_id: int, db: AsyncSession) -> RestaurantInfo:

        restaurant = await self.restaurant_repository.get_restaurant_by_id_or_none(restaurant_id, db)
        restaurant_image = await self.get_restaurants_image("00", restaurant.id, db)
        restaurant.image = restaurant_image[0] if restaurant_image else None
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
        restaurant.image = None
        return restaurant

    async def update_restaurant_data(self, restaurant: RestaurantUpdate, payload: dict, db: AsyncSession):
        user_role = payload.get("role")
        print(payload)
        if user_role not in UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You dont have permission to this action"
            )

        user_id = payload.get("id")
        founded_restaurant = await self.restaurant_repository.get_restaurant_by_owner_id(user_id, db)

        updated_restaurant = await self.restaurant_repository.update_restaurant(founded_restaurant, restaurant, db)
        updated_restaurant.image = None
        return updated_restaurant

    async def get_staff_users(self, payload: dict, db: AsyncSession) -> List[UserData]:
        pass

    async def create_staff_user(self, user: UserCreate, payload: dict, db: AsyncSession):
        user_role = payload.get("role")
        if user_role not in UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You dont have permission to this action"
            )

        has_user = await self.user_repository.get_user_by_email_or_none(user.email, db)
        if has_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with current email is already registered"
            )

        # Создание пользователя работника ресторана
        password = generate_password()
        hashed_password = hash_password(password)
        staff_account = await self.user_repository.create_user(user.email, hashed_password, db,
                                                               role=UserRole.STAFF)
        new_user = NewUserReturn(
            id=staff_account.id,
            email=staff_account.email,
            role=staff_account.role,
            password=password
        )

        return new_user

    async def get_restaurant_tags(self, payload: dict):
        user_role = payload.get("role")
        if user_role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You dont have permission to this action"
            )
        return restaurant_tags.tags

    async def create_restaurant_image(self, files: List[File], restaurant_id: int,  db: AsyncSession):
        media_root = settings.MEDIA_ROOT + f"{restaurant_id}/"
        for file in files:
            contents = file.file.read()
            os.makedirs(os.path.dirname(media_root + file.filename), exist_ok=True)
            with open(media_root + file.filename, "wb+") as f:
                f.write(contents)
                await self.restaurant_repository.create_restaurant_image(RestaurantImageCreate(
                    path=media_root + file.filename,
                    name=file.filename,
                    restaurant_id=restaurant_id),
                    db)
                f.close()

    async def get_restaurants_image(self, host, restaurant_id: int, db: AsyncSession):

        images = await self.restaurant_repository.get_images_by_restaurants(restaurant_id, db)
        return_lst = []
        for image in images:
            return_lst.append(
                f"https://85.10.216.104/api/media/{restaurant_id}/{image.name}"
            )

        return return_lst

    async def create_table(self, tables: TablesCreate, payload: dict, db: AsyncSession) -> List[TableInfo]:
        user_role = payload.get("role")
        if user_role not in UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You dont have permission to this action"
            )

        user_id = payload.get("id")
        founded_restaurant = await self.restaurant_repository.get_restaurant_by_owner_id(user_id, db)
        return_tables = []
        id = founded_restaurant.id
        for _ in range(tables.tables_count):
            table_info = TableCreate(people_count=tables.people_count, tags=tables.tags)
            new_table = await self.table_repository.create_table(table_info, id, db)
            return_tables.append(new_table)
        return return_tables

    async def delete_table(self, table_id: int, payload: dict, db: AsyncSession):
        user_role = payload.get("role")
        if user_role not in UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You dont have permission to this action"
            )
        await self.table_repository.delete_table(table_id, db)


