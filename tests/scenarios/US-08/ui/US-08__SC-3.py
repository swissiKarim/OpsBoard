# scenario-id: US-08/SC-3
# AC-2: Header shows page title and global search field
from asb_ui import page_session, screenshot
import json

with page_session() as (page, base_url):
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    header_title_visible = page.is_visible('[data-testid="header-title"]')
    header_search_visible = page.is_visible('[data-testid="header-search"]')

    screenshot(page, "US-08/SC-3")
    print(json.dumps({
        "url": page.url,
        "title": page.title(),
        "text": page.inner_text("body"),
        "visible": {
            "header-title": header_title_visible,
            "header-search": header_search_visible,
        },
    }))
