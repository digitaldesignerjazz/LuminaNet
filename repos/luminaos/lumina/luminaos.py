#!/usr/bin/env python3
"""
LuminaOS – Agentic Operating System Prototype
Nexus Layer: Orchestrator + Agentenschwarm + NetBird Mesh Awareness
"""
import asyncio
import subprocess
from datetime import datetime


def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=8)
        return r.stdout.strip() or r.stderr.strip()
    except Exception as e:
        return str(e)


def _first_line_matching(text, needles):
    for line in text.splitlines():
        low = line.lower()
        if any(n.lower() in low for n in needles):
            return line.strip()
    return ""


async def mesh_status():
    print("\nMESH LAYER")
    print("-" * 40)
    if not run_cmd("command -v netbird"):
        print("  NetBird: nicht installiert")
        print("  Install: curl -fsSL https://pkgs.netbird.io/install.sh | sh")
        return

    status = run_cmd("netbird status")
    connected = "connected" in status.lower() and "disconnected" not in status.splitlines()[0].lower() if status else False
    if "Daemon status" in status or "Management" in status or "NetBird IP" in status:
        daemon = _first_line_matching(status, ["Daemon status", "Status"]) or ("Connected" if "Connected" in status else "unknown")
        mgmt = _first_line_matching(status, ["Management"]) or "—"
        ip = _first_line_matching(status, ["NetBird IP", "IP Address", "IP:"]) or "—"
        iface = _first_line_matching(status, ["Interface", "WG interface"]) or "wt0"
        peers = _first_line_matching(status, ["Peers", "Peers count"]) or "Peers: ?"
        print(f"  NetBird: {daemon}")
        print(f"    {mgmt}")
        print(f"    {ip}")
        print(f"    {iface}")
        print(f"    {peers}")
    else:
        print("  NetBird: offline / kein Status")
        if status:
            print(f"    {status.splitlines()[0][:80]}")

    wt0 = run_cmd("ip -4 addr show wt0 2>/dev/null | awk '/inet / {print $2}'")
    print(f"  Interface wt0: {wt0 or 'nicht vorhanden'}")
    if connected or "Connected" in status:
        print("  Overlay: bereit")


async def swarm_status():
    print("\nAGENTENSCHWARM")
    print("-" * 40)
    print("  Orchestrator: bereit")
    print("  Agents: Perception, Planner, Executor, Critic, Memory")
    import sys
    sys.path.insert(0, "nexus")
    try:
        from agent_swarm import SharedMemory, Orchestrator, PerceptionAgent, PlannerAgent, ExecutorAgent, CriticAgent, MemoryAgent
        memory = SharedMemory()
        swarm = Orchestrator(memory)
        for cls, name, role in [
            (PerceptionAgent, "Perception", "Wahrnehmung"),
            (PlannerAgent, "Planner", "Planung"),
            (ExecutorAgent, "Executor", "Ausführung"),
            (CriticAgent, "Critic", "Kritiker"),
            (MemoryAgent, "Memory", "Gedächtnis"),
        ]:
            swarm.register_agent(cls(name, role, memory))
        await swarm.run("LuminaOS Boot – NetBird Mesh + Swarm Status erfassen und Nexus bereit melden")
    except Exception as e:
        print(f"  Swarm Fehler: {e}")


async def main():
    print("=" * 60)
    print("  LUMINA OS  –  Agentic Operating System")
    print(f"  Boot: {datetime.now().isoformat()}")
    print("=" * 60)
    await mesh_status()
    await swarm_status()
    print("\n" + "=" * 60)
    print("  LUMINA OS online – Nexus Stack bereit (NetBird)")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
