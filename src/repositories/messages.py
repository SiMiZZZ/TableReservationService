from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.message import Message as MessageModel
from models.user import User as UserModel
from models.table import Table
from models.restaurant_image import RestaurantImage
from schemas.restaurant import RestaurantCreate, RestaurantUpdate, CreatedRestaurant, RestaurantImageCreate


class MessagesRepository:

    async def create_message(self, message: RestaurantCreate,
                             db: AsyncSession) -> MessageModel:
        message_entity = MessageModel(**message.dict())
        db.add(message_entity)
        await db.commit()
        await db.refresh(message_entity)
        return message_entity

    async def get_messages_by_chat(self,
                                   restaurant_id: int,
                                   user_id: int,
                                   db: AsyncSession) -> List[MessageModel]:
        q = (select(MessageModel)
             .where(MessageModel.restaurant_id == restaurant_id and MessageModel.user_id == user_id))
        exec = await db.execute(q)
        messages = exec.scalar()
        return messages

    async def get_all_user_chat_id(self,
                                   restaurant_id: int,
                                   db: AsyncSession) -> List[int]:
        q = (select(UserModel.id, UserModel.name).join(UserModel)
             .where(MessageModel.restaurant_id == restaurant_id))
        exec = await db.execute(q)
        users_id = exec.scalars().all()
        return users_id
