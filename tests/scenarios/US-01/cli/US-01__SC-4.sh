#!/usr/bin/env bash
# scenario-id: US-01/SC-4
# SC-4: Required directory structure exists

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
cd "$REPO_ROOT"

MISSING=()
for dir in app tests "static/css" "static/js" "static/icons" templates; do
    [ -d "$dir" ] || MISSING+=("$dir")
done

if [ ${#MISSING[@]} -eq 0 ]; then
    python3 -c "import json; print(json.dumps({'exit_code': 0, 'missing': []}))"
else
    python3 -c "
import json, sys
missing = sys.argv[1:]
print(json.dumps({'exit_code': 1, 'missing': missing}))
" "${MISSING[@]}"
    exit 1
fi
