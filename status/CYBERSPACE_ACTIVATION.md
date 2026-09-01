# Cyberspace Activation — LuminaNet Overlay

- timestamp: 2026-09-01T03:24:00Z
- command: start cyberspace with Nexus Control Plane and luminanet overlay public repository GitHub
- operator: Sir
- agent: Lumia

## Public repositories

| Layer | Repository |
|---|---|
| Overlay protocol | https://github.com/digitaldesignerjazz/LuminaNet |
| Cyberspace node | https://github.com/digitaldesignerjazz/LuminaCyberspace |
| Control hub | https://github.com/digitaldesignerjazz/nexus |
| Control panel | https://github.com/digitaldesignerjazz/nexus-control-panel |

## Control plane

- Nexus Control Plane: **ONLINE** (state files + orchestrator sequence 7)
- LuminaNet loopback node: **ONLINE** on `127.0.0.1:8787` (`luminanetd` v0.1)
- First envelope: `mesh.ping` → `mesh.pong` (partition_hint=false)
- Scene: `fallback-warm`
- NetBird / Yggdrasil dataplane: **pending** on privileged Hannover node (binaries not present in this control host)

## Overlay contract

See `mesh/overlay-hints-v0.1.md` and `schema/envelope.schema.json`.
Transport remains endpoint-first. No peer tables and no keys in this pulse.

*Tragen, nicht verraten.*
