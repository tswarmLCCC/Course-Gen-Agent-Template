#!/usr/bin/env python3
"""
Applied Lab 03 Starter: Self-Healing Code Debugging StateGraph
Course: AINT 2050 - Applied AI Agent Architectures
Unit: Unit 03 - Code-First Stateful Graphs with LangGraph

Student Instructions:
Complete the marked sections to build a cyclical state machine modeling LangGraph:
1. InMemoryCheckpointer (save and retrieve state snapshots by thread_id)
2. StateGraph nodes (run_tests_node, analyze_node, patch_node)
3. Conditional edge router (evaluate_test_results)
"""

import copy
from typing import Dict, List, Any, Optional, Callable

START = "__START__"
END = "__END__"


# =====================================================================
# TASK 1: State Checkpointer (MemorySaver Model)
# =====================================================================
class InMemoryCheckpointer:
    """Stores state snapshots keyed by thread_id for persistence and HITL resumption."""
    
    def __init__(self):
        # thread_id -> list of state snapshots
        self.storage: Dict[str, List[Dict[str, Any]]] = {}

    def put(self, thread_id: str, state: Dict[str, Any]):
        if thread_id not in self.storage:
            self.storage[thread_id] = []
        # Store deepcopy to preserve historical snapshot
        self.storage[thread_id].append(copy.deepcopy(state))

    def get_latest(self, thread_id: str) -> Optional[Dict[str, Any]]:
        snapshots = self.storage.get(thread_id, [])
        return copy.deepcopy(snapshots[-1]) if snapshots else None

    def get_history(self, thread_id: str) -> List[Dict[str, Any]]:
        return copy.deepcopy(self.storage.get(thread_id, []))


