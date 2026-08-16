from functools import lru_cache
from typing import Any, Callable, Dict, Optional, Tuple

from fastapi import Request, Response
from fastapi.responses import HTMLResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.coder import Coder
from redis.asyncio import Redis

from src.core.config import settings


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
