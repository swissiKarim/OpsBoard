# scenario-id: US-08/SC-8
# AC-6: Incidents table converts to cards at viewport 480px
from asb_ui import page_session, screenshot
import json

with page_session() as (page, base_url):
    page.set_viewport_size({"width": 480, "height": 800})
    page.goto(base_url.rstrip("/") + "/incidents")
    page.wait_for_load_state("networkidle")

    incident_card_mobile_visible = page.is_visible('[data-testid="incident-card-mobile"]')

    screenshot(page, "US-08/SC-8")
    print(json.dumps({
        "url": page.url,
        "title": page.title(),
        "text": page.inner_text("body"),
        "visible": {
            "incident-card-mobile": incident_card_mobile_visible,
        },
    }))
