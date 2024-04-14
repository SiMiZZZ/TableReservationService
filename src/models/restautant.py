from uuid import uuid4
from enum import Enum
import uuid as uuid_pkg

import sqlalchemy
from sqlalchemy import Column, String, select, Integer, ForeignKey, Boolean, Double
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship
from sqlalchemy.types import Float, DOUBLE, REAL
from sqlalchemy.dialects.postgresql import ARRAY
from fastapi_restful.guid_type import GUID
from sqlalchemy.sql import func
from sqlalchemy.types import LargeBinary

from services.database import Base
from .user import User

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    city = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String, nullable=True)
    site = Column(String, nullable=True)
    tags = Column(ARRAY(String), nullable=True, default=[])
    account = relationship(User, lazy="selectin")
    phone_number = Column(String, nullable=True)
    active = Column(Boolean, nullable=True, default=False)
    account_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    open_from = Column(String, nullable=True)
    open_to = Column(String, nullable=True)


