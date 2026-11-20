# scenario-id: US-08/SC-11
# AC-9: Interactive elements have visible focus ring CSS rules
# PO then={exit_code equals 0}
# Platform evaluates then against JSON stdout field "exit_code"
import json
import sys

CSS_FILE = "static/css/main.css"

try:
    with open(CSS_FILE) as f:
        css = f.read()
except FileNotFoundError:
    print(json.dumps({"exit_code": 2, "found": False, "error": "CSS file not found"}))
    sys.exit(2)

found = "focus-visible" in css
exit_code = 0 if found else 1
print(json.dumps({"exit_code": exit_code, "found": found, "rule": "focus-visible"}))
sys.exit(exit_code)
