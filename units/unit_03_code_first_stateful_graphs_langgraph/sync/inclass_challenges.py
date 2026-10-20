#!/usr/bin/env python3
"""
Unit 03 In-Class Challenge: Stateful Cyclical Graph Engine
AINT 2050 - Applied AI Agent Architectures

In this challenge, students simulate LangGraph's core primitives using pure Python:
1. Define a state dictionary schema.
2. Implement graph nodes as pure functions mutating state.
3. Add normal and conditional edges.
4. Enforce recursion limits to prevent runaway cycles.
"""

from typing import Dict, Any, Callable, List, Optional

START = "__START__"
END = "__END__"


class StateGraph:
    """A lightweight pure-Python simulation of LangGraph's StateGraph."""
    
    def __init__(self):
        self.nodes: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, tuple] = {}  # source -> (routing_fn, path_map)

    def add_node(self, name: str, func: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.nodes[name] = func

    def add_edge(self, source: str, target: str):
        self.edges[source] = target

    def add_conditional_edges(self, source: str, routing_fn: Callable[[Dict[str, Any]], str], path_map: Dict[str, str]):
        self.conditional_edges[source] = (routing_fn, path_map)

    def compile(self, recursion_limit: int = 10):
        return CompiledGraph(self, recursion_limit)


class CompiledGraph:
    def __init__(self, graph: StateGraph, recursion_limit: int):
        self.graph = graph
        self.recursion_limit = recursion_limit

    def invoke(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        state = dict(initial_state)
        current_node = self.graph.edges.get(START)
        steps = 0
        execution_trace = []

        while current_node and current_node != END:
            steps += 1
            if steps > self.recursion_limit:
                raise RecursionError(f"Graph recursion limit ({self.recursion_limit}) exceeded.")

            execution_trace.append(current_node)
            node_fn = self.graph.nodes.get(current_node)
            if not node_fn:
                raise ValueError(f"Node '{current_node}' not found.")

            # Execute node function and merge partial state
            update = node_fn(state)
            state.update(update)

            # Determine next node via conditional edge or normal edge
            if current_node in self.graph.conditional_edges:
                routing_fn, path_map = self.graph.conditional_edges[current_node]
                route_key = routing_fn(state)
                current_node = path_map.get(route_key, END)
            else:
                current_node = self.graph.edges.get(current_node, END)

        state["_trace"] = execution_trace
        state["_total_steps"] = steps
        return state


# =====================================================================
# Synchronous In-Class Challenge Verification
# =====================================================================
def run_challenge():
    print("Testing StateGraph Cyclical Engine Simulation...")

    # Define Node Functions
    def draft_node(state: Dict[str, Any]) -> Dict[str, Any]:
        attempts = state.get("attempts", 0) + 1
        return {
            "attempts": attempts,
            "draft": f"Code version {attempts}",
            "quality_score": min(100, state.get("quality_score", 40) + 25)
        }

    def review_node(state: Dict[str, Any]) -> Dict[str, Any]:
        score = state.get("quality_score", 0)
        passed = score >= 85
        return {"review_passed": passed}

    # Conditional Routing Function
    def should_continue(state: Dict[str, Any]) -> str:
        if state.get("review_passed"):
            return "pass"
        elif state.get("attempts", 0) >= 4:
            return "max_reached"
        else:
            return "retry"

    # Assemble Graph
    builder = StateGraph()
    builder.add_node("drafter", draft_node)
    builder.add_node("reviewer", review_node)

    builder.add_edge(START, "drafter")
    builder.add_edge("drafter", "reviewer")
    builder.add_conditional_edges("reviewer", should_continue, {
        "pass": END,
        "retry": "drafter",
        "max_reached": END
    })

    app = builder.compile(recursion_limit=15)
    result = app.invoke({"initial_input": "Optimize sorting algorithm", "attempts": 0, "quality_score": 40})

    print(f"Final State: attempts={result['attempts']}, score={result['quality_score']}, passed={result['review_passed']}")
    print(f"Execution Trace: {' -> '.join(result['_trace'])}")

    # Assertions
    assert result["review_passed"] is True
    assert result["quality_score"] >= 85
    assert result["attempts"] == 2  # 40 + 25 = 65 (fail), 65 + 25 = 90 (pass)
    assert result["_total_steps"] == 4  # drafter -> reviewer -> drafter -> reviewer -> END
    print("\nAll Unit 03 in-class challenge assertions PASSED successfully!")


if __name__ == "__main__":
    run_challenge()
