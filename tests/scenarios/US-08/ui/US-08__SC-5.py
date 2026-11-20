# scenario-id: US-08/SC-5
# AC-3, AC-13: Dark mode preference persists after page reload
from asb_ui import page_session, screenshot
import json

with page_session() as (page, base_url):
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # Set dark theme via localStorage directly, then reload
    page.evaluate("localStorage.setItem('opsboard-theme', 'dark')")
    page.reload()
    page.wait_for_load_state("networkidle")

    theme_toggle_visible = page.is_visible('[data-testid="theme-toggle"]')

    # Verify dark theme is applied after reload
    data_theme = page.evaluate("document.documentElement.getAttribute('data-theme')")

    screenshot(page, "US-08/SC-5")
    print(json.dumps({
        "url": page.url,
        "title": page.title(),
        "text": page.inner_text("body"),
        "data_theme": data_theme,
        "visible": {
            "theme-toggle": theme_toggle_visible,
        },
    }))
