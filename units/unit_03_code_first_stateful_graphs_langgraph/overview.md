# Unit 03: Code-First Stateful Graphs with LangGraph

<div class="dp-header dp-basic-bar" style="background: #1e3a8a; color: #ffffff; padding: 1.5rem; border-radius: 6px; margin-bottom: 1.5rem;">
  <h1 style="margin: 0; color: #ffffff; font-size: 1.8rem;">Unit 03: Code-First Stateful Graphs with LangGraph</h1>
  <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Level 3 Agent Architectures: StateGraph, Cyclical Loops, Persistence & Human-in-the-Loop</p>
</div>

---

## 1. Executive Summary & Pedagogical Context
In Unit 01, we studied foundation assistants and linear ReAct loops. In Unit 02, we explored visual workflow automations in n8n and Langflow. While visual DAGs are outstanding for event ingestion and SaaS connectors, they struggle when tasks demand complex cyclical reasoning, non-linear state rollbacks, and programmatic branching.

**Unit 03 introduces Level 3 of the Agent Spectrum: Code-First Stateful Graphs with LangGraph.** Students examine how modern software systems represent agentic behavior as state machines. Students will master `StateGraph` architectures, `TypedDict` schemas with state reducers, deterministic conditional routing edges, persistent checkpointing with `MemorySaver`, and Human-in-the-Loop (HITL) approval breakpoints.

---

## 2. Course Learning Outcomes (CLO) Alignment
This unit directly advances the following course learning competencies:
- **CLO 3 (Level 3 Stateful Graphs)**: Engineer cyclical, multi-step agent graphs using LangGraph, incorporating typed state schemas, conditional edges, recursion guards, and checkpointer persistence.
- **CLO 4 (Tool Schema & API Integration)**: Standardize tool schemas and dynamic dispatching across cyclical graph nodes.
- **CLO 5 (System Safety & Guardrails)**: Implement recursion limits, loop termination criteria, and Human-in-the-Loop approval breakpoints before destructive actions.

---

## 3. Instructional Time Budget (300 Contact Minutes)

```
========================================================================================
300 TOTAL CONTACT MINUTES
├── ASYNCHRONOUS GUIDED LEARNING (150 MIN)
│   ├── Video Micro-Lectures (40 min)
│   │   ├── Video 3.1: Beyond DAGs: Why Complex Agents Require Cyclical Graphs (10 min)
│   │   ├── Video 3.2: LangGraph Core: StateGraph, TypedDict & Pure Function Nodes (10 min)
│   │   ├── Video 3.3: Conditional Edges & Dynamic Loop Routing (10 min)
│   │   └── Video 3.4: Persistence, Checkpointing & Human-in-the-Loop Gates (10 min)
│   ├── Architectural Documentation & Readings (50 min)
│   │   ├── LangGraph Conceptual Guide: State, Nodes, and Edges
│   │   ├── Checkpointing and MemorySaver Architecture
│   │   └── Human-in-the-Loop Breakpoints Reference
│   ├── Formative Self-Check Drills (30 min)
│   │   └── 5 interactive graph state transitions & conditional routing drills
│   └── Socratic AI Exploration (30 min)
│       └── Roleplay prompt: "Lead Systems Architect on Linear Chains vs. LangGraph State Machines"
└── SYNCHRONOUS ACTIVE LEARNING & LAB (150 MIN)
    ├── Part 1: Graph Topology Walkthrough & State Reducer Demo (45 min)
    ├── Part 2: Live In-Class Conditional Edge Challenge (30 min)
    ├── Part 3: Guided Applied Laboratory Development (60 min)
    │   └── Lab 03: Cyclical Code Debugging & Refactoring Agent in LangGraph
    └── Part 4: Code Review, SpeedGrader Rubric Alignment & Debrief (15 min)
========================================================================================
```

---

## 4. Weekly Deliverables & Gradebook Weight
- **Formative Self-Checks**: 5 interactive collapsible exercises in `async/self_check_drills.md`.
- **Synchronous Paired Coding**: In-class challenge script in `sync/inclass_challenges.py`.
- **Applied Lab 03**: `lab3_starter.py` passing automated unit assertions (40% Grade Category).
- **Unit 03 Assessment**: 15-question QTI 1.2 assessment in `assessments/unit_quiz.md` (20% Grade Category).
