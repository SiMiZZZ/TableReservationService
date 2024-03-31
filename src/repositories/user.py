from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User as UserModel
from models.user import UserRole


class UserRepository:

    async def create_user(self, email: str, password: bytes, db: AsyncSession, role: str = UserRole.CLIENT) -> UserModel:
        user = UserModel(email=email, password=password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def get_user_by_email_or_none(self, email: str, db: AsyncSession) -> UserModel:
        q = select(UserModel).where(UserModel.email == email)
        exec = await db.execute(q)
        user = exec.scalar()
        return user

    async def get_user_by_id_or_none(self, id: int, db: AsyncSession) -> UserModel:
        q = select(UserModel).where(UserModel.id == id)
        exec = await db.execute(q)
        user = exec.scalar()
        return user
