from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import schemas

from schemas.restaurant import RestaurantInfo, RestaurantCreate, RestaurantCreateFromAPI, CreatedRestaurant
from services.database import get_db
from services.restaurant import RestaurantService
from auth.utils import *

router = APIRouter(tags=["all"])

restaurant_service = RestaurantService()

@router.get("/restaurants/{restaurant_id}/images")
async def get_all_restaurant_images(request: Request, restaurant_id: int, db: AsyncSession = Depends(get_db)):
    host = request.headers.get("referer")
    return await restaurant_service.get_restaurants_image(host, restaurant_id, db)