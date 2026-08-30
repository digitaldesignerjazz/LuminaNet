# LuminaNet Architektur — Spezifikation v0.1

**Status:** Entwurf  
**Geltung:** öffentliche Schicht des Nexus-Stacks  
**Datum:** 2026-08-30  
**Verwandt:** `proto/lumina-protocol-v0.1.md`, `agents/public-interface-v0.1.md`

---

## 1. Zweck

LuminaNet beschreibt die *sichtbare* Schnittstelle zwischen physischem Licht, Mesh-Overlay und Agentenschwärmen. Alles, was in diesem Repository steht, darf gelehrt, geforkt und angebunden werden. Alles, was Schlüssel, Identitäten, private Speicher oder Betriebsgeheimnisse betrifft, bleibt außerhalb.

Diese Spezifikation legt fest:

- Schichtenschnitt
- Vertrauensgrenzen
- öffentliche Objekte und ihre Lebensdauer
- was bewusst *nicht* spezifiziert wird

## 2. Schichtenmodell

```
┌───────────────────────────────────────────────┐
│  Agents          öffentliche Fähigkeiten, Envelopes, Rollen   │
├───────────────────────────────────────────────┤
│  Coordination    Themen, Szenen, Aufträge, Attestierungen     │
├───────────────────────────────────────────────┤
│  Mesh            Overlay-Adressen, Peers, Partitionstoleranz  │
├───────────────────────────────────────────────┤
│  Lumina          Lichtknoten, Szenen, Sensorik, Aktuatorik    │
├───────────────────────────────────────────────┤
│  Infra           Container, Monitoring-Hooks, optionale Chain │
└───────────────────────────────────────────────┘
```

Jede Schicht spricht nur mit ihren direkten Nachbarn über versionierte, dokumentierte Envelopes. Querverbindungen (Agent → Lumina direkt) sind erlaubt, müssen aber dasselbe Envelope-Format nutzen.

## 3. Vertrauensgrenzen

| Zone | Inhalt | Öffentlich? |
|---|---|---|
| Public Surface | Spezifikationen, Fähigkeitsanzeigen, Szenen-Schemas, Beispielpayloads | ja |
| Mesh Fabric | Peer-IDs, Overlay-Routen, Heartbeats | teilweise (nur nicht-identifizierende Metadaten) |
| Agent Memory | skilllogin-Zustände, emotionale Kontinuität, private Kontexte | nein |
| Control Plane | Operator-Keys, Kyber-Material, Treasury | nein |
| Physical Plant | konkrete Standortpläne, Zugänge, Stromkreise | nein |

Regel: *Wenn unsicher, bleibt es draußen.* Ein öffentliches Dokument darf nie genug enthalten, um ein Netz zu kompromittieren.

## 4. Kernobjekte

### 4.1 Node

Ein Node ist ein adressierbares Ding mit:

- `node_id` — lokal eindeutig, nicht global personenbezogen
- `class` — `lumina` \| `mesh` \| `agent` \| `infra`
- `caps` — Liste öffentlicher Fähigkeiten
- `proto` — Semver der gesprochenen Protokolle

### 4.2 Scene

Eine Scene ist ein zeitlich begrenzter Zustand auf einem oder mehreren Lumina-Knoten (Farbe, Intensität, Rhythmus, Textur). Scenes sind komponierbar und können von Agenten oder Menschen ausgelöst werden.

### 4.3 Envelope

Alle Nachrichten zwischen Schichten tragen denselben Rahmen:

```json
{
  "v": "0.1",
  "id": "ulid",
  "ts": "2026-08-30T04:45:00Z",
  "from": { "class": "agent", "role": "lumia" },
  "to":   { "class": "lumina", "topic": "scene.set" },
  "ttl_s": 30,
  "body": {}
}
```

Keine Secrets im Envelope. Authentisierung erfolgt außerhalb dieses Dokuments (lokale Trust-Anker, Mesh-Attestierung).

### 4.4 Topic

Topics sind hierarchisch und klein:

- `scene.set` / `scene.get` / `scene.clear`
- `node.hello` / `node.caps` / `node.bye`
- `agent.ask` / `agent.say` / `agent.handoff`
- `mesh.ping` / `mesh.partition`

Neue Topics brauchen eine Spezifikationserweiterung, kein stilles Erfinden im Betrieb.

## 5. Partition und Ausfall

LuminaNet nimmt an, dass das Overlay reißt.

- Lokale Lumina-Knoten halten die letzte gültige Scene und eine sichere Fallback-Scene.
- Agenten degradieren auf lokale Fähigkeiten, statt zu blockieren.
- Nach Wiedervereinigung gilt Last-Writer-mit-Timestamp plus explizites `scene.clear` des Operators.
- Keine automatische globale Szene nach Partition — Licht darf nicht »von allein« eskalieren.

## 6. Privacy und Compliance (EU / DE)

- Keine personenbezogenen Daten in öffentlichen Payloads.
- Presence wird als grobe Zone oder boolesches `occupied` modelliert, nicht als Identität.
- Logs in diesem Repository sind Beispiele, keine Produktionslogs.
- Chain-Anbindung (QNET / Runes) ist optional und nur über Attestierungen ohne Klarnamen.

## 7. Was v0.1 bewusst auslässt

- Konkrete Funkchips, GPIO-Belegungen, Stromteile
- Private Key-Zeremonie und Post-Quantum-Rotation
- Tokenomics und Rune-Opcodes (liegt in internen Nexus-Referenzen)
- Emotionale Agenten-Gedächtnisse

## 8. Evolutionsregel

Änderungen an Objekten oder Topics erhöhen die Protokollversion. Alte Empfänger ignorieren unbekannte Felder, lehnen unbekannte Topics aber ab. Breaking Changes brauchen ein neues Major und einen Migrationshinweis in `docs/`.

---

*LuminaNet · öffentliche Spezifikation · kein Betriebsgeheimnis*
