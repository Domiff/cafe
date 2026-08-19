from fastapi import APIRouter

from src.users.auth import fastapi_users, auth_backend
from src.users.schemas import UserRead, UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_auth_router(auth_backend))
