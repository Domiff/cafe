from typing import Any

from fastapi import Request
from wtforms import SelectField

from src.admin.filters import (
    RuOperationColumnFilter,
    RuBooleanFilter,
)
from src.auth.enums import Role
from src.auth.models import User
from src.auth.utils import hash_password
from src.core.admin import BaseAdmin


class UserAdmin(BaseAdmin, model=User):
    column_list = [
        User.username,
        User.is_active,
        User.role,
    ]
    column_details_list = [
        User.username,
        User.password,
        User.is_active,
        User.role,
    ]
    column_labels = {
        User.username: "Имя пользователя",
        User.password: "Пароль",
        User.is_active: "Статус",
        User.role: "Роль",
    }
    column_searchable_list = [User.username]
    column_sortable_list = [User.username, User.is_active, User.role]
    column_filters = [
        RuOperationColumnFilter(User.role),
        RuBooleanFilter(User.is_active),
    ]

    form_overrides = {"role": SelectField}
    form_args = {
        "role": {
            "choices": [(e.name, e.value) for e in Role],
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

    name = "Пользователь"
    name_plural = "Пользователи"

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        password = data.pop("password")
        data["password"] = hash_password(password)
        