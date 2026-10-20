# Learn with AI: Exploring Stateful Graphs with LangGraph

Use the following structured Socratic prompts with an advanced foundation assistant (such as Anthropic Claude 3.5 Sonnet or Google Gemini 1.5 Pro) to deepen your conceptual understanding of Level 3 stateful graphs.

---

## Exercise 1: Migrating from Linear Chains to StateGraphs

Copy and paste the following prompt into your AI assistant:

```markdown
You are a Principal Software Engineer and core contributor to LangGraph.

I currently have an AI coding assistant built as a linear sequence of steps:
Step 1: User prompt ->
Step 2: Generate code ->
Step 3: Run static linter ->
Step 4: Output to user.

Problem: If the linter finds errors in Step 3, the linear pipeline fails and outputs broken code. I want to convert this into a cyclical self-correcting StateGraph with:
1. A strongly-typed state schema tracking code, lint_errors, attempt_count, and max_attempts.
2. A conditional edge from the linter node that routes back to the generator node if errors exist and attempts < 3.
3. A Human-in-the-Loop breakpoint if errors persist after 3 attempts.

Please:
- Walk me through the state schema design.
- Provide the Python code using LangGraph's StateGraph, nodes, and conditional edges.
- Explain how the state dictionary changes across 2 cycles of failed linting followed by a successful fix.
```

---

## Exercise 2: Socratic Architectural Interview on State Reducers

Copy and paste the following prompt:

```markdown
You are an expert in distributed state systems and agent orchestration.

Please conduct a Socratic interview with me regarding the design of State Schemas in LangGraph:
- Explain the trade-offs between overwriting state keys vs using reducer functions (e.g., `operator.add` or `add_messages`).
- Ask me 2 questions about how my application handles state rollback or multi-user concurrency.
- Critique why mutable global variables are considered an anti-pattern when developing multi-agent graph topologies.
```
