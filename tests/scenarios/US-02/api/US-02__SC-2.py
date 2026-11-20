# scenario-id: US-02/SC-2
"""SC-2: Open SEV1 incident sets service derived_status to outage.
Then: status equals 201; body.service.derived_status equals "outage"
"""
import json
import os

import httpx

BASE = os.environ.get("ASB_SVC_WEB_URL", os.environ.get("ASB_API_BASE", "http://localhost:8000"))


def main():
    svc_resp = httpx.post(f"{BASE}/api/services", json={"name": "SC2-Service", "description": "", "team": "ops"})
    svc_id = svc_resp.json()["id"]

    resp = httpx.post(f"{BASE}/api/incidents", json={
        "title": "SEV1 Incident",
        "service_id": svc_id,
        "severity": "SEV1",
        "description": "outage test",
        "actor": "ops1",
        "comment": "sev1 open",
    })

    body = resp.json()
    print(json.dumps({"status": resp.status_code, "body": body}))


if __name__ == "__main__":
    main()
