from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from src.core.database import SessionDep
from src.core.templates import templates
from src.landing.repository import get_landing_repository

router = APIRouter(prefix="", tags=["Landing"])


@router.get("/")
async def get_landing(request: Request, session: SessionDep) -> HTMLResponse:
    landing = await get_landing_repository(session).get_landing()
    if landing is None:
        raise HTTPException(status_code=404, detail="Лендинг не заполнен")
    return templates.TemplateResponse(request, "landing/index.html", {"landing": landing})
