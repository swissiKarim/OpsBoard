# scenario-id: US-08/SC-12
# AC-10: Templates use semantic HTML elements throughout
# PO then={exit_code equals 0}
import json
import os
import sys

TEMPLATES_DIR = "templates"

if not os.path.isdir(TEMPLATES_DIR):
    print(json.dumps({"found": False, "error": "Templates directory not found"}))
    sys.exit(2)

# Read all template files
content = ""
for root, dirs, files in os.walk(TEMPLATES_DIR):
    for fname in files:
        if fname.endswith(".html"):
            with open(os.path.join(root, fname)) as f:
                content += f.read()

required = ["<nav", "<main", "<header", "<section", "<button"]
found_elements = [el for el in required if el in content]
missing = [el for el in required if el not in content]

result = {
    "found": len(missing) == 0,
    "elements": [e.lstrip("<") for e in found_elements],
    "missing": [e.lstrip("<") for e in missing],
}
print(json.dumps(result))
sys.exit(0 if len(missing) == 0 else 1)
