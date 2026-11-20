"""REST API endpoints for Services."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Service, ServiceStatus

router = APIRouter(prefix="/api/services", tags=["services"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class ServiceCreate(BaseModel):
    name: str
    description: str = ""
    team: str = ""


class ServiceOut(BaseModel):
    id: int
    name: str
    description: str
    team: str
    derived_status: str

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("", response_model=list[ServiceOut])
def list_services(db: Session = Depends(get_db)):
    return db.query(Service).all()


@router.post("", response_model=ServiceOut, status_code=201)
def create_service(payload: ServiceCreate, db: Session = Depends(get_db)):
    svc = Service(
        name=payload.name,
        description=payload.description,
        team=payload.team,
        derived_status=ServiceStatus.operational.value,
    )
    db.add(svc)
    db.commit()
    db.refresh(svc)
    return svc


@router.get("/{service_id}", response_model=ServiceOut)
def get_service(service_id: int, db: Session = Depends(get_db)):
    svc = db.get(Service, service_id)
    if svc is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return svc


@router.put("/{service_id}", response_model=ServiceOut)
def update_service(
    service_id: int, payload: ServiceCreate, db: Session = Depends(get_db)
):
    svc = db.get(Service, service_id)
    if svc is None:
        raise HTTPException(status_code=404, detail="Service not found")
    svc.name = payload.name
    svc.description = payload.description
    svc.team = payload.team
    db.commit()
    db.refresh(svc)
    return svc


@router.delete("/{service_id}", status_code=204)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    svc = db.get(Service, service_id)
    if svc is None:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(svc)
    db.commit()
