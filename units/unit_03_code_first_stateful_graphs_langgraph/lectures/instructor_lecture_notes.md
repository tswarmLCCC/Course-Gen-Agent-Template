# Unit 03 Instructor Lecture Notes: Code-First Stateful Graphs with LangGraph

## 1. Pedagogical Framing & Conceptual Anchor
- **The Culmination of Agency**: Students have now traversed all three tiers of the agent spectrum:
  - *Level 1*: Conversational Foundation Models (Gemini/Claude) with linear tool loops.
  - *Level 2*: Visual Orchestrators (n8n/Langflow) with low-code DAGs and webhooks.
  - *Level 3*: Code-First Stateful Graphs (LangGraph) with cyclical state machines and checkpoints.
- **The Core Insight**: LangGraph bridges the gap between AI non-determinism and deterministic software engineering. The LLM handles unstructured perception and drafting; the graph structure guarantees loop limits, test assertions, and schema consistency.

---

## 2. Common Student Misconceptions & Pitfalls
1. **"A node function should decide what node runs next."**
   - *Correction*: Emphasize strict separation of concerns. In LangGraph, node functions *only* transform data and return partial state. Edges (and conditional edge routing functions) dictate the control flow.
2. **"State keys get appended automatically."**
   - *Correction*: By default, returning `{"messages": [new_msg]}` will overwrite the `messages` key entirely unless wrapped in `Annotated[list, add_messages]` or `Annotated[list, operator.add]`. Show this live in Python.
3. **"Infinite loops are impossible in state graphs."**
   - *Correction*: Remind students that without a conditional termination branch or a `recursion_limit` safeguard, cyclical graphs will loop infinitely until memory or API budget is exhausted.

---

## 3. Synchronous Lab Demonstration Tips
- Trace state evolution on the whiteboard or slide deck before opening code.
- Demonstrate what happens when a breakpoint interrupts graph execution, inspect the checkpointer dictionary in memory, and then demonstrate resuming with `app.invoke(None, config={"configurable": {"thread_id": "session_id"}})`.
