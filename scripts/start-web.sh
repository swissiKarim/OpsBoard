#!/usr/bin/env bash
# Start the OpsBoard web service, installing deps first if needed.
set -e

cd "$(dirname "$0")/.."

# Install dependencies if not already present
python3 -m pip install -q -r requirements.txt --break-system-packages 2>/dev/null || true

# Start uvicorn via python3 -m to avoid PATH issues
exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
