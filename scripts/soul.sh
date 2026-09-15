#!/usr/bin/env bash
# Live SOUL — tutorfilerna + Ollama. Inte stubbarna.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export VAULT_PATH="${VAULT_PATH:-$ROOT/vault}"
export OLLAMA_URL="${OLLAMA_URL:-http://127.0.0.1:11434}"
export MODEL_NAME="${MODEL_NAME:-llama3.2:3b}"
HOST="${GNISTA_DEMO_HOST:-127.0.0.1}"
PORT="${GNISTA_DEMO_PORT:-8080}"

if ! curl -sf "$OLLAMA_URL/api/tags" >/dev/null; then
  echo "Startar Ollama…"
  ollama serve >/tmp/ollama-soul.log 2>&1 &
  for _ in $(seq 1 30); do
    curl -sf "$OLLAMA_URL/api/tags" >/dev/null && break
    sleep 0.4
  done
fi
if ! curl -sf "$OLLAMA_URL/api/tags" >/dev/null; then
  echo "Ollama svarar inte på $OLLAMA_URL"
  exit 1
fi
if ! curl -sf "$OLLAMA_URL/api/tags" | grep -q "${MODEL_NAME%%:*}"; then
  echo "Hämtar $MODEL_NAME …"
  ollama pull "$MODEL_NAME"
fi

echo "Gnista SOUL ($MODEL_NAME) på http://${HOST}:${PORT}"
echo "Chatt: http://${HOST}:${PORT}/index.html"
cd "$ROOT/backend"
export PYTHONPATH="${ROOT}/backend${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m uvicorn soul_server:app --host "$HOST" --port "$PORT"
