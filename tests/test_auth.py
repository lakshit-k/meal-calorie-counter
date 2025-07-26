import pytest
from httpx import AsyncClient
from app.main import app
from app.managers.redis_manager import RedisManager
from app.middleware.security import hash_password
from app.managers.user_manager import UserManager
from app.utils import get_current_datetime
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="module")
async def test_user_data():
    return {
        "name": "Test User",
        "email": "test@example.com",
        "phone_number": "1234567890",
        "password": "testpassword"
    }

@pytest.fixture(scope="module")
async def registered_user(test_user_data, async_session: AsyncSession):
    password_hash, password_salt = hash_password(test_user_data["password"])
    user = User(
        name=test_user_data["name"],
        email=test_user_data["email"],
        phone_number=test_user_data["phone_number"],
        password_hash=password_hash,
        password_salt=password_salt,
        created_at=get_current_datetime(),
        updated_at=get_current_datetime()
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    return user

@pytest.fixture(scope="module")
async def auth_tokens(async_client: AsyncClient, test_user_data):
    response = await async_client.post("/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    return response.json()

class TestAuthentication:

    async def test_register_user(self, async_client: AsyncClient, test_user_data):
        response = await async_client.post("/auth/register", json=test_user_data)
        assert response.status_code == 200
        assert response.json()["user_created"] is True
        assert "access_token" in response.json()
