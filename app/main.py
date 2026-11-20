"""OpsBoard – FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="OpsBoard", version="0.1.0", lifespan=lifespan)

# Static files & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/services", response_class=HTMLResponse)
def services(request: Request):
    # Empty list until full CRUD is implemented in a later story
    return templates.TemplateResponse(request, "services.html", {"services": []})


@app.get("/incidents", response_class=HTMLResponse)
def incidents(request: Request):
    # Empty list until full CRUD is implemented in a later story
    return templates.TemplateResponse(request, "incidents.html", {"incidents": []})
