# Unit 1: Video Micro-Lecture Production Scripts

These verbatim instructional scripts provide the exact blueprints for recording the bite-sized video micro-lectures for **Unit 1: The Spectrum of AI Agents & Foundation Assistants**.

---

## Micro-Video 1.1: What Makes an Agent? Perception, Reasoning & Action Loops
* **Duration:** 8 Minutes (0:00 – 8:00)
* **Visual Asset:** Slide 3 & Slide 4 (Architecture & Agency Spectrum)

### Verbatim Recording Script
**[0:00 - 1:30] Welcome & The Agency Revolution**  
"Hello everyone, and welcome to Unit 1 of Applied AI Agent Architectures. For the past two years, the world has been fascinated by generative AI: asking a chatbot a question, and watching it generate text. But text completion is not agency. 

An agent does not just talk; an agent **acts**. An agent perceives an objective from its environment, reasons through a sequence of steps, executes tools to interact with real-world systems, observes the results, and adapts its behavior until the goal is achieved. Today, we begin our journey across the entire agency spectrum: from foundation models like Gemini and Claude, to visual workflow platforms like n8n and Langflow, all the way to production code-first state graphs in LangGraph."

**[1:30 - 4:00] The 4 Levels of AI Agents**  
"To design effective systems, we must categorize agents into four distinct tiers:
Level 1: Prompt-Driven Assistants. These are models like Google Gemini Spark or Claude Projects. They operate in a linear, turn-based dialog. They can call tools, but the user is in the driver's seat for every step.

Level 2: Visual Workflow Automations. Tools like n8n and Langflow. Here, we connect LLMs to drag-and-drop nodes: webhooks, Slack alerts, CRM queries, and vector databases. It allows rapid integration without writing hundreds of lines of glue code.

Level 3: Code-First Stateful Agent Graphs. This is LangGraph. When workflows need cyclical loops—where an agent writes code, runs tests, reads the error, and modifies the code in a loop until it passes—linear flows break down. LangGraph gives us stateful cyclical graphs with persistent memory and human approval breakpoints.

Level 4: Multi-Agent Swarms. Networks of specialized subagents—like a researcher, a coder, and a reviewer—collaborating under a supervisor agent to solve massive problems."

**[4:00 - 6:30] Anatomy of an Agent**  
"Every agent, regardless of complexity, consists of four fundamental components:
First, Perception: how the agent receives inputs—user text, webhook events, or files.
Second, the Cognitive Core: the LLM reasoning engine, such as Claude 3.5 Sonnet or Gemini 1.5 Pro.
Third, Memory: both short-term working scratchpads and long-term persistent storage.
And fourth, the Tool Engine: the deterministic functions—APIs, calculators, database drivers—that let the model affect reality."

**[6:30 - 8:00] Summary & Next Steps**  
"In our next micro-lecture, we will examine the cognitive pattern that made autonomous tool use reliable: the ReAct framework. See you in Video 1.2!"

---

## Micro-Video 1.2: The ReAct Pattern: Synergizing Reasoning & Acting in LLMs
* **Duration:** 8 Minutes (0:00 – 8:00)
* **Visual Asset:** Slide 4 (ReAct Process Flow)

### Verbatim Recording Script
**[0:00 - 2:00] Why Raw Language Models Hallucinate**  
"Welcome back! In Micro-Lecture 1.2, we explore the breakthrough reasoning pattern that powers modern agents: ReAct, or Reasoning plus Acting.

Why do raw LLMs hallucinate? Because language models are probabilistic token predictors. When you ask an LLM, 'What was the exact revenue of Acme Corp in Q3?', the model doesn't have an internal database of real-time facts. It predicts tokens that *look* like plausible business numbers. 

If we want fact-grounded answers, we must give the model tools. But if we *only* give it tools without reasoning, it struggles to decompose complex questions. That is where ReAct comes in."

**[2:00 - 5:30] The Thought-Action-Observation Loop**  
"In 2022, researchers at Princeton and Google introduced ReAct. Instead of asking the model for an immediate answer, ReAct forces the model to interleave its reasoning into three explicit phases:
First, Thought: The model generates an internal monologue explaining what it needs to find out. For example: 'Thought: I need to check the user's account balance before determining refund eligibility.'
Second, Action: The model produces a structured tool call. For example: `Action: query_account_balance(user_id=104)`.
Third, Observation: The host program executes the tool and injects the ground truth back into the model's prompt: `Observation: Balance is $12.50`.

