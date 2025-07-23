from fastapi import Request
from app.api.deps import BaseController
from app.managers.user_manager import UserManager
from app.schemas.auth import UserLogin
from app.core.security import verify_password
from app.processors.auth_processor import AuthProcessor
from app.utils.exceptions import UnauthorizedException
from sqlalchemy.ext.asyncio import AsyncSession

class LoginController(BaseController):

    async def process_post(self, request: Request):
        data = await request.json()
        login_data = UserLogin(**data)
        db: AsyncSession = request.state.db
        user = await UserManager.get_by_email(db, login_data.email)
        if not user or not verify_password(login_data.password, user.password_hash, user.password_salt):
            raise UnauthorizedException("Invalid credentials")
        await UserManager.update_last_login(db, user)
        access_token = AuthProcessor.create_access_token({"sub": str(user.uuid), "email": user.email})
        refresh_token = AuthProcessor.create_refresh_token({"sub": str(user.uuid), "email": user.email})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }