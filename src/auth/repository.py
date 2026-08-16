from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.core.database import BaseRepository


class UserRepository(BaseRepository):
    async def get_user_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


def get_user_repo(session: AsyncSession) -> UserRepository:
    return UserRepository(session)
