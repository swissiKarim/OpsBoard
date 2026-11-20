# scenario-id: US-02/SC-8
"""SC-8: Invalid status transition resolved->open is rejected with 422.
Then: status equals 422
"""
import json
import os

import httpx

BASE = os.environ.get("ASB_SVC_WEB_URL", os.environ.get("ASB_API_BASE", "http://localhost:8000"))


def main():
    # Create service
    svc_resp = httpx.post(f"{BASE}/api/services", json={"name": "SC8-Service", "description": "", "team": "ops"})
    svc_id = svc_resp.json()["id"]

    # Create incident
    inc_resp = httpx.post(f"{BASE}/api/incidents", json={
        "title": "Transition Test",
        "service_id": svc_id,
        "severity": "SEV2",
        "description": "",
        "actor": "ops1",
        "comment": "open",
    })
    inc_id = inc_resp.json()["id"]

    # Resolve the incident first
    httpx.post(f"{BASE}/api/incidents/{inc_id}/transition", json={
        "new_status": "resolved",
        "actor": "ops1",
        "comment": "done",
    })

    # Try invalid transition: resolved → open
    resp = httpx.post(f"{BASE}/api/incidents/{inc_id}/transition", json={
        "new_status": "open",
        "actor": "ops1",
        "comment": "reopen attempt",
    })

    body = resp.json()
    print(json.dumps({"status": resp.status_code, "body": body}))


if __name__ == "__main__":
    main()
