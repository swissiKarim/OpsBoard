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
    assert 'data-testid="header-title"' in body
    assert 'data-testid="theme-toggle"' in body
    assert 'data-testid="sidebar-toggle"' in body


def test_services_route():
    """GET /services returns 200 HTML with service-status-badge and 'operational'."""
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        response = client.get("/services")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    body = response.text
    assert 'data-testid="service-status-badge"' in body
    assert "operational" in body


def test_incidents_route():
    """GET /incidents returns 200 HTML with incident-card-mobile element."""
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        response = client.get("/incidents")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    body = response.text
    assert 'data-testid="incident-card-mobile"' in body
    assert 'data-testid="incident-cards-container"' in body


def test_css_no_hardcoded_hex_in_property_values():
    """CSS must not use hardcoded hex colours as property values (only in var defs)."""
    import re
    with open("static/css/main.css") as f:
        lines = f.readlines()
    violations = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Skip CSS variable definition lines (--something: #hex)
        if stripped.startswith("--"):
            continue
        # Check for hex colour usage in non-variable lines
        if re.search(r"#[0-9a-fA-F]{3,6}\b", stripped):
            violations.append(f"line {i}: {stripped}")
    assert violations == [], "Hardcoded hex colours found:\n" + "\n".join(violations)


def test_css_prefers_reduced_motion():
    """CSS must contain prefers-reduced-motion media query."""
    with open("static/css/main.css") as f:
        content = f.read()
    assert "prefers-reduced-motion" in content


def test_css_focus_visible():
    """CSS must contain :focus-visible rule for keyboard focus rings."""
    with open("static/css/main.css") as f:
        content = f.read()
    assert ":focus-visible" in content


def test_css_spacing_scale():
    """CSS must define 4px and 8px spacing values."""
    with open("static/css/main.css") as f:
        content = f.read()
    assert "4px" in content
    assert "8px" in content


def test_semantic_html_elements():
    """Templates must use semantic HTML elements: nav, main, section, header, button."""
    import glob
    template_files = glob.glob("templates/**/*.html", recursive=True)
    template_files += glob.glob("templates/*.html")
    all_content = ""
    for path in template_files:
        with open(path) as f:
            all_content += f.read()
    for element in ["<nav", "<main", "<section", "<header", "<button"]:
        assert element in all_content, f"Semantic element {element} not found in templates"
