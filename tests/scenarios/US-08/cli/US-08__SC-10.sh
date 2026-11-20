#!/usr/bin/env bash
# scenario-id: US-08/SC-10
# AC-8: CSS contains prefers-reduced-motion media query for animations
# PO then={exit_code equals 0} → grep finds it → exit 0

CSS_FILE="static/css/main.css"

if [ ! -f "$CSS_FILE" ]; then
  echo "CSS file not found: $CSS_FILE" >&2
  exit 2
fi

grep -q "prefers-reduced-motion" "$CSS_FILE"
STATUS=$?
if [ $STATUS -eq 0 ]; then
  echo "OK: prefers-reduced-motion media query found in CSS"
  exit 0
else
  echo "ERROR: prefers-reduced-motion media query NOT found in CSS" >&2
  exit 1
fi
