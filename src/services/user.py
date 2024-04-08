from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user import UserRepository
from schemas.user import UserAuthReturn, UserAuthData, UserData
from auth.utils import *

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def register_user(self, user: UserAuthData, db: AsyncSession) -> UserAuthReturn:
        # Проверка наличия пользователя с таким email
        has_user = await self.repository.get_user_by_email_or_none(user.email, db)
        if has_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with current email is already registered"
            )
        hashed_password = hash_password(user.password)
        user = await self.repository.create_user(user.email, hashed_password, db)

        token = encode_jwt({'id': user.id, "role": user.role})

        return UserAuthReturn(id=user.id, token=token, email=user.email)

    async def login_user(self, user: UserAuthData, db: AsyncSession) -> UserAuthReturn:
        user_from_db = await self.repository.get_user_by_email_or_none(user.email, db)

        if not user_from_db:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
        password_is_valid = validate_password(user.password, user_from_db.password)
        if not password_is_valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

        token = encode_jwt({'id': user_from_db.id, "role": user_from_db.role})
        return UserAuthReturn(id=user_from_db.id, token=token, email=user.email)

    async def get_user_by_id(self, id: int, db: AsyncSession) -> UserData:
        user = await self.repository.get_user_by_id_or_none(id, db)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect id")
        return user

