#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# 가상환경 생성
if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip

echo "Installing backend dependencies"
pip install -r backend/requirements.txt

echo "Installing frontend dependencies"
pip install -r frontend/requirements.txt

echo ""
echo "Install complete!"
echo "Run:"
echo "  ./scripts/run_backend.sh"
echo "  ./scripts/run_frontend.sh"
