from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from models import Message
from repositories.messages import MessagesRepository


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_db: bool):
        if add_to_db:
            await self.add_messages_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    # @staticmethod
    # async def add_messages_to_database(message: MessageCreate):
    #     async with async_session_maker() as session:
    #         stmt = insert(Messages).values(
    #             message=message
    #         )
    #         await session.execute(stmt)
    #         await session.commit()


manager = ConnectionManager()

class MessagesService:
    def __init__(self):
        self.message_repository = MessagesRepository()

    async def get_all_messages_from_chat(self,
                                         restaurant_id: int,
                                         user_id: int,
                                         db: AsyncSession) -> List[Message]:
        return await self.message_repository.get_messages_by_chat(restaurant_id, user_id, db)

    async def get_all_chats_messages(self):
        pass