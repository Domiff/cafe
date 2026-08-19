from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from src.staff.enums import Role
from src.core.database import Base


class Staff(Base):
    __tablename__ = "staff"

    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(250))
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.MANAGER)

    def __str__(self) -> str:
        return self.username
