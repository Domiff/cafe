from fastapi.templating import Jinja2Templates

from src.landing.context import cafe_context


templates = Jinja2Templates(directory="templates", context_processors=[cafe_context])
