
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
from app.models.request_log import RequestLog
from app.db.deps import get_db
from sqlalchemy.orm import Session

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/history", response_class=HTMLResponse)
async def get_history_page(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})


@router.get("/api/export")
def export_history(user_id: int, db: Session = Depends(get_db)):
    logs = db.query(RequestLog)\
             .filter(RequestLog.user_id == user_id)\
             .order_by(RequestLog.timestamp.desc())\
             .all()

    export_data = [
        {
            "operation": log.operation,
            "parameters": log.parameters,
            "result": log.result,
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M"),
            "is_cached": log.is_cached
        }
        for log in logs
    ]

    export_path = Path("exported_logs.json")
    export_path.write_text(json.dumps(export_data, indent=2), encoding="utf-8")

    return FileResponse(
        path=export_path,
        filename="istoric_calcule.json",
        media_type="application/json"
    )


@router.get("/metrics", response_class=HTMLResponse)
async def get_metrics_page(request: Request):
    return templates.TemplateResponse("metrics.html", {"request": request})
