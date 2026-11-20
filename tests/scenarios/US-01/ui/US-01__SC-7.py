# scenario-id: US-01/SC-7
"""SC-7: Base template interactive elements have data-testid attributes."""
from asb_ui import page_session, screenshot
import json

with page_session() as (page, base_url):
    page.goto(base_url + "/")
    page.wait_for_load_state("networkidle")

    visible = {
        "nav-sidebar": page.is_visible('[data-testid="nav-sidebar"]'),
        "header-search": page.is_visible('[data-testid="header-search"]'),
    }

    screenshot(page, "US-01/SC-7")

    print(json.dumps({
        "title": page.title(),
        "url": page.url,
        "text": page.inner_text("body"),
        "visible": visible,
    }))
