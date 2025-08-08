
from fastapi import (
    FastAPI,
    Request  
)  
from fastapi.templating import (
    Jinja2Templates  
)
from pathlib import (
    Path  
)

from app.api import endpoints

from app.api import auth

from app.api import ui

from app.core import config  # noqa: F401 - asigură importul înainte de AuthJWT


BASE_DIR = Path(
    __file__
).resolve().parent  # Obținem directorul curent al fișierului `main.py`
templates = Jinja2Templates(
    directory=str(
        BASE_DIR / "templates"  # Construim path-ul către `app/templates/`
    )
)

# Inițializăm aplicația FastAPI
app = FastAPI(title="Math Microservice")


async def read_root(
    request: Request  
):
    return templates.TemplateResponse(
        "index.html", {
            "request": request  # Trimite pagina HTML cu contextul
        }
    )

app.include_router(endpoints.router, prefix="/api")

app.include_router(auth.router, prefix="/api")

app.include_router(ui.router)
