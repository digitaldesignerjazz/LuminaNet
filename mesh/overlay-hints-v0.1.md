# Mesh Overlay Hints v0.1

**Status:** öffentliche Hinweise, kein Betriebsnetz  
**Schicht:** Mesh  
**Verwandt:** `docs/01-architecture.md`, `schema/`

---

## 1. Zweck

Dieses Dokument beschreibt, *wie* LuminaNet auf einem Overlay sitzen soll — nicht *wo* dein privates Netz liegt. Keine Peer-Listen, keine Keys, keine Standortkoordinaten.

Ziel: ein kleiner Knoten soll Envelope-Nachrichten tragen können, Partitionen überleben und fremde Payloads nicht ungeprüft ausführen.

## 2. Annahmen

- Es gibt ein Overlay mit stabilen Peer-IDs (Yggdrasil / vergleichbarer IPv6-Overlay, oder ein gleichwertiger Mesh).
- Transport ist bidirektional, aber nicht verlässlich. Duplikate und Verspätung sind normal.
- Ein Lumina- oder Agentenknoten darf nur ein schmales Topic-Fenster öffnen.
- Identität im Envelope (`from.role`) ist ein Label, keine kryptographische Aussage. Auth liegt außerhalb.

## 3. Adressierung

Öffentliche Konvention, lokal umsetzbar:

```
luminanet://<class>/<id-or-role>/<topic>
```

Beispiele:

```
luminanet://lumina/atelier-ambient/scene.set
luminanet://agent/lumia/agent.ask
luminanet://mesh/local/mesh.ping
```

Abbildung auf das Overlay bleibt Implementationssache:

- eine Overlay-Adresse pro Node, Topics im Envelope
- oder eine Overlay-Multicast-/PubSub-Gruppe pro `class.topic`

Beide sind konform, solange Envelope und Schema gelten.

## 4. Transportregeln

| Regel | Norm |
|---|---|
| Payload | genau ein JSON-Envelope, UTF-8, Schema `envelope.schema.json` |
| Maximale Größe | 16 KiB in v0.1 |
| TTL | `ttl_s` ist eine Höchstgrenze, kein Lieferversprechen |
| Duplikate | Empfänger dedupliziert über `id` (ULID/UUID), Fenster ≥ 10 min |
| Unbekanntes Topic | ablehnen, nicht weiterleiten |
| Unbekanntes Feld | ignorieren, wenn Schema `additionalProperties` es erlaubt; sonst nack |
| Replay | Nachrichten älter als `ts + ttl_s + 60s` verwerfen |

Weiterleitung fremder Envelopes nur, wenn der Knoten explizit Relay ist. Standardknoten sind Endpunkte.

## 5. Hello und Partition

### 5.1 `mesh.ping`

Leerer oder minimaler Body. Antwort `mesh.pong` mit:

```json
{
  "uptime_s": 3840,
  "partition_hint": false,
  "caps_hash": "sha256:optional"
}
```

`caps_hash` darf ein Hash der öffentlichen Caps sein, nie der Caps-Inhalt mit Geheimnissen.

### 5.2 Partition

Ein Knoten nimmt Partition an, wenn:

- kein Pong von mindestens einem konfigurierten Anchor innerhalb `3 * ping_interval`, oder
- Overlay-Self-Test fehlschlägt

Verhalten:

1. Lumina hält letzte gültige Scene, dann Fallback nach lokalem `hold_s`.
2. Agenten beantworten nur noch lokale Asks oder senden `nack.partition`.
3. Nach Wiederkehr kein automatisches globales `scene.set`.
4. Operator oder explizite neue Asks setzen den Zustand neu.

## 6. Trust-Anker (nur Muster)

Öffentlich erlaubt ist die *Form*, nicht das Material:

```text
trust:
  mode: allowlist            # allowlist | local-signed | closed
  allow_classes: [lumina, agent, mesh]
  max_priority_from_mesh: 2  # safety (3/4) nur lokal
```

`local-signed` bedeutet: Signaturprüfung gegen einen lokalen Trust-Store. Der Store selbst gehört nicht ins Repository.

## 7. Port- und Pfadhinweise (nicht-normativ)

Wenn jemand lokal testet, ohne Overlay:

- loopback HTTP `/v0.1/envelope` als Entwicklungsstich
- Unix-Socket `luminanet.sock` auf dem Gerät
- Overlay-Peer erst, wenn Hello + Schema-Validierung grün sind

Produktionsports und echte Overlay-IPs bleiben privat.

## 8. Testminimum

Ein Overlay-Adapter gilt als konform, wenn er:

1. nur schema-valide Envelopes annimmt,
2. zu große oder abgelaufene Nachrichten still verwirft,
3. unbekannte Topics nicht routed,
4. Partition dem Lumina- und Agenten-Layer signalisiert,
5. keine Peer-Tabelle und keine Keys persistiert, die versehentlich committbar wären.

## 9. Bewusst ausgelassen

- Yggdrasil-Config, NovaNet-Keys, Tenda-Seriennummern
- Bootstrap-Peers dieses Netzes
- Tor/I2P-Brücken-Details
- Bandbreiten- und Gebührenmodelle

---

*Tragen, nicht verraten.*
