#!/usr/bin/env bash
# scenario-id: US-08/SC-12
# AC-10: Templates use semantic HTML elements throughout
# PO then={exit_code equals 0}

TEMPLATES_DIR="templates"

if [ ! -d "$TEMPLATES_DIR" ]; then
  printf '{"found":false,"error":"Templates directory not found"}\n'
  exit 2
fi

ERRORS=0
FOUND=""

for element in nav main header section button; do
  if grep -rq "<${element}" "$TEMPLATES_DIR"; then
    FOUND="${FOUND}${element},"
  else
    ERRORS=$((ERRORS + 1))
  fi
done

FOUND="${FOUND%,}"

if [ $ERRORS -eq 0 ]; then
  printf '{"found":true,"elements":"%s"}\n' "$FOUND"
  exit 0
else
  printf '{"found":false,"elements":"%s","missing_count":%d}\n' "$FOUND" "$ERRORS"
  exit 1
fi
