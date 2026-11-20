#!/usr/bin/env bash
# scenario-id: US-08/SC-13
# AC-11: CSS contains 4px and 8px spacing values in the spacing scale
# PO then={exit_code equals 0}

CSS_FILE="static/css/main.css"

if [ ! -f "$CSS_FILE" ]; then
  printf '{"found":false,"error":"CSS file not found"}\n'
  exit 2
fi

ERRORS=0
HAS_4PX=false
HAS_8PX=false

if grep -q "4px" "$CSS_FILE"; then
  HAS_4PX=true
else
  ERRORS=$((ERRORS + 1))
fi

if grep -q "8px" "$CSS_FILE"; then
  HAS_8PX=true
else
  ERRORS=$((ERRORS + 1))
fi

if [ $ERRORS -eq 0 ]; then
  printf '{"found":true,"has_4px":%s,"has_8px":%s}\n' "$HAS_4PX" "$HAS_8PX"
  exit 0
else
  printf '{"found":false,"has_4px":%s,"has_8px":%s}\n' "$HAS_4PX" "$HAS_8PX"
  exit 1
fi
