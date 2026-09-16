#!/usr/bin/env bash
# Live SOUL — tutorfilerna + frontier/smart OSS. Inte Ollama-default.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export VAULT_PATH="${VAULT_PATH:-$ROOT/vault}"
HOST="${UTTER_DEMO_HOST:-127.0.0.1}"
PORT="${UTTER_DEMO_PORT:-8080}"

if [ "${UTTER_USE_OLLAMA:-}" = "1" ]; then
  export OLLAMA_URL="${OLLAMA_URL:-http://127.0.0.1:11434}"
  export MODEL_NAME="${MODEL_NAME:-llama3.2:3b}"
  if ! curl -sf "$OLLAMA_URL/api/tags" >/dev/null; then
    echo "Startar Ollama (UTTER_USE_OLLAMA=1)…"
    ollama serve >/tmp/ollama-soul.log 2>&1 &
    for _ in $(seq 1 30); do
      curl -sf "$OLLAMA_URL/api/tags" >/dev/null && break
      sleep 0.4
    done
  fi
fi

echo "Utter SOUL på http://${HOST}:${PORT}"
echo "Chatt: http://${HOST}:${PORT}/index.html"
cd "$ROOT/backend"
export PYTHONPATH="${ROOT}/backend${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m uvicorn soul_server:app --host "$HOST" --port "$PORT"
