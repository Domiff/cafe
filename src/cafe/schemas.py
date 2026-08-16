from decimal import Decimal

from src.core.schemas import BaseSchema


class CategorySchema(BaseSchema):
    name: str
    description: str | None = None
    image_url: str | None = None


class ProductSchema(BaseSchema):
    name: str
    description: str | None = None
    price: Decimal
    image_url: str | None = None
    is_available: bool
    weight_grams: int | None = None
    volume_ml: int | None = None
    calories: int | None = None


class MenuSchema(CategorySchema):
    products: list[ProductSchema] = []
