# scenario-id: US-08/SC-6
# AC-4: localStorage setting overrides prefers-color-scheme on load
from asb_ui import page_session, screenshot
import json

with page_session() as (page, base_url):
    page.set_viewport_size({"width": 1280, "height": 800})

    # Emulate a dark system preference
    page.emulate_media(color_scheme="dark")
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # Set light theme in localStorage (overrides system dark preference)
    page.evaluate("localStorage.setItem('opsboard-theme', 'light')")
    page.reload()
    page.wait_for_load_state("networkidle")

    theme_toggle_visible = page.is_visible('[data-testid="theme-toggle"]')

    # data-theme should be "light" even though system prefers dark
    data_theme = page.evaluate("document.documentElement.getAttribute('data-theme')")

    screenshot(page, "US-08/SC-6")
    print(json.dumps({
        "url": page.url,
        "title": page.title(),
        "text": page.inner_text("body"),
        "data_theme": data_theme,
        "visible": {
            "theme-toggle": theme_toggle_visible,
        },
    }))
