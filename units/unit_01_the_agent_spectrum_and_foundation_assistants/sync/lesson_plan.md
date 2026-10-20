# Synchronous Lesson Plan: Unit 1

**Course:** AINT 2050: Applied AI Agent Architectures  
**Topic:** The Agent Spectrum, ReAct Reasoning Loops & Tool Schemas  
**Format:** Accelerated Active Learning (Options for Two 75-Minute Sessions or One 150-Minute Block)  

---

## Delivery Track Option A: Two 75-Minute Sessions

### Session 1: The Agent Taxonomy & Foundation Model Tooling (75 min)
* **0:00 – 0:10 (10 min) The Live Hallucination Probe:**
  - Ask an ungrounded LLM a complex math or real-time fact question without tools. Show the hallucination.
  - Introduce the core question: *How do we make LLMs reliably interact with external truth?*
* **0:10 – 0:25 (15 min) The 4 Levels of Agency Whiteboard:**
  - Walk through Slide 3 (Prompt Assistants vs. Stateful Graphs).
  - Define the 4 levels: Level 1 (Gemini/Claude), Level 2 (n8n/Langflow), Level 3 (LangGraph), Level 4 (Swarms).
* **0:25 – 0:45 (20 min) The ReAct Pattern & Tool Schemas:**
  - Run `part1_agent_taxonomy_and_react.py` and `part2_function_calling_schemas.py`.
  - Trace the Thought-Action-Observation loop step by step.
* **0:45 – 1:05 (20 min) Collaborative In-Class Challenge 1:**
  - Students pair up to solve Challenge 1 in `sync/inclass_challenges.py` (Building Tool Registries & Dispatchers).
* **1:05 – 1:15 (10 min) Debrief & Socratic Q&A:**
  - Cold-call pairs to explain why string return formats are critical in tool observations.

### Session 2: Pure-Python ReAct Runtime & Lab 1 Kickoff (75 min)
* **0:00 – 0:10 (10 min) Warm-Up: Detecting Recursion Traps:**
  - Present a broken agent loop and have students identify missing `max_iterations` guards.
* **0:10 – 0:25 (15 min) Live Coding: Scratchpads & State Reducers:**
  - Run `part3_state_and_memory.py`.
  - Demonstrate formatting prompt scratchpads and handling tool exceptions without crashing.
* **0:25 – 0:45 (20 min) Collaborative Challenge 2:**
  - Students solve Challenge 2 in `sync/inclass_challenges.py` (Autonomous Multi-Step ReAct Loop).
* **0:45 – 1:10 (25 min) Applied Lab 1 Workshop:**
  - Walk through `guides/student_lab_guide.md` and `guides/lab1_starter.py`.
  - Students begin implementing Tasks 1 and 2 with live coaching.
* **1:10 – 1:15 (5 min) Wrap-Up:**
  - Remind students to test with `pytest` and upload `.py` to Canvas before Friday midnight.

---

## Delivery Track Option B: Single 150-Minute Block
* **0:00 – 0:20 (20 min):** Hallucination demonstration & The 4 Levels of Agency.
* **0:20 – 0:45 (25 min):** Deep dive: The ReAct Pattern & Tool Schemas (Gemini vs Claude).
* **0:45 – 1:15 (30 min):** Pair coding: Challenge 1 (Tool Registries & Validation).
* **1:15 – 1:25 (10 min):** Classroom Break.
* **1:25 – 1:55 (30 min):** Live coding: Pure-Python ReAct Runtime & Recursion Guards.
* **1:55 – 2:20 (25 min):** Pair coding: Challenge 2 (Multi-Step ReAct Loop).
* **2:20 – 2:45 (25 min):** Applied Lab 1 Workshop & Individual Coding.
* **2:45 – 2:50 (5 min):** Submission verification and wrap-up.
