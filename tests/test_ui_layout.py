"""Tests for US-08: UI Layout, Theming and Responsive Design."""
from fastapi.testclient import TestClient
from app.main import app


def get_client():
    return TestClient(app)


def test_services_route_200():
    """GET /services returns 200 HTML."""
    with get_client() as client:
        response = client.get("/services")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_incidents_route_200():
    """GET /incidents returns 200 HTML."""
    with get_client() as client:
        response = client.get("/incidents")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_base_has_sidebar_toggle_testid():
    """Base template must include data-testid='sidebar-toggle'."""
    with get_client() as client:
        response = client.get("/")
    assert 'data-testid="sidebar-toggle"' in response.text


def test_base_has_theme_toggle_testid():
    """Base template must include data-testid='theme-toggle'."""
    with get_client() as client:
        response = client.get("/")
    assert 'data-testid="theme-toggle"' in response.text


def test_base_has_header_title_testid():
    """Base template must include data-testid='header-title'."""
    with get_client() as client:
        response = client.get("/")
    assert 'data-testid="header-title"' in response.text


def test_base_has_nav_sidebar_testid():
    """Base template must include data-testid='nav-sidebar'."""
    with get_client() as client:
        response = client.get("/")
    assert 'data-testid="nav-sidebar"' in response.text


def test_base_has_header_search_testid():
    """Base template must include data-testid='header-search'."""
    with get_client() as client:
        response = client.get("/")
    assert 'data-testid="header-search"' in response.text


def test_services_has_status_badge():
    """Services page must include service-status-badge with 'operational'."""
    with get_client() as client:
        response = client.get("/services")
    assert 'data-testid="service-status-badge"' in response.text
    assert "operational" in response.text


def test_incidents_has_mobile_card():
    """Incidents page must include incident-card-mobile element."""
    with get_client() as client:
        response = client.get("/incidents")
    assert 'data-testid="incident-card-mobile"' in response.text


def test_base_uses_semantic_html():
    """Base template must use semantic HTML elements."""
    with get_client() as client:
        response = client.get("/")
    body = response.text
    assert "<nav" in body
    assert "<main" in body
    assert "<header" in body
    assert "<section" in body or "<article" in body


def test_css_has_prefers_reduced_motion():
    """CSS must contain prefers-reduced-motion media query."""
    with open("static/css/main.css") as f:
        css = f.read()
    assert "prefers-reduced-motion" in css


def test_css_has_focus_visible():
    """CSS must contain :focus-visible rule."""
    with open("static/css/main.css") as f:
        css = f.read()
    assert "focus-visible" in css


def test_css_has_spacing_scale():
    """CSS must contain 4px and 8px spacing values."""
    with open("static/css/main.css") as f:
        css = f.read()
    assert "4px" in css
    assert "8px" in css


def test_css_no_hardcoded_hex_in_rules():
    """CSS must not use hardcoded hex values in rule bodies (only in variable definitions)."""
    import re
    with open("static/css/main.css") as f:
        css = f.read()
    # Find lines with hex that are NOT variable definitions
    violations = []
    for line in css.splitlines():
        stripped = line.strip()
        if re.search(r'#[0-9a-fA-F]{3,8}\b', stripped):
            if not stripped.startswith("--"):
                violations.append(line)
    assert violations == [], f"Hardcoded hex found in CSS rules:\n" + "\n".join(violations)


def test_base_has_inline_theme_script():
    """Base template must have inline theme script in <head> to prevent FOUC."""
    with get_client() as client:
        response = client.get("/")
    assert "localStorage.getItem" in response.text
    assert "data-theme" in response.text
