# LuminaNet JSON Schema v0.1

Maschinenlesbare Verträge zur öffentlichen Schicht.

| Datei | Gegenstand |
|---|---|
| [envelope.schema.json](envelope.schema.json) | äußerer Nachrichtenrahmen |
| [scene.schema.json](scene.schema.json) | Body von `scene.set` / angewandte Scene |
| [agent-message.schema.json](agent-message.schema.json) | Bodies von `agent.hello|ask|say|handoff|nack` |
| [examples/](examples/) | gültige und ungültige Fixtures |

## Prüfen

```bash
sudo apt install -y python3 python3-jsonschema
./tools/run-validate.sh
```

oder:

```bash
python3 -m pip install --user -r tools/requirements.txt
python3 tools/validate.py
```

Das Script verlangt: alles unter `examples/valid/` gilt, alles unter `examples/invalid/` scheitert. CI auf `main` läuft dieselbe Kante.

## Grenzen

Schema prüft Form, nicht Absicht und nicht Vertrauenswürdigkeit. `priority` 4 im JSON macht eine Quelle nicht lokal vertrauenswürdig.
