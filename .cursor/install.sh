#!/usr/bin/env bash
# Idempotent Cloud Agent / local dev setup for Skooli Buddy.
#
# Prepares the "Open, local" surface (FastAPI backend + static frontend) and the
# messaging surface (Telegram bot + Streamlit dashboard) in a single virtualenv.
# The heavy external LLM (Ollama) is expected on the LAN and is NOT installed
# here — see AGENTS.md / README.md.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# System packages: python venv, plus headers + compiler needed to build
# chromadb's native chroma-hnswlib wheel, and zstd for archive extraction.
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -q
sudo apt-get install -y --no-install-recommends \
  python3.12-venv python3.12-dev build-essential zstd

# Python virtual environment with backend + messaging dependencies.
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt -r backend/requirements.txt

# The FastAPI backend hardcodes /app/{vault,agents,frontend} paths (matching the
# Docker image WORKDIR). Symlink /app -> repo root so uvicorn runs outside Docker.
sudo ln -sfn "$REPO_ROOT" /app

echo "Skooli Buddy environment ready."
