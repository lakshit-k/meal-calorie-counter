from fastapi import Request
from app.api.deps import BaseController
from app.managers.user_manager import UserManager
from app.schemas.auth import UserCreate, UserRead
from app.middleware.security import hash_password
from app.utils.exceptions import BadRequestException
from sqlalchemy.ext.asyncio import AsyncSession
from app.processors.auth_processor import AuthProcessor

class RegisterController(BaseController):

    async def process_post(self, request: Request):
        data = await request.json()
        user_data = UserCreate(**data)
        db: AsyncSession = request.state.db
        existing = await UserManager.get_by_email(db, user_data.email)
        if existing:
            raise BadRequestException("Email already registered")
        password_hash, password_salt = hash_password(user_data.password)
        user = await UserManager.create_user(
            db,
            name=user_data.name,
            email=user_data.email,
            phone_number=user_data.phone_number,
            password_hash=password_hash,
            password_salt=password_salt
        )
        access_token = AuthProcessor.create_access_token({"sub": str(user.uuid), "email": user.email})
        refresh_token = AuthProcessor.create_refresh_token({"sub": str(user.uuid), "email": user.email})
        return {
            "user_created": True,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }