#!/usr/bin/env bash
# Start the OpsBoard web service, installing deps first if needed.
set -e

cd "$(dirname "$0")/.."

# Install dependencies
python3 -m pip install -q -r requirements.txt --break-system-packages 2>/dev/null \
  || python3 -m pip install -q -r requirements.txt --user 2>/dev/null \
  || true

# Ensure user site-packages on PYTHONPATH
USER_SITE=$(python3 -m site --user-site 2>/dev/null || echo "")
if [ -n "$USER_SITE" ]; then
    export PYTHONPATH="${USER_SITE}:${PYTHONPATH:-}"
fi

# Start uvicorn via python3 -m to avoid PATH issues
exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
