from fastapi import APIRouter

from src.users.auth import CurrentUserDep
from src.users.schemas import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def me(user: CurrentUserDep) -> UserRead:
    return UserRead.model_validate(user)
