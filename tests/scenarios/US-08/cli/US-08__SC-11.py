# scenario-id: US-08/SC-11
# AC-9: Interactive elements have visible focus ring CSS rules
# then={exit_code equals 0} → JSON exit_code=0 means found
import subprocess
import sys
import json

result = subprocess.run(
    ["grep", "-r", "--include=*.css", ":focus-visible", "static/css/"],
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