The model then repeats this cycle: Thought 2, Action 2, Observation 2. Only when it has gathered sufficient facts does it emit: `Final Answer: Your refund of $12.50 has been approved.`"

**[5:30 - 7:00] Why ReAct Changes Everything**  
"This pattern achieves two massive engineering breakthroughs:
1. Grounded Interpretability: Humans can read the exact reasoning trajectory of the agent. If it fails, you can see whether it reasoned incorrectly or called the wrong tool.
2. Error Recovery: If a tool returns an error—like 'User Not Found'—the agent reads that in the Observation and can try an alternative search."

**[7:00 - 8:00] Wrap-up**  
"Next up, we compare how the two premier frontier models—Google Gemini and Anthropic Claude—implement tool calling under the hood. Join me in Video 1.3!"

---

## Micro-Video 1.3: Google Gemini Spark vs. Anthropic Claude Tooling Paradigms
* **Duration:** 7 Minutes (0:00 – 7:00)
* **Visual Asset:** Slide 6 (Tool Declaration Schemas)

### Verbatim Recording Script
**[0:00 - 2:30] Google Gemini: Multimodal Speed & Function Calling**  
"Welcome to Micro-Lecture 1.3. Today, we contrast the two leading foundation model ecosystems: Google Gemini and Anthropic Claude.

Google Gemini represents the pinnacle of native multimodality. Unlike models where vision is added as an adapter, Gemini processes video, audio, code, and text in the same unified representation. In agentic workflows, Gemini's Function Calling API adheres to the OpenAPI 3.0 specification. Gemini is blazing fast, supports enormous context windows up to 2 million tokens, and can return parallel tool calls—requesting data from three distinct APIs in a single round-trip inference."

**[2:30 - 5:00] Anthropic Claude: Strict Tool Use & Computer Use**  
"On the other side of the frontier is Anthropic Claude. Claude 3.5 Sonnet has become the industry benchmark for agentic coding and schema adherence. 

When you define a tool schema in Claude, its adherence to strict Pydantic and JSON validation is second to none. Claude rarely hallucinates non-existent arguments. Furthermore, Anthropic pioneered **Computer Use**—an agent interface where Claude receives desktop screenshots and emits mouse coordinates, keystrokes, and clicks to navigate applications like a human operator."

**[5:00 - 7:00] Architectural Selection Criteria**  
"So which should you choose?
- Use Gemini when: You need massive multimodal ingestion, live audio/video analysis, or ultra-low latency token generation (Gemini Flash).
- Use Claude when: You require complex multi-file code synthesis, strict tool parameter compliance, or direct GUI navigation."

---

## Micro-Video 1.4: Pure-Python ReAct Implementation: Scratchpads & Tool Execution
* **Duration:** 7 Minutes (0:00 – 7:00)
* **Visual Asset:** Slide 8 (Pure-Python ReAct Runtime Code)

### Verbatim Recording Script
**[0:00 - 2:00] Building the Runtime Loop**  
"Welcome back! In our final micro-lecture for Unit 1, we pull back the curtain and write a ReAct agent runtime in pure Python—no LangChain, no third-party frameworks.

Before you use powerful abstractions like LangGraph, you must understand the underlying runtime mechanics. How does an agent maintain state? Through a text buffer called the **Scratchpad**."

**[2:00 - 4:45] Walking Through the Code**  
"Let's look at the implementation:
1. We define our tools as regular Python functions—like `calculate(expr)` or `lookup_inventory(sku)`.
2. We create a `ToolRegistry` dictionary mapping string names to function pointers.
3. In our main loop, we pass the user's question along with the accumulated scratchpad into the LLM.
4. When the LLM outputs an action, our regex parser extracts the tool name and argument.
5. We execute the tool, capture the return string, and append it as `Observation X: ...` to the scratchpad.
6. The loop repeats until the LLM emits `Final Answer:`."

**[4:45 - 6:30] The Golden Safety Rule: Recursion Limits**  
"Notice line 15 in our script: `for step in range(1, max_iterations + 1)`. 
Never write `while True` in an autonomous agent! If an external API returns a 500 error or the model gets confused, an unbounded loop will burn through thousands of dollars of API tokens in minutes. A hard recursion limit ensures that your agent terminates safely if it cannot find an answer."

**[6:30 - 7:00] Lab 1 Preview**  
"In this week's Applied Lab, you will build and test this complete multi-tool ReAct engine. Check your study guide, complete the self-check drills, and let's start building in the lab!"
