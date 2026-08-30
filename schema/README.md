# LuminaNet JSON Schema v0.1

Maschinenlesbare Verträge zur öffentlichen Schicht.

| Datei | Gegenstand |
|---|---|
| [envelope.schema.json](envelope.schema.json) | äußerer Nachrichtenrahmen |
| [scene.schema.json](scene.schema.json) | Body von `scene.set` / angewandte Scene |
| [agent-message.schema.json](agent-message.schema.json) | Bodies von `agent.hello|ask|say|handoff|nack` |

## Nutzung

Validierung vor dem Senden und nach dem Empfang. Ungültige Envelopes werden verworfen, nicht geraten.

Beispiel mit Python:

```python
import json
from pathlib import Path
from jsonschema import Draft202012Validator

schema = json.loads(Path("schema/envelope.schema.json").read_text())
Draft202012Validator(schema).validate(envelope)
```

`$id` zeigt auf dieses Repository. Breaking Changes erhöhen die Envelope-Version `v` und bekommen neue Dateien, alte Schemas bleiben stehen.

## Grenzen

Schema prüft Form, nicht Absicht und nicht Vertrauenswürdigkeit. `priority` 4 im JSON macht eine Quelle nicht lokal vertrauenswürdig.
