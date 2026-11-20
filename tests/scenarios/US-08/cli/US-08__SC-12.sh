#!/usr/bin/env bash
# scenario-id: US-08/SC-12
# AC-10: Templates use semantic HTML elements throughout
# PO then={exit_code equals 0} → semantic elements found → exit 0

TEMPLATES_DIR="templates"

if [ ! -d "$TEMPLATES_DIR" ]; then
  echo "Templates directory not found" >&2
  exit 2
fi

ERRORS=0

check_element() {
  local element="$1"
  if grep -rq "<${element}" "$TEMPLATES_DIR"; then
    echo "OK: <${element}> found"
  else
    echo "ERROR: <${element}> NOT found in templates" >&2
    ERRORS=$((ERRORS + 1))
  fi
}

check_element "nav"
check_element "main"
check_element "header"
check_element "section"
check_element "button"

if [ $ERRORS -eq 0 ]; then
  echo "OK: All required semantic HTML elements present"
  exit 0
else
  echo "ERROR: $ERRORS semantic HTML element(s) missing" >&2
  exit 1
fi
