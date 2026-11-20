"""Business-logic layer: StatusCalculator and IncidentService."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import (
    Incident,
    IncidentSeverity,
    IncidentStatus,
    Service,
    ServiceStatus,
    TimelineEntry,
)

# ---------------------------------------------------------------------------
# Valid status transitions (BR-07)
# ---------------------------------------------------------------------------
VALID_TRANSITIONS: dict[str, list[str]] = {
    IncidentStatus.open.value: [IncidentStatus.investigating.value, IncidentStatus.resolved.value],
    IncidentStatus.investigating.value: [IncidentStatus.resolved.value],
    IncidentStatus.resolved.value: [],  # resolved is terminal
}


class InvalidTransitionError(ValueError):
    """Raised when a requested status transition is not allowed (BR-07)."""

    def __init__(self, from_status: str, to_status: str) -> None:
        self.from_status = from_status
        self.to_status = to_status
        super().__init__(
            f"Transition from '{from_status}' to '{to_status}' is not allowed."
        )


class StatusCalculator:
    """
    Derives the Service.derived_status from its open Incidents.

    Business rules:
      BR-01  derived_status is always computed – never set manually.
      BR-02  Any open SEV1 incident → outage.
      BR-03  Open SEV2 incident (no open SEV1) → degraded.
      BR-04  Open SEV3 incident (no open SEV1) → degraded.
      BR-05  No open incidents → operational.
      BR-06  Resolving a SEV1 incident triggers recalculation.
      BR-07  Invalid transitions are rejected (handled in IncidentService).
      BR-08  Every status change produces exactly one immutable TimelineEntry.
    """

    @staticmethod
    def recalculate(service: Service, db: Session) -> str:
        """
        Recalculate derived_status for *service* based on its open incidents
        and persist the new value.  Returns the new status string.
        """
        # Flush pending changes so the query sees the latest state (BR-06).
        db.flush()

        open_incidents = (
            db.query(Incident)
            .filter(
                Incident.service_id == service.id,
                Incident.status != IncidentStatus.resolved.value,
            )
            .all()
        )

        new_status = StatusCalculator.compute(open_incidents)
        service.derived_status = new_status
        db.add(service)
        return new_status

    @staticmethod
    def compute(open_incidents: list[Incident]) -> str:
        """
        Pure computation – derive the status string from a list of open incidents.
        No DB access; testable in isolation.
        """
        if not open_incidents:
            # BR-05
            return ServiceStatus.operational.value

        severities = {inc.severity for inc in open_incidents}

        if IncidentSeverity.SEV1.value in severities:
            # BR-02
            return ServiceStatus.outage.value

        if IncidentSeverity.SEV2.value in severities or IncidentSeverity.SEV3.value in severities:
            # BR-03 / BR-04
            return ServiceStatus.degraded.value

        return ServiceStatus.operational.value


class IncidentService:
    """
    Application-service layer for Incident operations.
    Wraps DB mutations and enforces BR-06, BR-07, BR-08.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    def create_incident(
        self,
        *,
        service_id: int,
        title: str,
        severity: str,
        description: str = "",
        actor: str,
        comment: str = "",
    ) -> Incident:
        """Create a new Incident with status=open and an initial TimelineEntry."""
        from app.models import Service  # avoid circular at module level

        service = self.db.get(Service, service_id)
        if service is None:
            raise ValueError(f"Service {service_id} not found.")

        incident = Incident(
            title=title,
            service_id=service_id,
            severity=severity,
            description=description,
            status=IncidentStatus.open.value,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
            updated_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        self.db.add(incident)
        self.db.flush()  # get incident.id

        # BR-08: create initial TimelineEntry for the 'open' status
        entry = TimelineEntry(
            incident_id=incident.id,
            actor=actor,
            new_status=IncidentStatus.open.value,
            comment=comment,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        self.db.add(entry)

        # BR-01 / BR-02 / BR-05: recalculate service status
        StatusCalculator.recalculate(service, self.db)

        self.db.commit()
        self.db.refresh(incident)
        self.db.refresh(service)
        return incident

    # ------------------------------------------------------------------
    # Transition
    # ------------------------------------------------------------------

    def change_status(
        self,
        *,
        incident_id: int,
        new_status: str,
        actor: str,
        comment: str = "",
    ) -> Incident:
        """
        Transition an Incident to *new_status*.

        Raises:
            ValueError: if incident not found.
            InvalidTransitionError: if the transition is forbidden (BR-07).
        """
        incident = self.db.get(Incident, incident_id)
        if incident is None:
            raise ValueError(f"Incident {incident_id} not found.")

        allowed = VALID_TRANSITIONS.get(incident.status, [])
        if new_status not in allowed:
            raise InvalidTransitionError(incident.status, new_status)

        incident.status = new_status
        incident.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        self.db.add(incident)

        # BR-08: exactly one TimelineEntry per status change
        entry = TimelineEntry(
            incident_id=incident.id,
            actor=actor,
            new_status=new_status,
            comment=comment,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        self.db.add(entry)

        # BR-06: recalculate service derived_status after transition
        service = self.db.get(Service, incident.service_id)
        if service is not None:
            StatusCalculator.recalculate(service, self.db)

        self.db.commit()
        self.db.refresh(incident)
        return incident
