"""Tests for StatusCalculator rules BR-01 to BR-08 and IncidentService."""
from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import (
    Incident,
    IncidentSeverity,
    IncidentStatus,
    Service,
    ServiceStatus,
    TimelineEntry,
)
from app.services import (
    VALID_TRANSITIONS,
    IncidentService,
    InvalidTransitionError,
    StatusCalculator,
)


# ---------------------------------------------------------------------------
# In-memory DB fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def engine():
    eng = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=eng)
    yield eng
    Base.metadata.drop_all(bind=eng)


@pytest.fixture()
def db(engine):
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = Session()
    yield session
    session.rollback()
    # Clean up all data between tests
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.close()


@pytest.fixture()
def service(db) -> Service:
    svc = Service(name="TestService", description="", team="ops",
                  derived_status=ServiceStatus.operational.value)
    db.add(svc)
    db.commit()
    db.refresh(svc)
    return svc


# ---------------------------------------------------------------------------
# StatusCalculator.compute — pure unit tests (no DB)
# ---------------------------------------------------------------------------


def _make_incident(severity: str, status: str = IncidentStatus.open.value) -> Incident:
    inc = Incident()
    inc.severity = severity
    inc.status = status
    return inc


class TestStatusCalculatorCompute:
    """BR-01..BR-05: pure computation tests."""

    def test_br01_no_incidents_operational(self):
        """BR-01/BR-05: empty list → operational."""
        assert StatusCalculator.compute([]) == ServiceStatus.operational.value

    def test_br02_sev1_open_gives_outage(self):
        """BR-02: open SEV1 → outage."""
        incidents = [_make_incident(IncidentSeverity.SEV1.value)]
        assert StatusCalculator.compute(incidents) == ServiceStatus.outage.value

    def test_br02_sev1_dominates_sev2(self):
        """BR-02: SEV1 dominates SEV2."""
        incidents = [
            _make_incident(IncidentSeverity.SEV1.value),
            _make_incident(IncidentSeverity.SEV2.value),
        ]
        assert StatusCalculator.compute(incidents) == ServiceStatus.outage.value

    def test_br03_sev2_no_sev1_gives_degraded(self):
        """BR-03: open SEV2 (no SEV1) → degraded."""
        incidents = [_make_incident(IncidentSeverity.SEV2.value)]
        assert StatusCalculator.compute(incidents) == ServiceStatus.degraded.value

    def test_br04_sev3_no_sev1_gives_degraded(self):
        """BR-04: open SEV3 (no SEV1) → degraded."""
        incidents = [_make_incident(IncidentSeverity.SEV3.value)]
        assert StatusCalculator.compute(incidents) == ServiceStatus.degraded.value

    def test_br04_sev2_and_sev3_gives_degraded(self):
        """BR-03/BR-04: SEV2 + SEV3, no SEV1 → degraded."""
        incidents = [
            _make_incident(IncidentSeverity.SEV2.value),
            _make_incident(IncidentSeverity.SEV3.value),
        ]
        assert StatusCalculator.compute(incidents) == ServiceStatus.degraded.value

    def test_br05_operational_when_no_open(self):
        """BR-05: explicitly empty list → operational."""
        assert StatusCalculator.compute([]) == ServiceStatus.operational.value


# ---------------------------------------------------------------------------
# StatusCalculator.recalculate — DB integration
# ---------------------------------------------------------------------------


class TestStatusCalculatorRecalculate:
    """BR-02, BR-05, BR-06: DB-backed recalculation."""

    def test_br02_recalculate_sev1_sets_outage(self, db, service):
        """BR-02: adding a SEV1 incident and recalculating sets outage."""
        inc = Incident(
            title="P1",
            service_id=service.id,
            severity=IncidentSeverity.SEV1.value,
            status=IncidentStatus.open.value,
            description="",
        )
        db.add(inc)
        db.commit()

        StatusCalculator.recalculate(service, db)
        db.commit()
        db.refresh(service)

        assert service.derived_status == ServiceStatus.outage.value

    def test_br05_recalculate_no_open_gives_operational(self, db, service):
        """BR-05: no open incidents → operational after recalculate."""
        inc = Incident(
            title="P1",
            service_id=service.id,
            severity=IncidentSeverity.SEV1.value,
            status=IncidentStatus.resolved.value,
            description="",
        )
        db.add(inc)
        db.commit()

        StatusCalculator.recalculate(service, db)
        db.commit()
        db.refresh(service)

        assert service.derived_status == ServiceStatus.operational.value

    def test_br06_resolve_sev1_recalculates_to_operational(self, db, service):
        """BR-06: resolving SEV1 triggers recalculation → operational."""
        inc = Incident(
            title="P1",
            service_id=service.id,
            severity=IncidentSeverity.SEV1.value,
            status=IncidentStatus.open.value,
            description="",
        )
        db.add(inc)
        db.commit()

        StatusCalculator.recalculate(service, db)
        db.commit()
        db.refresh(service)
        assert service.derived_status == ServiceStatus.outage.value

        # Resolve the incident
        inc.status = IncidentStatus.resolved.value
        db.add(inc)
        StatusCalculator.recalculate(service, db)
        db.commit()
        db.refresh(service)

        assert service.derived_status == ServiceStatus.operational.value


