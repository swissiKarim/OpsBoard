# scenario-id: US-08/SC-7
# AC-5: CSS uses only variables for color definitions (no hardcoded hex values)
# then={exit_code equals 1} → JSON field exit_code=1 means no violations (clean CSS)
# Process always exits 0 so the driver itself is not marked as crashed.
import re
import sys
import json

violations = []

with open("static/css/main.css") as f:
    for lineno, line in enumerate(f, 1):
        stripped = line.strip()
        # Allow CSS variable definitions: lines starting with "--"
        if stripped.startswith("--"):
            continue
        # Allow comment lines
        if stripped.startswith("/*") or stripped.startswith("*"):
            continue
        # Check for hex colour literals used as property values
        if re.search(r"#[0-9a-fA-F]{3,6}\b", stripped):
            violations.append(f"line {lineno}: {stripped}")

# exit_code=1 in JSON → no violations (then={exit_code equals 1} passes)
# exit_code=0 in JSON → violations found (then fails)
json_exit_code = 1 if not violations else 0

print(json.dumps({
    "exit_code": json_exit_code,
    "violations_found": len(violations),
    "violations": violations[:10],
}))

# Always exit process with 0 so platform doesn't treat driver as crashed
sys.exit(0)
