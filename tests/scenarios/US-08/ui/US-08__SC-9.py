# scenario-id: US-08/SC-9
# AC-7: Status badges are visible with descriptive text on services page
from asb_ui import page_session, screenshot
import json

with page_session() as (page, base_url):
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(base_url.rstrip("/") + "/services")
    page.wait_for_load_state("networkidle")

    service_status_badge_visible = page.is_visible('[data-testid="service-status-badge"]')
    page_text = page.inner_text("body")

    screenshot(page, "US-08/SC-9")
    print(json.dumps({
        "url": page.url,
        "title": page.title(),
        "text": page_text,
        "visible": {
            "service-status-badge": service_status_badge_visible,
        },
    }))
