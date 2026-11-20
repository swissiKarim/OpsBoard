#!/usr/bin/env bash
# scenario-id: US-01/SC-4
# SC-4: Required directory structure exists

cd "$(dirname "$0")/../../../.." || exit 1

MISSING=()
for dir in app tests "static/css" "static/js" "static/icons" templates; do
    [ -d "$dir" ] || MISSING+=("$dir")
done

if [ ${#MISSING[@]} -eq 0 ]; then
    python3 -c "import json; print(json.dumps({'exit_code': 0, 'missing': []}))"
else
    python3 -c "import json; print(json.dumps({'exit_code': 1, 'missing': $(python3 -c "import json,sys; print(json.dumps(sys.argv[1:]))" "${MISSING[@]}")}))"
    exit 1
fi
