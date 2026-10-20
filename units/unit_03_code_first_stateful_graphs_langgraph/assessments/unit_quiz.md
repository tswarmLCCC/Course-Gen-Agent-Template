# Unit 03 Assessment: Code-First Stateful Graphs with LangGraph

Welcome to the Unit 03 Quiz. This assessment evaluates your comprehension of Level 3 stateful graph architectures, LangGraph primitives, StateGraph mechanics, TypedDict state schemas, conditional edges, checkpointers, and Human-in-the-Loop workflows.

---

### Question 1
Why are Directed Acyclic Graphs (DAGs) insufficient for modeling complex, self-correcting cognitive agents?
* A) DAGs do not allow any text string processing.
* B) By definition, DAGs prohibit cycles or backward edges, preventing an agent from testing code, reviewing errors, and looping back to revise its work.
* C) DAGs can only be deployed on 32-bit hardware architectures.
* D) DAGs cannot execute database queries.

---

### Question 2
In LangGraph, what is the single source of truth passed to every node in the graph during execution?
* A) The operating system environment variables.
* B) The strongly-typed State dictionary (defined via `TypedDict`).
* C) An unformatted binary string dump of the model weights.
* D) A global mutable text file on the local file system.

---

### Question 3
What is the primary architectural responsibility of a Node function in LangGraph?
* A) To decide which node in the graph should execute next.
* B) To accept the current state as input and return a partial state dictionary updating one or more keys.
* C) To recompile the Python virtual environment.
* D) To manage network socket listeners for incoming webhooks.

---

### Question 4
How does a Conditional Edge differ from a standard Edge in LangGraph?
* A) A conditional edge runs on a separate GPU thread.
* B) A conditional edge evaluates a routing function that inspects the current state and returns a key mapping to the next destination node, whereas a standard edge transitions unconditionally.
* C) Standard edges can only transition to the `END` sentinel.
* D) Conditional edges require the user to press Enter on the keyboard.

---

### Question 5
When declaring a list field in an `AgentState` schema, what is the purpose of using `Annotated[List[str], operator.add]`?
* A) It converts all strings in the list to uppercase characters.
* B) It defines a reducer function instructing LangGraph to append newly returned items to the existing list rather than overwriting the entire list.
* C) It encrypts the list items using AES-256.
* D) It limits the list size to exactly two elements.

---

### Question 6
What built-in sentinel in LangGraph represents the termination of graph execution?
* A) `STOP`
* B) `EXIT`
* C) `END`
* D) `TERMINATE`

---

### Question 7
In LangGraph, what is the purpose of passing a `checkpointer` (such as `MemorySaver` or `SqliteSaver`) during graph compilation?
* A) To automatically take state snapshots after every node execution, enabling persistence, session resumption, and time-travel debugging.
* B) To verify spelling and grammatical errors in model prompts.
* C) To increase the floating-point calculation precision of neural network weights.
* D) To prevent Python from running out of system memory.

---

### Question 8
How does LangGraph track and isolate independent user sessions when persisting checkpoints?
* A) By the IP address of the local machine.
* B) By passing a unique `thread_id` inside the invocation configuration dictionary (`{"configurable": {"thread_id": "session_123"}}`).
* C) By creating a new GitHub repository for each user turn.
* D) By assigning sequential integers starting from zero on every machine reboot.

---

### Question 9
What error is raised in LangGraph when an agent enters an infinite loop that exceeds the configured `recursion_limit`?
* A) `ZeroDivisionError`
* B) `GraphRecursionError`
* C) `MemoryError`
* D) `FileNotFoundError`

---

### Question 10
In production agent architectures, what does the Human-in-the-Loop (HITL) `interrupt_before` configuration accomplish?
* A) It displays a popup banner asking the user to rate the application.
* B) It automatically saves state and pauses graph execution prior to executing designated high-risk nodes, allowing human review and authorization.
* C) It shuts down the host server if no human interacts within 60 seconds.
* D) It permanently disables all tool execution for the session.

---

