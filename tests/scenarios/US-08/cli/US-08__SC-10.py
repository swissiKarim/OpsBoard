# scenario-id: US-08/SC-10
# AC-8: CSS contains prefers-reduced-motion media query for animations
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

found = "prefers-reduced-motion" in css
exit_code = 0 if found else 1
print(json.dumps({"exit_code": exit_code, "found": found, "query": "prefers-reduced-motion"}))
sys.exit(exit_code)
