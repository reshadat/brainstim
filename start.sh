#!/usr/bin/env bash
# BrainStim — start the API server
# Usage: ./start.sh [port]
#
# Simulation mode works with no extra setup. For the full TRIBEv2 pipeline,
# install tribev2 separately (see README) and point VENV at its environment:
#   VENV=/path/to/tribev2/.venv ./start.sh

set -e

PORT="${1:-8000}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use an explicitly provided VENV if set; otherwise fall back to system Python.
# (No bogus default path — set VENV yourself if tribev2 lives in its own venv.)
if [ -n "${VENV:-}" ]; then
  echo "→ Using venv at $VENV"
else
  echo "→ Using system / active Python (simulation mode needs no tribev2)"
fi

PYTHON="${VENV:+$VENV/bin/python}"
PYTHON="${PYTHON:-python3}"
PIP="${VENV:+$VENV/bin/pip}"
PIP="${PIP:-pip3}"

echo "→ Installing dependencies…"
# requirements.txt covers simulation mode (nilearn, matplotlib, numpy, …);
# the rest are the web-server packages.
"$PIP" install -r "$SCRIPT_DIR/requirements.txt" -q
"$PIP" install fastapi "uvicorn[standard]" python-multipart soundfile -q

echo "→ Starting BrainStim on http://localhost:$PORT"
echo "   API docs: http://localhost:$PORT/docs"
echo ""

"$PYTHON" -m uvicorn main:app \
  --app-dir "$SCRIPT_DIR/api" \
  --host 0.0.0.0 \
  --port "$PORT" \
  --reload
