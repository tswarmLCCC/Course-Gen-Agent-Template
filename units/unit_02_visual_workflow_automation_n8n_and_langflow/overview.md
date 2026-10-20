# Unit 02: Visual Workflow Automation with n8n and Langflow

<div class="dp-header dp-basic-bar" style="background: #1e3a8a; color: #ffffff; padding: 1.5rem; border-radius: 6px; margin-bottom: 1.5rem;">
  <h1 style="margin: 0; color: #ffffff; font-size: 1.8rem;">Unit 02: Visual Workflow Automation with n8n and Langflow</h1>
  <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Level 2 Agent Architectures: Low-Code Canvases, Webhook Triggers, and Visual RAG Pipelines</p>
</div>

---

## 1. Executive Summary & Pedagogical Context
In Unit 01, we explored Level 1 foundation assistants and coded a pure-Python ReAct engine from scratch. While pure-code loops offer total algorithmic control, enterprise organizations frequently demand rapid workflow assembly, visual observability, and plug-and-play connectivity to hundreds of software-as-a-service (SaaS) APIs.

**Unit 02 introduces Level 2 of the Agent Spectrum: Visual Workflow Orchestration.** Students examine how visual canvas environments—specifically **n8n** and **Langflow**—bridge the gap between foundation models and production enterprise infrastructure. Students will master node-based graph composition, event-driven webhook execution, memory buffering, visual tool binding, and component-based Retrieval-Augmented Generation (RAG).

---

## 2. Course Learning Outcomes (CLO) Alignment
This unit directly advances the following course learning competencies:
- **CLO 2 (Level 2 Visual Orchestration)**: Architect and configure enterprise agent workflows within low-code visual environments (n8n and Langflow), incorporating webhook triggers, tool nodes, and persistent conversation memory.
- **CLO 4 (Tool Schema & API Integration)**: Standardize OpenAPI/JSON Schema contracts for HTTP tool calling across visual and code-first platforms.
- **CLO 5 (System Safety & Guardrails)**: Implement routing filters, conditional gates, and error branches in visual flows to prevent unintended tool execution.

---

## 3. Instructional Time Budget (300 Contact Minutes)

```
========================================================================================
300 TOTAL CONTACT MINUTES
├── ASYNCHRONOUS GUIDED LEARNING (150 MIN)
│   ├── Video Micro-Lectures (40 min)
│   │   ├── Video 2.1: The Visual Node Paradigm: Why Low-Code Agents Matter (10 min)
│   │   ├── Video 2.2: n8n Architecture: AI Agent Node, Tools, & Webhook Triggers (10 min)
│   │   ├── Video 2.3: Langflow Component Canvas: RAG Pipelines & Visual Routing (10 min)
│   │   └── Video 2.4: Production Readiness: Webhooks, Error Nodes & Rate Limits (10 min)
│   ├── Architectural Documentation & Readings (50 min)
│   │   ├── n8n AI Agent Documentation & Tool Calling Guide
│   │   ├── Langflow Core Concepts & Component Reference
│   │   └── Enterprise Low-Code vs. Code-First Trade-Off Matrix
│   ├── Formative Self-Check Drills (30 min)
│   │   └── 5 interactive JSON payload tracing & node routing drills
│   └── Socratic AI Exploration (30 min)
│       └── Roleplay prompt: "Senior Solutions Architect on n8n vs. Langflow for Support Ops"
└── SYNCHRONOUS ACTIVE LEARNING & LAB (150 MIN)
    ├── Part 1: Architecture Review & Node Flow Breakdown (45 min)
    ├── Part 2: Live In-Class Webhook & Tool Binding Challenge (30 min)
    ├── Part 3: Guided Applied Laboratory Development (60 min)
    │   └── Lab 02: Automated Customer Operations Agent with Webhook Dispatcher
    └── Part 4: Code Review, SpeedGrader Rubric Alignment & Debrief (15 min)
========================================================================================
```

---

## 4. Weekly Deliverables & Gradebook Weight
- **Formative Self-Checks**: 5 interactive collapsible exercises in `async/self_check_drills.md`.
- **Synchronous Paired Coding**: In-class challenge script in `sync/inclass_challenges.py`.
- **Applied Lab 02**: `lab2_starter.py` and exported workflow configuration (40% Grade Category).
- **Unit 02 Assessment**: 15-question QTI 1.2 assessment in `assessments/unit_quiz.md` (20% Grade Category).
