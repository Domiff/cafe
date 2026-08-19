from fastapi import FastAPI, Request
from sqladmin import Admin, I18nConfig
from sqladmin._menu import CategoryMenu

from src.admin.auth import AdminAuth
from src.staff.admin import StaffAdmin
from src.landing.admin import LandingAdmin
from src.cafe.admin import EmployeeAdmin, PositionAdmin, CategoryAdmin, ProductAdmin
from src.core.config import settings
from src.core.database import session_maker
from src.users.admin import UserAdmin


def _category_is_visible(self: CategoryMenu, request: Request) -> bool:
    return any(
        child.is_visible(request) and child.is_accessible(request)
        for child in self.children
    )


def setup_admin(app: FastAPI) -> None:
    CategoryMenu.is_visible = _category_is_visible

    admin = Admin(
        app,
        session_maker=session_maker,
        base_url="/admin",
        title="Cafe admin",
        templates_dir="templates",
        authentication_backend=AdminAuth(secret_key=settings.admin.ADMIN_SECRET_KEY),
        i18n_config=I18nConfig(
            default_locale="ru",
            language_switcher=["en", "az", "de", "ru", "tr"],
        ),
    )
    admin.add_view(EmployeeAdmin)
    admin.add_view(PositionAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(StaffAdmin)
    admin.add_view(LandingAdmin)
    admin.add_view(UserAdmin)
