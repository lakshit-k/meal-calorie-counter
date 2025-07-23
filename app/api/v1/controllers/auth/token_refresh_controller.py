from fastapi import Request
from app.api.deps import BaseController
from app.processors.auth_processor import AuthProcessor
from app.utils.exceptions import UnauthorizedException
from sqlalchemy.ext.asyncio import AsyncSession

class RefreshController(BaseController):
    def __init__(self, prefix: str):
        super().__init__(prefix)
        self.add_new_route("/", "POST", self.post)

    async def process_post(self, request: Request):
        data = await request.json()
        db: AsyncSession = request.state.db
        token = data.get("refresh_token")
        payload = AuthProcessor.verify_token(token, expected_type="refresh")
        if not payload:
            raise UnauthorizedException("Invalid refresh token")
        new_token = AuthProcessor.create_access_token({"sub": payload["sub"], "email": payload["email"]})
        return {"access_token": new_token, "token_type": "bearer"}