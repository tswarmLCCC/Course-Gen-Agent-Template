# Instructor Delivery Notes & Synchronous Runbook: Unit 1

**Course:** AINT 2050: Applied AI Agent Architectures  
**Topic:** The Agent Spectrum, ReAct Reasoning Loops & Tool Schemas  
**Audience:** Instructor / Teaching Assistant  

---

## 1. Pedagogical Strategy & Session Rhythm

In Unit 1, students often conflate "prompt engineering" with "building agents." Our primary goal is to establish the clear conceptual boundary between single-turn prompt completion and cyclical autonomous agency:
1. **The Live Hallucination Demo:** Start the session by asking a raw LLM without tools to calculate a complex math expression or state current weather in Cheyenne, WY. Watch it hallucinate or state its knowledge cutoff. Then show how adding a single tool call turns that failure into fact.
2. **Predict-Observe-Explain (POE):** Before executing `part1_agent_taxonomy_and_react.py`, ask students to trace the Thought-Action-Observation scratchpad.
3. **De-Mystifying Frameworks:** Emphasize that frameworks like LangGraph and CrewAI are NOT magic—they are structured loops over state dictionaries, exactly like the pure-Python loop we code today.

---

## 2. Common Student Traps & Misconceptions

| Trap / Misconception | Typical Student Error | Pedagogical Counter-Intervention |
| :--- | :--- | :--- |
| **LLMs Execute Python Directly** | Student believes the LLM itself runs the Python function code in the cloud. | Clarify that the LLM only generates text/JSON. The *host application* (your Python script) receives the JSON, runs the local function, and sends the output back. |
| **Unbounded While Loops** | Student writes `while not done:` without a `max_iterations` counter. | Trigger a mock API 500 error in live code to show the agent spinning in an infinite loop. Emphasize recursion limits. |
| **Tool Schema Ambiguity** | Student writes tool description as `"Does math"` without specifying parameters or return formats. | Show how vague descriptions lead to the LLM inventing parameter names (e.g. `query` vs `expr`). |
| **Skipping the Thought Phase** | Student tries to jump straight to tool calls without generating reasoning thoughts. | Show that without the Thought step, multi-step tool chaining fails because the LLM lacks a planning scratchpad. |

---

## 3. Live-Coding Demonstration Prompts

### Demo 1: The Pure-Python ReAct Loop (`part1_agent_taxonomy_and_react.py`)
- Show the step-by-step evolution of the scratchpad string.
- Print `Thought 1`, `Action 1`, `Observation 1`, `Thought 2`, `Final Answer` in real time.

### Demo 2: Declaring JSON Tool Schemas (`part2_function_calling_schemas.py`)
- Walk through declaring a schema for Google Gemini and Anthropic Claude.
- Demonstrate client-side parameter validation using Pydantic / Python type checking.

### Demo 3: Error Isolation & Recovery (`part3_state_and_memory.py`)
- Simulate a tool returning an error string (`"Error 404: Location Not Found"`).
- Show how the agent reads the error in its Observation and autonomously alters its query to recover.
