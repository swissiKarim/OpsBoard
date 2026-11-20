# scenario-id: US-02/SC-6
"""SC-6: Resolving SEV1 incident recalculates derived_status to operational.
Then: status equals 200; body.service.derived_status equals "operational"
"""
import json
import os

import httpx

BASE = os.environ.get("ASB_SVC_WEB_URL", os.environ.get("ASB_API_BASE", "http://localhost:8000"))


def main():
    # Create service
    svc_resp = httpx.post(f"{BASE}/api/services", json={"name": "SC6-Service", "description": "", "team": "ops"})
    svc_id = svc_resp.json()["id"]

    # Open SEV1 incident → service becomes outage
    inc_resp = httpx.post(f"{BASE}/api/incidents", json={
        "title": "SEV1 to resolve",
        "service_id": svc_id,
        "severity": "SEV1",
        "description": "",
        "actor": "ops1",
        "comment": "opening",
    })
    inc_id = inc_resp.json()["id"]

    # Resolve the incident
    resp = httpx.post(f"{BASE}/api/incidents/{inc_id}/transition", json={
        "new_status": "resolved",
        "actor": "ops1",
        "comment": "fixed",
    })

    body = resp.json()
    print(json.dumps({"status": resp.status_code, "body": body}))


if __name__ == "__main__":
    main()
