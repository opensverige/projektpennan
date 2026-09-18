#!/usr/bin/env bash
# Kärndemo — chatt + testchips, utan Ollama.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/backend"
export PYTHONPATH="${ROOT}/backend${PYTHONPATH:+:$PYTHONPATH}"
HOST="${UTTER_DEMO_HOST:-127.0.0.1}"
PORT="${UTTER_DEMO_PORT:-8080}"
echo "Utter kärndemo på http://${HOST}:${PORT}"
echo "Start:  http://${HOST}:${PORT}/start.html"
echo "Test:   http://${HOST}:${PORT}/test.html"
echo "Chatt:  http://${HOST}:${PORT}/index.html"
exec python3 -m uvicorn demo:app --host "$HOST" --port "$PORT"
