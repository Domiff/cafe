from fastapi import FastAPI
from guard import SecurityConfig, SecurityMiddleware, SecurityDecorator

from src.core.config import settings

config = SecurityConfig(
    enable_rate_limiting=settings.security.ENABLE_RATE_LIMITING,
    rate_limit=settings.security.RATE_LIMIT,
    rate_limit_window=settings.security.RATE_LIMIT_WINDOW,
    enable_redis=settings.security.ENABLE_REDIS,
    redis_url=settings.redis.REDIS_URL,
    redis_prefix=settings.security.REDIS_PREFIX,
    custom_log_file=settings.security.CUSTOM_LOG_FILE,
    endpoint_rate_limits={
        "/auth/login": (5, 60),
        "/auth/register": (3, 60),
        "/auth/forgot-password": (3, 300),
        "/auth/reset-password": (5, 300),
        "/auth/request-verify-token": (3, 300),
        "/auth/verify": (5, 300),
    },
)
guard = SecurityDecorator(config)


def setup_security(app: FastAPI) -> None:
    app.state.guard_decorator = guard
    app.add_middleware(SecurityMiddleware, config=config)
