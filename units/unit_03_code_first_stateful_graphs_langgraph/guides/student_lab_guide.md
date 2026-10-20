# Applied Lab 03 Guide: Self-Healing Code Debugging Agent in LangGraph

## Assignment Overview
- **Course**: AINT 2050 - Applied AI Agent Architectures
- **Unit**: Unit 03 - Code-First Stateful Graphs with LangGraph
- **Deliverable**: `lab3_starter.py` (Completed Python script passing 100% assertions)
- **Time Commitment**: 60–90 minutes
- **Grade Weight**: Part of the 40% Applied Labs category

---

## 1. Architectural Mission
In this laboratory, you will build a production-grade cyclical state machine modeling LangGraph's architecture. Your agent will autonomously debug and refactor broken Python code through iterative execution cycles:

```
               +-----------------------+
               |         START         |
               +-----------+-----------+
                           |
                           v
               +-----------------------+
        +----> |   test_runner_node    | <----+
        |      +-----------+-----------+      |
        |                  |                  |
        |                  v                  |
        |      +-----------------------+      |
        |      | Conditional Edge:     |      |
        |      | Pass / Fail / Max?    |      |
        |      +---+-------+-------+---+      |
        |          |       |       |          |
        |     Pass |  Fail |       | Max      |
        |          v       |       v          |
        |       [ END ]    |   [ Escalate ]   |
        |                  v                  |
        |      +-----------------------+      |
        |      |     analyzer_node     |      |
        |      +-----------+-----------+      |
        |                  |                  |
        |                  v                  |
        |      +-----------------------+      |
        +----- |      patch_node       |      |
               +-----------------------+      |
```

---

## 2. Technical Requirements & TODOs

Open [lab3_starter.py](file:///c:/dev/Course-Gen-Agent-Template/units/unit_03_code_first_stateful_graphs_langgraph/guides/lab3_starter.py) and implement the following components:

### Task 1: State Schema & Checkpoint Saver
- Define state dictionary keys: `code`, `test_results`, `error_log`, `fix_history`, `iteration`, `max_iterations`, `status`.
- Implement `InMemoryCheckpointer` that saves state copies keyed by `thread_id` and `step_index`.

### Task 2: Node Implementation
- `run_tests_node(state)`: Executes tests against code, updating `tests_passed` and `error_log`.
- `analyze_error_node(state)`: Diagnoses failure cause and appends to `fix_history`.
- `apply_patch_node(state)`: Applies corrective code patch and increments `iteration`.

### Task 3: Conditional Routing Function (`evaluate_test_results`)
- Inspect `tests_passed` and `iteration`.
- Return `"pass"` if `tests_passed` is `True` -> routes to `END`.
- Return `"escalate"` if `iteration >= max_iterations` -> routes to `escalate_node`.
- Return `"retry"` if tests failed and under limit -> routes to `analyze_error_node`.

---

## 3. Automated Verification & Testing
Execute the starter script directly:
```bash
python units/unit_03_code_first_stateful_graphs_langgraph/guides/lab3_starter.py
```
Or run via pytest:
```bash
pytest units/unit_03_code_first_stateful_graphs_langgraph/guides/lab3_starter.py
```
All 5 test assertions must exit with status `0` before submission.
