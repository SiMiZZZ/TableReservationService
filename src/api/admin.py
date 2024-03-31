from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import schemas

from schemas.restaurant import (RestaurantInfo, RestaurantCreate, RestaurantCreateFromAPI,
                                CreatedRestaurant, RestaurantUpdate)
from services.database import get_db
from services.restaurant import RestaurantService
from auth.utils import *

router = APIRouter(prefix="/admin", tags=["admin"])

restaurant_service = RestaurantService()

http_bearer = HTTPBearer()


@router.get("/restaurants", response_model=RestaurantInfo)
async def get_admin_restaurant(payload: dict = Depends(get_current_token_payload),
                               db: AsyncSession = Depends(get_db)):
    """
    Получить информацию о ресторане, админом которого является авторизованный пользователь
    :param payload:
    :param db:
    :return:
    """
    return await restaurant_service.get_admin_restaurant(payload, db)


@router.patch("/restaurants", response_model=RestaurantInfo)
async def update_restaurant_by_admin(restaurant: RestaurantUpdate,
                                     payload: dict = Depends(get_current_token_payload),
                                     db: AsyncSession = Depends(get_db)):
    """
    Обновить данные о ресторане, админом которого является авторизованный пользователь
    """

    return await restaurant_service.update_restaurant_data(restaurant, payload, db)
