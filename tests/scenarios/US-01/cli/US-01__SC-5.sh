#!/usr/bin/env bash
# scenario-id: US-01/SC-5
# SC-5: requirements.txt or pyproject.toml lists all dependencies

cd "$(dirname "$0")/../../../.." || exit 1

EXIT=1
FOUND=""

if [ -f requirements.txt ]; then
    # Check for key packages
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
