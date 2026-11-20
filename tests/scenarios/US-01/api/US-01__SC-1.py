# scenario-id: US-01/SC-1
"""SC-1: GET / returns HTTP 200."""
import json
import os
import urllib.request
import urllib.error

base_url = os.environ.get("ASB_SVC_WEB_URL") or os.environ.get("ASB_API_BASE", "http://localhost:8000")
base_url = base_url.rstrip("/")

try:
    req = urllib.request.Request(f"{base_url}/")
    with urllib.request.urlopen(req, timeout=10) as resp:
        status = resp.status
        headers = {k.lower(): v for k, v in resp.headers.items()}
        body = resp.read().decode("utf-8", errors="replace")
except urllib.error.HTTPError as e:
    status = e.code
    headers = {k.lower(): v for k, v in e.headers.items()}
    body = e.read().decode("utf-8", errors="replace")
except Exception as e:
    print(json.dumps({"status": 0, "headers": {}, "body": str(e)}))
    raise SystemExit(1)

print(json.dumps({
    "status": status,
    "headers": headers,
    "body": body,
}))
