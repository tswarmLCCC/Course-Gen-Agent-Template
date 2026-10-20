# Unit 1: Asynchronous Self-Check Drills & ReAct Tracing

Complete these self-check drills before attending synchronous class. Test your mental model by predicting the agent trajectory or identifying architectural flaws before expanding the collapsible answer keys.

---

### Drill 1: Identifying the ReAct Failure Mode
Examine the following agent trajectory:
```text
Question: "What was Apple's stock price at market close yesterday, and what is 15% of that value?"
Thought 1: "I know Apple's stock usually trades around $220. Let me compute 15% of 220."
Action 1: calculate(220 * 0.15)
Observation 1: "33.0"
Thought 2: "I now have the answer."
Final Answer: "Apple's stock price was $220, and 15% of that value is $33.00."
```
What critical flaw occurred in this agent loop? Which level of agency does this failure illustrate?

<details>
<summary>Click to view solution and rationale</summary>

**Identified Flaw:**
The agent skipped observation of external reality. Instead of querying a real-time financial tool (`get_stock_quote("AAPL")`), the model hallucinated the price (`$220`) inside its internal reasoning thought and fed an unverified number into the calculator.

**Architectural Lesson:**
An agent's reasoning must be used to **plan tool queries**, not invent data. If an agent assumes facts rather than observing them through tools, the entire downstream calculation becomes invalid. This is why strict tool use protocols (Level 1/3) force models to substantiate claims with tool observations before formulating a `Final Answer`.
</details>

---

### Drill 2: Comparing Level 2 (n8n) vs Level 3 (LangGraph)
An enterprise team wants to build an autonomous software patcher:
1. It reads incoming GitHub issues.
2. It attempts to generate a code fix.
3. It runs automated unit tests in a container.
4. If tests fail, it loops back to step 2 with the test error traceback to try a new fix, up to 5 times.
5. If tests pass, it opens a Pull Request.

Why is this use case better suited for **LangGraph (Level 3)** than a traditional linear DAG in **n8n / Zapier (Level 2)**?

<details>
<summary>Click to view solution and rationale</summary>

**Key Difference:**
Standard workflow engines (Level 2) are traditionally **Directed Acyclic Graphs (DAGs)**. They execute linearly from Trigger &rarr; Action A &rarr; Action B &rarr; End. While some support simple loops, they struggle with **arbitrary cyclical state management** where the agent must maintain a dynamic scratchpad of prior failed attempts and branch conditionally based on test results.

**Why LangGraph Excels:**
LangGraph is a **cyclical state machine**. It supports:
- State persistence (`TypedDict` tracking `attempt_count`, `code_draft`, `error_traceback`).
- Conditional routing edges (`if tests_passed: route_to_pr() else: route_to_fix()`).
- Recursion limits preventing infinite loops.
- Human-in-the-loop breakpoints if the fix fails 5 times.
</details>

---

### Drill 3: Function Calling JSON Schema Parsing
Examine the following tool definition:
```json
{
  "name": "fetch_user_record",
  "description": "Retrieves user account status by integer ID.",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "integer",
        "description": "The unique 6-digit numeric identifier."
      }
    },
    "required": ["user_id"]
  }
}
```
If an LLM produces the tool call: `fetch_user_record(user_id="USR-4091")`, what error will occur in a strictly validated runtime environment?

<details>
<summary>Click to view solution and rationale</summary>

**Error:** `ValidationError` (Schema Type Mismatch)

**Rationale:**
The schema explicitly specifies `"type": "integer"`. Passing a string `"USR-4091"` violates the type contract. In production agent runtimes (like Pydantic / Anthropic Tool Use / Gemini), this error is captured by the tool dispatcher and returned to the LLM as an observation:
`Observation: ValidationError: Input should be a valid integer, unable to parse string as an integer.`  
The LLM then adjusts its call in the next iteration.
</details>

---

### Drill 4: Google Gemini vs Anthropic Claude Tooling Paradigms
Which model introduced native operating system desktop interaction (**Computer Use**) allowing the agent to view screens, move the mouse cursor, and click desktop interface elements?

<details>
<summary>Click to view solution and rationale</summary>

**Correct Answer:** Anthropic Claude (Claude 3.5 Sonnet)

**Rationale:**
Anthropic introduced the **Computer Use API**, which equips Claude with special tools (`mouse_move`, `left_click`, `type`, `screenshot`) allowing the model to interact with any desktop GUI just like a human operator. Google Gemini focuses extensively on native multimodality (processing video/audio streams directly) and high-speed function calling.
</details>

---

### Drill 5: Recursion Limits & Infinite Loop Traps
Why must every production agent loop implement a strict `max_iterations` counter? What happens if an agent encounters a broken API endpoint without a recursion guard?

<details>
<summary>Click to view solution and rationale</summary>

**Answer:**
Without a recursion guard, an agent entering an error state may continuously retry calling the failing tool indefinitely:
`Thought: Tool failed. I will try again.` &rarr; `Action` &rarr; `Observation: 500 Error` &rarr; `Thought: Tool failed...`  
This causes:
1. Massive API token consumption and financial cost.
2. Thread starvation and process lockup.
3. Rate limit bans from the API provider.  
*Best Practice:* Always cap execution loops (e.g. `max_iterations = 10` or LangGraph's `recursion_limit`).
</details>
