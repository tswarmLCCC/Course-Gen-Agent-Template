"""
AINT 2050: Applied AI Agent Architectures
Unit 3 Lecture Demonstration - Part 1: TypedDict State Schema & Reducer Semantics
Demonstrates state machines with strongly typed schemas and reducer accumulation.
"""

from typing import TypedDict, Annotated, List
import operator

class AgentState(TypedDict):
    task: str
    iteration: int
    tests_passed: bool
    fix_history: Annotated[List[str], operator.add]

def simulate_node_step(state: AgentState, step_note: str) -> dict:
    """A pure node function that takes current state and returns partial state update."""
    return {
        "iteration": state["iteration"] + 1,
        "fix_history": [f"Step {state['iteration'] + 1}: {step_note}"]
    }

if __name__ == "__main__":
    initial_state: AgentState = {
        "task": "Fix NullPointerException in payment_gateway.py",
        "iteration": 0,
        "tests_passed": False,
        "fix_history": ["Initial State: Discovered test failure."]
    }

    print("Initial State:", initial_state)
    
    # Simulate first cycle
    update_1 = simulate_node_step(initial_state, "Added None check before accessing user.email")
    # Reducer application
    current_history = initial_state["fix_history"] + update_1["fix_history"]
    state_step_1 = {**initial_state, **update_1, "fix_history": current_history}
    print("\nState After Step 1:", state_step_1)

    # Simulate second cycle
    update_2 = simulate_node_step(state_step_1, "Verified assertions and re-ran unit suite.")
    current_history = state_step_1["fix_history"] + update_2["fix_history"]
    state_step_2 = {**state_step_1, **update_2, "fix_history": current_history, "tests_passed": True}
    print("\nState After Step 2:", state_step_2)

    assert len(state_step_2["fix_history"]) == 3
    assert state_step_2["tests_passed"] is True
    print("\nState reducer demonstration passed successfully!")
