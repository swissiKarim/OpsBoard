#!/usr/bin/env bash
# scenario-id: US-01/SC-2
# SC-2: SQLite database initialised with WAL mode

cd "$(dirname "$0")/../../../.." || exit 1

# Ensure deps installed
python3 -m pip install -q -r requirements.txt --break-system-packages >/dev/null 2>&1 || true

MODE=$(python3 - <<'EOF'
import sys, os
sys.path.insert(0, os.getcwd())
from app.database import engine, init_db
from sqlalchemy import text
init_db()
with engine.connect() as conn:
    result = conn.execute(text("PRAGMA journal_mode")).fetchone()
    print(result[0])
EOF
)

python3 -c "import json; print(json.dumps({'journal_mode': '$MODE', 'stdout': '$MODE'}))"