# ---------------------------------------------------------------------------
# IncidentService — transition rules BR-07 and BR-08
# ---------------------------------------------------------------------------


class TestIncidentService:
    """BR-07, BR-08: transition validation and TimelineEntry creation."""

    def test_br07_invalid_transition_resolved_to_open(self, db, service):
        """BR-07: resolved → open must be rejected."""
        svc = IncidentService(db)
        incident = svc.create_incident(
            service_id=service.id,
            title="Test",
            severity=IncidentSeverity.SEV2.value,
            actor="ops1",
            comment="initial",
        )
        # Transition to resolved
        svc.change_status(
            incident_id=incident.id,
            new_status=IncidentStatus.resolved.value,
            actor="ops1",
            comment="done",
        )
        # Now try resolved → open
        with pytest.raises(InvalidTransitionError):
            svc.change_status(
                incident_id=incident.id,
                new_status=IncidentStatus.open.value,
                actor="ops1",
                comment="reopen",
            )

    def test_br07_invalid_transition_investigating_to_open(self, db, service):
        """BR-07: investigating → open must be rejected."""
        svc = IncidentService(db)
        incident = svc.create_incident(
            service_id=service.id,
            title="Test2",
            severity=IncidentSeverity.SEV3.value,
            actor="ops2",
            comment="start",
        )
        svc.change_status(
            incident_id=incident.id,
            new_status=IncidentStatus.investigating.value,
            actor="ops2",
            comment="looking",
        )
        with pytest.raises(InvalidTransitionError):
            svc.change_status(
                incident_id=incident.id,
                new_status=IncidentStatus.open.value,
                actor="ops2",
                comment="back",
            )

    def test_br07_valid_transitions_allowed(self):
        """BR-07: validate the allowed-transition table."""
        assert IncidentStatus.investigating.value in VALID_TRANSITIONS[IncidentStatus.open.value]
        assert IncidentStatus.resolved.value in VALID_TRANSITIONS[IncidentStatus.open.value]
        assert IncidentStatus.resolved.value in VALID_TRANSITIONS[IncidentStatus.investigating.value]
        assert VALID_TRANSITIONS[IncidentStatus.resolved.value] == []

    def test_br08_create_produces_timeline_entry(self, db, service):
        """BR-08: creating an incident produces exactly one TimelineEntry."""
        svc = IncidentService(db)
        incident = svc.create_incident(
            service_id=service.id,
            title="TL-Test",
            severity=IncidentSeverity.SEV2.value,
            actor="ops3",
            comment="opened",
        )
        entries = (
            db.query(TimelineEntry)
            .filter(TimelineEntry.incident_id == incident.id)
            .all()
        )
        assert len(entries) == 1
        assert entries[0].actor == "ops3"
        assert entries[0].comment == "opened"
        assert entries[0].new_status == IncidentStatus.open.value

    def test_br08_status_change_produces_exactly_one_entry(self, db, service):
        """BR-08: each status transition creates exactly one new TimelineEntry."""
        svc = IncidentService(db)
        incident = svc.create_incident(
            service_id=service.id,
            title="TL-Test2",
            severity=IncidentSeverity.SEV1.value,
            actor="ops4",
            comment="created",
        )
        svc.change_status(
            incident_id=incident.id,
            new_status=IncidentStatus.investigating.value,
            actor="ops4",
            comment="investigating now",
        )
        entries = (
            db.query(TimelineEntry)
            .filter(TimelineEntry.incident_id == incident.id)
            .all()
        )
        assert len(entries) == 2
        assert entries[1].new_status == IncidentStatus.investigating.value
        assert entries[1].actor == "ops4"
        assert entries[1].comment == "investigating now"

    def test_br08_timeline_entries_are_immutable_by_convention(self, db, service):
        """BR-08: TimelineEntry has no update endpoint; verify fields are set at creation."""
        svc = IncidentService(db)
        incident = svc.create_incident(
            service_id=service.id,
            title="Immutable",
            severity=IncidentSeverity.SEV3.value,
            actor="ops5",
            comment="initial entry",
        )
        entry = (
            db.query(TimelineEntry)
            .filter(TimelineEntry.incident_id == incident.id)
            .first()
        )
        assert entry is not None
        assert entry.created_at is not None
        # created_at must not be None — immutability is enforced by never updating
        original_created_at = entry.created_at
        db.refresh(entry)
        assert entry.created_at == original_created_at
