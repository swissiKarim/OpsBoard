# scenario-id: US-01/SC-2
"""SC-2: SQLite database initialised with WAL mode."""
import json
import sys
import os

# Ensure app package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from sqlalchemy import text
from app.database import engine, init_db

init_db()

with engine.connect() as conn:
    result = conn.execute(text("PRAGMA journal_mode")).fetchone()
    mode = result[0]

print(json.dumps({"journal_mode": mode, "stdout": mode}))
