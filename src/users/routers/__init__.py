from src.users.routers.auth import router as auth_router
from src.users.routers.pages import router as pages_router
from src.users.routers.users import router as users_router


__all__ = ["auth_router", "pages_router", "users_router"]
