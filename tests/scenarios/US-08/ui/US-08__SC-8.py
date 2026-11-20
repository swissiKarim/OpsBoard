# scenario-id: US-08/SC-8
# AC-6: Incidents table converts to cards at viewport 480px
from asb_ui import page_session, screenshot
import json

with page_session() as (page, base_url):
    # Use 479px to safely trigger max-width:480px media query
    page.set_viewport_size({"width": 479, "height": 800})
    page.goto(base_url.rstrip("/") + "/incidents")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(300)

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
