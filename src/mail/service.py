from fastapi_mail.schemas import MessageType, MessageSchema as MailMessage
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from src.core.config import settings
from src.core.logging import get_logger
from src.mail.enums import MessageCode
from src.mail.repository import get_message_repository
from src.mail.config import mail
from src.mail.schemas import MessageSchema

logger = get_logger(__name__)


class MailService:
    def __init__(self, session: AsyncSession):
        self.fm = mail
        self.repo = get_message_repository(session)

    @staticmethod
    def _build_context(message: MessageSchema, link: str | None = None):
        context = {
            "subject": message.subject,
            "title": message.title,
            "body": message.body,
        }

        if link:
            context["link"] = link

        return context

    async def _send(self, code: MessageCode, email: EmailStr, link: str | None = None):
        message = await self.repo.get_by_code(code)
        message_schema = MessageSchema.from_orm(message)
        mail_message = MailMessage(
            subject=message_schema.subject,
            recipients=[email],
            template_body={**self._build_context(message_schema, link)},
            subtype=MessageType.html,
        )
        await self.fm.send_message(mail_message, template_name="email_message.html")

    async def send_register(self, email: EmailStr):
        await self._send(MessageCode.REGISTER, email)

    async def send_verify(self, email: EmailStr, token: str):
        link = f"{settings.BASE_URL}/auth/verify?token={token}"
        await self._send(MessageCode.VERIFY, email, link)

    async def send_reset_password(self, email: EmailStr, token: str):
        link = f"{settings.BASE_URL}/auth/reset-password?token={token}"
        await self._send(MessageCode.RESET_PASSWORD, email, link)
