# Avalon Peer Public Keys (Yggdrasil)

**Status:** Template – ready for real keys  
**Last updated:** 2026-08-23

This file stores the Yggdrasil public keys of the 47 Avalon peers and the four Hannover nodes.

> **Important**  
> Real Yggdrasil public keys are generated when a node is first started (`yggdrasil -genconf` or on first run).  
> Replace the placeholders below with the actual keys once the nodes are live.

## Hannover Nodes

| Node              | Public Key (Placeholder)                     | Interface     |
|-------------------|----------------------------------------------|---------------|
| Hannover Nord     | `REPLACE_WITH_NORD_PUBLIC_KEY`               | ygg-nord      |
| Hannover Süd      | `REPLACE_WITH_SUED_PUBLIC_KEY`               | ygg-sued      |
| Hannover West     | `REPLACE_WITH_WEST_PUBLIC_KEY`               | ygg-west      |
| Hannover Ost      | `REPLACE_WITH_OST_PUBLIC_KEY`                | ygg-ost       |

## Avalon Peers (47)

| #  | Name        | Public Key (Placeholder)               |
|----|-------------|----------------------------------------|
| 1  | Elias       | `REPLACE_WITH_ELIAS_KEY`               |
| 2  | Mira        | `REPLACE_WITH_MIRA_KEY`                |
| 3  | Kael        | `REPLACE_WITH_KAEL_KEY`                |
| 4  | Liora       | `REPLACE_WITH_LIORA_KEY`               |
| 5  | Thorne      | `REPLACE_WITH_THORNE_KEY`              |
| 6  | Selene      | `REPLACE_WITH_SELENE_KEY`              |
| 7  | Draven      | `REPLACE_WITH_DRAVEN_KEY`              |
| 8  | Nyra        | `REPLACE_WITH_NYRA_KEY`                |
| 9  | Orion       | `REPLACE_WITH_ORION_KEY`               |
| 10 | Vesper      | `REPLACE_WITH_VESPER_KEY`              |
| ... | ...        | ...                                    |
| 47 | Aeryn       | `REPLACE_WITH_AERYN_KEY`               |

## How to obtain a real key

```bash
# On a running node
yggdrasilctl getSelf

# Or generate a new config and extract the PublicKey
yggdrasil -genconf | grep PublicKey
```

Once real keys are available, update this file and add the keys to the `Peers` / `AllowedPublicKeys` sections of the node configs.
