#!/usr/bin/env python3
"""
Generate Unit 2 Presentation Slide Deck for AINT 2050
Uses scripts/slide_engine.py to create a 16:9 widescreen, WCAG 2.1 AAA PowerPoint (.pptx).
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from slide_engine import SlideEngine

def build_unit_02_deck(output_paths):
    prs = SlideEngine.create_presentation()

    # Slide 1: Split-Hero Title Slide
    SlideEngine.build_split_hero_title(
        prs,
        badge="AINT 2050 LECTURE",
        title="Visual Workflow Automation with n8n and Langflow",
        subtitle="Bridging Imperative Code and Enterprise Low-Code AI Topologies",
        metadata="Instructor: Tim Swarm | Laramie County Community College\nCourse: AINT 2050 - Fall 2026",
        hero_badge="AINT",
        hero_sub="Artificial Intelligence & Autonomous Systems",
        notes="Welcome to Unit 02 of Applied AI Agent Architectures. Today we step up from Level 1 foundation assistants into Level 2: Visual Workflow Orchestration with n8n and Langflow."
    )

    # Slide 2: Section Divider
    SlideEngine.build_section_divider(
        prs,
        sec_num=1,
        title="The Visual Node Paradigm",
        subtitle="Why modern enterprise operations need low-code AI workflows",
        notes="We explore why raw Python scripts do not scale across cross-functional operations teams and how visual DAGs solve deployment velocity."
    )

    # Slide 3: Two-Column Comparison (Imperative vs Visual)
    SlideEngine.build_two_column(
        prs,
        badge="WORKFLOW PARADIGMS",
        title="Imperative Python vs. Visual Node Graphs",
        subtitle="Balancing low-level programmatic control against high-velocity visual orchestration",
        left_title="Imperative Python (Level 1 / 3)",
        left_items=[
            ("Algorithmic Control", "Full programmatic control over memory, threads, and custom data structures."),
            ("Engineering Overhead", "Requires git branches, PRs, CI/CD pipelines, and developer deployments."),
            ("Opaque Runtime State", "Execution state and intermediate variables are invisible to non-engineers."),
            ("Custom Plumbing", "Every API client, webhook receiver, and retry loop must be hand-coded.")
        ],
        right_title="Visual Node Canvases (Level 2)",
        right_items=[
            ("Rapid Composition", "Assemble complex AI pipelines visually via drag-and-drop nodes."),
            ("Pre-Built Connectors", "Direct access to 400+ SaaS integrations, database nodes, and webhook triggers."),
            ("Visual Telemetry", "Inspect every intermediate payload, token count, and execution latency visually."),
            ("Cross-Functional Agility", "Business leads and operations staff can adjust prompts and routing safely.")
        ],
        notes="Both paradigms have distinct strengths. Production organizations frequently use hybrid topologies: visual flows for SaaS ingestion and stateful code graphs for deep reasoning."
    )

    # Slide 4: Process Flow Architecture
    SlideEngine.build_full_width_card(
        prs,
        badge="N8N ORCHESTRATION",
        title="End-to-End n8n AI Agent Workflow Lifecycle",
        subtitle="Tracing real-time webhook payload ingestion, model reasoning, and tool dispatch",
        card_title="5-Stage Webhook Execution Pipeline",
        items=[
            ("1. Inbound Webhook", "External service emits event POST payload to /webhook/ticket endpoint."),
            ("2. HMAC Security", "Cryptographic node verifies SHA-256 signature against enterprise secret."),
            ("3. AI Agent Node", "Claude 3.5 Sonnet / Gemini Pro reasons over customer request and schemas."),
            ("4. Tool Dispatch", "Modular HTTP nodes query internal CRM or issue customer refund credits."),
            ("5. Response Post", "Dispatcher formats and delivers synthesized answer to Slack or Zendesk API.")
        ],
        notes="Walk through the lifecycle of a real-time webhook transaction through the node graph."
    )

    # Slide 5: Two-Column Comparison (n8n vs Langflow)
    SlideEngine.build_two_column(
        prs,
        badge="PLATFORM SELECTION",
        title="n8n vs. Langflow: Choosing the Right Engine",
        subtitle="Comparing operational multi-SaaS automation against component-based RAG prototyping",
        left_title="n8n Workflows",
        left_items=[
            ("Target Architecture", "Multi-SaaS enterprise automations, scheduled batch jobs, and event triggers."),
            ("Ecosystem Integrations", "Hundreds of enterprise business connectors (Salesforce, Stripe, Jira, Slack)."),
            ("Trigger Mechanisms", "HTTP webhooks, polling intervals, cron schedules, app event streams."),
            ("Runtime Engine", "Node.js asynchronous runtime with LangChain core agent bindings.")
        ],
        right_title="Langflow Canvases",
        right_items=[
            ("Target Architecture", "RAG pipeline prototyping, prompt evaluation, and vector retrieval tuning."),
            ("Ecosystem Integrations", "Native vector databases (Chroma, Pinecone, Astra DB, Milvus)."),
            ("Trigger Mechanisms", "Interactive chat playground, FastAPI endpoints, pure Python SDK."),
            ("Runtime Engine", "Pure Python backend with native LangChain and LlamaIndex support.")
        ],
        notes="Contrast the operational focus of n8n with the AI experimentation focus of Langflow."
    )

    # Slide 6: Monospace Code Container (HMAC Verification)
    code_sample = (
        'import hmac\nimport hashlib\n\n'
        'def verify_webhook_signature(payload_bytes: bytes, secret: str, sig_header: str) -> bool:\n'
        '    expected_hex = sig_header.replace("sha256=", "").strip()\n'
        '    computed = hmac.new(secret.encode(), payload_bytes, hashlib.sha256).hexdigest()\n'
        '    return hmac.compare_digest(computed, expected_hex)\n'
    )
    SlideEngine.build_code_slide(
        prs,
        badge="SECURITY GOVERNANCE",
        title="Inbound Webhook HMAC SHA-256 Signature Verification",
        subtitle="Securing public-facing agent endpoints against spoofing, forgery, and replay attacks",
        spec_title="Security Safeguards",
        spec_items=[
            ("Constant-Time Comparison", "hmac.compare_digest prevents timing attack vulnerabilities across network boundaries."),
            ("Cryptographic Signing", "Guarantees payload origin authenticity and integrity before token spend."),
            ("Zero-Trust Gateway", "Invalid signatures are dropped at the HTTP boundary before triggering AI nodes.")
        ],
        code_snippet=code_sample,
        notes="Explain why hmac.compare_digest is mandatory to avoid timing vulnerability attacks."
    )

    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        prs.save(p)
        print(f"[+] Saved Unit 02 Presentation deck: {p}")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
    targets = [
        os.path.join(base_dir, "presentations", "AINT_2050_Unit_02_Presentation.pptx"),
        os.path.join(base_dir, "units", "unit_02_visual_workflow_automation_n8n_and_langflow", "lectures", "AINT_2050_Unit_02_Presentation.pptx")
    ]
    build_unit_02_deck(targets)
