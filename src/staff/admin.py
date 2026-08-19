from typing import Any

from fastapi import Request
from wtforms import SelectField

from src.admin.filters import RuBooleanFilter
from src.staff.enums import Role
from src.staff.models import Staff
from src.core.security import hash_password
from src.admin.base import BaseAdmin


class StaffAdmin(BaseAdmin, model=Staff):
    allowed_roles = {Role.ADMIN.name}
    write_roles = {Role.ADMIN.name}

    column_list = [
        Staff.username,
        Staff.is_active,
        Staff.role,
    ]
    column_details_list = [
        Staff.username,
        Staff.password,
        Staff.is_active,
        Staff.role,
    ]
    column_labels = {
        Staff.username: "Имя пользователя",
        Staff.password: "Пароль",
        Staff.is_active: "Статус",
        Staff.role: "Роль",
    }
    column_searchable_list = [Staff.username]
    column_sortable_list = [
        Staff.username,
        Staff.is_active,
        Staff.role,
    ]
    column_filters = [
        RuBooleanFilter(Staff.is_active, title="Статус"),
    ]

    form_overrides = {"role": SelectField}
    form_args = {
        "role": {
            "choices": [(e.name, e.value) for e in Role],
            "coerce": lambda v: v.name if isinstance(v, Role) else str(v),
        }
    }
    form_create_rules = [
        "username",
        "password",
        "role",
    ]
    form_edit_rules = form_create_rules + ["is_active"]

    icon = "fa-solid fa-user-shield"
    category = "Доступ"
    category_icon = "fa-solid fa-lock"

    name = "Учётная запись"
    name_plural = "Учётные записи"

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        password = data.pop("password")
        data["password"] = hash_password(password)
