"""
AINT 2050: Applied AI Agent Architectures
Unit 3 Lecture Demonstration - Part 3: Persistent Checkpointing & Human-in-the-Loop (HITL)
Demonstrates session state snapshotting and human review breakpoints.
"""

from typing import Dict, Any

class MockCheckpointer:
    def __init__(self):
        # Maps thread_id -> list of state snapshots
        self.storage: Dict[str, list] = {}

    def save_checkpoint(self, thread_id: str, state: dict):
        if thread_id not in self.storage:
            self.storage[thread_id] = []
        # Deep copy simulated
        snapshot = dict(state)
        self.storage[thread_id].append(snapshot)
        print(f"  [CHECKPOINT] Saved state snapshot for thread '{thread_id}': step {len(self.storage[thread_id])}")

    def load_latest(self, thread_id: str) -> dict:
        snapshots = self.storage.get(thread_id, [])
        if not snapshots:
            raise KeyError(f"No checkpoint found for thread {thread_id}")
        return snapshots[-1]

def execute_high_risk_node_with_hitl(state: dict, checkpointer: MockCheckpointer, thread_id: str, approved: bool) -> dict:
    """Simulates an interrupt_before breakpoint requiring human authorization."""
    print("\n--- Evaluating High-Risk Node (Database Mutation) ---")
    checkpointer.save_checkpoint(thread_id, state)
    print("  [HITL GATE] Pausing graph execution. Awaiting human operator approval...")

    if not approved:
        print("  [HITL GATE] Action REJECTED by human operator. Aborting transaction.")
        return {**state, "status": "rejected", "aborted": True}

    print("  [HITL GATE] Action APPROVED by human operator. Resuming graph execution.")
    return {**state, "status": "executed", "aborted": False}

if __name__ == "__main__":
    checkpointer = MockCheckpointer()
    session_thread = "user_session_44102"
    
    current_state = {
        "operation": "DROP TABLE legacy_user_tokens;",
        "author": "agent_auto_refactor",
        "iteration": 2
    }

    # Test rejection
    result_rejected = execute_high_risk_node_with_hitl(current_state, checkpointer, session_thread, approved=False)
    assert result_rejected["aborted"] is True

    # Test approval
    result_approved = execute_high_risk_node_with_hitl(current_state, checkpointer, session_thread, approved=True)
    assert result_approved["status"] == "executed"

    # Verify checkpointer persistence
    latest = checkpointer.load_latest(session_thread)
    assert latest["iteration"] == 2
    print("\nHITL and checkpointer simulation completed successfully!")
