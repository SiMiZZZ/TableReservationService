from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import schemas

from schemas.restaurant import RestaurantInfo, RestaurantCreate, RestaurantCreateFromAPI, CreatedRestaurant
from services.database import get_db
from services.restaurant import RestaurantService
from auth.utils import *

router = APIRouter(prefix="/superadmin", tags=["superadmin"])

restaurant_service = RestaurantService()

http_bearer = HTTPBearer()


@router.post("/restaurants", response_model=CreatedRestaurant)
async def create_restaurant(restaurant: RestaurantCreateFromAPI,
                            payload: dict = Depends(get_current_token_payload),
                            db: AsyncSession = Depends(get_db)):
    """
    Создание нового ресторана

    Доступно только для пользователя с ролью Superadmin
    """
    role = payload.get("role")
    return await restaurant_service.create_restaurant(role, restaurant, db)


@router.get("/restaurants", response_model=List[RestaurantInfo])
async def get_all_restaurants(db: AsyncSession = Depends(get_db)):
    """
    Получение списка всех созданных ресторанов


    Доступно только для пользователя с ролью Superadmin
    """
    return await restaurant_service.get_list_of_restaurants(db)


@router.get("/restaurants/{restaurant_id}", response_model=RestaurantInfo)
async def get_restaurant_by_id(restaurant_id: int,
                               db: AsyncSession = Depends(get_db)):
    """
    Получение информации о ресторане по его id
    """
    role = payload.get("role")
    return await restaurant_service.get_restaurant_by_id(role, restaurant_id, db)
