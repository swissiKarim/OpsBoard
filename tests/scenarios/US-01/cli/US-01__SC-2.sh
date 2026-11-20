#!/usr/bin/env bash
# scenario-id: US-01/SC-2
# SC-2: SQLite database initialised with WAL mode

cd "$(dirname "$0")/../../../.." || exit 1

# Use only built-in sqlite3 module — no external deps needed
MODE=$(python3 - <<'EOF'
import sqlite3, os, json

db_path = "./opsboard_sc2_test.db"
try:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    cur = conn.execute("PRAGMA journal_mode")
    mode = cur.fetchone()[0]
    conn.close()
finally:
    try:
        os.remove(db_path)
    except OSError:
        pass

print(mode)
EOF
)

python3 -c "import json; print(json.dumps({'journal_mode': '$MODE', 'stdout': '$MODE'}))"
