# scenario-id: US-08/SC-12
# AC-10: Templates use semantic HTML elements throughout
# then={exit_code equals 0} → JSON exit_code=0 means all found
import subprocess
import sys
import json

required_elements = ["<nav", "<main", "<section", "<header", "<button"]
results = {}

for element in required_elements:
    r = subprocess.run(
        ["grep", "-rl", "--include=*.html", element, "templates/"],
        capture_output=True, text=True,
    )
    results[element] = r.returncode == 0

all_found = all(results.values())
json_exit_code = 0 if all_found else 1

print(json.dumps({
    "exit_code": json_exit_code,
    "all_semantic_elements_found": all_found,
    "details": results,
}))

sys.exit(0)
