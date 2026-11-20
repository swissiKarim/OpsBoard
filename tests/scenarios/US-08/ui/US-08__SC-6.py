# scenario-id: US-08/SC-6
# AC-4: localStorage setting overrides prefers-color-scheme on load
# then={visible.theme-toggle equals true}
from asb_ui import page_session, screenshot
import json

with page_session() as (page, base_url):
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # Manually set localStorage to "dark" to simulate a saved preference
    page.evaluate("localStorage.setItem('opsboard-theme', 'dark')")

    # Reload — the inline script in <head> should apply data-theme="dark" before paint
    page.reload()
    page.wait_for_load_state("networkidle")

    theme_toggle_visible = page.is_visible('[data-testid="theme-toggle"]')

    screenshot(page, "US-08/SC-6")
    print(json.dumps({
        "title": page.title(),
        "url": page.url,
        "text": page.inner_text("body"),
        "visible": {
            "theme-toggle": theme_toggle_visible,
        },
    }))
