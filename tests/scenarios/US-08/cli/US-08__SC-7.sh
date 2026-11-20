#!/usr/bin/env bash
# scenario-id: US-08/SC-7
# AC-5: CSS uses only variables for color definitions (no hardcoded hex values)
# PO then={exit_code equals 1}
# grep exits 1 when NO match found → CSS is clean → script exits 1 (PO passes)

CSS_FILE="static/css/main.css"

if [ ! -f "$CSS_FILE" ]; then
  printf '{"error":"CSS file not found"}\n'
  exit 2
fi

# Find non-variable-definition lines that contain hex colour literals.
# Variable definition lines start with optional whitespace then "--".
# If any such lines exist, CSS has hardcoded hex in rules (violation).
VIOLATIONS=$(grep -E '#[0-9a-fA-F]{3,8}' "$CSS_FILE" | grep -Ev '^\s*--[a-zA-Z]' || true)

if [ -z "$VIOLATIONS" ]; then
  # No violations — CSS is clean
  printf '{"violations":0,"clean":true}\n'
  exit 1
else
  COUNT=$(echo "$VIOLATIONS" | wc -l | tr -d ' ')
  printf '{"violations":%s,"clean":false}\n' "$COUNT"
  exit 0
fi
