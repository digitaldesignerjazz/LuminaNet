#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 fehlt. Unter Debian/Ubuntu:"
  echo "  sudo apt update && sudo apt install -y python3 python3-jsonschema"
  exit 2
fi

if ! python3 -c "import jsonschema" >/dev/null 2>&1; then
  echo "jsonschema fehlt. Ein Weg genügt:"
  echo "  sudo apt install -y python3-jsonschema"
  echo "  oder: python3 -m pip install --user -r tools/requirements.txt"
  exit 2
fi

exec python3 tools/validate.py
