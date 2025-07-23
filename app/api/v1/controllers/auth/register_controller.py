from fastapi import Request
from app.api.deps import BaseController
from app.managers.user_manager import UserManager
from app.schemas.auth import UserCreate, UserRead
from app.core.security import hash_password
from app.utils.exceptions import BadRequestException
from sqlalchemy.ext.asyncio import AsyncSession

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
        return UserRead.model_validate(user)