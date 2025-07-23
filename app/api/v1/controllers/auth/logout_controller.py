from fastapi import Request
from app.api.deps import BaseController
from sqlalchemy.ext.asyncio import AsyncSession

class LogoutController(BaseController):
    def __init__(self, prefix: str):
        super().__init__(prefix)
        self.add_new_route("/", "POST", self.post)

    async def process_post(self,db: AsyncSession, request: Request):
        return {"message": "Logout successful (client should discard token)"}