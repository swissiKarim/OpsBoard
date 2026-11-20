#!/usr/bin/env bash
# scenario-id: US-01/SC-3
# SC-3: pytest runs with zero failures

cd "$(dirname "$0")/../../../.." || exit 1

# Ensure deps installed (try both methods)
python3 -m pip install -q -r requirements.txt --break-system-packages >/dev/null 2>&1 \
  || python3 -m pip install -q -r requirements.txt --user >/dev/null 2>&1 \
  || true

# Add user site-packages to PYTHONPATH in case --break-system-packages was needed
USER_SITE=$(python3 -m site --user-site 2>/dev/null || echo "")
export PYTHONPATH="${USER_SITE}:${PYTHONPATH}"

python3 -m pytest -q --tb=short >&2
EXIT=$?

python3 -c "import json; print(json.dumps({'exit_code': $EXIT}))"
