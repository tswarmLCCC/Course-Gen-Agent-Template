"""
AINT 2050: Applied AI Agent Architectures
Unit 1 Lecture Demonstration - Part 3: Working Memory, Scratchpads & Context Management
"""

from typing import List, Dict, Any


class AgentMemoryContext:
    """Manages short-term scratchpad and long-term key-value state."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.scratchpad: List[Dict[str, str]] = []
        self.persistent_facts: Dict[str, Any] = {}

    def log_thought(self, step: int, thought: str):
        self.scratchpad.append({"type": "thought", "step": step, "content": thought})

    def log_action(self, step: int, tool: str, args: str):
        self.scratchpad.append({"type": "action", "step": step, "tool": tool, "args": args})

    def log_observation(self, step: int, result: str):
        self.scratchpad.append({"type": "observation", "step": step, "content": result})

    def store_fact(self, key: str, value: Any):
        self.persistent_facts[key] = value

    def render_prompt_history(self) -> str:
        lines = []
        for entry in self.scratchpad:
            if entry["type"] == "thought":
                lines.append(f"Thought {entry['step']}: {entry['content']}")
            elif entry["type"] == "action":
                lines.append(f"Action {entry['step']}: {entry['tool']}({entry['args']})")
            elif entry["type"] == "observation":
                lines.append(f"Observation {entry['step']}: {entry['content']}")
        return "\n".join(lines)


if __name__ == "__main__":
    mem = AgentMemoryContext("session_001")
    mem.log_thought(1, "Customer requires refund authorization.")
    mem.log_action(1, "query_policy", "refunds_under_50")
    mem.log_observation(1, "Policy permits automatic refund up to $50.00 for active accounts.")
    mem.store_fact("max_auto_refund", 50.0)

    print("Rendered ReAct Scratchpad Prompt:")
    print("-" * 50)
    print(mem.render_prompt_history())
    print("-" * 50)
    print("Persistent Memory Facts:", mem.persistent_facts)
