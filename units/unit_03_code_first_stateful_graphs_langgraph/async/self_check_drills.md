# Unit 03 Self-Check Drills: Code-First Stateful Graphs (LangGraph)

Test your understanding of state machines, typed schemas, cyclical edges, and checkpoint persistence before attending synchronous lab.

---

### Drill 1: State Schema Reducer Behavior
**Scenario**: You define an agent state schema in LangGraph as follows:
```python
from typing import TypedDict, Annotated, List
import operator

class ReviewState(TypedDict):
    critique_notes: Annotated[List[str], operator.add]
    iteration_count: int
```
Node A returns `{"critique_notes": ["Check edge case 0"], "iteration_count": 1}`.
Node B then returns `{"critique_notes": ["Add docstring"], "iteration_count": 2}`.

What is the resulting value of `state["critique_notes"]` after both nodes run?

* A) `["Add docstring"]` (Node B overwrote Node A)
* B) `["Check edge case 0", "Add docstring"]` (Values concatenated via `operator.add`)
* C) `["Check edge case 0"]` (Node B was rejected because key already exists)
* D) `[]` (List cleared after each turn)

<details>
<summary>Check Answer & Explanation</summary>

**Correct Answer**: **B) `["Check edge case 0", "Add docstring"]`**

**Explanation**: In LangGraph state schemas, wrapping a field in `Annotated[T, reducer_fn]` configures how partial state updates are merged. Using `operator.add` instructs LangGraph to concatenate newly returned list items with existing list items rather than overwriting them.
</details>

---

### Drill 2: Conditional Edge Routing Logic
**Scenario**: Consider the following conditional routing function in a code-fixing agent:
```python
def check_test_status(state: CodeFixState) -> str:
    if state["tests_passed"] is True:
        return "deploy"
    elif state["attempts"] >= 3:
        return "abort"
    else:
        return "revise"
```
The graph is configured with:
```python
workflow.add_conditional_edges("test_runner", check_test_status, {
    "deploy": "deploy_code_node",
    "abort": "human_escalation_node",
    "revise": "patch_generator_node"
})
```
If `state["tests_passed"]` is `False` and `state["attempts"]` is `2`, which node will execute next?

* A) `deploy_code_node`
* B) `human_escalation_node`
* C) `patch_generator_node`
* D) `END`

<details>
<summary>Check Answer & Explanation</summary>

**Correct Answer**: **C) `patch_generator_node`**

**Explanation**: `tests_passed` is False and `attempts` (2) is less than 3. The function returns `"revise"`, which maps via the routing dictionary to `"patch_generator_node"`.
</details>

---

### Drill 3: Human-in-the-Loop (HITL) Interruption
**Scenario**: You compile a StateGraph with:
```python
app = workflow.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["delete_customer_account"]
)
```
What occurs when graph execution reaches the `"delete_customer_account"` node?

* A) The node executes immediately without stopping.
* B) The graph saves its current state to the checkpointer and pauses execution before running the node, returning control to the caller.
* C) The process raises an unhandled `SystemExit` exception and shuts down Python.
* D) The node is skipped entirely and execution jumps to `END`.

<details>
<summary>Check Answer & Explanation</summary>

**Correct Answer**: **B) The graph saves its current state to the checkpointer and pauses execution before running the node.**

**Explanation**: `interrupt_before` creates an intentional breakpoint before the designated node. The current state is checkpointed under the active `thread_id`, allowing a human supervisor to inspect the state and authorize continuation.
</details>

---

### Drill 4: Recursion Limit Guardrails
**Scenario**: An autonomous agent enters an unintended cycle where Node A calls Node B, which calls Node A continuously. 

How does LangGraph prevent runaway API costs and infinite loops?

* A) LangGraph detects duplicate strings and shuts down the computer.
* B) LangGraph enforces a configurable `recursion_limit` (defaulting to 25 steps); exceeding this limit raises a `GraphRecursionError`.
* C) LangGraph requires manual human intervention every 5 seconds.
* D) Cyclical graphs are mathematically impossible to run in LangGraph.

<details>
<summary>Check Answer & Explanation</summary>

**Correct Answer**: **B) LangGraph enforces a configurable `recursion_limit` (default 25 steps), raising `GraphRecursionError`.**

**Explanation**: Every invocation in LangGraph accepts a config dictionary specifying `recursion_limit`. If node transitions exceed this limit before reaching `END`, LangGraph safely halts execution with a `GraphRecursionError`.
</details>

---

### Drill 5: Resuming Execution with `thread_id`
**Scenario**: A user started an interactive diagnostic session on Monday. The graph paused at an approval step. On Tuesday, the user returns to resume their session.

How does the host application instruct LangGraph to pick up where the user left off?

* A) By re-running the entire graph from the beginning with the original prompt.
* B) By calling `app.invoke(None, config={"configurable": {"thread_id": user_session_id}})`.
* C) By editing the compiled Python bytecode file.
* D) By assigning a random new UUID to the session.

<details>
<summary>Check Answer & Explanation</summary>

**Correct Answer**: **B) By calling `app.invoke(None, config={"configurable": {"thread_id": user_session_id}})`.**

**Explanation**: LangGraph's checkpointer retrieves the latest state snapshot matching the specified `thread_id`. Passing `None` or updated inputs resumes execution directly from the saved breakpoint.
</details>
