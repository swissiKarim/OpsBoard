#!/usr/bin/env bash
# scenario-id: US-08/SC-11
# AC-9: Interactive elements have visible focus ring CSS rules
# PO then={exit_code equals 0}

CSS_FILE="static/css/main.css"

if [ ! -f "$CSS_FILE" ]; then
  printf '{"found":false,"error":"CSS file not found"}\n'
  exit 2
fi

if grep -q "focus-visible" "$CSS_FILE"; then
  printf '{"found":true,"rule":"focus-visible"}\n'
  exit 0
else
  printf '{"found":false,"rule":"focus-visible"}\n'
  exit 1
fi
