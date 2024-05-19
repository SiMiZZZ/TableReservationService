from uuid import uuid4
from enum import Enum
import uuid as uuid_pkg

import sqlalchemy
from sqlalchemy import Column, String, select, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship
from fastapi_restful.guid_type import GUID
from sqlalchemy.sql import func
from sqlalchemy.types import LargeBinary

from .restautant import Restaurant
from .table import Table
from .user import User

from services.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    time_from = Column(DateTime)
    time_to = Column(DateTime)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=True)
    table = relationship(Table, lazy="selectin")
    people_count = Column(Integer, default=1)
    comment = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User, lazy="selectin")
    duration = Column(Integer)


