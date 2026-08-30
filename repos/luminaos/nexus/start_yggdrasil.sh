#!/bin/bash
# Yggdrasil Boot-Helper – Nexus / LuminaOS
set -e
CONF="${YGG_CONF:-/home/workdir/artifacts/yggdrasil.conf}"
LOG="${YGG_LOG:-/tmp/yggdrasil.log}"

if ! command -v yggdrasil >/dev/null 2>&1; then
  echo "Yggdrasil nicht installiert. Installiere..."
  if [ -f /tmp/yggdrasil.deb ]; then
    dpkg -i /tmp/yggdrasil.deb
  else
    wget -q "https://github.com/yggdrasil-network/yggdrasil-go/releases/download/v0.5.14/yggdrasil-0.5.14-amd64.deb" -O /tmp/yggdrasil.deb
    dpkg -i /tmp/yggdrasil.deb
  fi
fi

if pgrep -f "yggdrasil -useconffile" >/dev/null 2>&1; then
  echo "Yggdrasil läuft bereits."
  yggdrasilctl -endpoint=tcp://127.0.0.1:9001 getSelf 2>/dev/null | head -8
  exit 0
fi

echo "Starte Yggdrasil..."
yggdrasil -useconffile "$CONF" > "$LOG" 2>&1 &
sleep 4
yggdrasilctl -endpoint=tcp://127.0.0.1:9001 getSelf 2>/dev/null | head -10
echo "Yggdrasil gestartet. Log: $LOG"
