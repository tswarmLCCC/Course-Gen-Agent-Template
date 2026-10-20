# Unit 1 Overview: The Spectrum of AI Agents & Foundation Assistants

Welcome to **Unit 1: The Spectrum of AI Agents & Foundation Assistants**. This foundational unit establishes the architectural mental model for autonomous artificial intelligence: moving beyond static prompt-completion interactions into dynamic, goal-directed agentic loops. You will examine the core anatomy of an agent (Perception, Reasoning, Memory, and Action), compare leading foundation model architectures (Google Gemini Spark and Anthropic Claude), and construct a pure-Python ReAct reasoning engine from scratch.

---

## Instructional Time Budget (300 Contact Minutes)

Each week is budgeted for **300 minutes of structured instructional engagement**:
* **Asynchronous Guided Learning (150 Minutes)**:
  - Micro-Video 1.1: What Makes an Agent? Perception, Reasoning & Action Loops (8 min)
  - Micro-Video 1.2: The ReAct Pattern: Synergizing Reasoning & Acting in LLMs (8 min)
  - Micro-Video 1.3: Google Gemini Spark vs. Anthropic Claude Tooling Paradigms (7 min)
  - Micro-Video 1.4: Pure-Python ReAct Implementation: Scratchpads & Tool Execution (7 min)
  - Curated Readings: Yao et al. ReAct Paper, Claude Tool Use & Gemini Function Calling (~60 min)
  - Formative Self-Check Drills: ReAct execution tracing and payload analysis (~30 min)
  - Socratic AI Practice Drill: "Agent Zero on Prompt Chaining vs. Autonomous Tool Use" (~30 min)
* **Synchronous Active Learning & Practical Lab (150 Minutes)**:
  - Session 1 (75 min): Architecture breakdown: Tool schemas (JSON Schema / Pydantic) and dispatching Python function calls.
  - Session 2 (75 min): Live-coding a pure-Python ReAct loop with multi-tool dispatch and loop termination guards.
  - Practical Lab: Building a Multi-Tool ReAct Agent from Scratch.

---

## Weekly Learning Objectives & Competency Alignment

By the end of this unit, you will be able to:
1. **Classify the 4 Levels of AI Agents**: Differentiate Level 1 Conversational Assistants, Level 2 Visual Workflow Automations, Level 3 Stateful Code Graphs, and Level 4 Autonomous Swarms. *(CLO 1 — Understanding)*
2. **Deconstruct the Core Agent Loop**: Map the continuous interaction between an agent's Cognitive Core (LLM), Internal State/Memory, Environment Observation, and Tool Execution. *(CLO 1 — Analyzing)*
3. **Compare Foundation Model Tooling**: Contrast Google Gemini's multimodal function calling against Anthropic Claude's tool use protocols and computer use interfaces. *(CLO 1, CLO 4 — Evaluating)*
4. **Implement the ReAct Framework**: Build a working Reasoning + Acting loop in pure Python that iterates through Thought &rarr; Action &rarr; Observation &rarr; Final Answer cycles. *(CLO 1, CLO 4 — Creating)*
5. **Enforce Safety & Loop Guards**: Implement recursion limits, execution timeout boundaries, and graceful error handling on tool failures. *(CLO 5 — Evaluating)*

---

## Weekly Roadmap & Deliverables

| Step | Activity | Location | Estimated Time | Deliverable |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Watch Micro-Lectures 1.1–1.4 | Asynchronous Modules | 30 min | Lecture Notes |
| **2** | Complete Curated Readings | `async/study_guide.md` | 60 min | Reading Comprehension |
| **3** | Formative Self-Check Drills | `async/self_check_drills.md` | 30 min | Self-Assessment |
| **4** | Socratic AI Practice Drill | `async/learn_with_ai.md` | 30 min | Discussion Debrief |
| **5** | Synchronous Class Meetings | Live Sessions 1 & 2 | 150 min | In-Class Challenges |
| **6** | Complete Applied Lab 1 | `guides/student_lab_guide.md` | Lab Block | `lab1_yourlastname.py` (50 pts) |
| **7** | Unit 1 Knowledge Check | Canvas Quiz Module | 30 min | Canvas Quiz (30 pts) |
