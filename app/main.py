# Importăm clasele și funcțiile de care avem nevoie
from fastapi import (
    FastAPI,
    Request  # FastAPI este framework-ul; Request e folosit pentru acces
)  # la datele din cerere HTTP
from fastapi.templating import (
    Jinja2Templates  # Clasa care știe să proceseze șabloane HTML (cu Jinja2)
)
from pathlib import (
    Path  # Pentru a construi căi de directoare compatibile cu orice OS
)

from app.api import endpoints

from app.api import auth

from app.api import ui


# Setăm directorul unde se află fișierele HTML (șabloanele)
BASE_DIR = Path(
    __file__
).resolve().parent  # `main.py` e în `app/`, deci `parent` e `app/`
templates = Jinja2Templates(
    directory=str(
        BASE_DIR / "templates"  # Construim path-ul către `app/templates/`
    )
)

# Inițializăm aplicația FastAPI
app = FastAPI(title="Math Microservice")


async def read_root(
    request: Request  # FastAPI cere să treci explicit
):
    return templates.TemplateResponse(
        "index.html", {
            "request": request  # Trimite pagina HTML cu contextul (request)
        }
    )

app.include_router(endpoints.router, prefix="/api")

app.include_router(auth.router, prefix="/api")

app.include_router(ui.router)
