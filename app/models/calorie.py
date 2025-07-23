import uuid
from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from app.db.models_base import Base
import datetime

class Calorie(Base):
    __tablename__ = 'calories'
    uuid = Column(String(37), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    title = Column(String, nullable=False)
    ingredients = Column(String, nullable=False)  # You can use JSON or Text for more complex data
    calorie_calculation = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.timezone.utc, nullable=False)
    updated_at = Column(DateTime, default=datetime.timezone.utc, onupdate=datetime.timezone.utc, nullable=False)
