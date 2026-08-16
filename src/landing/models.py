from sqlalchemy import CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base
from src.core.types import FileType


class Landing(Base):
    __tablename__ = "landing"
    __table_args__ = (CheckConstraint("id = 1", name="ck_landing_singleton"),)

    title: Mapped[str] = mapped_column(String(120))
    subtitle: Mapped[str | None] = mapped_column(String(250))
    hero_image: Mapped[str | None] = mapped_column(FileType)

    about_title: Mapped[str | None] = mapped_column(String(120))
    about_text: Mapped[str | None] = mapped_column(Text)

    address: Mapped[str] = mapped_column(String(250))
    phone: Mapped[str | None] = mapped_column(String(32))
    email: Mapped[str | None] = mapped_column(String(256))
    working_hours: Mapped[str | None] = mapped_column(String(250))
    map_url: Mapped[str | None] = mapped_column(String(500))

    vk_url: Mapped[str | None] = mapped_column(String(500))
    reviews_url: Mapped[str | None] = mapped_column(String(500))

    has_wifi: Mapped[bool] = mapped_column(default=True)
    has_sockets: Mapped[bool] = mapped_column(default=True)
    has_terrace: Mapped[bool] = mapped_column(default=False)
    is_pet_friendly: Mapped[bool] = mapped_column(default=False)
    has_takeaway: Mapped[bool] = mapped_column(default=True)

    def __str__(self) -> str:
        return self.title
