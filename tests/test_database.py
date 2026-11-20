"""Database initialisation tests."""
from sqlalchemy import text
from app.database import engine


def test_wal_mode():
    """SQLite must be configured with WAL journal mode."""
    with engine.connect() as conn:
        result = conn.execute(text("PRAGMA journal_mode")).fetchone()
    assert result[0].lower() == "wal"


def test_tables_created():
    """Base.metadata.create_all must succeed without error."""
    from app.database import Base, init_db
    init_db()  # idempotent
    assert Base.metadata is not None
