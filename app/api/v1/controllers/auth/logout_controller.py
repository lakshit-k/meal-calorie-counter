from fastapi import Request
from app.api.deps import BaseController
from sqlalchemy.ext.asyncio import AsyncSession
from app.processors.auth_processor import AuthProcessor
from app.utils.exceptions import UnauthorizedException
from app.managers.redis_manager import RedisManager

class LogoutController(BaseController):
    def __init__(self, prefix: str):
        super().__init__(prefix)
        self.add_new_route("/", "POST", self.post)

    async def process_post(self, request: Request):
        data = await request.json()
        refresh_token = data.get("refresh_token")
        if not refresh_token:
            raise UnauthorizedException("Refresh token is required")
        if await RedisManager.get_key(f"blacklist:{refresh_token}"):
            raise UnauthorizedException("Refresh token is already blacklisted")
        payload = AuthProcessor.verify_token(refresh_token, expected_type="refresh")
        if not payload:
            raise UnauthorizedException("Invalid refresh token")

        await RedisManager.set_key_with_ttl(f"blacklist:{refresh_token}", "blacklisted", 86400) # 1 day TTL
        return {"message": "Logged out successfully"}
