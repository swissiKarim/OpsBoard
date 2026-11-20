#!/usr/bin/env bash
# scenario-id: US-08/SC-13
# AC-11: CSS contains 4px and 8px spacing values in the spacing scale
# PO then={exit_code equals 0} → both values found → exit 0

CSS_FILE="static/css/main.css"

if [ ! -f "$CSS_FILE" ]; then
  echo "CSS file not found: $CSS_FILE" >&2
  exit 2
fi

ERRORS=0

if grep -q "4px" "$CSS_FILE"; then
  echo "OK: 4px spacing found"
else
  echo "ERROR: 4px spacing NOT found in CSS" >&2
  ERRORS=$((ERRORS + 1))
fi

if grep -q "8px" "$CSS_FILE"; then
  echo "OK: 8px spacing found"
else
  echo "ERROR: 8px spacing NOT found in CSS" >&2
  ERRORS=$((ERRORS + 1))
fi

if [ $ERRORS -eq 0 ]; then
  exit 0
else
  exit 1
fi
