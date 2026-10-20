# Applied Lab 3 Assessment Rubric: LangGraph StateMachine & Checkpointing

## Overview
- **Course**: AINT 2050 - Applied AI Agent Architectures
- **Unit**: Unit 03 - Code-First Stateful Graphs with LangGraph
- **Assignment**: Lab 03 - Self-Healing Code Debugging StateGraph
- **Total Points**: 100
- **Grading Weight**: Included in the 40% Applied Labs category

---

## Analytic Grading Matrix

| Performance Dimension | Exemplary (90-100%) | Proficient (80-89%) | Developing (70-79%) | Inadequate (0-69%) | Score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. State Schema & Checkpointer Design** (25 pts) | State schema is strongly typed; correctly stores historical state snapshots in an in-memory or SQLite checkpointer indexed by `thread_id` without in-place mutation side-effects. (23-25 pts) | Checkpointer stores states and supports thread lookup; minor issues with shallow vs deep copying of state dictionaries. (20-22 pts) | Checkpointer only stores latest state, losing the historical trace; or fails on invalid thread IDs. (17-19 pts) | Checkpointing not implemented or state is mutated globally across threads. (0-16 pts) | /25 |
| **2. Cyclical Graph Execution & Node Functions** (25 pts) | Nodes implemented as pure functions taking state and returning partial updates. Execution cleanly cycles between testing, analyzing, and patching until resolution. (23-25 pts) | Graph executes cyclical loop successfully; minor redundancy in state dictionary returns. (20-22 pts) | Nodes mutate external state directly rather than returning updates, causing race conditions in multi-step cycles. (17-19 pts) | Graph cannot loop back (functions as a linear DAG) or node execution raises unhandled exceptions. (0-16 pts) | /25 |
| **3. Conditional Routing & Recursion Limits** (25 pts) | Conditional edge cleanly routes to pass (`END`), retry (`analyzer`), or escalation (`escalate`). Enforces deterministic recursion limits to prevent runaway execution. (23-25 pts) | Conditional edge routes correctly for pass and retry; escalation edge is fragile or off-by-one on loop limits. (20-22 pts) | Routing functions return invalid string keys that do not map to defined nodes, or recursion limit is missing. (17-19 pts) | Agent enters infinite loops or crashes during conditional branch evaluation. (0-16 pts) | /25 |
| **4. Code Quality & Test Verification** (25 pts) | Code strictly adheres to PEP 8, uses clear type annotations, includes docstrings, and passes 100% of automated unit test assertions. (23-25 pts) | Code is well-structured and passes all automated test assertions with minor formatting inconsistencies. (20-22 pts) | Code passes 4 of 5 automated test cases; contains minor syntax or typing warnings. (17-19 pts) | Code fails multiple automated test assertions or contains syntax errors. (0-16 pts) | /25 |

---

## Grading Scale
- **93.0% - 100.0%**: Grade A (Mastery of cyclical state machines and checkpointing)
- **90.0% - 92.9%**: Grade A-
- **87.0% - 89.9%**: Grade B+
- **83.0% - 86.9%**: Grade B (Proficient implementation)
- **80.0% - 82.9%**: Grade B-
- **77.0% - 79.9%**: Grade C+
- **70.0% - 76.9%**: Grade C (Baseline functionality)
- **Below 70.0%**: Grade F (Non-functional engine or missing core components)
