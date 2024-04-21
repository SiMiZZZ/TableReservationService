from uuid import uuid4
from enum import Enum
import uuid as uuid_pkg

import sqlalchemy
from sqlalchemy import Column, String, select, Integer, ForeignKey, Boolean, Double
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship, Relationship
from sqlalchemy.types import Float, DOUBLE, REAL
from sqlalchemy.dialects.postgresql import ARRAY
from fastapi_restful.guid_type import GUID
from sqlalchemy.sql import func
from sqlalchemy.types import LargeBinary

from services.database import Base
from .user import User
from .restautant import Restaurant

class RestaurantImage(Base):
    __tablename__ = "restaurant_images"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    path = Column(String, nullable=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=True)
    restaurant = account = relationship(Restaurant, lazy="selectin")
