# scenario-id: US-08/SC-12
# AC-10: Templates use semantic HTML elements throughout
# then={exit_code equals 0} means all required elements found → passes
import subprocess
import sys
import json

required_elements = ["<nav", "<main", "<section", "<header", "<button"]
results = {}

for element in required_elements:
    r = subprocess.run(
        ["grep", "-rl", "--include=*.html", element, "templates/"],
        capture_output=True,
        text=True,
    )
    results[element] = r.returncode == 0

all_found = all(results.values())
exit_code = 0 if all_found else 1

print(json.dumps({
    "exit_code": exit_code,
    "all_semantic_elements_found": all_found,
    "details": results,
}))

sys.exit(exit_code)
