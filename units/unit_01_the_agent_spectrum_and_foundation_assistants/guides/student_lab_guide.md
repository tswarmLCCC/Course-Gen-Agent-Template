# Unit 1 Applied Lab Guide: Building a Multi-Tool ReAct Agent from Scratch

**Course:** AINT 2050: Applied AI Agent Architectures  
**Lab Assignment:** Unit 1 Applied Programming Lab  
**Points:** 50 Points Total (Evaluated via SpeedGrader with Analytic Rubric)  
**Deliverable File:** `lab1_yourlastname.py`  
**Target Environment:** Python 3.11 in GitHub Codespaces  

---

## Technical Scenario & Problem Narrative

You are working as an AI Systems Engineer at **Nexus Cognitive Systems**. Your organization is building an internal autonomous operations assistant capable of performing multi-step financial audits and data reconciliation. 

While commercial platforms like LangGraph, n8n, and Langflow provide high-level abstractions, your team's lead architect has instructed you to build a foundational **Pure-Python ReAct Autonomous Agent** (`lab1_starter.py`) from first principles. By constructing the tool registry, scratchpad memory buffer, action parser, and recursion guards from scratch, you will gain an intimate understanding of the failure modes, state transitions, and execution loops that govern all higher-level agent frameworks.

---

## Technical Specifications & Required Tasks

Open `guides/lab1_starter.py` and implement the four core modular tasks:

### Task 1: Tool Registry & Safe Execution Engine (`ToolRegistry`)
Implement a robust tool registry class that:
1. Registers callable Python functions associated with string tool names (`register_tool`).
2. Provides a `dispatch(tool_name: str, argument: str) -> str` method that catches runtime exceptions, isolates errors, and returns informative error strings to the agent scratchpad without crashing the host application.
3. Implements three deterministic core tools:
   - `calculator(expression: str) -> str`: Safely evaluates basic arithmetic expressions (`+`, `-`, `*`, `/`, `**`).
   - `search_knowledge_base(query: str) -> str`: Queries a structured mock database of corporate accounts and returns matched records.
   - `convert_currency(args: str) -> str`: Converts currency amounts using current exchange rates (e.g. `USD_TO_EUR`, `USD_TO_GBP`).

### Task 2: ReAct Scratchpad & Action Parser (`parse_agent_action`)
Implement a regex parser capable of extracting the agent's intent from the LLM's response stream:
1. Detects `Final Answer: [text]` to trigger successful mission termination.
2. Extracts tool calls formatted as `Action: tool_name(arguments)`.
3. Handles malformed or non-compliant syntax gracefully by returning `(False, "MALFORMED_ACTION", raw_text)`.

### Task 3: Autonomous ReAct Execution Loop (`ReActAgent.run`)
Implement the core iterative reasoning engine:
1. Initialize an empty scratchpad for the conversation session.
2. In each iteration step (up to `max_iterations = 6`):
   - Format the full prompt containing the user question, accumulated scratchpad history, and step number.
   - Obtain the model response (using the mock LLM engine or real API call).
   - If `Final Answer:` is reached, return the extracted solution string.
   - If an action is requested, dispatch the tool, capture the observation, and append it to the scratchpad as `Observation {step}: {result}`.
3. Enforce a strict recursion limit. If `step > max_iterations` without a `Final Answer:`, terminate safely and return `"Error: Agent reached maximum recursion limit (possible loop detected)."`.

### Task 4: Comparative Architectural Audit (Gemini vs. Claude)
In the module docstring or comment section of your script, document a concise 1-page comparative analysis answering:
1. How does Google Gemini's function calling schema differ from Anthropic Claude's tool use protocol?
2. Why is Claude currently favored for complex code generation, and in what scenarios is Gemini Flash preferred?
3. What is the fundamental risk of deploying Level 1 prompt assistants without Level 3 cyclical graph guards?

---

## Submission & Verification Protocol

1. Run the built-in test suite in Codespaces:
   ```bash
   python3 units/unit_01_the_agent_spectrum_and_foundation_assistants/guides/lab1_starter.py
   ```
2. Confirm that all assertion tests pass with `[PASS]` and zero runtime errors.
3. Save your file as `lab1_yourlastname.py` (e.g. `lab1_smith.py`).
4. Upload your `.py` file to the **Unit 1 Applied Lab Assignment** in Canvas.

---

## Analytic Grading Rubric (50 Points Total)

| Evaluation Criterion | Exemplary (Full Credit) | Competent (Minor Deductions) | Developing (Major Deductions) | Unacceptable (Zero Credit) |
| :--- | :--- | :--- | :--- | :--- |
| **1. ReAct Loop & Autonomy (20 pts)** | The agent iteratively executes multiple tool calls, updates scratchpad state, handles multi-step reasoning, and terminates cleanly on `Final Answer:`. Passes 100% of tests. *(20 pts)* | ReAct loop functions but fails on 1 edge case (e.g. missing whitespace in action regex); passes $\ge 80\%$ of tests. *(16–19 pts)* | Loop does not correctly append observations or gets stuck in loops; passes $<80\%$ of tests. *(10–15 pts)* | Code does not implement ReAct loop or crashes on execution. *(0–9 pts)* |
| **2. Tool Registry & Error Isolation (15 pts)** | Tools are cleanly registered; dispatcher catches exceptions (e.g. division by zero, invalid lookups) and returns error observations without crashing the application. *(15 pts)* | Dispatcher works but lets 1 unhandled exception leak through to the host process. *(12–14 pts)* | Tools are hardcoded directly into the loop without a dynamic registry. *(8–11 pts)* | No tool registry or dispatcher implemented. *(0–7 pts)* |
| **3. Recursion & Safety Guards (10 pts)** | Hard recursion limit (`max_iterations`) strictly prevents infinite looping; handles empty inputs and malformed actions gracefully. *(10 pts)* | Recursion limit exists but allows 1 extra iteration beyond maximum. *(8–9 pts)* | No recursion limit (unbounded loop hazard); crashes on malformed LLM responses. *(5–7 pts)* | Infinite loop triggered or zero error guards. *(0–4 pts)* |
| **4. Architectural Analysis & PEP-8 (5 pts)** | Thorough, accurate comparative analysis of Gemini vs. Claude; clean docstrings, type annotations, and `snake_case` naming. *(5 pts)* | Minor omission in Gemini vs. Claude comparison or minor PEP-8 naming flaw. *(4 pts)* | Superficial analysis; pervasive PEP-8 violations. *(2–3 pts)* | Analysis omitted; unreadable code. *(0–1 pts)* |
