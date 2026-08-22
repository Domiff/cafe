from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends

from src.core.broker import broker
from src.core.database import get_session
from src.mail.service import get_mail_service


@broker.task("send_register_task", retry_on_error=True)
async def send_register_task(
    email: str, session: Annotated[AsyncSession, TaskiqDepends(get_session)]
):
    await get_mail_service(session).send_register(email)


@broker.task("send_verify_task", retry_on_error=True)
async def send_verify_task(
    email: str, token: str, session: Annotated[AsyncSession, TaskiqDepends(get_session)]
):
    await get_mail_service(session).send_verify(email, token)


@broker.task("send_reset_password_task", retry_on_error=True)
async def send_reset_password_task(
    email: str, token: str, session: Annotated[AsyncSession, TaskiqDepends(get_session)]
):
    await get_mail_service(session).send_reset_password(email, token)
