from fastapi import APIRouter, Request, HTTPException
from app.api.deps import BaseController
from app.managers.user_manager import UserManager
from app.schemas.auth import UserCreate, UserLogin, UserRead
from app.core.security import hash_password, verify_password
from app.processors.auth_processor import AuthProcessor
from sqlalchemy.ext.asyncio import AsyncSession
import json

class AuthController(BaseController):

    def __init__(self, prefix: str):
        super().__init__(prefix)
        self.add_new_route("/login", "POST", self.login)
        self.add_new_route("/register", "POST", self.register)
        self.add_new_route("/logout", "POST", self.logout)
        self.add_new_route("/refresh", "POST", self.refresh)
        

    async def login(self, request: Request):
        data = await request.json()
        login_data = UserLogin(**data)
        db: AsyncSession = request.state.db  # Ensure DB session is set in middleware/dependency
        user = await UserManager.get_by_email(db, login_data.email)
        if not user or not verify_password(login_data.password, user.password_hash, user.password_salt):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        await UserManager.update_last_login(db, user)
        token = AuthProcessor.create_access_token({"sub": str(user.uuid), "email": user.email})
        return {"access_token": token, "token_type": "bearer"}
    
    async def register(self, request: Request):
        data = await request.json()
        user_data = UserCreate(**data)
        db: AsyncSession = request.state.db
        existing = await UserManager.get_by_email(db, user_data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        password_hash, password_salt = hash_password(user_data.password)
        user = await UserManager.create_user(
            db,
            name=user_data.name,
            email=user_data.email,
            phone_number=user_data.phone_number,
            password_hash=password_hash,
            password_salt=password_salt
        )
        return UserRead.from_orm(user).dict()
    
    async def logout(self, request: Request):
        # For stateless JWT, logout is handled client-side (token discard). Optionally, implement token blacklist.
        return {"message": "Logout successful (client should discard token)"}
    
    async def refresh(self, request: Request):
        data = await request.json()
        token = data.get("refresh_token")
        payload = AuthProcessor.verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        new_token = AuthProcessor.create_access_token({"sub": payload["sub"], "email": payload["email"]})
        return {"access_token": new_token, "token_type": "bearer"}

