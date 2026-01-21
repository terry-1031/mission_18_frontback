#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
source .venv/bin/activate

# 기본값: 로컬 백엔드
export API_BASE_URL="${API_BASE_URL:-http://localhost:8000}"

streamlit run frontend/app.py