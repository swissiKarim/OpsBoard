# scenario-id: US-08/SC-1
# AC-1: Sidebar is visible at viewport width 1280px
from asb_ui import page_session, screenshot
import json

with page_session() as (page, base_url):
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    nav_sidebar_visible = page.is_visible('[data-testid="nav-sidebar"]')

    screenshot(page, "US-08/SC-1")
    print(json.dumps({
        "url": page.url,
        "title": page.title(),
        "text": page.inner_text("body"),
        "visible": {
            "nav-sidebar": nav_sidebar_visible,
        },
    }))
