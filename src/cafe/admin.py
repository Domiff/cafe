from fastapi import Request
from wtforms import SelectField
from wtforms.validators import Optional, Regexp

from src.auth.enums import Role
from src.cafe.enums import EmploymentType
from src.cafe.models import Employee, Position, Category, Product
from src.cafe.formattes import phone
from src.admin.filters import (
    RuOperationColumnFilter,
    RuBooleanFilter,
    RuForeignKeyFilter,
)
from src.admin.base import BaseAdmin


class EmployeeAdmin(BaseAdmin, model=Employee):
    allowed_roles = {Role.ADMIN.name, Role.MANAGER.name}
    write_roles = {Role.ADMIN.name}

    column_list = [
        Employee.full_name,
        Employee.position,
        Employee.phone,
        Employee.hired_at,
        Employee.fired_at,
    ]
    column_details_list = [
        Employee.full_name,
        Employee.position,
        Employee.employment_type,
        Employee.salary,
        Employee.phone,
        Employee.email,
        Employee.birth_date,
        Employee.hired_at,
        Employee.fired_at,
    ]
    column_labels = {
        Employee.full_name: "ФИО",
        Employee.first_name: "Имя",
        Employee.last_name: "Фамилия",
        Employee.patronymic: "Отчество",
        Employee.position: "Должность",
        Employee.employment_type: "Тип занятости",
        Employee.salary: "Зарплата",
        Employee.phone: "Номер телефона",
        Employee.email: "Email",
        Employee.birth_date: "Дата рождения",
        Employee.hired_at: "Дата найма",
        Employee.fired_at: "Дата увольнения",
    }
    column_searchable_list = [Employee.last_name, Employee.first_name, Employee.phone]
    column_sortable_list = [
        Employee.last_name,
        Employee.hired_at,
        Employee.fired_at,
    ]
    column_default_sort = [("last_name", False)]
    column_filters = [
        RuForeignKeyFilter(
            Employee.position_id,
            Position.name,
            foreign_model=Position,
            title="Должность",
        ),
        RuOperationColumnFilter(Employee.hired_at, title="Дата найма"),
        RuOperationColumnFilter(Employee.fired_at, title="Дата увольнения"),
    ]
    column_formatters = {Employee.phone: phone}
    column_formatters_detail = {Employee.phone: phone}

    form_overrides = {"employment_type": SelectField}
    form_args = {
        "phone": {
            "validators": [
                Optional(),
                Regexp(r"^\+?[0-9\s\-()]{7,20}$", message="Формат: +7 900 123-45-67"),
            ]
        },
        "employment_type": {
            "choices": [(e.name, e.value) for e in EmploymentType],
            # без coerce SelectField сравнивает choices со str(enum), а у StrEnum
            # это значение, а не имя — текущий вариант не подсвечивается
            "coerce": lambda v: v.name if isinstance(v, EmploymentType) else str(v),
        },
    }
    form_create_rules = [
        "last_name",
        "first_name",
        "patronymic",
        "birth_date",
        "position",
        "employment_type",
        "salary",
        "phone",
        "email",
        "hired_at",
    ]
    form_edit_rules = form_create_rules + ["fired_at"]

    icon = "fa-solid fa-users"
    category = "Персонал"
    category_icon = "fa-solid fa-id-card"

    name = "Сотрудник"
    name_plural = "Сотрудники"

    async def on_model_change(
        self, data: dict, model: Employee, is_created: bool, request: Request
    ):
        hired, fired = data.get("hired_at"), data.get("fired_at")

        if fired and not hired:
            raise ValueError("Нельзя уволить сотрудника без даты найма")

        if hired and fired and fired < hired:
            raise ValueError("Дата увольнения раньше даты найма")

        salary = data.get("salary")
        if salary is not None and salary < 0:
            raise ValueError("Зарплата не может быть отрицательной")


