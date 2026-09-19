#!/usr/bin/env bash
# Idempotent Cloud Agent / local setup for Utter.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -q
sudo apt-get install -y --no-install-recommends \
  python3.12-venv python3.12-dev build-essential zstd

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt -r backend/requirements.txt

sudo ln -sfn "$REPO_ROOT" /app

echo "Utter environment ready."
