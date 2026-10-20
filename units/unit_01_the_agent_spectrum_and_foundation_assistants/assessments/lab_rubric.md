# Applied Lab 1 Assessment Rubric: ReAct Agent and Schema-Driven Tool Calling

## Overview
- **Course**: AINT 2050 - Applied AI Agent Architectures
- **Unit**: Unit 01 - The Agent Spectrum and Foundation Assistants
- **Assignment**: Lab 01 - Building a Pure-Python ReAct Engine with Structured Tool Execution
- **Total Points**: 100
- **Grading Weight**: Included in the 40% Applied Labs category

---

## Analytic Grading Matrix

| Performance Dimension | Exemplary (90-100%) | Proficient (80-89%) | Developing (70-79%) | Inadequate (0-69%) | Score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Tool Registry & JSON Schema Definitions** (25 pts) | Implements complete, valid OpenAPI/JSON Schema contracts for all registered tools with explicit parameter types, descriptions, and required fields. All types match runtime function arguments exactly. (23-25 pts) | All tools registered with working schema definitions. Minor ambiguity in descriptions or missing non-critical required fields. (20-22 pts) | Tools registered but schemas lack parameter validation, contain incorrect types, or omit parameter descriptions entirely. (17-19 pts) | Tools are hardcoded without structured schemas, or schema errors cause tool dispatch crashes. (0-16 pts) | /25 |
| **2. ReAct Cycle Execution & Parsing** (25 pts) | ReAct loop flawlessly parses Thought, Action, and Action Input stages across iterative cycles. Dispatches tool calls to the registry, captures observation strings, and injects results back into context until a Final Answer is reached. (23-25 pts) | ReAct cycle completes the test queries correctly. Minor formatting fragility when regex parses non-standard model responses. (20-22 pts) | ReAct loop executes but occasionally misidentifies tool parameters or skips the observation reflection stage before emitting answers. (17-19 pts) | Agent fails to loop cyclically, cannot extract tool calls from structured outputs, or hallucinates tool executions. (0-16 pts) | /25 |
| **3. Safety Guardrails & Recursion Limits** (25 pts) | Implements deterministic maximum iteration limits (`max_iterations`), runtime exception interceptors around tool execution, and clear error recovery observations. Prevents infinite execution loops without crashing the host process. (23-25 pts) | Recursion limit is enforced and tool exceptions are caught, but error messages returned to the agent lack diagnostic detail. (20-22 pts) | Recursion limit exists but causes unhandled runtime exceptions upon timeout, or tool crashes leak tracebacks directly to the user. (17-19 pts) | No recursion limit implemented (agent can enter infinite loops), or tool errors immediately crash the agent engine. (0-16 pts) | /25 |
| **4. State Tracking, History, & Code Quality** (25 pts) | Trajectory history accurately records the timestamped sequence of thoughts, actions, observations, and tool returns. Code follows strict PEP 8, uses comprehensive type annotations, passes all automated assertions, and includes clear docstrings. (23-25 pts) | Trajectory is logged and state is preserved across turns. Code is clean and functional with minor style or typing omissions. Passes all test assertions. (20-22 pts) | Trajectory logs are incomplete or drop intermediate observations. Code contains inconsistent formatting or incomplete type hints. Fails 1 unit assertion. (17-19 pts) | State is mutated destructively, intermediate reasoning steps are lost, or code fails multiple automated assertions. (0-16 pts) | /25 |

---

## Submission & Verification Checklist

To achieve full credit, students must verify the following automated criteria before submitting to Canvas SpeedGrader:

- [ ] Automated Test Suite: Execute `pytest test_lab1.py` or run `python lab1_starter.py` and confirm 100% assertions pass without warnings.
- [ ] Schema Compliance: Validate that all tool parameter dictionaries validate against Python standard types (`str`, `int`, `float`, `dict`, `list`).
- [ ] Zero Emoticons Policy: Ensure no emoticons or decorative Unicode symbols are output in terminal logs or response strings.
- [ ] Clean Repository: Commit only `lab1_starter.py` and optional scratch scripts; do not commit virtual environment files or cache directories.

---

## Grading Scale
- **93.0% - 100.0%**: Grade A (Mastery of ReAct cognitive looping and tool schemas)
- **90.0% - 92.9%**: Grade A-
- **87.0% - 89.9%**: Grade B+
- **83.0% - 86.9%**: Grade B (Proficient implementation with minor edge-case oversights)
- **80.0% - 82.9%**: Grade B-
- **77.0% - 79.9%**: Grade C+
- **70.0% - 76.9%**: Grade C (Baseline functionality; recurring formatting or loop issues)
- **Below 70.0%**: Grade F (Non-functional engine or missing core ReAct components)
