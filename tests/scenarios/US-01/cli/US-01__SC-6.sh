#!/usr/bin/env bash
# scenario-id: US-01/SC-6
# SC-6: .gitignore excludes __pycache__, *.pyc, *.db, .env

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
cd "$REPO_ROOT"

EXIT=0
MISSING=()

for pattern in "__pycache__" "*.pyc" "*.db" ".env"; do
    grep -qF "$pattern" .gitignore || MISSING+=("$pattern")
done

if [ ${#MISSING[@]} -gt 0 ]; then
    EXIT=1
fi

python3 -c "
import json, sys
missing = sys.argv[1:]
print(json.dumps({'exit_code': $EXIT, 'missing_patterns': missing}))
" "${MISSING[@]}"
exit $EXIT
