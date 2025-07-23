import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.models_base import Base
import datetime
from app.utils import get_current_datetime

class User(Base):
    __tablename__ = 'users'
    uuid = Column(String(37), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    password_salt = Column(String, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=get_current_datetime(), nullable=False)
    updated_at = Column(DateTime, default=get_current_datetime(), onupdate=get_current_datetime(), nullable=False)
