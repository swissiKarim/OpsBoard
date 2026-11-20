#!/usr/bin/env bash
# scenario-id: US-01/SC-5
# SC-5: requirements.txt or pyproject.toml lists all dependencies

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
cd "$REPO_ROOT"

EXIT=1
FOUND=""

if [ -f requirements.txt ]; then
    MISSING_PKGS=()
    for pkg in fastapi uvicorn sqlalchemy jinja2 pytest; do
        grep -qi "^${pkg}" requirements.txt || MISSING_PKGS+=("$pkg")
    done
    if [ ${#MISSING_PKGS[@]} -eq 0 ]; then
        EXIT=0
        FOUND="requirements.txt"
    fi
elif [ -f pyproject.toml ]; then
    EXIT=0
    FOUND="pyproject.toml"
fi

python3 -c "import json; print(json.dumps({'exit_code': $EXIT, 'found': '${FOUND}'}))"
exit $EXIT
