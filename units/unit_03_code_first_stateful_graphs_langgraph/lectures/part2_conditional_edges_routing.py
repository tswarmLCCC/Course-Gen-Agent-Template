"""
AINT 2050: Applied AI Agent Architectures
Unit 3 Lecture Demonstration - Part 2: Conditional Edges & Cyclical Loop Routing
Demonstrates conditional routing logic in LangGraph architectures.
"""

from typing import Dict, Any, Literal

def route_after_test_execution(state: Dict[str, Any], max_attempts: int = 3) -> Literal["pass", "retry", "escalate"]:
    """
    Conditional routing function inspecting runtime state to decide graph destination.
    """
    if state.get("tests_passed", False):
        return "pass"
    if state.get("iteration", 0) >= max_attempts:
        return "escalate"
    return "retry"

if __name__ == "__main__":
    print("--- Demonstrating Conditional Routing Scenarios ---")

    # Scenario 1: Tests pass on first attempt
    state_passing = {"iteration": 1, "tests_passed": True}
    route_1 = route_after_test_execution(state_passing)
    print(f"Scenario 1 Route: {route_1} (Expected: pass)")
    assert route_1 == "pass"

    # Scenario 2: Tests fail on attempt 1
    state_failing = {"iteration": 1, "tests_passed": False}
    route_2 = route_after_test_execution(state_failing)
    print(f"Scenario 2 Route: {route_2} (Expected: retry)")
    assert route_2 == "retry"

    # Scenario 3: Tests fail and reached max attempts
    state_exhausted = {"iteration": 3, "tests_passed": False}
    route_3 = route_after_test_execution(state_exhausted)
    print(f"Scenario 3 Route: {route_3} (Expected: escalate)")
    assert route_3 == "escalate"

    print("All conditional edge routing tests passed successfully!")
