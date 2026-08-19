from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.core.cache import setup_cache
from src.admin.setup import setup_admin
from src.core.config import settings
from src.core.logging import get_logger
from src.cafe.router import router as cafe_router
from src.landing.router import router as landing_router
from src.users.router import router as users_router

logger = get_logger(__name__)


async def lifespan(app: FastAPI):
    logger.debug("Starting application")

    setup_cache("cafe")

    yield

    logger.debug("Stopping application")


def create_app() -> FastAPI:
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
