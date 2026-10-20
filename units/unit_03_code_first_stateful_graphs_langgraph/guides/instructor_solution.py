#!/usr/bin/env python3
"""
Applied Lab 03 Instructor Reference Solution: Self-Healing Code Debugging StateGraph
Course: AINT 2050 - Applied AI Agent Architectures
Unit: Unit 03 - Code-First Stateful Graphs with LangGraph
"""

from lab3_starter import (
    InMemoryCheckpointer,
    StateGraph,
    run_tests_node,
    analyze_error_node,
    patch_code_node,
    escalate_node,
    evaluate_test_results,
    run_tests
)

if __name__ == "__main__":
    print("Running Instructor Solution Verification for Lab 03:")
    run_tests()
