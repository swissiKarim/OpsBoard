#!/usr/bin/env bash
# scenario-id: US-01/SC-3
# SC-3: pytest runs with zero failures

# Navigate to repo root (absolute path from script location)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
cd "$REPO_ROOT"

# Ensure deps installed
python3 -m pip install -q -r requirements.txt --break-system-packages >/dev/null 2>&1 \
  || python3 -m pip install -q -r requirements.txt --user >/dev/null 2>&1 \
  || true

# Add user site-packages to PYTHONPATH
USER_SITE=$(python3 -m site --user-site 2>/dev/null || echo "")
if [ -n "$USER_SITE" ]; then
  export PYTHONPATH="${USER_SITE}:${PYTHONPATH:-}"
fi

python3 -m pytest -q --tb=short >&2
EXIT=$?

python3 -c "import json; print(json.dumps({'exit_code': $EXIT}))"
