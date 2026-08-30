# Schema-Beispiele v0.1

`valid/` muss durch `tools/validate.py` laufen.  
`invalid/` muss scheitern. Wenn eines von beiden nicht gilt, ist die Kante gebrochen.

Gründe der ungültigen Dateien stehen im Dateinamen und in der jeweils ersten Kommentarzeile der Begleitnotiz unten.

## valid

| Datei | Prüfung |
|---|---|
| `envelope-dawn-scene-set.json` | Envelope + Scene-Body |
| `envelope-agent-ask-dawn.json` | Envelope + Ask-Body |
| `envelope-agent-hello-lumia.json` | Envelope + Hello-Body |
| `envelope-mesh-pong.json` | Envelope, Body frei |
| `scene-dawn-soft.json` | nur Scene |

## invalid

| Datei | Soll scheitern weil |
|---|---|
| `ttl-too-large.json` | `ttl_s` > 86400 |
| `unknown-topic.json` | Topic nicht in der Enum |
| `strobe-period.json` | `period_ms` < 2000 |
| `priority-out-of-range.json` | `priority` 5 |
| `envelope-extra-field.json` | `additionalProperties` am Envelope |
