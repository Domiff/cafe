from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.core.templates import templates

router = APIRouter(tags=["Pages"])


@router.get("/login")
async def login_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "users/pages/login.html")


@router.get("/register")
async def register_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "users/pages/register.html")


@router.get("/logout")
async def logout_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "users/pages/logout.html")


@router.get("/verify")
async def verify_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "users/pages/verify.html")


@router.get("/forgot-password")
async def forgot_password_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "users/pages/forgot-password.html")


@router.get("/reset-password")
async def reset_password_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "users/pages/reset-password.html")


@router.get("/account")
async def account_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "users/pages/me.html")
