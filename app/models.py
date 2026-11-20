"""SQLAlchemy ORM models for OpsBoard."""
from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class ServiceStatus(str, enum.Enum):
    operational = "operational"
    degraded = "degraded"
    outage = "outage"


class IncidentSeverity(str, enum.Enum):
    SEV1 = "SEV1"
    SEV2 = "SEV2"
    SEV3 = "SEV3"


class IncidentStatus(str, enum.Enum):
    open = "open"
    investigating = "investigating"
    resolved = "resolved"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class Service(Base):
    """A service monitored by OpsBoard."""

    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    team: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    derived_status: Mapped[str] = mapped_column(
        Enum(ServiceStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=ServiceStatus.operational.value,
        server_default=ServiceStatus.operational.value,
    )

    incidents: Mapped[list[Incident]] = relationship(
        "Incident", back_populates="service", lazy="select"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "team": self.team,
            "derived_status": self.derived_status,
        }


class Incident(Base):
    """An operational incident linked to a Service."""

    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    service_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("services.id"), nullable=False
    )
    severity: Mapped[str] = mapped_column(
        Enum(IncidentSeverity, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[str] = mapped_column(
        Enum(IncidentStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=IncidentStatus.open.value,
        server_default=IncidentStatus.open.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    service: Mapped[Service] = relationship("Service", back_populates="incidents")
    timeline: Mapped[list[TimelineEntry]] = relationship(
        "TimelineEntry",
        back_populates="incident",
        order_by="TimelineEntry.created_at",
        lazy="select",
    )

    def to_dict(self, include_service: bool = False, include_timeline: bool = False) -> dict:
        d = {
            "id": self.id,
            "title": self.title,
            "service_id": self.service_id,
            "severity": self.severity,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_service and self.service:
            d["service"] = self.service.to_dict()
        if include_timeline:
            d["timeline"] = [e.to_dict() for e in self.timeline]
        return d


class TimelineEntry(Base):
    """An immutable record of an Incident status change."""

    __tablename__ = "timeline_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("incidents.id"), nullable=False
    )
    actor: Mapped[str] = mapped_column(String(255), nullable=False)
    new_status: Mapped[str] = mapped_column(
        Enum(IncidentStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    comment: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    incident: Mapped[Incident] = relationship("Incident", back_populates="timeline")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "incident_id": self.incident_id,
            "actor": self.actor,
            "new_status": self.new_status,
            "comment": self.comment,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
