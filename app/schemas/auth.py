from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    password: str

class UserRead(BaseModel):
    uuid: UUID
    name: str
    email: EmailStr
    phone_number: str
    last_login_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str
