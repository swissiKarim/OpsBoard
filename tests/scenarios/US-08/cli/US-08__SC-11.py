# scenario-id: US-08/SC-11
# AC-9: Interactive elements have visible focus ring CSS rules
# exit_code=0 means found → passes.
import subprocess
import sys
import json

result = subprocess.run(
    ["grep", "-r", "--include=*.css", ":focus-visible", "static/css/"],
    capture_output=True,
    text=True,
)

found = result.returncode == 0
matches = result.stdout.strip().splitlines()

print(json.dumps({
    "found": found,
    "matches": matches[:5],
}))

sys.exit(0 if found else 1)
