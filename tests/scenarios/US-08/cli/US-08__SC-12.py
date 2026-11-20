# scenario-id: US-08/SC-12
# AC-10: Templates use semantic HTML elements throughout
# PO then={exit_code equals 0}
# Platform evaluates then against JSON stdout field "exit_code"
import json
import os
import sys

TEMPLATES_DIR = "templates"

if not os.path.isdir(TEMPLATES_DIR):
    print(json.dumps({"exit_code": 2, "found": False, "error": "Templates directory not found"}))
    sys.exit(2)

content = ""
for root, dirs, files in os.walk(TEMPLATES_DIR):
    for fname in files:
        if fname.endswith(".html"):
            with open(os.path.join(root, fname)) as f:
                content += f.read()

required = ["<nav", "<main", "<header", "<section", "<button"]
found_elements = [el.lstrip("<") for el in required if el in content]
missing = [el.lstrip("<") for el in required if el not in content]

exit_code = 0 if len(missing) == 0 else 1
print(json.dumps({
    "exit_code": exit_code,
    "found": len(missing) == 0,
    "elements": found_elements,
    "missing": missing,
}))
sys.exit(exit_code)