# =====================================================================
# TASK 2: StateGraph Engine
# =====================================================================
class StateGraph:
    """Pure-Python cyclical state machine modeling LangGraph's architecture."""
    
    def __init__(self):
        self.nodes: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, tuple] = {}
        self.checkpointer = InMemoryCheckpointer()

    def add_node(self, name: str, func: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.nodes[name] = func

    def add_edge(self, source: str, target: str):
        self.edges[source] = target

    def add_conditional_edges(self, source: str, routing_fn: Callable[[Dict[str, Any]], str], path_map: Dict[str, str]):
        self.conditional_edges[source] = (routing_fn, path_map)

    def invoke(self, initial_state: Dict[str, Any], thread_id: str = "default_session", recursion_limit: int = 15) -> Dict[str, Any]:
        state = copy.deepcopy(initial_state)
        current_node = self.edges.get(START)
        steps = 0
        execution_trace = []

        self.checkpointer.put(thread_id, state)

        while current_node and current_node != END:
            steps += 1
            if steps > recursion_limit:
                raise RecursionError(f"Recursion limit ({recursion_limit}) exceeded in StateGraph.")

            execution_trace.append(current_node)
            node_fn = self.nodes.get(current_node)
            if not node_fn:
                raise ValueError(f"Node '{current_node}' not registered.")

            # Execute node and merge update
            update = node_fn(state)
            state.update(update)
            
            # Checkpoint state after step
            self.checkpointer.put(thread_id, state)

            # Determine next node via conditional or static edge
            if current_node in self.conditional_edges:
                routing_fn, path_map = self.conditional_edges[current_node]
                route_key = routing_fn(state)
                current_node = path_map.get(route_key, END)
            else:
                current_node = self.edges.get(current_node, END)

        state["_trace"] = execution_trace
        state["_steps"] = steps
        return state


# =====================================================================
# TASK 3: Self-Healing Code Debugging Nodes & Routing
# =====================================================================

def run_tests_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Runs tests against current code string and records outcomes."""
    code = state.get("code", "")
    iteration = state.get("iteration", 0)

    # Simulated test evaluation:
    # Requires correct function definition of 'calculate_discount(price, tier)'
    if "def calculate_discount" in code and "tier == 'VIP'" in code and "price * 0.8" in code:
        return {
            "tests_passed": True,
            "error_log": "",
            "status": "PASSED"
        }
    else:
        error_msg = "AssertionError: calculate_discount(100, 'VIP') returned incorrect discount"
        return {
            "tests_passed": False,
            "error_log": error_msg,
            "status": "TESTS_FAILED"
        }


def analyze_error_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Examines stack trace and generates diagnostic critique."""
    error = state.get("error_log", "")
    history = list(state.get("fix_history", []))
    
    diagnostic = f"Diagnosed failure: {error}. Root cause: VIP discount logic missing 20% rate."
    history.append(diagnostic)
    
    return {
        "diagnostic": diagnostic,
        "fix_history": history
    }


def patch_code_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Applies code patch and increments iteration counter."""
    iteration = state.get("iteration", 0) + 1
    
    # In iteration 1, introduce correct VIP discount implementation
    patched_code = """
def calculate_discount(price, tier):
    if tier == 'VIP':
        return price * 0.8
    return price
"""
    return {
        "code": patched_code.strip(),
        "iteration": iteration
    }


def escalate_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback node when max iterations reached."""
    return {
        "status": "ESCALATED_TO_HUMAN",
        "human_ticket": "BUG-8821"
    }


def evaluate_test_results(state: Dict[str, Any]) -> str:
    """Conditional edge routing logic."""
    if state.get("tests_passed") is True:
        return "pass"
    elif state.get("iteration", 0) >= state.get("max_iterations", 3):
        return "max_attempts"
    else:
        return "retry"


# =====================================================================
# Automated Unit Test Suite
# =====================================================================
def run_tests():
    print("Executing Applied Lab 03 StateGraph Unit Tests...")

    # Build Graph
    graph = StateGraph()
    graph.add_node("test_runner", run_tests_node)
    graph.add_node("analyzer", analyze_error_node)
    graph.add_node("patcher", patch_code_node)
    graph.add_node("escalate", escalate_node)

    graph.add_edge(START, "test_runner")
    graph.add_conditional_edges("test_runner", evaluate_test_results, {
        "pass": END,
        "retry": "analyzer",
        "max_attempts": "escalate"
    })
    graph.add_edge("analyzer", "patcher")
    graph.add_edge("patcher", "test_runner")
    graph.add_edge("escalate", END)

    # Initial Broken Code
    initial_broken_code = """
def calculate_discount(price, tier):
    return price
"""

    initial_state = {
        "code": initial_broken_code.strip(),
        "iteration": 0,
        "max_iterations": 3,
        "tests_passed": False,
        "fix_history": [],
        "status": "INITIAL"
    }

    session_id = "test_thread_42"
    final_state = graph.invoke(initial_state, thread_id=session_id)

    # Test 1: Self-healing resolution
    assert final_state["tests_passed"] is True
    assert final_state["status"] == "PASSED"
    print("  [+] Test 1: Self-healing cycle resolved tests successfully.")

    # Test 2: Execution trace shows cyclical loop
    expected_trace = ["test_runner", "analyzer", "patcher", "test_runner"]
    assert final_state["_trace"] == expected_trace
    print(f"  [+] Test 2: Cyclical execution trace verified: {' -> '.join(final_state['_trace'])}.")

    # Test 3: Iteration counter incremented correctly
    assert final_state["iteration"] == 1
    assert len(final_state["fix_history"]) == 1
    print("  [+] Test 3: Iteration and fix history state updated correctly.")

    # Test 4: Checkpointer historical snapshots
    snapshots = graph.checkpointer.get_history(session_id)
    assert len(snapshots) >= 4
    assert snapshots[0]["tests_passed"] is False
    assert snapshots[-1]["tests_passed"] is True
    print(f"  [+] Test 4: Checkpointer verified {len(snapshots)} state snapshots in thread.")

    # Test 5: Max iterations escalation branch
    stubborn_state = {
        "code": "broken code that never passes",
        "iteration": 3,
        "max_iterations": 3,
        "tests_passed": False,
        "fix_history": [],
        "status": "INITIAL"
    }
    escalated_res = graph.invoke(stubborn_state, thread_id="thread_escalate")
    assert escalated_res["status"] == "ESCALATED_TO_HUMAN"
    assert "escalate" in escalated_res["_trace"]
    print("  [+] Test 5: Escalation conditional edge verified.")

    print("\nAll 5 Applied Lab 03 tests PASSED successfully!")


if __name__ == "__main__":
    run_tests()
