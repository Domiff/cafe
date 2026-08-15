import secrets

from sqladmin.authentication import AuthenticationBackend
from fastapi import Request

from src.core.config import settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = str(form.get("username", ""))
        password = str(form.get("password", ""))

        is_valid = secrets.compare_digest(
            username, settings.admin.USERNAME
        ) & secrets.compare_digest(password, settings.admin.PASSWORD)

        if not is_valid:
            return False

        request.session["user"] = username
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return "user" in request.session
