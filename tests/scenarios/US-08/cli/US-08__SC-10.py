# scenario-id: US-08/SC-10
# AC-8: CSS contains prefers-reduced-motion media query for animations
# then={exit_code equals 0} means found → passes
import subprocess
import sys
import json

result = subprocess.run(
    ["grep", "-r", "--include=*.css", "prefers-reduced-motion", "static/css/"],
    capture_output=True,
    text=True,
)

found = result.returncode == 0
exit_code = 0 if found else 1

print(json.dumps({
    "exit_code": exit_code,
    "found": found,
    "matches": result.stdout.strip().splitlines()[:5],
}))

sys.exit(exit_code)
