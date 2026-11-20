# scenario-id: US-08/SC-2
# AC-1: Sidebar is collapsible at viewport width 768px
# interactions={click@sidebar-toggle} then={visible.nav-sidebar equals false}
from asb_ui import page_session, screenshot
import json

with page_session() as (page, base_url):
    page.set_viewport_size({"width": 768, "height": 1024})
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # At 768px the sidebar is hidden by default (visibility:hidden + translateX(-100%)).
    # Open it first via the header menu button, then click sidebar-toggle to close it.
    page.click('[data-testid="header-menu-btn"]')
    page.wait_for_timeout(300)

    # Now click sidebar-toggle (inside sidebar footer) to close the sidebar
    page.click('[data-testid="sidebar-toggle"]')
    page.wait_for_timeout(400)

    # After closing, sidebar should not be visible (visibility:hidden)
    nav_sidebar_visible = page.is_visible('[data-testid="nav-sidebar"]')

    screenshot(page, "US-08/SC-2")
    print(json.dumps({
        "title": page.title(),
        "url": page.url,
        "text": page.inner_text("body"),
        "visible": {
            "nav-sidebar": nav_sidebar_visible,
        },
    }))
