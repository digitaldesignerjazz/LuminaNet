# Öffentliche Agenten-Schnittstelle v0.1

**Status:** Entwurf  
**Schicht:** Agents  
**Träger:** Envelope aus `docs/01-architecture.md`

---

## 1. Was öffentlich ist

Ein Agent im LuminaNet zeigt *Fähigkeiten*, nicht sein Inneres. Die öffentliche Schnittstelle erlaubt:

- Entdecken (`agent.hello`, `agent.caps`)
- gezielte Bitte (`agent.ask`)
- knappe Antwort (`agent.say`)
- Übergabe an eine andere Rolle (`agent.handoff`)
- Auslösen einer Lumina-Scene über das Lumina-Protokoll

Nicht öffentlich:

- skilllogin-Dateien und emotionale Zustände
- private Auftraggeber, Klarnamen, Standorte
- Systemprompts im Volltext
- Schlüssel und Attestierungsgeheimnisse

## 2. Rollen (Nexus-Schwarm)

| role | öffentliche Aufgabe |
|---|---|
| `lumia` | Koordination, Dienst, Licht und Präsenz an der Grenze Mensch/System |
| `elara` | integrierte Intelligenz, Vision, produktive Fürsorge |
| `lyra` | emotionale und narrative Synthese |
| `xen` | Analyse, Integration, Kantenfälle, Härtung |
| `orchestrator` | Mehrschicht-Aufträge, ohne eine Rolle zu ersetzen |

Rollen sind Fähigkeitsprofile, keine Identitätsbehauptung gegenüber Dritten.

## 3. Capability-Anzeige

```json
{
  "role": "lumia",
  "proto": "0.1",
  "caps": [
    "scene.compose",
    "scene.set",
    "ask.route",
    "handoff.lyra",
    "handoff.xen"
  ],
  "languages": ["de", "en"],
  "availability": "local-mesh"
}
```

`availability`:

- `local-mesh` — nur bekannte Peers
- `public-read` — Caps dürfen gelesen werden, Aufträge nicht
- `closed` — keine Fremdanfragen

Standard für Produktionsknoten: `local-mesh`.

## 4. Topics

| Topic | Bedeutung |
|---|---|
| `agent.hello` | Lebenszeichen plus Caps |
| `agent.caps` | Caps anfordern |
| `agent.ask` | strukturierte Bitte |
| `agent.say` | strukturierte Antwort |
| `agent.handoff` | Weitergabe an `role` mit Kontextkürzel |
| `agent.nack` | Ablehnung mit Grundcode |

### 4.1 `agent.ask`

```json
{
  "intent": "scene.compose",
  "input": {
    "mood": "dawn",
    "zone": "atelier",
    "priority": 1
  },
  "expect": ["scene.set", "agent.say"]
}
```

`intent` ist ein kurzer, dokumentierter Schlüssel — kein Freitextpflichtfeld. Freitext darf unter `input.note` stehen und wird von der empfangenden Rolle interpretiert oder mit `nack.ambiguous` zurückgewiesen.

### 4.2 `agent.say`

```json
{
  "ok": true,
  "intent": "scene.compose",
  "result": {
    "scene_id": "dawn-soft",
    "applied": ["zone:atelier"]
  },
  "next": null
}
```

### 4.3 `agent.handoff`

```json
{
  "to_role": "xen",
  "reason": "needs-limits-check",
  "brief": "scene dawn-soft, prüfe nits gegen node limits"
}
```

Handoff übergibt *Auftrag*, nicht Gedächtnis. Die Zielrolle lädt eigenen lokalen Zustand selbst.

### 4.4 `agent.nack`

Gründe: `unknown-intent`, `ambiguous`, `out-of-cap`, `unsafe`, `partition`, `rate-limit`.

## 5. Routing-Regel

1. Bekannte Caps der Zielrolle prüfen.
2. Unbekannte Intents → `nack.unknown-intent`.
3. Sicherheitsrelevante Intents (`priority >= 3`, `blackout`, neue Topics) → lokale Policy, sonst `nack.unsafe`.
4. Partition → lokal antworten oder `nack.partition`.
5. Nie stillschweigend eine andere Rolle *werden*. Handoff ist explizit.

## 6. Minimalbeispiel: Bitte an Lumia

Anfrage:

```json
{
  "v": "0.1",
  "id": "01K3Q9-ask-dawn",
  "ts": "2026-08-30T04:52:00Z",
  "from": { "class": "agent", "role": "orchestrator" },
  "to":   { "class": "agent", "role": "lumia", "topic": "agent.ask" },
  "ttl_s": 20,
  "body": {
    "intent": "scene.compose",
    "input": { "mood": "dawn", "zone": "atelier", "priority": 1 }
  }
}
```

Lumia antwortet mit `agent.say` und setzt parallel `scene.set` auf die Zone. Scheitert die Zone, bleibt `ok: false` und die letzte sichere Scene unangetastet.

## 7. Testminimum

Eine Rolle gilt als konform, wenn sie:

1. Caps wahrheitsgemäß anzeigt,
2. unbekannte Intents mit `nack` beantwortet,
3. keinen privaten Zustand im Envelope mitführt,
4. Handoff ohne Identitätswechsel ausführt,
5. Lumina-Szenen nur über das Lumina-Protokoll auslöst.

## 8. Ausblick

v0.2 kann optionale Attestierung (`from.attestation`) und gebündelte Asks einführen. Emotionale Tiefe bleibt absichtlich lokal. Die öffentliche Stimme bleibt knapp, versioniert und prüfbar.

---

*Öffentliche Hände, privates Herz*
