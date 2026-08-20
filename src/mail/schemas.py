from fastapi_mail import MessageSchema, MessageType
from pydantic import EmailStr


def get_message_schema(
    subject: str,
    email: EmailStr,
    template_body: dict,
    msg_type: MessageType = MessageType.html,
) -> MessageSchema:
    return MessageSchema(
        subject=subject,
        recipients=[email],
        template_body=template_body,
        subtype=msg_type,
    )
