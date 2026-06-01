#!/usr/bin/env bash
# BrainStim — start the API server
# Usage: ./start.sh [port]
#
# Requires tribev2 to be installed in the Python environment.
# If using the local tribev2 checkout:
#   VENV=../tribev2/path/to/venv ./start.sh

set -e

PORT="${1:-8000}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Prefer explicitly set VENV, then local tribev2 venv, then system Python
if [ -z "$VENV" ]; then
  CANDIDATE="$SCRIPT_DIR/../tribev2/path/to/venv"
  if [ -d "$CANDIDATE" ]; then
    VENV="$CANDIDATE"
    echo "→ Using tribev2 venv at $VENV"
  else
    VENV=""
    echo "→ Using system Python (make sure tribev2 is installed)"
  fi
fi

PYTHON="${VENV:+$VENV/bin/python}"
PYTHON="${PYTHON:-python3}"
PIP="${VENV:+$VENV/bin/pip}"
PIP="${PIP:-pip3}"

echo "→ Installing server deps…"
"$PIP" install fastapi "uvicorn[standard]" python-multipart soundfile -q

echo "→ Starting BrainStim on http://localhost:$PORT"
echo "   API docs: http://localhost:$PORT/docs"
echo ""

"$PYTHON" -m uvicorn main:app \
  --app-dir "$SCRIPT_DIR/api" \
  --host 0.0.0.0 \
  --port "$PORT" \
  --reload
