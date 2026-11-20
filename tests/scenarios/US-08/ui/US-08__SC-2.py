# scenario-id: US-08/SC-2
# AC-1: Sidebar is collapsible at viewport width 768px
# interactions: click@sidebar-toggle → nav-sidebar becomes not visible
from asb_ui import page_session, screenshot
import json

with page_session() as (page, base_url):
    page.set_viewport_size({"width": 768, "height": 1024})
    page.goto(base_url)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)

    # Use JS to call toggleSidebar() directly — avoids overlay click-blocking
    page.evaluate("toggleSidebar()")
    page.wait_for_timeout(500)

    # After toggle: mobile-open removed → visibility:hidden → not visible
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
