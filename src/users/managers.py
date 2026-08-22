from typing import Annotated

from fastapi import Request, Depends
from fastapi_users import BaseUserManager, IntegerIDMixin, models
from fastapi_users.db import SQLAlchemyUserDatabase

from src.mail.tasks import send_reset_password_task, send_register_task, send_verify_task
from src.core.logging import get_logger
from src.users.models import User
from src.core.database import SessionDep
from src.core.config import settings

logger = get_logger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.users.RESET_SECRET_KEY
    verification_token_secret = settings.users.VERIFICATION_SECRET_KEY

    async def on_after_register(
        self, user: User, request: Request | None = None
    ) -> None:
        await self.request_verify(user, request)

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        await send_verify_task.kiq(user.email, token)
        logger.info("Verification email sent", extra={"email": user.email})

    async def on_after_verify(
        self, user: models.UP, request: Request | None = None
    ) -> None:
        await send_register_task.kiq(user.email)
        logger.info("Welcome email sent", extra={"email": user.email})

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        await send_reset_password_task.kiq(user.email, token)
        logger.info("Password reset email sent", extra={"email": user.email})


async def get_user_manager(session: SessionDep) -> UserManager:
    return UserManager(SQLAlchemyUserDatabase(session, User))

UserManagerDep = Annotated[UserManager, Depends(get_user_manager)]
