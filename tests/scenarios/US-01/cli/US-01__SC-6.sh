#!/usr/bin/env bash
# scenario-id: US-01/SC-6
# SC-6: .gitignore excludes __pycache__, *.pyc, *.db, .env

cd "$(dirname "$0")/../../../.." || exit 1

EXIT=0
MISSING=()

for pattern in "__pycache__" "*.pyc" "*.db" ".env"; do
    grep -qF "$pattern" .gitignore || MISSING+=("$pattern")
done

if [ ${#MISSING[@]} -gt 0 ]; then
    EXIT=1
fi

python3 -c "import json; print(json.dumps({'exit_code': $EXIT, 'missing_patterns': $(python3 -c "import json,sys; print(json.dumps(sys.argv[1:]))" "${MISSING[@]}")}))"
exit $EXIT
