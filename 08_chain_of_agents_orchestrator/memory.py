from typing import Dict, Any, List
from datetime import datetime

class MultiAgentMemory:
    """Implementa memoria de trabajo (scratchpad) y memoria episódica persistente."""
    def __init__(self):
        self.working_memory: Dict[str, Any] = {}
        self.episodic_memory: List[Dict[str, Any]] = []

    def update_working_memory(self, key: str, value: Any):
        self.working_memory[key] = value

    def log_episode(self, sender: str, payload: Any, status: str = "success"):
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "sender": sender,
            "status": status,
            "payload": payload
        }
        self.episodic_memory.append(record)
        self.working_memory[sender] = payload