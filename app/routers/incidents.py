"""REST API endpoints for Incidents."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Incident, IncidentSeverity, IncidentStatus, Service
from app.services import IncidentService, InvalidTransitionError

router = APIRouter(prefix="/api/incidents", tags=["incidents"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class IncidentCreate(BaseModel):
    title: str
    service_id: int
    severity: str
    description: str = ""
    actor: str
    comment: str = ""

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, v: str) -> str:
        allowed = [e.value for e in IncidentSeverity]
        if v not in allowed:
            raise ValueError(f"severity must be one of {allowed}")
        return v


class StatusTransition(BaseModel):
    new_status: str
    actor: str
    comment: str = ""

    @field_validator("new_status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = [e.value for e in IncidentStatus]
        if v not in allowed:
            raise ValueError(f"new_status must be one of {allowed}")
        return v


class TimelineEntryOut(BaseModel):
    id: int
    incident_id: int
    actor: str
    new_status: str
    comment: str
    created_at: str | None = None

    model_config = {"from_attributes": True}


class ServiceOut(BaseModel):
    id: int
    name: str
    description: str
    team: str
    derived_status: str

    model_config = {"from_attributes": True}


class IncidentOut(BaseModel):
    id: int
    title: str
    service_id: int
    severity: str
    description: str
    status: str
    created_at: str | None = None
    updated_at: str | None = None
    service: ServiceOut | None = None
    timeline: list[TimelineEntryOut] | None = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _incident_to_dict(
    incident: Incident,
    include_service: bool = True,
    include_timeline: bool = False,
) -> dict:
    d = incident.to_dict(
        include_service=include_service,
        include_timeline=include_timeline,
    )
    return d


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("", response_model=list[IncidentOut])
def list_incidents(db: Session = Depends(get_db)):
    incidents = db.query(Incident).all()
    return [i.to_dict(include_service=True) for i in incidents]


@router.post("", status_code=201)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    # Validate service exists
    service = db.get(Service, payload.service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    svc = IncidentService(db)
    incident = svc.create_incident(
        service_id=payload.service_id,
        title=payload.title,
        severity=payload.severity,
        description=payload.description,
        actor=payload.actor,
        comment=payload.comment,
    )
    # Refresh service to get updated derived_status
    db.refresh(service)
    return incident.to_dict(include_service=True, include_timeline=True)


@router.get("/{incident_id}")
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.get(Incident, incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident.to_dict(include_service=True, include_timeline=True)


@router.post("/{incident_id}/transition", status_code=200)
def transition_incident(
    incident_id: int,
    payload: StatusTransition,
    db: Session = Depends(get_db),
):
    incident = db.get(Incident, incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    svc = IncidentService(db)
    try:
        incident = svc.change_status(
            incident_id=incident_id,
            new_status=payload.new_status,
            actor=payload.actor,
            comment=payload.comment,
        )
    except InvalidTransitionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return incident.to_dict(include_service=True, include_timeline=True)
