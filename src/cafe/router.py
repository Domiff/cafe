from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi_cache.decorator import cache

from src.core.database import SessionDep
from src.cafe.repository import get_cafe_repository
from src.core.templates import templates

router = APIRouter(prefix="", tags=["Cafe"])


@router.get("/menu")
@cache(namespace="menu")
async def get_menu(request: Request, session: SessionDep) -> HTMLResponse:
    menu = await get_cafe_repository(session).get_menu()
    return templates.TemplateResponse(request, "cafe/list.html", {"menu": menu})


@router.get("/menu/{product_id}")
@cache(namespace="menu")
async def get_product(request: Request, session: SessionDep, product_id: int) -> HTMLResponse:
    product = await get_cafe_repository(session).get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    return templates.TemplateResponse(request, "cafe/detail.html", {"product": product})
