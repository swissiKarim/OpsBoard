# scenario-id: US-08/SC-13
# AC-11: CSS contains 4px and 8px spacing values in the spacing scale
# exit_code=0 means both found → passes.
import subprocess
import sys
import json

checks = {
    "4px": "4px",
    "8px": "8px",
}
results = {}

for label, pattern in checks.items():
    r = subprocess.run(
        ["grep", "-r", "--include=*.css", pattern, "static/css/"],
        capture_output=True,
        text=True,
    )
    results[label] = r.returncode == 0

all_found = all(results.values())

print(json.dumps({
    "all_spacing_values_found": all_found,
    "details": results,
}))

sys.exit(0 if all_found else 1)
