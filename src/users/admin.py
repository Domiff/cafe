from src.admin.base import BaseAdmin
from src.staff.enums import Role
from src.users.models import User


class UserAdmin(BaseAdmin, model=User):
    allowed_roles = write_roles = {Role.ADMIN.name}

    can_create = False
    can_delete = False

    column_list = column_details_list = [User.email, User.is_active, User.is_verified]
    column_labels = {
        User.email: "Email",
        User.is_active: "Статус",
        User.is_verified: "Почта подтверждена",
    }
    column_searchable_list = [User.email]

    form_edit_rules = ["is_active", "is_verified"]

    icon = "fa-solid fa-circle-user"
    category = "Клиенты"
    category_icon = "fa-solid fa-address-book"

    name = "Пользователь"
    name_plural = "Пользователи"
