# scenario-id: US-02/SC-1
"""SC-1: Service, Incident and TimelineEntry models persist to DB.
Then: status equals 201; body.id exists true
"""
import json
import os

import httpx

BASE = os.environ.get("ASB_SVC_WEB_URL", os.environ.get("ASB_API_BASE", "http://localhost:8000"))


def main():
    # Create a service first
    svc_resp = httpx.post(f"{BASE}/api/services", json={"name": "SC1-Service", "description": "test", "team": "ops"})
    svc_id = svc_resp.json()["id"]

    # Create an incident (persists Incident + TimelineEntry transactionally)
    resp = httpx.post(f"{BASE}/api/incidents", json={
        "title": "SC1 Incident",
        "service_id": svc_id,
        "severity": "SEV2",
        "description": "persistence test",
        "actor": "ops1",
        "comment": "created",
    })

    body = resp.json()
    print(json.dumps({"status": resp.status_code, "body": body}))


if __name__ == "__main__":
    main()
