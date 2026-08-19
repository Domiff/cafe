from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.staff.models import Staff
from src.core.database import BaseRepository


class StaffRepository(BaseRepository):
    async def get_by_username(self, username: str) -> Staff | None:
        query = select(Staff).where(Staff.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


def get_staff_repo(session: AsyncSession) -> StaffRepository:
    return StaffRepository(session)
