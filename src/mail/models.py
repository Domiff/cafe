from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base
from src.mail.enums import MessageCode


class Message(Base):
    __tablename__ = "messages"

    code: Mapped[MessageCode] = mapped_column(unique=True, index=True)
    subject: Mapped[str] = mapped_column(String(120))
    title: Mapped[str] = mapped_column(String(120))
    body: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(default=True)

    def __str__(self) -> str:
        return self.code
