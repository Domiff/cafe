from src.core.schemas import BaseSchema
from src.mail.enums import MessageCode


class MessageSchema(BaseSchema):
    code: MessageCode
    subject: str
    title: str
    body: str