### Question 11
Consider a StateGraph where node `test_runner` executes tests on code. If tests fail, it routes to `analyzer`, which routes to `patcher`, which routes back to `test_runner`. What topology does this represent?
* A) A strictly linear Directed Acyclic Graph.
* B) A cyclical state machine with iterative feedback loops.
* C) A star topology with a centralized broker node.
* D) A client-server RPC broadcast network.

---

### Question 12
When a graph paused by an `interrupt_before` breakpoint is ready to resume after human approval, how does the application restart execution?
* A) By re-initializing the graph with a blank state.
* B) By invoking the compiled app with `None` or updated inputs while specifying the exact same `thread_id` in the config.
* C) By rebooting the cloud virtual machine.
* D) By running `git reset --hard HEAD`.

---

### Question 13
Why is keeping node functions "pure" or side-effect-free (returning partial state updates rather than modifying global variables) essential in LangGraph?
* A) Global variables are not supported in Python 3.
* B) It ensures determinism, supports thread-safe concurrent execution, and allows the checkpointer to accurately snapshot and roll back state without corrupted references.
* C) Pure functions run 10 times faster than impure functions.
* D) LangGraph automatically deletes any Python files containing global variables.

---

### Question 14
Which of the following represents a primary advantage of Level 3 code-first frameworks (LangGraph) over Level 2 visual platforms (n8n/Langflow)?
* A) Level 3 frameworks do not require an internet connection to run foundation LLMs.
* B) Level 3 frameworks support native unit testing, CI/CD integration, version-controlled git branching, strongly-typed state, and arbitrary cyclic execution topologies.
* C) Level 3 frameworks eliminate the need to write Python code.
* D) Level 3 frameworks are completely free while visual platforms require multimillion-dollar licenses.

---

### Question 15
In the complete 3-level agent maturity spectrum, how does the progression of agency flow?
* A) Level 1 (Conversational Assistants) -> Level 2 (Visual Low-Code Orchestrators) -> Level 3 (Code-First Stateful Graphs).
* B) Level 1 (Autonomous Robots) -> Level 2 (Chatbots) -> Level 3 (Spreadsheets).
* C) Level 1 (Visual Canvases) -> Level 2 (Conversational Assistants) -> Level 3 (Zero Code).
* D) Level 1 (Pure SQL) -> Level 2 (Bash Scripts) -> Level 3 (Spreadsheets).

---

## Answer Key

| Question # | Correct Answer | Concept Tested & Rationale |
| :--- | :--- | :--- |
| **1** | **B** | DAGs forbid backward cycles, making iterative critique-revision or self-healing loops impossible without graph state machines. |
| **2** | **B** | LangGraph uses a centralized TypedDict state schema as the single source of truth shared across all graph nodes. |
| **3** | **B** | Nodes are pure transformation functions that take the current state and return partial updates; edges determine routing. |
| **4** | **B** | Conditional edges execute a routing function inspecting state values to dynamically choose the destination node. |
| **5** | **B** | State reducers like `operator.add` instruct LangGraph to append list updates rather than replacing the list. |
| **6** | **C** | `END` is the native LangGraph sentinel constant representing graph termination. |
| **7** | **A** | Checkpointers serialize and store state snapshots after every node execution for persistence and resumption. |
| **8** | **B** | LangGraph partitions state checkpoints across sessions using the `thread_id` key in the configuration. |
| **9** | **B** | Exceeding `recursion_limit` raises a `GraphRecursionError` to prevent infinite loops and runaway costs. |
| **10** | **B** | `interrupt_before` creates breakpoints before designated nodes so humans can review actions before execution. |
| **11** | **B** | Cycling between testing, analyzing, and patching creates a cyclical state machine with dynamic feedback. |
| **12** | **B** | Resuming a checkpointed graph is achieved by calling `app.invoke()` with the target `thread_id`. |
| **13** | **B** | Pure functions prevent race conditions, enable safe state rollback, and ensure checkpointer fidelity. |
| **14** | **B** | Code-first frameworks provide full software engineering lifecycle support: typing, unit tests, CI/CD, and git version control. |
| **15** | **A** | The course taxonomy progresses from Level 1 foundation assistants to Level 2 visual workflows to Level 3 stateful code graphs. |
