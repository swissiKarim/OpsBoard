# scenario-id: US-02/SC-7
"""SC-7: Status change creates exactly one immutable TimelineEntry.
Then: status equals 200; body.timeline.length equals 2;
      body.timeline[1].actor equals "ops1"; body.timeline[1].comment equals "starting"
"""
import json
import os

import httpx

BASE = os.environ.get("ASB_SVC_WEB_URL", os.environ.get("ASB_API_BASE", "http://localhost:8000"))


def main():
    # Create service
    svc_resp = httpx.post(f"{BASE}/api/services", json={"name": "SC7-Service", "description": "", "team": "ops"})
    svc_id = svc_resp.json()["id"]

    # Create incident (produces 1st TimelineEntry)
    inc_resp = httpx.post(f"{BASE}/api/incidents", json={
        "title": "Timeline Test",
        "service_id": svc_id,
        "severity": "SEV2",
        "description": "",
        "actor": "ops1",
        "comment": "opened",
    })
    inc_id = inc_resp.json()["id"]

    # Transition to investigating (produces 2nd TimelineEntry)
    resp = httpx.post(f"{BASE}/api/incidents/{inc_id}/transition", json={
        "new_status": "investigating",
        "actor": "ops1",
        "comment": "starting",
    })

    body = resp.json()
    print(json.dumps({"status": resp.status_code, "body": body}))


if __name__ == "__main__":
    main()
