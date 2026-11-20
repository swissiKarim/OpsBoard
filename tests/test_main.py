"""Placeholder tests for the project scaffold."""


def test_health():
    """GET /health returns 200."""
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_index():
    """GET / returns 200 HTML."""
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_index_contains_testids():
    """Base template must include key data-testid attributes."""
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        response = client.get("/")
    body = response.text
    assert 'data-testid="nav-sidebar"' in body
    assert 'data-testid="header-search"' in body
