"""Shared pytest fixtures."""
import pytest


def _get_app_and_deps():
    """Lazy import after root conftest ensures deps are installed."""
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.database import Base, get_db
    from app.main import app
    return TestClient, create_engine, sessionmaker, Base, get_db, app


TEST_DB_URL = "sqlite:///./test.db"


@pytest.fixture(scope="session")
def test_engine():
    from sqlalchemy import create_engine
    from app.database import Base
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(test_engine):
    from sqlalchemy.orm import sessionmaker
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session):
    from fastapi.testclient import TestClient
    from app.database import get_db
    from app.main import app

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
