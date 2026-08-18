from fastapi import Request, Response

from src.core.cache import invalidate_cache
from src.admin.base import BaseAdmin
from src.auth.enums import Role
from src.landing.models import Landing


class LandingAdmin(BaseAdmin, model=Landing):
    allowed_roles = {Role.ADMIN.name, Role.MANAGER.name}
    write_roles = {Role.ADMIN.name}

    can_delete = False
    can_export = False

    column_list = [
        Landing.title,
        Landing.address,
        Landing.phone,
        Landing.working_hours,
    ]
    column_details_list = [
        Landing.title,
        Landing.subtitle,
        Landing.hero_image,
        Landing.about_title,
        Landing.about_text,
        Landing.address,
        Landing.phone,
        Landing.email,
        Landing.working_hours,
        Landing.map_url,
        Landing.vk_url,
        Landing.reviews_url,
        Landing.has_wifi,
        Landing.has_sockets,
        Landing.has_terrace,
        Landing.is_pet_friendly,
        Landing.has_takeaway,
    ]
    column_labels = {
        Landing.title: "Название",
        Landing.subtitle: "Подзаголовок",
        Landing.hero_image: "Фото на первом экране",
        Landing.about_title: "Заголовок блока «О нас»",
        Landing.about_text: "Текст «О нас»",
        Landing.address: "Адрес",
        Landing.phone: "Телефон",
        Landing.email: "Email",
        Landing.working_hours: "Часы работы",
        Landing.map_url: "Ссылка на карту",
        Landing.vk_url: "ВКонтакте",
        Landing.reviews_url: "Отзывы",
        Landing.has_wifi: "Wi-Fi",
        Landing.has_sockets: "Розетки",
        Landing.has_terrace: "Веранда",
        Landing.is_pet_friendly: "Можно с питомцем",
        Landing.has_takeaway: "Навынос",
    }

    form_create_rules = form_edit_rules = [
        "title",
        "subtitle",
        "hero_image",
        "about_title",
        "about_text",
        "address",
        "phone",
        "email",
        "working_hours",
        "map_url",
        "vk_url",
        "reviews_url",
        "has_wifi",
        "has_sockets",
        "has_terrace",
        "is_pet_friendly",
        "has_takeaway",
    ]
    form_widget_args = {
        "about_text": {"rows": 14},
        "subtitle": {"rows": 2},
        "working_hours": {"placeholder": "Пн–Пт 8:00–22:00, Сб–Вс 9:00–23:00"},
        "phone": {"placeholder": "+7 900 123-45-67"},
    }

    icon = "fa-solid fa-house"
    category = "Сайт"
    category_icon = "fa-solid fa-globe"

    name = "Лендинг"
    name_plural = "Лендинг"

    async def after_model_change(
        self, data: dict, model: Landing, is_created: bool, request: Request
    ) -> Response | None:
        await invalidate_cache("landing")
