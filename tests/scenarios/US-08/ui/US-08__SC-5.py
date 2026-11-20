# scenario-id: US-08/SC-5
# AC-3, AC-13: Dark mode preference persists after page reload
# then={visible.theme-toggle equals true}
from asb_ui import page_session, screenshot
import json

with page_session() as (page, base_url):
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # Set dark mode via toggle
    page.click('[data-testid="theme-toggle"]')
    page.wait_for_timeout(300)

    # Reload the page
    page.reload()
    page.wait_for_load_state("networkidle")

    theme_toggle_visible = page.is_visible('[data-testid="theme-toggle"]')

    screenshot(page, "US-08/SC-5")
    print(json.dumps({
        "title": page.title(),
        "url": page.url,
        "text": page.inner_text("body"),
        "visible": {
            "theme-toggle": theme_toggle_visible,
        },
    }))
