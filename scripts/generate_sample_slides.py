#!/usr/bin/env python3
"""
Generate Sample Unit 1 Presentation Slide Deck for AINT 2050
Uses scripts/slide_engine.py to programmatically create a 16:9 widescreen,
WCAG 2.1 AAA high-contrast PowerPoint (.pptx) presentation.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from slide_engine import SlideEngine


def build_unit_01_deck(output_pptx_path: str):
    print(f"Generating 16:9 Widescreen Presentation: {output_pptx_path}")
    prs = SlideEngine.create_presentation()

    # -------------------------------------------------------------------------
    # Slide 1: Split-Hero Title Slide
    # -------------------------------------------------------------------------
    SlideEngine.build_split_hero_title(
        prs,
        badge="AINT 2050 LECTURE",
        title="The AI Agent Spectrum & Foundation Assistants",
        subtitle="From Conversational Spark to ReAct Cognitive Loops & Tool Calling",
        metadata="Instructor: Tim Swarm | Laramie County Community College\nCourse: AINT 2050 - Fall 2026",
        hero_badge="AINT",
        hero_sub="Artificial Intelligence & Autonomous Systems",
        notes=(
            "Welcome students to AINT 2050: Applied AI Agent Architectures. Emphasize that our goal this semester "
            "is demystifying the buzzword 'agent' by examining the exact engineering primitives that separate "
            "conversational chatbots from truly autonomous, tool-calling systems. "
            "Today's roadmap covers the Agent Maturity Spectrum, Google Gemini Spark, Anthropic Claude 3.5 Sonnet, "
            "the ReAct paper architecture, OpenAPI tool schemas, and pure-Python loop execution."
        )
    )

    # -------------------------------------------------------------------------
    # Slide 2: High-Contrast Section Divider 1
    # -------------------------------------------------------------------------
    SlideEngine.build_section_divider(
        prs,
        sec_num=1,
        title="The Agent Taxonomy & Cognitive Architecture",
        subtitle="Deconstructing what transforms a probabilistic model into an autonomous actor",
        notes=(
            "Transition into the fundamental definition of agency. Explain why a large language model on its own "
            "is merely a next-token prediction engine, and how wrapping it in a feedback loop with external tools "
            "creates autonomous agency."
        )
    )

    # -------------------------------------------------------------------------
    # Slide 3: Two-Column Comparison Card (Chatbot vs Agent)
    # -------------------------------------------------------------------------
    SlideEngine.build_two_column(
        prs,
        badge="AGENT TAXONOMY",
        title="Static Chatbot vs. Autonomous Execution Agent",
        subtitle="Contrasting single-turn probabilistic generation against cyclical observation-action loops",
        left_title="Static Conversational LLM",
        left_items=[
            ("Single-Turn Inference", "User inputs prompt; model emits tokens until stop token is reached."),
            ("Stateless Isolation", "Model cannot inspect runtime state or verify factual claims against live systems."),
            ("No Environmental Actuation", "Outputs passive recommendations; cannot query databases or invoke APIs directly."),
            ("Hallucination Vulnerability", "Fills knowledge voids with plausible probabilistic tokens without verification.")
        ],
        right_title="Autonomous Agent Architecture",
        right_items=[
            ("Iterative Cognitive Loop", "Operates within an autonomous loop (Thought -> Action -> Observation)."),
            ("External Tool Dispatch", "Translates intent into structured OpenAPI/JSON Schema function calls."),
            ("Environmental Grounding", "Inspects tool observation outputs and self-corrects based on runtime error logs."),
            ("Goal-Driven Autonomy", "Executes multi-step sub-goals until meeting deterministic completion criteria.")
        ],
        notes=(
            "Walk students through the differences. Highlight that an agent is an architecture, not just a model. "
            "The model acts as the reasoning engine (CPU), the prompt trajectory acts as RAM, and tools act as I/O peripherals."
        )
    )

    # -------------------------------------------------------------------------
    # Slide 4: Full-Width Process Flow Card (The 3-Level Spectrum)
    # -------------------------------------------------------------------------
    SlideEngine.build_full_width_card(
        prs,
        badge="THE SPECTRUM",
        title="The 3-Level Agent Spectrum: From Spark to Stateful Graphs",
        subtitle="The progression of autonomous AI architecture across enterprise software engineering",
        card_title="Architectural Tiers of AI Agency",
        items=[
            ("Level 1: Conversational Assistants & Tool Callers", "Foundation models (Google Gemini 1.5, Anthropic Claude 3.5 Sonnet) capable of structured reasoning, zero-shot tool selection, and linear ReAct loops within client runtimes."),
            ("Level 2: Visual Workflow Orchestrators", "Low-code canvas environments (n8n, Langflow) connecting models to event-driven webhooks, modular memory buffers, and 400+ pre-built SaaS connectors."),
            ("Level 3: Code-First Stateful Graphs", "Cyclical state machines (LangGraph) with strongly-typed schemas, persistent checkpointers, Human-in-the-Loop approval gates, and multi-agent supervisors.")
        ],
        notes=(
            "Emphasize that this three-level taxonomy guides our entire course progression. "
            "In Unit 1, we master Level 1. In Unit 2, we build Level 2 workflows in n8n and Langflow. "
            "In Unit 3 and beyond, we engineer Level 3 cyclical graphs in LangGraph."
        )
    )

    # -------------------------------------------------------------------------
    # Slide 5: High-Contrast Section Divider 2
    # -------------------------------------------------------------------------
    SlideEngine.build_section_divider(
        prs,
        sec_num=2,
        title="Foundation Assistants: Gemini Spark & Claude 3.5",
        subtitle="Harnessing million-token context windows and state-of-the-art tool orchestration",
        notes=(
            "Introduce the two leading frontier models powering modern agent development: Google Gemini 1.5 Pro "
            "and Anthropic Claude 3.5 Sonnet. Compare their operational capabilities."
        )
    )

    # -------------------------------------------------------------------------
    # Slide 6: Two-Column Comparison Card (Gemini vs Claude)
    # -------------------------------------------------------------------------
    SlideEngine.build_two_column(
        prs,
        badge="MODEL FRONTIER",
        title="Foundation Leaders: Google Gemini 1.5 Pro vs. Anthropic Claude 3.5",
        subtitle="Evaluating architectural strengths for enterprise agent backends",
        left_title="Google Gemini 1.5 Pro",
        left_items=[
            ("Massive Context Window", "Native 1M to 2M+ token window enables ingesting entire codebases and hour-long videos."),
            ("Multimodal Grounding", "Natively perceives video streams, audio waveforms, images, and text simultaneously."),
            ("Gemini Spark Integration", "High-speed token throughput for real-time conversational streaming and quick tool triage."),
            ("System Instructions", "Deterministic developer instruction framing separating system rules from user input.")
        ],
        right_title="Anthropic Claude 3.5 Sonnet",
        right_items=[
            ("Industry-Leading Coding", "Top benchmark accuracy on SWE-bench for complex multi-file refactoring and debugging."),
            ("Artifacts & Computer Use", "Perceives GUI screens, moves cursor coordinates, and interacts with desktop apps."),
            ("Structured Tool Formatting", "Exceptional JSON schema fidelity with minimal hallucination of argument parameters."),
            ("Nuanced Reasoning", "Superior adherence to edge-case safety constraints and ethical system guardrails.")
        ],
        notes=(
            "Discuss when to use which model. Gemini is unbeatable for large-context ingestion and multimodal analysis. "
            "Claude 3.5 Sonnet is the gold standard for agentic coding, precise tool calling, and structured JSON generation."
        )
    )

    # -------------------------------------------------------------------------
    # Slide 7: Monospace Code Syntax Container (JSON Schema Contract)
    # -------------------------------------------------------------------------
    SlideEngine.build_code_slide(
        prs,
        badge="TOOL CONTRACTS",
        title="Standardizing Tool Signatures via OpenAPI & JSON Schema",
        subtitle="The universal interface bridging language models to native system functions",
        spec_title="Tool Declaration Specification",
        spec_items=[
            ("Contract Standard", "OpenAPI 3.0 / JSON Schema parameter dictionary."),
            ("Type Constraints", "Explicit data types (string, integer, number, boolean, array)."),
            ("Property Descriptions", "Provides the semantic rationale guiding the LLM when to pick this tool."),
            ("Required Enforcement", "Prevents runtime KeyErrors by mandating essential arguments.")
        ],
        code_snippet="""{
  "name": "lookup_customer_tier",
  "description": "Queries CRM for customer membership tier and balance.",
  "parameters": {
    "type": "object",
    "properties": {
      "customer_id": {
        "type": "string",
        "description": "Unique ID format 'cust_1234'"
      },
      "include_history": {
        "type": "boolean",
        "description": "Whether to fetch historical billing records."
      }
    },
    "required": ["customer_id"]
  }
}""",
        notes=(
            "Explain that the LLM never executes Python code directly in Level 1; it reads this JSON schema, "
            "generates a JSON payload matching the arguments, and emits it to the host Python engine. "
            "The host validates the schema and executes the local function."
        )
    )

    # -------------------------------------------------------------------------
    # Slide 8: Full-Width Process Flow Card (ReAct Framework)
    # -------------------------------------------------------------------------
    SlideEngine.build_full_width_card(
        prs,
        badge="COGNITIVE FRAMEWORK",
        title="The ReAct Paradigm: Synergizing Reasoning and Acting",
        subtitle="How language models decompose complex queries into iterative problem-solving steps",
        card_title="The 3-Stage ReAct Execution Cycle (Yao et al., 2022)",
        items=[
            ("Phase 1: Thought (Internal Reasoning)", "The agent articulates its internal reasoning, breaks down the user request into sub-problems, and determines whether an external tool is required."),
            ("Phase 2: Action (Tool Selection & Dispatch)", "The agent emits a formatted action token identifying the specific tool name and serializes the parameter values into a structured JSON string."),
            ("Phase 3: Observation (Environment Feedback)", "The execution engine runs the function, captures the return payload or error message, and injects it back into context as working memory.")
        ],
        notes=(
            "Detail the seminal ReAct paper by Yao et al. Emphasize that reasoning without acting causes hallucination, "
            "while acting without reasoning leads to aimless tool thrashing. The combination produces robust autonomous behavior."
        )
    )

    # -------------------------------------------------------------------------
    # Slide 9: Monospace Code Syntax Container (Pure-Python ReAct Engine)
    # -------------------------------------------------------------------------
    SlideEngine.build_code_slide(
        prs,
        badge="ENGINEERING",
        title="Pure-Python ReAct Engine Execution Loop",
        subtitle="Deterministic host orchestration with regex parsing and loop guardrails",
        spec_title="Runtime Safeguards",
        spec_items=[
            ("Max Iteration Cap", "Hard stops runaway loops if the model fails to reach a final answer."),
            ("Exception Interception", "Catches runtime tool crashes and passes error text as an observation."),
            ("Regex Dispatch", "Extracts 'Action: tool' and 'Action Input: json' tokens cleanly."),
            ("Trajectory Logging", "Preserves immutable episodic history across every step.")
        ],
        code_snippet="""for step in range(max_iterations):
    response = call_llm(scratchpad)
    if "Final Answer:" in response:
        return extract_answer(response)
    
    action, action_input = parse_action(response)
    try:
        obs = tool_registry.execute(action, action_input)
    except Exception as ex:
        obs = f"ToolExecutionError: {str(ex)}"
        
    scratchpad += f"\\nObservation: {obs}\\n"
