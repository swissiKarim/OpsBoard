# scenario-id: US-08/SC-7
# AC-5: CSS uses only variables for color definitions (no hardcoded hex values)
# then={exit_code equals 1} → exit_code=1 in JSON means no violations (clean CSS)
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
        # Allow comment-only lines
        if stripped.startswith("/*") or stripped.startswith("*"):
            continue
        # Check for hex colour literals used as property values
        if re.search(r"#[0-9a-fA-F]{3,6}\b", stripped):
            violations.append(f"line {lineno}: {stripped}")

# exit_code=1 → no violations (passes then={exit_code equals 1})
# exit_code=0 → violations found (fails)
exit_code = 1 if not violations else 0

print(json.dumps({
    "exit_code": exit_code,
    "violations_found": len(violations),
    "violations": violations[:10],
}))

sys.exit(exit_code)
