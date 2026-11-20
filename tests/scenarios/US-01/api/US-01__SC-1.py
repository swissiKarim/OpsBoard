# scenario-id: US-01/SC-1
"""SC-1: GET / returns HTTP 200."""
import json
import os
import urllib.request

base_url = os.environ.get("ASB_SVC_WEB_URL", os.environ.get("ASB_API_BASE", "http://localhost:8000"))
base_url = base_url.rstrip("/")

req = urllib.request.Request(f"{base_url}/")
try:
    with urllib.request.urlopen(req) as resp:
        status = resp.status
        headers = dict(resp.headers)
        body = resp.read().decode("utf-8", errors="replace")
except urllib.error.HTTPError as e:
    status = e.code
    headers = dict(e.headers)
    body = e.read().decode("utf-8", errors="replace")

print(json.dumps({
    "status": status,
    "headers": {k.lower(): v for k, v in headers.items()},
    "body": body,
}))
