# scenario-id: US-08/SC-7
# AC-5: CSS uses only variables for color definitions (no hardcoded hex values)
# PO then={exit_code equals 1}
# Platform evaluates then against JSON stdout field "exit_code"
# exit_code=1 means "grep found no violations" (clean CSS)
import json
import re
import sys

CSS_FILE = "static/css/main.css"

try:
    with open(CSS_FILE) as f:
        css = f.read()
except FileNotFoundError:
    print(json.dumps({"exit_code": 2, "error": "CSS file not found"}))
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

if len(violations) == 0:
    # CSS is clean — exit_code=1 as PO expects (grep convention: no match = exit 1)
    print(json.dumps({"exit_code": 1, "violations": 0, "clean": True}))
    sys.exit(1)
else:
    # Violations found
    print(json.dumps({"exit_code": 0, "violations": len(violations), "clean": False}))
    sys.exit(0)
