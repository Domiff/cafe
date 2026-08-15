from fastapi import Request
from pwdlib.exceptions import UnknownHashError
from sqladmin.authentication import AuthenticationBackend

from src.auth.models import User
from src.auth.repository import get_user_repo
from src.auth.utils import check_password
from src.core.database import session_maker


class AdminAuth(AuthenticationBackend):
    @staticmethod
    async def _get_user(username: str) -> User | None:
        if not username:
            return None

        async with session_maker() as session:
            return await get_user_repo(session).get_user_by_username(username)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = str(form.get("username", ""))
        password = str(form.get("password", ""))

        user = await self._get_user(username)

        if user is None or not user.is_active:
            return False

        try:
            check_password(password, user.password)
        except UnknownHashError:
            return False

        request.session.update({"user": user.username, "role": user.role.name})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        user = await self._get_user(request.session.get("user", ""))
        return bool(user and user.is_active)
