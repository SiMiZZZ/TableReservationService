import os
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import schemas
from starlette.responses import FileResponse
from fastapi.responses import FileResponse

from schemas.restaurant import (RestaurantInfo, RestaurantCreate, RestaurantCreateFromAPI,
                                CreatedRestaurant, RestaurantUpdate)
from schemas.user import NewUserReturn, UserCreate
from services.database import get_db
from services.restaurant import RestaurantService
from auth.utils import *
from config import settings

router = APIRouter(prefix="/media", tags=["media"])

restaurant_service = RestaurantService()

@router.get("/{id}/{name}", response_class=FileResponse)
async def get_imgages(id: int, name: str):
    return settings.MEDIA_ROOT + f"/{id}/{name}"

