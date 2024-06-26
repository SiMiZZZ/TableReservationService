import os
from tempfile import NamedTemporaryFile
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import schemas
from starlette.responses import FileResponse
from fastapi.responses import FileResponse

from models import Booking
from schemas.restaurant import (RestaurantInfo, RestaurantCreate, RestaurantCreateFromAPI,
                                CreatedRestaurant, RestaurantUpdate)
from schemas.table import TableInfo, TablesCreate
from schemas.user import NewUserReturn, UserCreate
from schemas.booking import BookingUpdate, BookingInfo
from services.database import get_db
from services.restaurant import RestaurantService
from auth.utils import *
from typing import Optional

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
                                  db: AsyncSession = Depends(get_db)
                                 ): #  payload: dict = Depends(get_current_token_payload)
    # await restaurant_service.create_restaurant_image(files, restaurant_id, db)


    return await restaurant_service.create_restaurant_image(files, restaurant_id, db)


@router.post("/restaurants/tables")
async def create_table(table: TablesCreate,
                       db: AsyncSession = Depends(get_db),
                       payload: dict = Depends(get_current_token_payload)):
    data = await restaurant_service.create_table(table, payload, db)
    # print(data[0].id, data[0].restaurant_id)
    return True


@router.delete("/restaurants/tables/{table_id}")
async def delete_table(table_id: int,
                       db: AsyncSession = Depends(get_db),
                       payload: dict = Depends(get_current_token_payload)):
    await restaurant_service.delete_table(table_id, payload, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/restaurants/bookings")
async def get_all_bookings(db: AsyncSession = Depends(get_db),
                       payload: dict = Depends(get_current_token_payload)):
    return await restaurant_service.get_all_bookings(payload, db)


@router.patch("/restaurants/bookings/{booking_id}", response_model=BookingInfo)
async def update_booking(booking_id: int,
                         booking: BookingUpdate,
                         db: AsyncSession = Depends(get_db)):
    return await restaurant_service.update_booking(booking_id, booking, db)
