from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase

from src.users.models import User
from src.core.database import SessionDep
from src.core.config import settings


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.users.RESET_SECRET_KEY
    verification_token_secret = settings.users.VERIFICATION_SECRET_KEY


async def get_user_manager(session: SessionDep):
    yield UserManager(SQLAlchemyUserDatabase(session, User))
