# scenario-id: US-08/SC-10
# AC-8: CSS contains prefers-reduced-motion media query for animations
# exit_code=0 means grep found it → passes.
import subprocess
import sys
import json

result = subprocess.run(
    ["grep", "-r", "--include=*.css", "prefers-reduced-motion", "static/css/"],
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
