#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [ ! -f .env ]; then
  echo ".env not found. Copy .env.example to .env first." >&2
  exit 1
fi
TRANSPORT="${MCP_TRANSPORT:-stdio}"
python3 -m kakao_heritage --transport "$TRANSPORT"
