from src.admin.base import BaseAdmin
from src.mail.models import Message
from src.staff.enums import Role


class MessageAdmin(BaseAdmin, model=Message):
    allowed_roles = write_roles = {Role.ADMIN.name}

    can_delete = False
    can_export = False

    column_list = [
        Message.code,
        Message.subject,
        Message.title,
        Message.is_active,
        Message.updated_at,
    ]
    column_details_list = [
        Message.code,
        Message.subject,
        Message.title,
        Message.body,
        Message.is_active,
        Message.updated_at,
    ]
    column_labels = {
        Message.code: "Письмо",
        Message.subject: "Тема",
        Message.title: "Заголовок",
        Message.body: "Текст",
        Message.is_active: "Включено",
        Message.updated_at: "Изменено",
    }
    column_default_sort = [(Message.code, False)]
    column_searchable_list = [Message.subject, Message.body]

    form_create_rules = form_edit_rules = ["code", "subject", "title", "body", "is_active"]
    form_widget_args = {
        "body": {"rows": 8},
        "subject": {"placeholder": "Видно в списке входящих"},
        "title": {"placeholder": "Крупный заголовок внутри письма"},
    }

    icon = "fa-solid fa-envelope"
    category = "Сайт"
    category_icon = "fa-solid fa-globe"

    name = "Письмо"
    name_plural = "Письма"