class PositionAdmin(BaseAdmin, model=Position):
    allowed_roles = {Role.ADMIN.name, Role.MANAGER.name}
    write_roles = {Role.ADMIN.name}

    column_list = [
        Position.name,
        Position.description,
        Position.salary_min,
        Position.salary_max,
    ]
    column_details_list = [
        Position.name,
        Position.description,
        Position.salary_min,
        Position.salary_max,
    ]
    column_labels = {
        Position.name: "Должность",
        Position.description: "Описание должности",
        Position.salary_min: "Минимальная зарплата",
        Position.salary_max: "Максимальная зарплата",
        Position.employees: "Сотрудники",
    }
    column_searchable_list = [Position.name]
    column_sortable_list = [Position.name, Position.salary_min, Position.salary_max]
    form_create_rules = form_edit_rules = [
        "name",
        "description",
        "salary_min",
        "salary_max",
    ]

    icon = "fa-solid fa-briefcase"
    category = "Персонал"
    category_icon = "fa-solid fa-id-card"

    name = "Должность"
    name_plural = "Должности"

    async def on_model_change(
        self, data: dict, model: Position, is_created: bool, request: Request
    ):
        salary_min, salary_max = data.get("salary_min"), data.get("salary_max")

        if (salary_min and salary_max) and (salary_min > salary_max):
            raise ValueError(
                "Минимальная граница зарплаты не может превышать максимальную"
            )


class CategoryAdmin(BaseAdmin, model=Category):
    allowed_roles = write_roles = {Role.ADMIN.name, Role.MANAGER.name}

    column_list = [
        Category.name,
        Category.description,
    ]
    column_details_list = [
        Category.name,
        Category.description,
        Category.image_url,
    ]
    column_labels = {
        Category.name: "Категория",
        Category.description: "Описание",
        Category.image_url: "Изображение",
    }
    column_searchable_list = [Category.name]
    column_sortable_list = [Category.name]

    form_create_rules = form_edit_rules = [
        "name",
        "description",
        "image_url",
    ]

    icon = "fa-solid fa-layer-group"
    category = "Меню"
    category_icon = "fa-solid fa-utensils"

    name = "Категория"
    name_plural = "Категории"


class ProductAdmin(BaseAdmin, model=Product):
    allowed_roles = write_roles = {Role.ADMIN.name, Role.MANAGER.name}

    column_list = [
        Product.name,
        Product.description,
        Product.price,
        Product.is_available,
        Product.weight_grams,
        Product.volume_ml,
        Product.calories,
        Product.category,
    ]
    column_details_list = [
        Product.name,
        Product.description,
        Product.price,
        Product.image_url,
        Product.is_available,
        Product.weight_grams,
        Product.volume_ml,
        Product.calories,
        Product.category,
    ]
    column_labels = {
        Product.name: "Название",
        Product.description: "Описание",
        Product.price: "Цена",
        Product.image_url: "Изображение",
        Product.is_available: "В наличии",
        Product.weight_grams: "Вес, г",
        Product.volume_ml: "Объём, мл",
        Product.calories: "Калорийность",
        Product.category: "Категория",
    }
    column_searchable_list = [Product.name]
    column_sortable_list = [
        Product.name,
        Product.price,
        Product.is_available,
        Product.weight_grams,
        Product.volume_ml,
        Product.calories,
    ]
    column_filters = [
        RuBooleanFilter(
            Product.is_available,
            title="Наличие",
            true_label="В наличии",
            false_label="Нет в наличии",
        ),
        RuForeignKeyFilter(
            Product.category_id, Category.name, foreign_model=Category, title="Категория"
        ),
        RuOperationColumnFilter(Product.weight_grams, title="Вес блюда"),
        RuOperationColumnFilter(Product.volume_ml, title="Объём напитка"),
        RuOperationColumnFilter(Product.calories, title="Количество калорий"),
    ]

    form_create_rules = form_edit_rules = [
        "name",
        "description",
        "price",
        "image_url",
        "is_available",
        "weight_grams",
        "volume_ml",
        "calories",
        "category",
    ]

    icon = "fa-solid fa-mug-hot"
    category = "Меню"
    category_icon = "fa-solid fa-utensils"

    name = "Блюдо"
    name_plural = "Блюда"
