import os
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import schemas
from starlette.responses import FileResponse
from fastapi.responses import FileResponse

from schemas.restaurant import (RestaurantInfo, RestaurantCreate, RestaurantCreateFromAPI,
                                CreatedRestaurant, RestaurantUpdate)
from schemas.table import TableInfo, TableCreate
from schemas.user import NewUserReturn, UserCreate
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


@router.post("/staff", response_model=NewUserReturn)
async def create_staff_user(user: UserCreate,
                            payload: dict = Depends(get_current_token_payload),
                            db: AsyncSession = Depends(get_db)):
    """
    Создание пользователя-работника ресторана со стороны администратора
    """

    return await restaurant_service.create_staff_user(user, payload, db)


@router.get("/staff/", response_model=List[UserData])
async def get_all_staff_users(payload: dict = Depends(get_current_token_payload),
                              db: AsyncSession = Depends(get_db)):
    return await restaurant_service.get_staff_users(payload, db)


@router.get("/tags/")
async def get_all_tags(payload: dict = Depends(get_current_token_payload)):
    return await restaurant_service.get_restaurant_tags(payload)


@router.post("/restaurants/{restaurant_id}/images")
async def upload_restaurant_image(restaurant_id: int,
                                  files: List[UploadFile] = File(...),
                                  db: AsyncSession = Depends(get_db),
                                  payload: dict = Depends(get_current_token_payload)):
    # await restaurant_service.create_restaurant_image(files, restaurant_id, db)
    return await restaurant_service.create_restaurant_image(files, restaurant_id, db)


@router.get("/restaurants/{restaurant_id}/imgages", response_class=FileResponse)
async def get_imgages():
    print(os.getcwd() + "/media/1/Фаербол.png")
    return os.getcwd() + "/media/1/Фаербол.png"


@router.post("/restaurants/tables", response_model=TableInfo)
async def create_table(table: TableCreate,
                       db: AsyncSession = Depends(get_db),
                       payload: dict = Depends(get_current_token_payload)):
    return await restaurant_service.create_table(table, payload, db)


@router.delete("/restaurants/tables/{table_id}")
async def delete_table(table_id: int,
                       db: AsyncSession = Depends(get_db),
                       payload: dict = Depends(get_current_token_payload)):
    await restaurant_service.delete_table(table_id, payload, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
