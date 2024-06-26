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


class UserRole:
    SUPER_ADMIN = "superadmin"
    ADMIN = "admin"
    STAFF = "staff"
    CLIENT = "client"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String, default="client")
    phone_number = Column(String, nullable=True)
    email = Column(String, unique=True)
    password = Column(BYTEA, nullable=True)
    created_at = Column(sqlalchemy.DateTime(timezone=True), server_default=func.now())

