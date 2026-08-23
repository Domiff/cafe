from src.core.schemas import BaseSchema


class CafeSchema(BaseSchema):
    """Variables for header and footer in html templates"""

    title: str
    address: str
    phone: str | None
    working_hours: str | None
