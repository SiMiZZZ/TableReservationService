from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import schemas

from schemas.user import UserAuthData, UserAuthReturn, UserData
from services.database import get_db
from services.user import UserService
from auth.utils import *

router = APIRouter(prefix="/auth", tags=["auth"])

auth_service = UserService()



@router.post("/register", response_model=UserAuthReturn)
async def register(user: UserAuthData, db: AsyncSession = Depends(get_db)) -> UserAuthReturn:
    return await auth_service.register_user(user, db)


@router.post("/login", response_model=UserAuthReturn)
async def login(user: UserAuthData, db: AsyncSession = Depends(get_db)) -> UserAuthReturn:
    return await auth_service.login_user(user, db)


@router.get("/user", response_model=UserData)
async def get_authorised_user(payload: dict = Depends(get_current_token_payload), db: AsyncSession = Depends(get_db)):
    return await auth_service.get_user_by_id(payload["id"], db)
