# Lumina-Protokoll v0.1

**Status:** Skizze  
**Schicht:** physische Licht- und Ambient-Knoten  
**Träger:** Mesh-Envelope aus `docs/01-architecture.md`

---

## 1. Idee

Ein Lumina-Knoten ist eine adressierbare Lichtfläche mit optionaler grober Sensorik. Er versteht Szenen, nicht Personen. Er leuchtet zuverlässig auch dann, wenn Agenten oder Overlay fehlen.

Lumina ist die *sichtbare Stimme* des Nexus — nicht dessen Gedächtnis.

## 2. Knotenmodell

```text
LuminaNode
  id          lokale, rotierbare Kennung
  channels    1..n logische Lichtkanäle (z. B. ambient, task, accent, signal)
  gamut       srgb | tunable-white | rgbw
  limits      max_nits, max_change_per_s, blackout_ok
  sensors     optional: lux, occupied, temp  (keine Kameras in v0.1)
  fallback    sichere Scene bei Timeout oder Partition
```

`occupied` ist ein boolesches oder enumeriertes Feld (`unknown|empty|present`). Es trägt keine Identität.

## 3. Scene-Objekt

```json
{
  "scene_id": "dawn-soft",
  "priority": 2,
  "hold_s": 600,
  "channels": {
    "ambient": { "mode": "rgb", "rgb": [255, 214, 170], "nits": 40, "ease_ms": 1800 },
    "signal":  { "mode": "off" }
  },
  "rhythm": { "kind": "none" }
}
```

Felder:

- `priority` — 0 idle, 1 comfort, 2 task, 3 signal, 4 safety. Höhere Zahl gewinnt lokal.
- `hold_s` — nach Ablauf kehrt der Knoten zur Fallback-Scene zurück, sofern kein Refresh kommt.
- `ease_ms` — harte Sprünge nur bei `priority >= 3`.
- `rhythm.kind` — `none` \| `breathe` \| `pulse`. Kein Strobe in v0.1.

### Safety

- `priority 4` darf nur von lokal vertrauenswürdigen Quellen gesetzt werden.
- Blinkfrequenzen unter 3 Hz, keine photosensitiven Muster.
- `blackout_ok: false` verhindert vollständiges Ausschalten (Flure, Stufen).

## 4. Topics

| Topic | Richtung | Body |
|---|---|---|
| `node.hello` | node → mesh | caps, gamut, limits |
| `node.caps` | any → node | leer; Antwort wie hello |
| `scene.set` | agent/operator → node | Scene |
| `scene.get` | any → node | aktuelle Scene + source |
| `scene.clear` | operator → node | zurück auf Fallback |
| `sense.sample` | node → mesh | lux / occupied / temp |

Antworten nutzen dasselbe Envelope, `to` und `from` getauscht, `in_reply_to` = ursprüngliche `id`.

## 5. Beispiel: sanfte Dämmerung

```json
{
  "v": "0.1",
  "id": "01K3Q8 lumina-dawn",
  "ts": "2026-08-30T04:50:00Z",
  "from": { "class": "agent", "role": "lumia" },
  "to":   { "class": "lumina", "topic": "scene.set" },
  "ttl_s": 15,
  "body": {
    "scene_id": "dawn-soft",
    "priority": 1,
    "hold_s": 1800,
    "channels": {
      "ambient": { "mode": "rgb", "rgb": [255, 214, 170], "nits": 28, "ease_ms": 4000 }
    },
    "rhythm": { "kind": "breathe", "period_ms": 12000, "depth": 0.08 }
  }
}
```

Der Knoten bestätigt mit der tatsächlich angewandten Scene (kann durch lokale Limits geklemmt sein).

## 6. Komposition

Mehrere Knoten bilden eine *Zone*. Eine Zone ist in v0.1 nur eine Namenskonvention (`zone:atelier`), kein eigener Konsens. Der Sender adressiert entweder einen Knoten oder ein Topic mit Zone-Hinweis. Bei Widerspruch entscheidet jeder Knoten lokal nach Priority und Timestamp.

## 7. Hardware-Hinweis (nicht-normativ)

v0.1 schreibt keine Platine vor. Ein gültiger Knoten kann sein:

- adressierbarer LED-Controller hinter einem kleinen Overlay-Peer
- Displayfläche mit Ambient-Kanal
- schlichte Tunable-White-Leuchte mit einem Steuerkanal

Maßgeblich ist das Scene-Objekt, nicht der Treiber.

## 8. Testminimum

Ein Knoten gilt als konform, wenn er:

1. `node.hello` sendet und `node.caps` beantwortet,
2. eine gültige `scene.set` innerhalb der Limits anwendet,
3. nach `hold_s` oder verlorenem Overlay auf Fallback zurückkehrt,
4. `priority 4` von unbekannten Quellen ablehnt,
5. keine personenbezogenen Felder emitiert.

---

*Skizze · Lumina leuchtet auch allein*
