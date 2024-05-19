from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from models.user import User as UserModel
from models.restautant import Restaurant as RestaurantModel
from models.booking import Booking as BookingModel
from models.restaurant_image import RestaurantImage
from schemas.table import TablesCreate, TableCreate
from schemas.booking import BookingCreate


class BookingRepository:

    async def create_booking(self, booking: BookingCreate,
                             table_id: int,
                             user_id: int,
                             db: AsyncSession,
                             time_to: None) -> BookingModel:
        booking = BookingModel(time_to=time_to, table_id=table_id, user_id=user_id, **booking.dict())
        db.add(booking)
        await db.commit()
        await db.refresh(booking)
        return booking

    async def delete_booking(self, booking_id: int, db: AsyncSession) -> None:
        q = delete(BookingModel).where(BookingModel.id == booking_id)
        await db.execute(q)
        await db.commit()

    async def get_bookings_by_restaurant(self, restaurant_id: int, db: AsyncSession):
        q = select(BookingModel).where(BookingModel.restaurant_id == restaurant_id).options(
            selectinload(BookingModel.table)).options(selectinload(BookingModel.user))
        exec = await db.execute(q)
        bookings = exec.scalars()
        return bookings
