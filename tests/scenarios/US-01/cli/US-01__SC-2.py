# scenario-id: US-01/SC-2
"""SC-2: SQLite database initialised with WAL mode — uses only built-in sqlite3."""
import json
import os
import sqlite3
import tempfile

# Create a temp DB, enable WAL, verify
db_fd, db_path = tempfile.mkstemp(suffix=".db")
os.close(db_fd)

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

print(json.dumps({"journal_mode": mode, "stdout": mode}))
