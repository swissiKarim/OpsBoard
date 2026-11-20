# scenario-id: US-08/SC-2
# AC-1: Sidebar is collapsible at viewport width 768px
# interactions: click@sidebar-toggle → nav-sidebar becomes not visible
from asb_ui import page_session, screenshot
import json

with page_session() as (page, base_url):
    page.set_viewport_size({"width": 768, "height": 1024})
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # At 768px JS auto-opens sidebar (mobile-open class added on load).
    # sidebar-toggle is the header menu button, visible at all widths.
    page.wait_for_selector('[data-testid="sidebar-toggle"]', state="visible")
    page.click('[data-testid="sidebar-toggle"]')
    page.wait_for_timeout(400)

    # After click, mobile-open is removed → visibility:hidden → not visible
    nav_sidebar_visible = page.is_visible('[data-testid="nav-sidebar"]')

    screenshot(page, "US-08/SC-2")
    print(json.dumps({
        "url": page.url,
        "title": page.title(),
        "text": page.inner_text("body"),
        "visible": {
            "nav-sidebar": nav_sidebar_visible,
        },
    }))
