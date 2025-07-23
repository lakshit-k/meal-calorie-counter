from fastapi import APIRouter, Request
from app.api.deps import BaseController

class CaloriesController(BaseController):

    async def get(self, request: Request):
        return {"message": "Calories router is working!"}
