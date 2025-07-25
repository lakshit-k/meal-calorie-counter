from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from uuid import uuid4
from app.utils import get_current_datetime

class UserManager:
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def create_user(db: AsyncSession, name: str, email: str, phone_number: str, password_hash: str, password_salt: str):
        user = User(
            uuid=str(uuid4()),
            name=name,
            email=email,
            phone_number=phone_number,
            password_hash=password_hash,
            password_salt=password_salt,
            created_at=get_current_datetime(),
            updated_at=get_current_datetime()
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update_last_login(db: AsyncSession, user: User):
        user.last_login_at = get_current_datetime()
        await db.commit()
        await db.refresh(user)
        return user
