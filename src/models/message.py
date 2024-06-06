import enum

import sqlalchemy
from sqlalchemy import Column, String, select, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship
from fastapi_restful.guid_type import GUID
from sqlalchemy.sql import func
from sqlalchemy.types import LargeBinary
from .table import Table
from .user import User

from services.database import Base

class OwnerEnum(enum.Enum):
    CLIENT = "client"
    SUPPORT = "support"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    # created_at = Column(sqlalchemy.DateTime(timezone=True), server_default=func.now())
    # data = Column(String)
    # # user_id = Column(Integer, ForeignKey("users.id"))
    # # user = relationship("User", back_populates="chat_messages")
    # restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    # restaurant = relationship("Restaurant", back_populates="tables")
    # message_owner = Column(Enum(OwnerEnum))

