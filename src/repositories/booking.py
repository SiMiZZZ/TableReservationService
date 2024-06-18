import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import Column, Integer, DateTime, select, and_
from sqlalchemy.sql import func

from models.user import User as UserModel
from models.restautant import Restaurant as RestaurantModel
from models.booking import Booking as BookingModel
from models.table import Table as TableModel
from models.restaurant_image import RestaurantImage
from schemas.table import TablesCreate, TableCreate
from schemas.booking import BookingCreate, BookingUpdate


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
        q = (select(BookingModel).join(TableModel).join(RestaurantModel)
             .where(RestaurantModel.id == restaurant_id)
             .options(selectinload(BookingModel.table))
             .options(selectinload(BookingModel.user)))
        exec = await db.execute(q)
        bookings = exec.scalars().all()
        return bookings

    async def get_bookings_by_status(self, status: str, db: AsyncSession) -> List[BookingModel]:
        q = (select(BookingModel).join(TableModel)
             .where(BookingModel.status == status)
             .options(selectinload(BookingModel.table))
             .options(selectinload(BookingModel.user)))
        exec = await db.execute(q)
        bookings = exec.scalars().all()
        return bookings

    async def get_booking_by_id(self, booking_id: int, db: AsyncSession):
        q = (select(BookingModel).join(TableModel).join(RestaurantModel)
             .where(BookingModel.id == booking_id))
        exec = await db.execute(q)
        booking = exec.scalar()
        return booking

    async def get_bookings_by_date(self, date: datetime.datetime, db: AsyncSession) -> List[BookingModel]:
        stmt = select(BookingModel).where(
            func.date(BookingModel.time_from) == date.date()
        )

        result = await db.execute(stmt)
        bookings = result.scalars().all()
        return bookings

    async def update_booking(self,
                             booking_model: BookingModel,
                             booking: BookingUpdate,
                             db: AsyncSession) -> BookingModel:
        for name, value in booking.model_dump(exclude_unset=True).items():
            setattr(booking_model, name, value)
        await db.commit()
        await db.refresh(booking_model)
        return booking_model

    async def get_bookings_by_user(self, user_id: int, db: AsyncSession):
        q = (select(BookingModel).join(UserModel).join(TableModel).join(RestaurantModel)
             .where(UserModel.id == user_id))
        exec = await db.execute(q)
        bookings = exec.scalars().all()
        return bookings