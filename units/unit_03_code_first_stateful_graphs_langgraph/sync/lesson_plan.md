# Synchronous Lesson Plan: Unit 03 - Code-First Stateful Graphs with LangGraph

## Session Logistics
- **Course**: AINT 2050 - Applied AI Agent Architectures
- **Unit**: Unit 03 - Code-First Stateful Graphs with LangGraph
- **Total Duration**: 150 Synchronous Minutes (or Two 75-Minute Sessions)
- **Format**: Active Learning, Graph Topology Demonstration, Paired Coding & Lab Clinic

---

## 150-Minute Unified Schedule Breakdown

### Part 1: Graph Topology Walkthrough & State Reducer Demo (45 min)
- **00-15 min: Concept Review**:
  - The Level 3 paradigm: Moving beyond DAGs to cyclical state graphs.
  - State schemas as single sources of truth.
  - Reviewing the anatomy of `StateGraph`, `TypedDict`, and `add_conditional_edges`.
- **15-30 min: Live Demonstration**:
  - Instructor live-codes a minimal cyclical graph in Python.
  - Demonstrating state evolution across cycles: `Draft -> Review -> Revise`.
  - Showing how conditional edges evaluate state to decide whether to loop or terminate.
- **30-45 min: Checkpointing & Breakpoint Demonstration**:
  - Setting up an in-memory checkpointer (`MemorySaver`).
  - Halting graph execution at an approval gate (`interrupt_before=["publish"]`).
  - Inspecting the checkpointed state and resuming via `thread_id`.

### Part 2: Synchronous Paired Coding Challenge (30 min)
- **45-70 min: In-Class Challenge**:
  - Students pair up and run `sync/inclass_challenges.py`.
  - Challenge: Implement conditional routing edges and recursion limits on a stateful graph engine.
- **70-75 min: Challenge Debrief**:
  - Review student solutions and discuss loop termination conditions.

### Part 3: Guided Applied Laboratory Clinic (60 min)
- **75-80 min: Lab 03 Mission Briefing**:
  - Reviewing `guides/student_lab_guide.md`: Self-Healing Code Debugging & Refactoring Agent.
  - Reviewing the automated test assertions in `guides/lab3_starter.py`.
- **80-135 min: Independent / Paired Engineering**:
  - Students implement the StateGraph nodes (Linter, Patch Generator, Test Runner) and conditional routing edges.
  - Instructor circulates for live debugging assistance.

### Part 4: Code Review, Rubric Alignment & Debrief (15 min)
- **135-145 min: Verification Clinic**:
  - Students run automated unit tests and check against the 100-point rubric in `assessments/lab_rubric.md`.
- **145-150 min: Unit Synthesis**:
  - Reflecting on the journey from Level 1 (conversational assistants) to Level 2 (visual workflows) to Level 3 (stateful code graphs).
