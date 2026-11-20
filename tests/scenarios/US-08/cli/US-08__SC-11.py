# scenario-id: US-08/SC-11
# AC-9: Interactive elements have visible focus ring CSS rules
# PO then={exit_code equals 0}
import json
import sys

CSS_FILE = "static/css/main.css"

try:
    with open(CSS_FILE) as f:
        css = f.read()
except FileNotFoundError:
    print(json.dumps({"found": False, "error": "CSS file not found"}))
    sys.exit(2)

found = "focus-visible" in css
print(json.dumps({"found": found, "rule": "focus-visible"}))
sys.exit(0 if found else 1)
