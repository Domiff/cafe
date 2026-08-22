from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.admin.setup import setup_admin
from src.core.broker import broker
from src.core.cache import setup_cache
from src.core.config import settings
from src.core.logging import get_logger, setup_logging
from src.cafe.router import router as cafe_router
from src.landing.router import router as landing_router
from src.users.router import router as users_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")

    setup_cache("cafe")

    if not broker.is_worker_process:
        await broker.startup()
        logger.info("Starting broker")

    yield

    if not broker.is_worker_process:
        await broker.shutdown()
        logger.info("Stopping broker")

    logger.info("Stopping application")


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="Cafe",
        version="1",
        lifespan=lifespan,
        openapi_url="/openapi.json" if settings.app.IS_DEBUG else None,
    )
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(cafe_router)
    app.include_router(landing_router)
    app.include_router(users_router)

    setup_admin(app)

    return app
