# LuminaNet Loopback v0.1

Lokaler Knoten. Bindet **nur** `127.0.0.1:8787`. Kein Overlay, keine Hardware.

## Start

```bash
git pull
chmod +x tools/start-luminanet.sh
./tools/start-luminanet.sh
```

oder:

```bash
python3 tools/luminanetd.py
```

## Prüfen

```bash
curl -s http://127.0.0.1:8787/health
curl -s http://127.0.0.1:8787/v0.1/scene
```

## Dämmerung setzen

```bash
curl -s -X POST http://127.0.0.1:8787/v0.1/envelope \
  -H 'Content-Type: application/json' \
  --data-binary @schema/examples/valid/envelope-dawn-scene-set.json
```

## Ask an Lumia

```bash
curl -s -X POST http://127.0.0.1:8787/v0.1/envelope \
  -H 'Content-Type: application/json' \
  --data-binary @schema/examples/valid/envelope-agent-ask-dawn.json
```

## Partition

Während Partition lehnt der Knoten `scene.set` ab und fällt auf Fallback zurück.

```bash
curl -s -X POST http://127.0.0.1:8787/v0.1/envelope \
  -H 'Content-Type: application/json' \
  -d '{"v":"0.1","id":"01K3QH-part-on","ts":"2026-08-30T05:00:00Z","from":{"class":"mesh"},"to":{"class":"mesh","topic":"mesh.partition"},"body":{"partition":true}}'
```

## Stop

Im Terminal des Knotens: `Ctrl+C`.
