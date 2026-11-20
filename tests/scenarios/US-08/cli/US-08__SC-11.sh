#!/usr/bin/env bash
# scenario-id: US-08/SC-11
# AC-9: Interactive elements have visible focus ring CSS rules
# PO then={exit_code equals 0} → grep finds focus-visible rules → exit 0

CSS_FILE="static/css/main.css"

if [ ! -f "$CSS_FILE" ]; then
  echo "CSS file not found: $CSS_FILE" >&2
  exit 2
fi

grep -q "focus-visible" "$CSS_FILE"
STATUS=$?
if [ $STATUS -eq 0 ]; then
  echo "OK: focus-visible rule found in CSS"
  exit 0
else
  echo "ERROR: No focus-visible rule found in CSS" >&2
  exit 1
fi
