# scenario-id: US-08/SC-14
# AC-12: All interactive UI elements have data-testid attributes on dashboard
# then={visible.theme-toggle equals true; visible.sidebar-toggle equals true}
from asb_ui import page_session, screenshot
import json

with page_session() as (page, base_url):
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    theme_toggle_visible = page.is_visible('[data-testid="theme-toggle"]')
    sidebar_toggle_visible = page.is_visible('[data-testid="sidebar-toggle"]')

    screenshot(page, "US-08/SC-14")
    print(json.dumps({
        "title": page.title(),
        "url": page.url,
        "text": page.inner_text("body"),
        "visible": {
            "theme-toggle": theme_toggle_visible,
            "sidebar-toggle": sidebar_toggle_visible,
        },
    }))
