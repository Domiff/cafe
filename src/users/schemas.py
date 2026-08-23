from fastapi_users import schemas

from src.core.schemas import BaseSchema, UTCDatetime


class UserRead(BaseSchema, schemas.BaseUser[int]):
    created_at: UTCDatetime


class UserCreate(BaseSchema, schemas.BaseUserCreate):
    pass


class UserUpdate(BaseSchema, schemas.BaseUserUpdate):
    pass
