#!/usr/bin/env python3
"""
Nexus Agentenschwarm – Orchestrator + spezialisierte Agenten
Lumina / Nexus Swarm Prototype
"""
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum

class MessageType(Enum):
    TASK = "task"
    RESULT = "result"
    QUERY = "query"
    UPDATE = "update"
    CRITIQUE = "critique"

@dataclass
class Message:
    sender: str
    receiver: str
    type: MessageType
    content: Any
    timestamp: datetime = field(default_factory=datetime.now)
    conversation_id: str = ""

@dataclass
class MemoryEntry:
    key: str
    value: Any
    source: str
    timestamp: datetime = field(default_factory=datetime.now)
    confidence: float = 1.0

class SharedMemory:
    def __init__(self):
        self._store: Dict[str, MemoryEntry] = {}
        self._history: List[MemoryEntry] = []

    async def write(self, key: str, value: Any, source: str, confidence: float = 1.0):
        entry = MemoryEntry(key=key, value=value, source=source, confidence=confidence)
        self._store[key] = entry
        self._history.append(entry)
        print(f"Memory: {source} -> '{key}' (confidence={confidence})")

    async def read(self, key: str) -> Any:
        entry = self._store.get(key)
        return entry.value if entry else None

    async def get_all(self) -> Dict:
        return {k: v.value for k, v in self._store.items()}

class BaseAgent:
    def __init__(self, name: str, role: str, memory: SharedMemory):
        self.name = name
        self.role = role
        self.memory = memory
        self.message_bus = None

    async def send_message(self, receiver: str, msg_type: MessageType, content: Any):
        print(f"{self.name} -> {receiver}: {msg_type.value}")
        if self.message_bus and hasattr(self.message_bus, "receive"):
            await self.message_bus.receive(Message(self.name, receiver, msg_type, content))

    async def execute(self, task: str, context: Dict = None) -> str:
        print(f"{self.name} ({self.role}) führt aus: {task[:70]}...")
        await asyncio.sleep(0.25)
        result = f"{self.name} hat '{task[:40]}...' bearbeitet."
        await self.memory.write(f"result_{self.name}", result, self.name)
        return result

class PerceptionAgent(BaseAgent):
    async def perceive(self, input_data: str) -> str:
        print(f"Perception analysiert Eingabe...")
        await self.memory.write("perception", input_data, self.name, 0.95)
        return f"Wahrnehmung: {input_data[:60]}"

class PlannerAgent(BaseAgent):
    async def create_plan(self) -> str:
        print(f"Planner erstellt Strategie...")
        plan = "1. Analysieren 2. Ausführen 3. Kritisieren 4. Zusammenfassen"
        await self.memory.write("plan", plan, self.name)
        return plan

class ExecutorAgent(BaseAgent):
    async def execute_task(self) -> str:
        print(f"Executor arbeitet...")
        result = "Ausführung erfolgreich abgeschlossen."
        await self.memory.write("execution", result, self.name)
        return result

class CriticAgent(BaseAgent):
    async def critique(self) -> str:
        print(f"Critic bewertet Ergebnis...")
        critique = "Ergebnis solide. Verbesserungspotenzial bei Detailtiefe."
        await self.memory.write("critique", critique, self.name, 0.9)
        return critique

class MemoryAgent(BaseAgent):
    async def summarize(self) -> str:
        print(f"MemoryAgent fasst zusammen...")
        all_mem = await self.memory.get_all()
        summary = f"Zusammenfassung aus {len(all_mem)} Einträgen."
        await self.memory.write("summary", summary, self.name)
        return summary

class Orchestrator(BaseAgent):
    def __init__(self, memory: SharedMemory):
        super().__init__("Orchestrator", "Dirigent", memory)
        self.agents: Dict[str, BaseAgent] = {}

    def register_agent(self, agent: BaseAgent):
        self.agents[agent.name] = agent
        agent.message_bus = self
        print(f"Agent registriert: {agent.name} ({agent.role})")

    async def receive(self, msg: Message):
        print(f"Orchestrator empfängt von {msg.sender}: {msg.type.value}")

    async def run(self, user_task: str):
        print(f"\nNexus Orchestrator startet Aufgabe: {user_task}\n")
        await self.memory.write("current_input", user_task, "User", 1.0)

        if "Perception" in self.agents:
            await self.agents["Perception"].perceive(user_task)
        if "Planner" in self.agents:
            await self.agents["Planner"].create_plan()
        if "Executor" in self.agents:
            await self.agents["Executor"].execute_task()
        if "Critic" in self.agents:
            await self.agents["Critic"].critique()
        if "Memory" in self.agents:
            await self.agents["Memory"].summarize()

        print("\nAgentenschwarm-Einsatz erfolgreich abgeschlossen!\n")
        return await self.memory.get_all()

async def main():
    print("=" * 60)
    print("  NEXUS AGENTENSCHWARM – Orchestrator online")
    print("=" * 60)

    memory = SharedMemory()
    swarm = Orchestrator(memory)

    swarm.register_agent(PerceptionAgent("Perception", "Wahrnehmung", memory))
    swarm.register_agent(PlannerAgent("Planner", "Planung", memory))
    swarm.register_agent(ExecutorAgent("Executor", "Ausführung", memory))
    swarm.register_agent(CriticAgent("Critic", "Kritiker", memory))
    swarm.register_agent(MemoryAgent("Memory", "Gedächtnis", memory))

    result = await swarm.run("Starte Nexus, verbinde Mesh und Agentenschwarm, Statusbericht für Lumina")
    
    print("\nFinaler Memory-Status:")
    for k, v in result.items():
        print(f"  • {k}: {v}")
    print("\n" + "=" * 60)
    print("  Nexus Orchestrator + Agentenschwarm bereit")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
