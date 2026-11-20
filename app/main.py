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
    # Demo services for UI scenarios until a full DB layer is wired
    demo_services = [
        {"name": "API Gateway", "team": "Platform", "status": "operational",
         "description": "Main API gateway for all external traffic"},
        {"name": "Auth Service", "team": "Security", "status": "operational",
         "description": "Authentication and authorisation service"},
        {"name": "Payment Service", "team": "Payments", "status": "degraded",
         "description": "Handles payment processing"},
    ]
    return templates.TemplateResponse(request, "services.html",
                                      {"services": demo_services})


@app.get("/incidents", response_class=HTMLResponse)
def incidents(request: Request):
    # Demo incidents for UI scenarios until a full DB layer is wired
    demo_incidents = [
        {"title": "API Gateway latency spike", "service": "API Gateway",
         "severity": "SEV2", "status": "investigating",
         "updated_at": "2024-01-15 10:30"},
        {"title": "Payment timeouts", "service": "Payment Service",
         "severity": "SEV1", "status": "open",
         "updated_at": "2024-01-15 09:00"},
    ]
    return templates.TemplateResponse(request, "incidents.html",
                                      {"incidents": demo_incidents})
