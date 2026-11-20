# scenario-id: US-08/SC-7
# AC-5: CSS uses only variables for color definitions (no hardcoded hex values)
# PO then={exit_code equals 1}
# Convention: exit 1 = no violations found (CSS is clean)
import json
import re
import sys

CSS_FILE = "static/css/main.css"

try:
    with open(CSS_FILE) as f:
        css = f.read()
except FileNotFoundError:
    print(json.dumps({"error": "CSS file not found", "violations": -1}))
    sys.exit(2)

violations = []
for line in css.splitlines():
    stripped = line.strip()
    # Skip CSS variable definition lines (--varname: value)
    if stripped.startswith("--"):
        continue
    # Check for hex colour literals
    if re.search(r'#[0-9a-fA-F]{3,8}\b', stripped):
        violations.append(stripped)

print(json.dumps({"violations": len(violations), "clean": len(violations) == 0}))

if len(violations) == 0:
    # CSS is clean — exit 1 as PO expects
    sys.exit(1)
else:
    # Violations found — exit 0 (unexpected)
    sys.exit(0)
