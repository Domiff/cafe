from datetime import date
from decimal import Decimal

from sqlalchemy import String, func, Numeric, Text, ForeignKey, CheckConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from src.core.database import Base
from src.cafe.enums import EmploymentType
from src.core.types import FileType


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = (
        CheckConstraint("salary >= 0", name="ck_employees_salary_non_negative"),
    )

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100), index=True)
    patronymic: Mapped[str | None] = mapped_column(String(100))

    employment_type: Mapped[EmploymentType] = mapped_column(
        Enum(EmploymentType), index=True
    )

    phone: Mapped[str | None] = mapped_column(String(32), index=True, unique=True)
    email: Mapped[str | None] = mapped_column(String(256), index=True, unique=True)

    salary: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    hired_at: Mapped[date | None]
    fired_at: Mapped[date | None]
    birth_date: Mapped[date | None]

    position_id: Mapped[int] = mapped_column(
        ForeignKey("positions.id", ondelete="RESTRICT")
    )
    position: Mapped["Position"] = relationship(back_populates="employees")

    @hybrid_property
    def full_name(self) -> str:
        parts = [self.last_name, self.first_name, self.patronymic]
        return " ".join(p for p in parts if p)

    @full_name.inplace.expression
    @classmethod
    def _full_name(cls):
        return func.trim(
            func.coalesce(cls.last_name, "")
            + " "
            + func.coalesce(cls.first_name, "")
            + " "
            + func.coalesce(cls.patronymic, "")
        )

    def __str__(self) -> str:
        return self.full_name


class Position(Base):
    __tablename__ = "positions"
    __table_args__ = (
        CheckConstraint(
            "salary_min IS NULL OR salary_min >= 0",
            name="ck_positions_salary_min_non_negative",
        ),
        CheckConstraint(
            "salary_min IS NULL OR salary_max IS NULL OR salary_max >= salary_min",
            name="ck_positions_salary_range",
        ),
    )

    name: Mapped[str] = mapped_column(String(100), index=True, unique=True)
    description: Mapped[str | None] = mapped_column(Text)

    salary_min: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    salary_max: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))

    employees: Mapped[list["Employee"]] = relationship(
        back_populates="position", passive_deletes="all"
    )

    def __str__(self) -> str:
        return self.name


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(FileType)

    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def __str__(self) -> str:
        return self.name


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    image_url: Mapped[str | None] = mapped_column(FileType)

    is_available: Mapped[bool] = mapped_column(default=True)

    weight_grams: Mapped[int | None]
    volume_ml: Mapped[int | None]
    calories: Mapped[int | None]

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="products")

    def __str__(self) -> str:
        return self.name
