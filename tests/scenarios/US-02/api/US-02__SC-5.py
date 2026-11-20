# scenario-id: US-02/SC-5
"""SC-5: No open incidents sets service to operational.
Then: status equals 200; body.derived_status equals "operational"
"""
import json
import os

import httpx

BASE = os.environ.get("ASB_SVC_WEB_URL", os.environ.get("ASB_API_BASE", "http://localhost:8000"))


def main():
    # Create a service with no incidents → derived_status must be operational
    svc_resp = httpx.post(f"{BASE}/api/services", json={"name": "SC5-Service", "description": "", "team": "ops"})
    svc_id = svc_resp.json()["id"]

    # Fetch the service – no incidents attached
    resp = httpx.get(f"{BASE}/api/services/{svc_id}")
    body = resp.json()
    print(json.dumps({"status": resp.status_code, "body": body}))


if __name__ == "__main__":
    main()
