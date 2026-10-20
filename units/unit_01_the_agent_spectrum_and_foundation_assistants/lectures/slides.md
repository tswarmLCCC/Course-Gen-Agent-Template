# Unit 1 Lecture Presentation: The Spectrum of AI Agents

**Course:** AINT 2050: Applied AI Agent Architectures  
**Format:** 16:9 Widescreen Presentation (WCAG 2.1 AAA Compliant)  
**Slide Archetypes Used:** Split-Hero Title, High-Contrast Section Dividers, Two-Column Comparisons, Process Flows, Monospace Code Containers  

---

### Slide 1: Split-Hero Title Slide (Archetype 1)
- **Left Hero Badge:** AINT
- **Left Program Subtitle:** Applied AI Systems & Autonomous Agents
- **Right Eyebrow:** UNIT 01 CURRICULUM
- **Main Headline:** The Spectrum of AI Agents & Foundation Assistants
- **Subtitle:** From Prompt-Driven Spark to ReAct Loops & Visual Workflows
- **Metadata:** Instructor: Tim Swarm | Laramie County Community College
- **Speaker Notes:**
  Welcome students to AINT 2050. Today we begin our deep dive into the world of AI Agents. We will demystify what turns a language model into an autonomous agent, outline the 4 levels of agency from Gemini and Claude to n8n and LangGraph, and build a pure-Python ReAct reasoning engine from scratch.

---

### Slide 2: Section Divider: The 4 Levels of Agency (Archetype 2)
- **Section Number:** SECTION 01
- **Section Title:** The Spectrum of Autonomous Agency
- **Subtitle:** From simple prompt completion to cyclical multi-agent graphs
- **Speaker Notes:**
  Transition to the agency taxonomy. Explain why distinguishing between simple prompt completion and true agentic loops is the most important mental model in modern AI engineering.

---

### Slide 3: Two-Column Comparison: Prompt Assistants vs. Stateful Graphs (Archetype 3)
- **Badge:** ARCHITECTURE
- **Headline:** Two Agent Paradigms: Linear Prompting vs. Cyclical Graphs
- **Subtitle:** Comparing conversational models against stateful graph-driven systems
- **Left Column (Ice Blue):** Level 1: Conversational Assistants (Gemini / Claude)
  - • Turn-Based Dialog: Linear request-response lifecycle driven by user input.
  - • Transient Memory: Context is bounded by the model's active window buffer.
  - • Tool Dispatch: Single-turn or basic parallel function execution.
  - • Primary Use: Interactive pair programming, dynamic drafting, ad-hoc research.
- **Right Column (Warm Cream):** Level 3: Stateful Code Graphs (LangGraph)
  - • Cyclical Execution: Arbitrary loopback edges with dynamic multi-step branching.
  - • Persistent State: Strongly-typed schemas with persistent SQLite/Postgres checkpointers.
  - • Autonomous Control: The graph routes between planning, execution, and critique nodes.
  - • Primary Use: Enterprise workflows, code debugging loops, self-healing data pipelines.
- **Speaker Notes:**
  Emphasize that Gemini and Claude are the reasoning engines, but LangGraph provides the execution scaffolding. Without a cyclical graph, prompt assistants cannot self-correct or iterate through multi-step failures.

---

### Slide 4: Full-Width Process Flow: The ReAct Reasoning Loop (Archetype 4)
- **Badge:** REASONING ENGINE
- **Headline:** The ReAct Framework: Thought &rarr; Action &rarr; Observation Loop
- **Subtitle:** How agents eliminate hallucination through continuous environment grounding
- **Card Title:** The Step-by-Step ReAct Autonomous Execution Cycle
- **Items:**
  - ► Step 1: Cognitive Thought: The LLM analyzes the user prompt and working memory, stating its immediate reasoning goal without giving direct ungrounded answers.
  - ► Step 2: Tool Action Call: The agent emits a structured tool call payload (`tool_name(args)`) adhering to a declared JSON / Pydantic schema.
  - ► Step 3: Environment Observation: The client application executes the tool (API query, shell command, database search) and returns the ground-truth result.
  - ► Step 4: Synthesis or Termination: The agent reads the observation; if sufficient, it emits `Final Answer: ...`; if not, it loops back to Step 1.
- **Speaker Notes:**
  Walk through the ReAct loop. Show why interleaving thoughts with actions prevents hallucinations: the model admits what it doesn't know, queries reality, and bases its final synthesis on verified observations.

---

### Slide 5: Section Divider: Foundation Model Tooling (Archetype 2)
- **Section Number:** SECTION 02
- **Section Title:** Foundation Model Tooling: Gemini vs. Claude
- **Subtitle:** Examining how frontier models implement structured function calling
- **Speaker Notes:**
  Compare Google Gemini Spark and Anthropic Claude. Highlight Gemini's native multimodal speed and Claude's strict JSON schema adherence and Computer Use.

---

### Slide 6: Code Syntax Container: Declaring Tool Schemas (Archetype 5)
- **Badge:** API PROTOCOLS
- **Headline:** Declaring Tool Schemas: The JSON & Pydantic Contract
- **Subtitle:** Enforcing strict parameter types to prevent hallucinated arguments
- **Left Spec Card:** Technical Specifications
  - • Schema Specification: Declare name, description, and parameter types using JSON Schema.
  - • Field Validation: Required fields guarantee essential arguments are passed.
  - • Model Steering: Descriptive docstrings guide the LLM on *when* and *how* to invoke tools.
  - • Error Boundary: Malformed payloads trigger immediate client-side validation errors.
