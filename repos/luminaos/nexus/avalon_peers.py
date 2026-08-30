#!/usr/bin/env python3
"""
Avalon Peer Connection Layer for LuminaOS / Nexus
Connects the 47 Avalon peers to the Agentenschwarm.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class PeerStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    SYNCING = "syncing"

@dataclass
class AvalonPeer:
    id: int
    name: str
    status: PeerStatus = PeerStatus.ONLINE
    public_key: Optional[str] = None
    quadrant: Optional[str] = None

AVALON_PEERS: List[AvalonPeer] = [
    AvalonPeer(1, "Elias"),
    AvalonPeer(2, "Mira"),
    AvalonPeer(3, "Kael"),
    AvalonPeer(4, "Liora"),
    AvalonPeer(5, "Thorne"),
    AvalonPeer(6, "Selene"),
    AvalonPeer(7, "Draven"),
    AvalonPeer(8, "Nyra"),
    AvalonPeer(9, "Orion"),
    AvalonPeer(10, "Vesper"),
    AvalonPeer(11, "Cassian"),
    AvalonPeer(12, "Elowen"),
    AvalonPeer(13, "Ragnar"),
    AvalonPeer(14, "Sylas"),
    AvalonPeer(15, "Freya"),
    AvalonPeer(16, "Azrael"),
    AvalonPeer(17, "Isolde"),
    AvalonPeer(18, "Lucian"),
    AvalonPeer(19, "Seraphine"),
    AvalonPeer(20, "Darius"),
    AvalonPeer(21, "Amara"),
    AvalonPeer(22, "Valerian"),
    AvalonPeer(23, "Lyra"),
    AvalonPeer(24, "Korvin"),
    AvalonPeer(25, "Astrid"),
    AvalonPeer(26, "Malachi"),
    AvalonPeer(27, "Ravenna"),
    AvalonPeer(28, "Theron"),
    AvalonPeer(29, "Calista"),
    AvalonPeer(30, "Bael"),
    AvalonPeer(31, "Niamh"),
    AvalonPeer(32, "Zephyr"),
    AvalonPeer(33, "Morrigan"),
    AvalonPeer(34, "Eldric"),
    AvalonPeer(35, "Aveline"),
    AvalonPeer(36, "Soren"),
    AvalonPeer(37, "Thalia"),
    AvalonPeer(38, "Garrick"),
    AvalonPeer(39, "Elara"),
    AvalonPeer(40, "Ronan"),
    AvalonPeer(41, "Brienne"),
    AvalonPeer(42, "Kairos"),
    AvalonPeer(43, "Vanya"),
    AvalonPeer(44, "Leander"),
    AvalonPeer(45, "Seraphina"),
    AvalonPeer(46, "Drystan"),
    AvalonPeer(47, "Aeryn"),
]

HANNOVER_NODES = {
    "nord": "Avalon-Hannover-Nord",
    "sued": "Avalon-Hannover-Sued",
    "west": "Avalon-Hannover-West",
    "ost":  "Avalon-Hannover-Ost",
}

def get_peer_by_name(name: str) -> Optional[AvalonPeer]:
    for peer in AVALON_PEERS:
        if peer.name.lower() == name.lower():
            return peer
    return None

def get_online_peers() -> List[AvalonPeer]:
    return [p for p in AVALON_PEERS if p.status == PeerStatus.ONLINE]

def peer_status_report() -> str:
    online = len(get_online_peers())
    total = len(AVALON_PEERS)
    lines = [
        f"Avalon Peer Connection Report",
        f"{'='*40}",
        f"Total Peers : {total}",
        f"Online      : {online}",
        f"Status      : {'FULLY CONNECTED' if online == total else 'PARTIAL'}",
        f"{'='*40}",
    ]
    for peer in AVALON_PEERS:
        lines.append(f"  {peer.id:02d}. {peer.name:<12} [{peer.status.value}]")
    return "\n".join(lines)

if __name__ == "__main__":
    print(peer_status_report())
    print("\nHannover Nodes:")
    for q, name in HANNOVER_NODES.items():
        print(f"  {q.upper():<6} -> {name}")
