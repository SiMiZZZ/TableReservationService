import os
from tempfile import NamedTemporaryFile
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, Response, WebSocket, WebSocketDisconnect, Depends
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
from services.websocket import manager

router = APIRouter(tags=["ws"])

restaurant_service = RestaurantService()

http_bearer = HTTPBearer()

@router.websocket("/{client_id}/{restaurant_id}")
async def websocket_endpoint(websocket: WebSocket,
                             client_id: int,
                             payload: dict = Depends(get_current_token_payload)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)