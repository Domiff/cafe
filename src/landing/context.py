from fastapi import Request
from redis.exceptions import (
    ConnectionError as RedisConnectionError,
    TimeoutError as RedisTimeoutError,
)

from src.landing.schemas import CafeSchema
from src.core.cache import redis
from src.core.database import session_maker
from src.landing.repository import get_landing_repository


async def load_cafe() -> CafeSchema | None:
    cache_key = "cafe"

    try:
        cached = await redis.get(cache_key)
        if cached:
            return CafeSchema.model_validate_json(cached)
    except (RedisConnectionError, RedisTimeoutError):
        pass

    async with session_maker() as session:
        landing = await get_landing_repository(session).get_landing()

    if landing is None:
        return None

    cached = CafeSchema.from_orm(landing)
    try:
        await redis.set(cache_key, cached.model_dump_json())
    except (RedisConnectionError, RedisTimeoutError):
        pass

    return cached


def cafe_context(request: Request) -> dict:
    return {"cafe": getattr(request.state, "cafe", None)}