- **Right Monospace Code Box:**
```python
# Universal Tool Declaration Schema (Gemini & Claude Compatible)
calculator_tool = {
    "name": "calculate",
    "description": "Evaluates a mathematical expression and returns the numeric result.",
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Mathematical expression string (e.g. '15 * 4.5')."
            }
        },
        "required": ["expression"]
    }
}
```
- **Speaker Notes:**
  Show students that tools are simply contracts. The LLM does NOT run the Python code; the LLM outputs a JSON payload matching your schema, and your host application executes the function.

---

### Slide 7: Section Divider: Pure-Python ReAct Implementation (Archetype 2)
- **Section Number:** SECTION 03
- **Section Title:** Building a ReAct Agent in Pure Python
- **Subtitle:** Assembling the reasoning loop, tool registry, and recursion guards
- **Speaker Notes:**
  Transition to hands-on code. Live-code the core ReAct dispatch loop.

---

### Slide 8: Code Syntax Container: The Autonomous ReAct Loop (Archetype 5)
- **Badge:** AGENT RUNTIME
- **Headline:** The ReAct Dispatch Engine: Parsing & Executing Tools
- **Subtitle:** Iterating through scratchpads with strict recursion limits
- **Left Spec Card:** Engine Specifications
  - • Scratchpad Buffer: Accumulates thought and observation history across iterations.
  - • Tool Dispatcher: Maps tool names to callable Python functions.
  - • Termination Detection: Regex detection for 'Final Answer:' terminates the loop.
  - • Recursion Guard: Hard limit (e.g. max_iterations=5) prevents infinite loops.
- **Right Monospace Code Box:**
```python
def run_react_agent(user_query: str, max_iterations: int = 5) -> str:
    scratchpad = ""
    for step in range(1, max_iterations + 1):
        prompt = f"{user_query}\n{scratchpad}\nThought {step}:"
        response = call_llm(prompt)
        scratchpad += f"\nThought {step}: {response}"
        
        if "Final Answer:" in response:
            return response.split("Final Answer:")[-1].strip()
            
        action, args = parse_action(response)
        observation = execute_tool(action, args)
        scratchpad += f"\nObservation {step}: {observation}"
        
    return "Error: Agent reached maximum recursion limit."
```
- **Speaker Notes:**
  Walk through the code line by line. Emphasize that this exact loop is what powers sophisticated agent frameworks under the hood!

---

### Slide 9: Section Divider: The Road Ahead — Low-Code & Graphs (Archetype 2)
- **Section Number:** SECTION 04
- **Section Title:** Visual Flows (n8n) to Stateful Graphs (LangGraph)
- **Subtitle:** Scaling from single scripts to visual pipelines and enterprise graph engines
- **Speaker Notes:**
  Preview the rest of the course: Unit 2 will look at visual orchestration in n8n, Unit 3 at Langflow, and Units 4–8 will master LangGraph.

---

### Slide 10: Two-Column Comparison: n8n vs Langflow vs LangGraph (Archetype 3)
- **Badge:** ORCHESTRATION
- **Headline:** Choosing Your Agent Framework: Visual vs. Code-First
- **Subtitle:** When to drag-and-drop vs. when to write stateful graph code
- **Left Column (Ice Blue):** Visual Orchestrators (n8n / Langflow)
  - • Visual Canvas: Drag-and-drop nodes for quick prototype assembly.
  - • 400+ Connectors: Built-in nodes for Slack, Salesforce, Notion, PostgreSQL.
  - • Low Technical Barrier: Non-developers can inspect and adjust workflows.
  - • Limitation: Challenging to implement complex state reducers or dynamic swarms.
- **Right Column (Warm Cream):** Code-First Graphs (LangGraph)
  - • Python Native: Full power of Python data structures, debugging, and git version control.
  - • Arbitrary State: Define typed states with custom reducers and persistent checkpointers.
  - • Human-in-the-Loop: Built-in breakpoints and state inspection hooks.
  - • Limitation: Requires strong software engineering and graph modeling skills.
- **Speaker Notes:**
  Explain that enterprise architects use both: n8n for rapid integrations and alerting, and LangGraph for core autonomous reasoning and cyclical debugging systems.

---

### Slide 11: Full-Width Content Card: Lab 1 Engineering Blueprint (Archetype 4)
- **Badge:** APPLIED LABORATORY
- **Headline:** Lab 1: Multi-Tool ReAct Agent from Scratch
- **Subtitle:** Engineering a deterministic autonomous agent without third-party frameworks
- **Card Title:** Required Technical Deliverables & Specifications
- **Items:**
  - ► Task 1: Tool Registry & Schema Declarations: Declare strict tool schemas for calculator, unit conversion, and database lookup tools.
  - ► Task 2: Dispatcher & Safe Execution Engine: Implement dynamic tool execution with parameter validation and exception isolation.
  - ► Task 3: Autonomous ReAct Reasoning Engine: Build the iterative loop maintaining scratchpad state and detecting termination.
  - ► Task 4: Automated Verification Suite: Run all embedded assertion tests verifying multi-step tool chaining and recursion limits.
- **Speaker Notes:**
  Introduce Lab 1. Remind students that building the loop from scratch is essential before using higher-level abstractions like LangGraph.

---

### Slide 12: Split-Hero Summary Slide (Archetype 1)
- **Left Hero Badge:** MASTERY
- **Left Program Subtitle:** Unit 01 Checkpoint
- **Right Eyebrow:** KEY TAKEAWAYS
- **Main Headline:** Agent Foundations Mastered: Moving to Visual Flows
- **Subtitle:** Core Principles Established & Lab Deliverables
- **Metadata:** Homework: Complete Lab 1 & Unit 1 Quiz by Friday Midnight
- **Speaker Notes:**
  Conclude the presentation. Congratulate students on mastering Unit 1 concepts. Open the floor for active learning questions.
