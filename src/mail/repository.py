from sqlalchemy import select

from src.mail.models import Message
from src.core.database import BaseRepository


class MessageRepository(BaseRepository):
    async def get_by_code(self, code: str) -> Message | None:
        query = select(Message).where(Message.code == code, Message.is_active == True)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


def get_message_repository(session) -> MessageRepository:
    return MessageRepository(session)
