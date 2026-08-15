from fastapi import FastAPI

from src.admin.setup import setup_admin
from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)


async def lifespan(app: FastAPI):
    logger.debug("Starting application")

    yield

    logger.debug("Stopping application")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Cafe",
        version="1",
        lifespan=lifespan,
        openapi_url="/openapi.json" if settings.app.IS_DEBUG else None,
    )

    setup_admin(app)

    return app