raise RuntimeError("Max iterations reached")""",
        notes=(
            "Walk through the Python execution loop. Point out how exceptions are caught and passed back as observations. "
            "This gives the model the opportunity to self-heal rather than crashing the host process."
        )
    )

    # -------------------------------------------------------------------------
    # Slide 10: High-Contrast Section Divider 3
    # -------------------------------------------------------------------------
    SlideEngine.build_section_divider(
        prs,
        sec_num=3,
        title="Bridging the Spectrum: Visual & Graph Systems",
        subtitle="Understanding how Level 1 loops evolve into n8n visual flows and LangGraph state machines",
        notes=(
            "Connect today's Level 1 fundamentals with the rest of the course. Explain why writing raw loops "
            "is necessary for foundational comprehension, but why enterprise architectures require visual tools "
            "and state graph engines."
        )
    )

    # -------------------------------------------------------------------------
    # Slide 11: Two-Column Comparison Card (Level 2 vs Level 3)
    # -------------------------------------------------------------------------
    SlideEngine.build_two_column(
        prs,
        badge="ADVANCED ARCHITECTURES",
        title="Level 2 (Visual Orchestration) vs. Level 3 (Stateful Graphs)",
        subtitle="Comparing low-code visual canvases against code-first cyclical state machines",
        left_title="Level 2: Visual Canvases (n8n & Langflow)",
        left_items=[
            ("Visual DAG Nodes", "Drag-and-drop connectors for webhooks, models, and memory buffers."),
            ("Enterprise Integrations", "400+ pre-built SaaS connectors to Slack, Jira, Salesforce, Stripe."),
            ("Operational Velocity", "Non-engineering operations teams can inspect and modify business rules."),
            ("Trade-off", "Struggles with arbitrary cyclical backtracking and deep state machines.")
        ],
        right_title="Level 3: Stateful Graphs (LangGraph)",
        right_items=[
            ("Cyclical StateGraph", "Allows true cycles (Draft -> Test -> Analyze -> Patch -> Retest)."),
            ("Strongly Typed State", "TypedDict schema acts as immutable, version-controlled source of truth."),
            ("Persistent Checkpointing", "MemorySaver and SQLite snapshots allow session pause and resumption."),
            ("Human-in-the-Loop", "Native breakpoints pause execution before high-risk actions.")
        ],
        notes=(
            "Preview Units 02 and 03. Emphasize that professional AI engineers know when to deploy a visual tool "
            "like n8n for rapid webhook integrations, and when to architect a LangGraph state machine for complex "
            "self-healing systems."
        )
    )

    # -------------------------------------------------------------------------
    # Slide 12: Full-Width Process Flow Card (Safety & Production Guardrails)
    # -------------------------------------------------------------------------
    SlideEngine.build_full_width_card(
        prs,
        badge="PRODUCTION GUARDRAILS",
        title="Enterprise Agent Safety: 3-Layer Defensive Architecture",
        subtitle="Preventing runaway billing, prompt injections, and destructive tool executions",
        card_title="The Defensive Production Guardrail Stack",
        items=[
            ("Layer 1: Deterministic Iteration & Cost Caps", "Enforce strict execution timeouts and recursion limits (e.g., maximum 5 iterations) to prevent runaway billing loops when tools fail."),
            ("Layer 2: Strict Client-Side Schema Validation", "Validate all LLM tool arguments using Pydantic and JSON Schema before function dispatch to prevent invalid arguments or injection attacks."),
            ("Layer 3: Human-in-the-Loop (HITL) Gateways", "Require cryptographic signatures and manual human approval for any destructive operations (e.g., database drops, financial refunds > $100).")
        ],
        notes=(
            "Highlight production safety. Without these 3 layers, autonomous agents can enter expensive loops, "
            "crash downstream systems, or execute unauthorized operations."
        )
    )

    # -------------------------------------------------------------------------
    # Slide 13: Split-Hero Title (Applied Lab Mission)
    # -------------------------------------------------------------------------
    SlideEngine.build_split_hero_title(
        prs,
        badge="APPLIED LAB MISSION",
        title="Unit 01 Lab: Pure-Python Multi-Tool ReAct Agent",
        subtitle="Implementing Schemas, Dynamic Dispatching, and Recursion Guardrails",
        metadata="Due Date: Sunday 11:59 PM | SpeedGrader Submission\nDeliverable: lab1_starter.py (Passing 100% Assertions)",
        hero_badge="LAB 1",
        hero_sub="Applied Hands-On Engineering",
        notes=(
            "Conclude the lecture and introduce Applied Lab 01. Review the requirements: "
            "students will build a pure-Python ReAct engine from scratch, implement tool schemas, "
            "dispatch function calls, and verify execution using automated unit tests."
        )
    )

    # Save presentation
    os.makedirs(os.path.dirname(os.path.abspath(output_pptx_path)), exist_ok=True)
    prs.save(output_pptx_path)
    print(f"Presentation saved successfully ({len(prs.slides)} slides): {output_pptx_path}")


if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(SCRIPT_DIR), "presentations")
    output_path = os.path.join(output_dir, "AINT_2050_Unit_01_Presentation.pptx")
    build_unit_01_deck(output_path)
