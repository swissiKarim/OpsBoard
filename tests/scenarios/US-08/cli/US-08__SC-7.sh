#!/usr/bin/env bash
# scenario-id: US-08/SC-7
# AC-5: CSS uses only variables for color definitions (no hardcoded hex values)
# PO then={exit_code equals 1}
# Convention: grep exits 1 when NO match is found.
# This script greps for hardcoded hex colour literals in CSS rule bodies
# (excluding lines that are CSS variable definitions: "  --foo: #...").
# When CSS is clean (no hardcoded hex in rules), grep exits 1 → PO passes.

CSS_FILE="static/css/main.css"

if [ ! -f "$CSS_FILE" ]; then
  echo "CSS file not found: $CSS_FILE" >&2
  exit 2
fi

# Strip lines that are variable definitions (start with optional whitespace then --)
# Then grep for hex colour literals (#xxx or #xxxxxx) in the remaining lines.
# grep exits 0 if found (violation), 1 if not found (clean).
grep -E '#[0-9a-fA-F]{3,8}' "$CSS_FILE" \
  | grep -Ev '^\s*--[a-zA-Z]' \
  | grep -qE '#[0-9a-fA-F]{3,8}'

# If grep -q above exits 0 → violations found → we exit 0 (unexpected, PO would fail)
# If grep -q above exits 1 → no violations → we exit 1 (PO expects 1 → pass)
# Invert: exit with opposite of grep result
STATUS=$?
if [ $STATUS -eq 0 ]; then
  echo "ERROR: Hardcoded hex values found in CSS rule bodies" >&2
  grep -E '#[0-9a-fA-F]{3,8}' "$CSS_FILE" | grep -Ev '^\s*--[a-zA-Z]' >&2
  exit 0
else
  exit 1
fi
