#!/usr/bin/env bash
# Schaltet versionierte Hooks unter .githooks/ scharf.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .git ]]; then
  echo "Kein Git-Repo. Erst klonen:"
  echo "  git clone https://github.com/digitaldesignerjazz/LuminaNet.git"
  exit 2
fi

chmod +x .githooks/pre-commit .githooks/commit-msg .githooks/pre-push
git config core.hooksPath .githooks

echo "Hooks aktiv: $(git config --get core.hooksPath)"
echo "  pre-commit  Secrets + JSON + validate.py"
echo "  commit-msg  Betrefflänge und Typ-Hinweis"
echo "  pre-push    validate.py falls jsonschema da ist"
