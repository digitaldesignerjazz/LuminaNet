#!/usr/bin/env bash
# NetBird Boot-Helper – Nexus / LuminaOS
set -euo pipefail

KEY="${NETBIRD_SETUP_KEY:-}"
MGMT="${NETBIRD_MGMT:-}"

if ! command -v netbird >/dev/null 2>&1; then
  echo "NetBird fehlt — installiere Client..."
  curl -fsSL https://pkgs.netbird.io/install.sh | sh
fi

if netbird status 2>/dev/null | grep -qiE 'Daemon status:\s*Connected|Status:\s*Connected'; then
  echo "NetBird läuft bereits."
  netbird status | head -16
  ip -4 addr show wt0 2>/dev/null || true
  exit 0
fi

echo "Starte NetBird..."
if [ -n "$KEY" ]; then
  if [ -n "$MGMT" ]; then
    netbird up --setup-key "$KEY" --management-url "$MGMT"
  else
    netbird up --setup-key "$KEY"
  fi
else
  if [ -n "$MGMT" ]; then
    netbird up --management-url "$MGMT"
  else
    netbird up
  fi
fi

sleep 2
echo "=== NetBird Status ==="
netbird status || true
ip -4 addr show wt0 2>/dev/null || echo "wt0 noch nicht da — Login/Setup-Key prüfen"
