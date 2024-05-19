from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import schemas

from schemas.user import UserAuthData, UserAuthReturn, UserData, UserRegisteredData
from services.database import get_db
from services.user import UserService
from auth.utils import *

router = APIRouter(prefix="/client", tags=["client"])

auth_service = UserService()

http_bearer = HTTPBearer()

@router.post("/auth/register", response_model=UserAuthReturn)
async def register_client_user(user: UserRegisteredData, db: AsyncSession = Depends(get_db)) -> UserAuthReturn:
    """
    Регистрация клиента
    """
    return await auth_service.register_user(user, db)


@router.post("/auth/login", response_model=UserAuthReturn)
async def login_client_user(user: UserAuthData, db: AsyncSession = Depends(get_db)) -> UserAuthReturn:
    """
    Ааторизация клиента

    """
    return await auth_service.login_user(user, db)


@router.get("/user", response_model=UserData)
async def get_authorised_user_information(
        user_id: int = Depends(get_current_user_id),
        db: AsyncSession = Depends(get_db)):
    """
    Получение информации о авторизированном пользователе

    Требуется токен
    """
    return await auth_service.get_user_by_id(user_id, db)


