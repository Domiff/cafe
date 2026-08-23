from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from src.admin.setup import setup_admin
from src.core.broker import broker
from src.core.cache import setup_cache
from src.core.config import settings
from src.core.logging import get_logger, setup_logging
from src.landing.context import load_cafe
from src.cafe.router import router as cafe_router
from src.landing.router import router as landing_router
from src.users.routers import auth_router, pages_router, users_router

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

    @app.middleware("http")
    async def attach_cafe(request: Request, call_next):
        if not request.url.path.startswith("/static"):
            request.state.cafe = await load_cafe()

        return await call_next(request)

    app.include_router(cafe_router)
    app.include_router(landing_router)
    app.include_router(pages_router)
    app.include_router(auth_router)
    app.include_router(users_router)

    setup_admin(app)

    return app
