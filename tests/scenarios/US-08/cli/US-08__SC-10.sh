#!/usr/bin/env bash
# scenario-id: US-08/SC-10
# AC-8: CSS contains prefers-reduced-motion media query for animations
# PO then={exit_code equals 0}

CSS_FILE="static/css/main.css"

if [ ! -f "$CSS_FILE" ]; then
  printf '{"found":false,"error":"CSS file not found"}\n'
  exit 2
fi

if grep -q "prefers-reduced-motion" "$CSS_FILE"; then
  printf '{"found":true,"query":"prefers-reduced-motion"}\n'
  exit 0
else
  printf '{"found":false,"query":"prefers-reduced-motion"}\n'
  exit 1
fi
