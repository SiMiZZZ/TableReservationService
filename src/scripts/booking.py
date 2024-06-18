from datetime import datetime, time, timedelta
from typing import List, Tuple
from models.booking import Booking as BookingModel

def generate_available_slots(open_time: time,
                             close_time: time,
                             bookings: List[BookingModel]) -> List[time]:
    intervals = []
    current_time = datetime.combine(datetime.today(), open_time)
    close_datetime = datetime.combine(datetime.today(), close_time)

    while current_time + timedelta(minutes=30) <= close_datetime:
        intervals.append((current_time.time(), (current_time + timedelta(minutes=30)).time()))
        current_time += timedelta(minutes=30)

    available_intervals = []
    for interval_start, interval_end in intervals:
        is_available = True
        for booking in bookings:
            if interval_start >= booking.time_from.time() and interval_end <= booking.time_to.time():
                is_available = False
                break
        if is_available:
            available_intervals.append(interval_start)

    return available_intervals


