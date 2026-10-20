# AINT 2050: Master External Resources Guide

This document indexes verified, authoritative documentation, research papers, visual tools, and video lectures for **AINT 2050: Applied AI Agent Architectures: From Conversational Spark to LangGraph Systems**.

---

## 1. Foundational Research Papers
- **ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., ICLR 2023):**
  - [arXiv:2210.03629](https://arxiv.org/abs/2210.03629) — The seminal paper introducing the Thought-Action-Observation interleaving loop.
- **Toolformer: Language Models Can Teach Themselves to Use Tools (Schick et al., 2023):**
  - [arXiv:2302.04761](https://arxiv.org/abs/2302.04761) — Self-supervised tool learning.
- **Reflexion: Language Agents with Verbal Reinforcement Learning (Shinn et al., 2023):**
  - [arXiv:2303.11366](https://arxiv.org/abs/2303.11366) — Dynamic memory and self-critique loops.

---

## 2. Official Platform & Framework Documentation

### Level 1: Foundation Models & Tool Calling
- **Google Gemini API & AI Studio:**
  - [Gemini Function Calling Documentation](https://ai.google.dev/gemini-api/docs/function-calling) — How Gemini generates structured tool calls.
  - [Google Gemini System Instructions Guide](https://ai.google.dev/gemini-api/docs/system-instructions) — Persona and constraint steering.
- **Anthropic Claude:**
  - [Claude Tool Use (Function Calling)](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — Strict tool execution format.
  - [Claude Computer Use API](https://docs.anthropic.com/en/docs/build-with-claude/computer-use) — Groundbreaking desktop GUI control.

### Level 2: Visual & Low-Code Workflow Engines
- **n8n AI Workflow Automation:**
  - [n8n AI Agent Node Documentation](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/) — Connecting LLMs to webhooks, tools, and enterprise databases.
- **Langflow:**
  - [Langflow Documentation](https://docs.langflow.org/) — Drag-and-drop component-based AI agent builder.

### Level 3 & 4: Code-First Stateful Agent Graphs
- **LangChain & LangGraph:**
  - [LangGraph Official Documentation](https://langchain-ai.github.io/langgraph/) — Authoritative guide for cyclical state machines.
  - [LangGraph Conceptual Guides](https://langchain-ai.github.io/langgraph/concepts/) — State, Nodes, Edges, Checkpointing, and Human-in-the-loop.
  - [LangSmith Observability](https://docs.smith.langchain.com/) — Production tracing and agent evaluation.

---

## 3. High-Yield Video Lectures & Walkthroughs

| Unit | Topic | Video Source | Focus Concepts |
| :---: | :--- | :--- | :--- |
| **Unit 1** | Prompting to Autonomous ReAct | DeepLearning.AI | ReAct pattern, observation scratchpads, tool dispatching. |
| **Unit 2** | n8n Visual AI Agent Workflows | n8n Official Channel | Setting up AI Agent nodes, injecting tools, webhook triggers. |
| **Unit 3** | Building Visual Graphs in Langflow | DataStax / Langflow | Component wiring, vector stores, API export. |
| **Unit 4** | LangGraph Architecture & StateGraphs | LangChain YouTube | StateGraph vs DAGs, TypedDict state, conditional edges. |
| **Unit 5** | Tools & Checkpointing in LangGraph | Harrison Chase (LangChain) | MemorySaver, SqliteSaver, thread IDs, state replay. |
| **Unit 6** | Multi-Agent Supervisor Networks | LangChain Multi-Agent Series | Supervisor routing, specialized worker graphs. |
| **Unit 7** | Human-in-the-Loop & Time Travel | LangChain Advanced Series | Breakpoints, state interrupts, human approval workflows. |
| **Unit 8** | Production Evaluation with LangSmith | LangSmith Production Series | Tracing latency, token spend, automated evaluators. |
