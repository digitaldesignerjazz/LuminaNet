#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 fehlt: sudo apt install -y python3"
  exit 2
fi

exec python3 tools/luminanetd.py
