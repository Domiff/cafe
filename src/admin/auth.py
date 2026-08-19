from fastapi import Request
from pwdlib.exceptions import UnknownHashError
from sqladmin.authentication import AuthenticationBackend

from src.staff.models import Staff
from src.staff.repository import get_staff_repo
from src.core.security import check_password
from src.core.database import session_maker


class AdminAuth(AuthenticationBackend):
    @staticmethod
    async def _get_account(username: str) -> Staff | None:
        if not username:
            return None

        async with session_maker() as session:
            return await get_staff_repo(session).get_by_username(username)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = str(form.get("username", ""))
        password = str(form.get("password", ""))

        account = await self._get_account(username)

        if account is None or not account.is_active:
            return False

        try:
            is_valid = check_password(password, account.password)
        except UnknownHashError:
            return False

        if not is_valid:
            return False

        request.session.update({"user": account.username, "role": account.role.name})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        account = await self._get_account(request.session.get("user", ""))
        return bool(account and account.is_active)
