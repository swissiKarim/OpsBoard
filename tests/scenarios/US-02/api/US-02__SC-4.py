# scenario-id: US-02/SC-4
"""SC-4: Open SEV3 incident (no SEV1) sets service to degraded.
Then: status equals 201; body.service.derived_status equals "degraded"
"""
import json
import os

import httpx

BASE = os.environ.get("ASB_SVC_WEB_URL", os.environ.get("ASB_API_BASE", "http://localhost:8000"))


def main():
    svc_resp = httpx.post(f"{BASE}/api/services", json={"name": "SC4-Service", "description": "", "team": "ops"})
    svc_id = svc_resp.json()["id"]

    resp = httpx.post(f"{BASE}/api/incidents", json={
        "title": "SEV3 Incident",
        "service_id": svc_id,
        "severity": "SEV3",
        "description": "degraded via sev3",
        "actor": "ops1",
        "comment": "sev3 open",
    })

    body = resp.json()
    print(json.dumps({"status": resp.status_code, "body": body}))


if __name__ == "__main__":
    main()
