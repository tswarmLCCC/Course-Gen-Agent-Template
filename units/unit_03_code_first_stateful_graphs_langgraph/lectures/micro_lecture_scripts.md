# Unit 03 Micro-Lecture Scripts: Code-First Stateful Graphs with LangGraph

## Video 3.1: Beyond DAGs: Why Complex Agents Require Cyclical Graphs (10 min)
**Instructor Teleprompter Script**:
"Welcome to Unit 03 of Applied AI Agent Architectures. Throughout Units 01 and 02, we worked with foundation assistants and visual DAG workflows. But as you build more sophisticated autonomous agents, you will run directly into the limitations of Directed Acyclic Graphs.

Consider how humans solve non-trivial problems. When an engineer writes software, they do not write a single draft, submit it to production, and walk away. They run a test suite. When tests fail, they inspect the stack trace, hypothesize a fix, update the code, and run tests again. 

This is an inherently cyclical process. Because DAGs strictly forbid backward edges, forcing an iterative loop into a DAG requires awkward workarounds or unrolling loops. In this video, we break the acyclic barrier and introduce Level 3: Stateful Graphs with LangGraph."

---

## Video 3.2: LangGraph Core: StateGraph, TypedDict & Pure Function Nodes (10 min)
**Instructor Teleprompter Script**:
"At the heart of LangGraph is a powerful paradigm: an agent is a state machine. In LangGraph, we define a centralized state schema using Python's `TypedDict`. This schema is the single source of truth across the entire lifecycle of the agent.

Nodes in LangGraph are discrete, pure Python functions. A node takes the current state as its sole argument and returns a dictionary of keys to update. It does not decide what node runs next. That separation of concerns—separating computation from flow control—is what makes LangGraph architectures so modular and testable.

Furthermore, by annotating schema fields with reducer functions like `operator.add`, LangGraph can automatically append new observations and messages to lists rather than destructively overwriting them."

---

## Video 3.3: Conditional Edges & Dynamic Loop Routing (10 min)
**Instructor Teleprompter Script**:
"In a standard graph, an edge connects Node A unconditionally to Node B. But agents need autonomy—they must decide whether to continue looping, seek human help, or finish.

This is where Conditional Edges come in. In LangGraph, we use `workflow.add_conditional_edges()`. We provide a routing function that inspects the current state. For instance, in our code debugging agent, our routing function checks: did the unit tests pass? If yes, return 'pass'. Have we attempted three fixes already? If yes, return 'max_attempts'. Otherwise, return 'retry'.

The graph engine maps those string keys to destination nodes: routing 'pass' to the END sentinel, 'retry' back to the analyzer, or 'max_attempts' to a human escalation node. This gives you complete, deterministic control over cyclical loops."

---

## Video 3.4: Persistence, Checkpointing & Human-in-the-Loop Gates (10 min)
**Instructor Teleprompter Script**:
"When running an agent in an enterprise environment, two requirements are non-negotiable: persistence across sessions and safety gates for high-risk operations.

LangGraph solves this with Checkpointers. When you compile a graph with `MemorySaver` or `SqliteSaver`, LangGraph automatically saves a complete snapshot of state after every single node execution. By passing a `thread_id` in your execution config, you can pause an agent on Monday and resume it on Tuesday from the exact state snapshot.

Even more importantly, LangGraph allows you to set `interrupt_before` breakpoints. Before executing high-risk actions—such as deploying code or charging a credit card—the graph halts, checkpoints, and waits. A human operator can review the proposed action and approve it before the graph resumes."
