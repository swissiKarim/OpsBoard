# scenario-id: US-08/SC-7
# AC-5: CSS uses only variables for color definitions (no hardcoded hex values)
# Greps for hex colour literals used as property VALUES (not inside --var: definitions).
# exit_code=1 means grep found nothing → no violations → test passes.
import subprocess
import sys
import json

# Pattern: a hex colour (#xxx or #xxxxxx) that appears as a CSS property value,
# i.e. NOT on a line that is purely a CSS variable definition (--something: #…)
# We look for lines that contain a hex colour but are NOT variable declarations.
result = subprocess.run(
    [
        "grep", "-rn",
        # Match hex colours (#RGB or #RRGGBB) that appear in property values
        # i.e. the line does NOT start with optional whitespace then "--"
        "--include=*.css",
        "-P",
        r"(?<!--)(?<!var\()#[0-9a-fA-F]{3,6}\b",
        "static/css/",
    ],
    capture_output=True,
    text=True,
)

# Filter out lines that are CSS variable DEFINITIONS (--color-xxx: #yyy)
# Those are allowed; only usages as direct values are forbidden.
violations = []
for line in result.stdout.splitlines():
    stripped = line.split(":", 2)[-1].strip() if ":" in line else line.strip()
    # Allow lines that are variable definitions: start with "--"
    if stripped.startswith("--"):
        continue
    violations.append(line)

print(json.dumps({
    "violations_found": len(violations),
    "violations": violations[:10],
}))

# exit 0 if violations found (grep "succeeded"), exit 1 if clean
sys.exit(0 if violations else 1)
