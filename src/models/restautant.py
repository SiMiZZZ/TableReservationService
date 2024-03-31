from uuid import uuid4
from enum import Enum
import uuid as uuid_pkg

import sqlalchemy
from sqlalchemy import Column, String, select, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship
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
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    account = relationship(User, lazy="selectin")
    account_id = Column(Integer, ForeignKey("users.id"), nullable=True)


