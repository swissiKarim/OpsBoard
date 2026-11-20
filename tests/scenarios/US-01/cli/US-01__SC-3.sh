#!/usr/bin/env bash
# scenario-id: US-01/SC-3
# SC-3: pytest runs with zero failures

cd "$(dirname "$0")/../../../.." || exit 1

pytest -q --tb=short 2>&1
EXIT=$?

python3 -c "import json; print(json.dumps({'exit_code': $EXIT}))"
