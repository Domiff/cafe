from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import BaseRepository
from src.landing.models import Landing


class LandingRepository(BaseRepository):
    async def get_landing(self) -> Landing | None:
        query = select(Landing).limit(1)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


def get_landing_repository(session: AsyncSession) -> LandingRepository:
    return LandingRepository(session)
