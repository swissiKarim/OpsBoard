# scenario-id: US-08/SC-13
# AC-11: CSS contains 4px and 8px spacing values in the spacing scale
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

has_4px = "4px" in css
has_8px = "8px" in css
found = has_4px and has_8px

print(json.dumps({"found": found, "has_4px": has_4px, "has_8px": has_8px}))
sys.exit(0 if found else 1)
