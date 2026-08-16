from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.cafe.models import Category, Product
from src.core.database import BaseRepository


class CafeRepository(BaseRepository):
    async def get_menu(self) -> Sequence[Category]:
        query = (
            select(Category)
            .options(
                selectinload(Category.products.and_(Product.is_available.is_(True)))
            )
            .order_by(Category.name)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_product(self, product_id: int) -> Product | None:
        query = (
            select(Product)
            .where(Product.id == product_id)
            .options(selectinload(Product.category))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


def get_cafe_repository(session: AsyncSession) -> CafeRepository:
    return CafeRepository(session)
