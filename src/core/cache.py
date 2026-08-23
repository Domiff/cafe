from functools import lru_cache
from typing import Any, Callable, Dict, Optional, Tuple

from fastapi import Request, Response
from fastapi.responses import HTMLResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.coder import Coder
from redis.asyncio import Redis
from redis.exceptions import (
    ConnectionError as RedisConnectionError,
    TimeoutError as RedisTimeoutError,
)

from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)


class HTMLCoder(Coder):
    @classmethod
    def encode(cls, value: Response) -> bytes:
        return value.body

    @classmethod
    def decode(cls, value: bytes) -> HTMLResponse:
        return HTMLResponse(content=value)


@lru_cache
def _get_redis() -> Redis:
    return Redis.from_url(
        url=settings.redis.REDIS_URL,
        max_connections=settings.redis.CONNECTION_POOL_MAXSIZE,
        decode_responses=False,
    )


def path_key_builder(
    __function: Callable[..., Any],
    __namespace: str = "",
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    path = request.url.path if request else __function.__name__
    return f"{__namespace}:{path}"


def setup_cache(prefix: str) -> None:
    FastAPICache.init(
        RedisBackend(_get_redis()),
        prefix=prefix,
        expire=settings.redis.EXPIRE,
        coder=HTMLCoder,
        key_builder=path_key_builder,
    )


async def invalidate_cache(namespace: str | None = None) -> None:
    await FastAPICache.clear(namespace)


class RedisClient:
    def __init__(self):
        self.redis = _get_redis()

    async def set(self, key: str, value) -> None:
        try:
            await self.redis.set(key, value, ex=settings.redis.EXPIRE)
        except (RedisConnectionError, RedisTimeoutError):
            logger.error("Redis connection error", extra={"key": key}, exc_info=True)
            raise
        except Exception:
            logger.error("Redis set failed", extra={"key": key}, exc_info=True)
            raise

    async def get(self, key: str) -> str | None:
        try:
            value = await self.redis.get(key)
            if value:
                return value
            else:
                return None
        except (RedisConnectionError, RedisTimeoutError):
            logger.error("Redis connection error", extra={"key": key}, exc_info=True)
            raise
        except Exception:
            logger.error("Redis get failed", extra={"key": key}, exc_info=True)
            raise

    async def delete(self, key: str) -> None:
        try:
            await self.redis.delete(key)
        except (RedisConnectionError, RedisTimeoutError):
            logger.error("Redis connection error", extra={"key": key}, exc_info=True)
            raise
        except Exception:
            logger.error("Redis delete failed", extra={"key": key}, exc_info=True)
            raise


redis = RedisClient()
