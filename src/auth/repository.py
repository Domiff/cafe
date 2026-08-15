from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.core.database import SessionDep


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_user_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


def get_user_repo(session: SessionDep) -> UserRepository:
    return UserRepository(session)
