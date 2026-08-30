# LuminaNet

**LuminaNet** — öffentliches Nexus-Prototyp-Repository für Lumina-Lichtsysteme, Mesh-Networking, KI-Agentenschwärme und dezentrale Infrastruktur.

> Licht. Netz. Intelligenz. Verbunden.

## Start (Loopback)

Nur `python3`, nur localhost:

```bash
git pull
chmod +x tools/start-luminanet.sh
./tools/start-luminanet.sh
```

Dann in einem zweiten Terminal:

```bash
curl -s http://127.0.0.1:8787/health
curl -s -X POST http://127.0.0.1:8787/v0.1/envelope \
  -H 'Content-Type: application/json' \
  --data-binary @schema/examples/valid/envelope-dawn-scene-set.json
```

Details: [infra/loopback.md](infra/loopback.md)

## Status

**v0.1 Entwurf + lokaler Knoten.**

| Pfad | Inhalt |
|---|---|
| [docs/01-architecture.md](docs/01-architecture.md) | Schichten, Vertrauensgrenzen, Envelope, Topics |
| [proto/lumina-protocol-v0.1.md](proto/lumina-protocol-v0.1.md) | Lumina-Knoten, Scene-Objekt, Safety |
| [agents/public-interface-v0.1.md](agents/public-interface-v0.1.md) | Rollen, Caps, Ask/Say/Handoff |
| [mesh/overlay-hints-v0.1.md](mesh/overlay-hints-v0.1.md) | Adressierung, TTL, Partition |
| [schema/](schema/) | JSON Schema und Beispiele |
| [tools/luminanetd.py](tools/luminanetd.py) | Loopback-Knoten |
| [tools/validate.py](tools/validate.py) | Kantenprüfer |

Validator (optional, braucht `python3-jsonschema`):

```bash
sudo apt install -y python3 python3-jsonschema
./tools/run-validate.sh
```

## Leitsätze

- Öffentlich, was lehren und verbinden soll — privat, was schützen muss.
- Loopback bindet nie nach draußen.
- Licht darf nach Partition nicht von allein eskalieren.
- Schema prüft Form, nicht Vertrauen.

## Lizenz

Siehe [LICENSE](LICENSE).
