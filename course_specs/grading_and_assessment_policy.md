# AINT 2050: Grading & Assessment Policy

## Grading Architecture
Final grades in AINT 2050 are based on active engineering, architectural rigor, and verifiable agent reliability:

| Assessment Category | Weight | Frequency | Description |
| :--- | :---: | :--- | :--- |
| **Weekly Practical Agent Labs** | **40%** | Weekly (Units 1–7) | Hands-on agent implementations (Python ReAct loops, n8n workflows, Langflow canvases, and LangGraph codebases) evaluated on autonomy, error recovery, and tool accuracy. |
| **Weekly Architecture Quizzes** | **20%** | Weekly (Units 1–8) | 15-question Canvas quizzes testing agent theory (30%), state graph routing prediction (40%), and failure mode diagnosis (30%). |
| **Asynchronous Self-Checks & AI Drills** | **10%** | Weekly (Units 1–8) | Formative knowledge checks and Socratic AI drill completions completed prior to synchronous class meetings. |
| **Comprehensive Agent Capstone Project** | **30%** | Week 8 | End-to-end autonomous multi-agent system: stateful LangGraph design, tool integration, human-in-the-loop safeguards, telemetry, and live defense. |
| **Total** | **100%** | | |

---

## Grading Scale
- **A**: 90.0% – 100%
- **B**: 80.0% – 89.9%
- **C**: 70.0% – 79.9%
- **D**: 60.0% – 69.9%
- **F**: Below 60.0%

---

## Agent Engineering Standards (Deduction Criteria)
In production AI engineering, an agent that occasionally works but gets stuck in infinite loops or takes unmonitored destructive actions is unacceptable. All lab submissions are evaluated against the following standards:

1. **State Determinism & Loop Guards**: Every cyclical agent loop must have an explicit maximum iteration guard (`max_iterations` or `recursion_limit`) to prevent infinite looping and token exhaustion.
2. **Strict Tool Validation**: All tools exposed to an agent must define strict Pydantic/JSON schemas with explicit field types and parameter descriptions.
3. **Graceful Error Recovery**: Tool failure or malformed LLM responses must be captured and fed back into the agent's scratchpad as an observation rather than crashing the runtime.
4. **Safety & Human-in-the-Loop Gating**: Destructive actions (deleting files, executing shell commands, transferring funds) must be gated behind approval breakpoints.
5. **Clean Code & Typings**: Python scripts must use explicit type hints (`TypedDict`, Pydantic models) and adhere to PEP-8 standards.

---

## AI Augmentation & Academic Integrity Policy
In alignment with modern agent development:
- **Permitted AI Use**: Students are encouraged to use LLMs (Claude, Gemini, ChatGPT) as pair programmers and architectural sounding boards.
- **The Defense Rule**: Full credit requires the ability to explain every edge, node, state transition, and tool schema in your agent during synchronous code reviews. Submitting agent code that you cannot explain or debug live results in zero credit.
