# Synchronous Lesson Plan: Unit 02 - Visual Workflow Automation (n8n & Langflow)

## Session Logistics
- **Course**: AINT 2050 - Applied AI Agent Architectures
- **Unit**: Unit 02 - Visual Workflow Automation with n8n and Langflow
- **Total Duration**: 150 Synchronous Minutes (or Two 75-Minute Sessions)
- **Format**: Active Learning, Live Node Architecture Demonstration, Paired Coding & Lab Clinic

---

## 150-Minute Unified Schedule Breakdown

### Part 1: Architectural Deep Dive & Live Node Dissection (45 min)
- **00-15 min: Concept Review**:
  - The Level 2 paradigm: Visual graphs vs. imperative loops.
  - Reviewing the n8n AI Agent node topology: model node, tool node, memory node plugs.
  - Inspecting Langflow's visual RAG canvas: splitters, embeddings, vector stores.
- **15-30 min: Live Demonstration**:
  - Instructor boots local n8n instance in Docker / Codespaces.
  - Constructing a live incoming Webhook node (`POST /webhook/support-ticket`).
  - Binding Claude 3.5 Sonnet Chat Model and an HTTP Tool node querying a mock customer database.
- **30-45 min: Socratic Q&A & Error Demonstration**:
  - Deliberately triggering an HTTP 500 error in the tool node.
  - Demonstrating how "Continue On Fail" and error nodes prevent pipeline crashes.

### Part 2: Synchronous Paired Coding Challenge (30 min)
- **45-70 min: In-Class Challenge**:
  - Students pair up and run `sync/inclass_challenges.py`.
  - Challenge: Complete the visual-graph simulation engine that parses a node graph JSON schema, executes simulated webhook triggers, and routes data to the correct tool handlers.
- **70-75 min: Challenge Debrief**:
  - Review student solutions and discuss parameter mapping edge cases.

### Part 3: Guided Applied Laboratory Clinic (60 min)
- **75-80 min: Lab 02 Mission Briefing**:
  - Reviewing `guides/student_lab_guide.md`: Automated Customer Operations Agent with Webhook Dispatcher.
  - Inspecting the automated test assertions in `guides/lab2_starter.py`.
- **80-135 min: Independent / Paired Engineering**:
  - Students implement the webhook handler, node routing logic, and tool dispatchers.
  - Instructor circulates for live debugging assistance.

### Part 4: Code Review, Rubric Alignment & Debrief (15 min)
- **135-145 min: Verification Clinic**:
  - Students run automated unit tests and check against the 100-point rubric in `assessments/lab_rubric.md`.
- **145-150 min: Preview of Unit 03**:
  - Previewing Level 3: Moving beyond DAGs to cyclic state graphs in LangGraph.
