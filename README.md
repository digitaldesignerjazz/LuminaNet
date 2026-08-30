# LuminaNet

**LuminaNet** — öffentliches Nexus-Prototyp-Repository für Lumina-Lichtsysteme, Mesh-Networking, KI-Agentenschwärme und dezentrale Infrastruktur.

> Licht. Netz. Intelligenz. Verbunden.

## Vision

LuminaNet ist die öffentliche Schicht des Nexus-Stacks. Es macht ausgewählte Prototypen, Spezifikationen und Integrationsmuster sichtbar, ohne interne Betriebsgeheimnisse oder private Schlüssel preiszugeben.

Schwerpunkte:

- **Lumina** — Licht-, Display- und Ambient-Systeme als physische Schnittstelle des Nexus
- **Mesh** — resilienter Overlay (xMesh / NovaNet / QNET / Yggdrasil) als Kommunikationssubstrat
- **Agentenschwärme** — koordinierte, persistente KI-Agenten (Lumia, Elara, Lyra, Xen) mit skilllogin-Kontinuität
- **Dezentrale Infrastruktur** — Anbindung an Blockchain-Anreize, Privacy-Layer (Tor/I2P) und Edge-Prototypen

## Status

**v0.1 Entwurf** — Spezifikation, Protokoll, Agenten-Schnittstelle, Overlay-Hinweise und JSON-Schema.

| Pfad | Inhalt |
|---|---|
| [docs/01-architecture.md](docs/01-architecture.md) | Schichten, Vertrauensgrenzen, Envelope, Topics |
| [proto/lumina-protocol-v0.1.md](proto/lumina-protocol-v0.1.md) | Lumina-Knoten, Scene-Objekt, Safety |
| [agents/public-interface-v0.1.md](agents/public-interface-v0.1.md) | Rollen, Caps, Ask/Say/Handoff |
| [mesh/overlay-hints-v0.1.md](mesh/overlay-hints-v0.1.md) | Adressierung, TTL, Partition, Trust-Muster |
| [schema/](schema/) | JSON Schema für Envelope, Scene, Agent-Bodies |

## Struktur

```
LuminaNet/
├── docs/          Spezifikationen, Architektur, Protokolle
├── proto/         Hardware- und Firmware-Skizzen (Lumina)
├── mesh/          Overlay-Konfigurationen und Peer-Hinweise
├── agents/        Öffentliche Agenten-Schnittstellen und Prompt-Muster
├── schema/        Maschinenlesbare JSON-Schemas
├── infra/         Deployment-Notizen, Container, Monitoring-Hooks
└── LICENSE
```

## Leitsätze

- Öffentlich, was lehren und verbinden soll — privat, was schützen muss.
- Modular, selbst-dokumentierend, testbar.
- Privacy by design. Keine Secrets im Repository.
- Evolution statt Big-Bang: kleine, nachvollziehbare Commits.
- Licht darf nach Partition nicht von allein eskalieren.
- Schema prüft Form, nicht Vertrauen.

## Mitwirken

Issues und Pull Requests sind willkommen. Bitte keine Zugangsdaten, private Keys oder personenbezogene Daten committen.

## Lizenz

Siehe [LICENSE](LICENSE).

---

*Teil des Nexus-Ökosystems · Esslinger Consulting / digitaldesignerjazz*
