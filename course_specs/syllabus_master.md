# AINT 2050: Master Syllabus & 8-Week Modular Schedule

## Course Overview
- **Course Prefix & Number:** AINT 2050
- **Course Title:** Applied AI Agent Architectures: From Conversational Spark to LangGraph Systems
- **Credit Hours:** 3.0 Semester Credit Hours
- **Term:** Fall 2026
- **Institution:** Laramie County Community College (LCCC)
- **Instructional Format:** 8-Week Accelerated Hybrid (Active Learning)

---

## Course Structure: The 300-Minute Hybrid Model
Each week is budgeted for **300 minutes of total structured instructional engagement**:
- **150 Minutes of Asynchronous Guided Learning**:
  - Bite-sized video micro-lectures (5–10 mins each).
  - Curated documentation readings & architectural design patterns (see [Master External Resources Guide](file:///c:/dev/Course-Gen-Agent-Template/course_specs/external_resources_guide.md)).
  - Formative self-check knowledge checks with interactive collapsible accordions.
  - Socratic AI practice drills using roleplay prompts.
- **150 Minutes of Synchronous Active Learning & Practical Lab**:
  - Either **two 75-minute sessions** (e.g., Tuesday/Thursday) or **one 150-minute block**.
  - Instructor live-coding demonstrations and architecture reviews.
  - Paired lab development and live-debugging clinics.
- *(Independent homework/capstone engineering occurs outside these 300 instructional contact minutes).*

---

## 8-Week Master Schedule: The Agency Spectrum

### Week 1: Level 1 — The Agent Spectrum & Conversational Assistants (Gemini & Claude)
* **Theme**: The Agent Taxonomy, Perception-Reasoning-Action loops, ReAct prompting pattern, Google Gemini (Gemini Spark, System Instructions, Function Calling), and Anthropic Claude (Tool Use, Artifacts, Computer Use).
* **Difficulty Rating**: 1–2 / 5
* **Async Guided Study (150 min)**:
  - Micro-Video 1.1: What Makes an Agent? Perception, Reasoning & Action Loops (8 min).
  - Micro-Video 1.2: The ReAct Pattern: Synergizing Reasoning and Acting in LLMs (8 min).
  - Micro-Video 1.3: Google Gemini Spark vs. Anthropic Claude Tooling Paradigms (7 min).
  - Micro-Video 1.4: Pure-Python ReAct Implementation: Scratchpads & Tool Execution (7 min).
  - Readings: Yao et al. (ReAct Paper), Anthropic Tool Use Guide, Google Gemini Function Calling Reference.
  - Formative Self-Checks: 5-question ReAct trace and tool payload prediction drills.
  - Socratic AI Drill: "Agent Zero on Prompt Chaining vs. Autonomous Tool Use".
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Architecture breakdown: Parsing tool definitions (`tools` schema) and dispatching Python function calls.
  - Session 2 (75 min): Live-coding a pure-Python ReAct loop with calculator, weather, and database tools.
  - Lab Activity: Pure-Python Multi-Tool ReAct Agent Lab.
* **Deliverable**: Lab 1 Python Script + Unit 1 Quiz.

### Week 2: Level 2 — Visual Workflow Automation with n8n
* **Theme**: Visual orchestration, n8n AI Agent nodes, tool nodes, memory nodes, webhook triggers, and enterprise API integrations without raw code.
* **Difficulty Rating**: 2–3 / 5
* **Async Guided Study (150 min)**:
  - Micro-Videos: Visual node architectures, n8n AI Agent component breakdown, connecting LLMs to REST APIs.
  - Readings: n8n AI Agent Documentation, LangChain integration in n8n.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Setting up local/cloud n8n workflows with OpenAI/Gemini chat nodes.
  - Session 2 (75 min): Building an automated customer support triaging agent with external webhooks and Slack/email notifications.
  - Lab Activity: n8n Autonomous Customer Operations Agent Lab.
* **Deliverable**: Lab 2 Exported Workflow JSON & Walkthrough Report + Unit 2 Quiz.

### Week 3: Level 2 — Visual Graph Prototyping with Langflow
* **Theme**: Component-based AI pipelines, Langflow canvas, prompt chaining, document vector stores, and custom component scripting.
* **Difficulty Rating**: 2–3 / 5
* **Async Guided Study (150 min)**:
  - Micro-Videos: Langflow visual interface, RAG pipelines, agentic routing in visual graphs.
  - Readings: Langflow Core Concepts, Flowise comparison.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Designing visual agent graphs with memory buffers and custom Python components.
  - Session 2 (75 min): Exporting visual flows to Python code and integrating into API endpoints.
  - Lab Activity: Langflow Enterprise Knowledge Assistant Lab.
* **Deliverable**: Lab 3 Langflow Flow Package + Unit 3 Quiz.

### Week 4: Level 3 — Code-First Stateful Agent Graphs (LangGraph Core)
* **Theme**: Moving beyond linear DAGs to cyclical state graphs. LangGraph architecture: `StateGraph`, `TypedDict` state schema, nodes, normal edges, and conditional routing edges.
* **Difficulty Rating**: 3–4 / 5
* **Async Guided Study (150 min)**:
  - Micro-Videos: Why DAGs fail for complex agents; StateGraph fundamentals; Nodes as pure functions; Conditional edges for loop routing.
  - Readings: LangGraph Conceptual Guides, LangGraph Glossary.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Defining custom state schemas with `Annotated` reducers; compiling StateGraphs.
  - Session 2 (75 min): Implementing conditional branching: routing between research, drafting, and critique loops.
  - Lab Activity: LangGraph Cyclical Code Debugging Agent Lab.
* **Deliverable**: Lab 4 Python Script + Unit 4 Quiz (Midterm Architecture Checkpoint).

### Week 5: Level 3 — Dynamic Tool Dispatch & Persistence in LangGraph
* **Theme**: Pre-built LangGraph `ToolNode`, bind_tools, state persistence via checkpointers (MemorySaver, SqliteSaver), and conversation resumption.
* **Difficulty Rating**: 3–4 / 5
* **Async Guided Study (150 min)**:
  - Micro-Videos: ReAct graphs in LangGraph; ToolNode execution; SQLite checkpointer persistence; Thread IDs and session tracking.
  - Readings: LangGraph Tool Calling Reference, Persistence and Checkpointing.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Building a production ReAct graph with custom Pydantic tools and SQLite memory.
  - Session 2 (75 min): Resuming conversations across threads and inspecting state checkpoints.
  - Lab Activity: Tool-Augmented Research Agent with Persistent SQLite Memory.
* **Deliverable**: Lab 5 Python Script + Unit 5 Quiz.

### Week 6: Level 4 — Multi-Agent Systems & Hierarchical Supervisors
* **Theme**: Multi-agent collaboration, supervisor router pattern, specialized subagents (Researcher, Coder, Reviewer), and agent-to-agent message passing.
* **Difficulty Rating**: 4–5 / 5
* **Async Guided Study (150 min)**:
  - Micro-Videos: Single agent vs multi-agent trade-offs; Supervisor architecture; State isolation; Router decision logic.
  - Readings: LangGraph Multi-Agent Workflows, CrewAI / AutoGen comparative review.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Coding a multi-agent supervisor graph that delegates sub-tasks to specialized worker nodes.
  - Session 2 (75 min): Aggregating worker outputs into a final synthesized report.
  - Lab Activity: Multi-Agent Market Intelligence Team Lab.
* **Deliverable**: Lab 6 Python Script + Unit 6 Quiz.

### Week 7: Enterprise Safety, Human-in-the-Loop & Governance
* **Theme**: Safety governance, human-in-the-loop (HITL) breakpoints, state interrupts (`interrupt_before`, `interrupt_after`), time-travel state editing, and prompt injection defense.
* **Difficulty Rating**: 4–5 / 5
* **Async Guided Study (150 min)**:
  - Micro-Videos: Designing fail-safes for autonomous agents; Breakpoints and human approval gates; State rewind and time travel.
  - Readings: LangGraph Human-in-the-loop Guide, OWASP Top 10 for LLM Applications.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Implementing interrupt hooks for sensitive actions (financial transfers, database modifications).
  - Session 2 (75 min): Modifying graph state during interruption and resuming execution.
  - Lab Activity: Human-in-the-Loop Financial Approval System Lab.
* **Deliverable**: Lab 7 Python Script + Unit 7 Quiz.

### Week 8: Production Deployment, Telemetry & Capstone Agent Defense
* **Theme**: Telemetry and observability (LangSmith), benchmarking agent reliability, latency vs cost trade-offs, and Capstone Project defense.
* **Difficulty Rating**: 3–5 / 5
* **Async Guided Study (150 min)**:
  - Micro-Videos: Observability in agent swarms; Tracing tool calls in LangSmith; Automated agent evaluation.
  - Readings: LangSmith Evaluation Documentation, Production Agent Best Practices.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Setting up evaluation pipelines and measuring hallucination / tool failure rates.
  - Session 2 (75 min): Live Capstone Agent architecture presentations, live demo runs, and defense.
  - Lab Activity: Comprehensive Autonomous Agent Capstone Defense.
* **Deliverable**: Final Capstone Submission + Capstone Live Defense.
