# scenario-id: US-08/SC-10
# AC-8: CSS contains prefers-reduced-motion media query for animations
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

found = "prefers-reduced-motion" in css
print(json.dumps({"found": found, "query": "prefers-reduced-motion"}))
sys.exit(0 if found else 1)
