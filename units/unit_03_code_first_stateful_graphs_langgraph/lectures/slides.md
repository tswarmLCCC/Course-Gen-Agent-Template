# Unit 03 Lecture Slides Outline: Code-First Stateful Graphs with LangGraph

## Slide 1: Split-Hero Title
- **Title**: AINT 2050: Applied AI Agent Architectures
- **Subtitle**: Unit 03: Code-First Stateful Graphs with LangGraph
- **Presenter**: Applied AI Engineering Faculty
- **Notes**: Welcome to Unit 03. Today we transition into Level 3 of the Agent Spectrum: Code-First Stateful Graph Architectures using LangGraph.

## Slide 2: Section Divider
- **Category**: Section 1
- **Title**: Why DAGs Fail for Advanced Agents
- **Subtitle**: Breaking the acyclic barrier to unlock iterative reasoning
- **Notes**: We explore why Directed Acyclic Graphs cannot represent human-like trial, error, testing, and self-correction.

## Slide 3: Two-Column Comparison
- **Title**: Visual DAGs vs. LangGraph State Machines
- **Column 1 Header**: Visual DAGs (Level 2)
  - Data flows strictly forward from source to sink.
  - Loops must be unrolled into repetitive nodes.
  - State is passed as ad-hoc JSON payloads.
  - Great for linear SaaS integrations and webhooks.
- **Column 2 Header**: LangGraph State Machines (Level 3)
  - Cyclical edges allow continuous feedback loops.
  - Strongly-typed `TypedDict` schema acts as single source of truth.
  - Reducer functions define precise mutation rules.
  - Engineered for complex reasoning, self-healing code, and reflection.
- **Notes**: Compare the structural limitations of DAGs with the flexibility of cyclical state machines.

## Slide 4: Process Flow Architecture
- **Title**: The Self-Healing Code Refactoring Cycle
- **Step 1**: Test Runner Node executes unit tests against candidate code.
- **Step 2**: Conditional Edge checks tests_passed status.
- **Step 3**: If tests fail, Analyzer Node diagnoses the root failure cause.
- **Step 4**: Patch Node applies targeted code fix and increments iteration count.
- **Step 5**: If tests pass or max attempts reached, graph safely terminates at END.
- **Notes**: Detail the 4-step cyclical feedback loop students implement in Lab 03.

## Slide 5: Monospace Code Syntax Container
- **Title**: LangGraph State Schema with Reducers
- **Code Block**:
```python
from typing import TypedDict, Annotated, List
import operator

class AgentState(TypedDict):
    code: str
    iteration: int
    tests_passed: bool
    fix_history: Annotated[List[str], operator.add]
```
- **Notes**: Explain how `Annotated` with `operator.add` prevents destructive overwriting of historical notes during cycles.

## Slide 6: Two-Column Comparison
- **Title**: Persistence & Human-in-the-Loop (HITL)
- **Column 1 Header**: Checkpointing Architecture
  - `MemorySaver` / `SqliteSaver` snapshots state after every node step.
  - Keyed by `thread_id` to isolate independent user sessions.
  - Supports time-travel debugging and state rollbacks.
- **Column 2 Header**: Human-in-the-Loop Breakpoints
  - `interrupt_before=["high_risk_node"]` pauses execution safely.
  - Human reviews state before destructive operations.
  - Session resumes cleanly using `app.invoke(None, config)`.
- **Notes**: Conclude with production governance and safety patterns.
