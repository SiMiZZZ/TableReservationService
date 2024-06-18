from worker import app
from repositories.booking import BookingRepository
from services.database import get_db
from schemas.booking import BookingUpdate
import datetime
import asyncio

@app.task
def update_bookings_status_task():
    asyncio.run(update_confirmed_booking_status())


booking_repository = BookingRepository()


async def update_confirmed_booking_status():
    async with get_db() as db:
        bookings = await booking_repository.get_bookings_by_status("confirmed", db)
        for booking in bookings:
            if booking.time_to < datetime.datetime.now():
                await booking_repository.update_booking(booking, BookingUpdate(status="completed"), db)

