# scenario-id: US-08/SC-10
# AC-8: CSS contains prefers-reduced-motion media query
# then={exit_code equals 0} → JSON exit_code=0 means found
import subprocess
import sys
import json

result = subprocess.run(
    ["grep", "-r", "--include=*.css", "prefers-reduced-motion", "static/css/"],
    capture_output=True, text=True,
)

found = result.returncode == 0
json_exit_code = 0 if found else 1

print(json.dumps({
    "exit_code": json_exit_code,
    "found": found,
    "matches": result.stdout.strip().splitlines()[:5],
}))

sys.exit(0)
