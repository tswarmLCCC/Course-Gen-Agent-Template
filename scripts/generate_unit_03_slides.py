#!/usr/bin/env python3
"""
Generate Unit 3 Presentation Slide Deck for AINT 2050
Uses scripts/slide_engine.py to create a 16:9 widescreen, WCAG 2.1 AAA PowerPoint (.pptx).
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from slide_engine import SlideEngine

def build_unit_03_deck(output_paths):
    prs = SlideEngine.create_presentation()

    # Slide 1: Split-Hero Title Slide
    SlideEngine.build_split_hero_title(
        prs,
        badge="AINT 2050 LECTURE",
        title="Code-First Stateful Graphs with LangGraph",
        subtitle="Architecting Cyclical Agent State Machines, Checkpointing & HITL",
        metadata="Instructor: Tim Swarm | Laramie County Community College\nCourse: AINT 2050 - Fall 2026",
        hero_badge="AINT",
        hero_sub="Artificial Intelligence & Autonomous Systems",
        notes="Welcome to Unit 03 of Applied AI Agent Architectures. Today we transition into Level 3 of the Agent Spectrum: Code-First Stateful Graph Architectures using LangGraph."
    )

    # Slide 2: Section Divider
    SlideEngine.build_section_divider(
        prs,
        sec_num=1,
        title="Why DAGs Fail for Advanced Agents",
        subtitle="Breaking the acyclic barrier to unlock iterative reasoning and self-healing",
        notes="We explore why Directed Acyclic Graphs cannot represent human-like trial, error, testing, and self-correction."
    )

    # Slide 3: Two-Column Comparison (Visual DAGs vs LangGraph)
    SlideEngine.build_two_column(
        prs,
        badge="GRAPH TOPOLOGIES",
        title="Visual DAGs vs. LangGraph State Machines",
        subtitle="Comparing linear forward-flow pipelines against cyclical stateful reasoning loops",
        left_title="Visual DAGs (Level 2)",
        left_items=[
            ("Forward Flow", "Data flows strictly forward from source to sink without backward recursion."),
            ("Loop Workarounds", "Iterative loops must be unrolled into repetitive, duplicated nodes."),
            ("Ad-hoc Schemas", "State is passed as untyped JSON payloads across arbitrary connectors."),
            ("Target Use Case", "Engineered for linear SaaS integrations, notifications, and webhooks.")
        ],
        right_title="LangGraph State Machines (Level 3)",
        right_items=[
            ("Cyclical Edges", "Backward edges enable true autonomous trial, evaluation, and correction."),
            ("Typed State Schema", "Centralized TypedDict defines the single strongly-typed source of truth."),
            ("State Reducers", "operator.add and custom reducers govern immutable history append."),
            ("Target Use Case", "Engineered for self-healing code, deep research, and reflection agents.")
        ],
        notes="Compare the structural limitations of DAGs with the flexibility of cyclical state machines."
    )

    # Slide 4: Full-Width Card (Self-Healing Code Refactoring Cycle)
    SlideEngine.build_full_width_card(
        prs,
        badge="CYCLICAL EXECUTION",
        title="The Self-Healing Code Refactoring Cycle",
        subtitle="A 5-step stateful feedback loop for automated code diagnosis, patching, and verification",
        card_title="StateGraph Iterative Loop Stages",
        items=[
            ("1. Test Runner Node", "Executes unit test suite against candidate code and captures exit code and stderr."),
            ("2. Conditional Edge", "Inspects state['tests_passed'] boolean and remaining iteration budget."),
            ("3. Diagnosis & Analyzer Node", "LLM parses traceback and identifies precise syntax or logical defect."),
            ("4. Targeted Patch Node", "Emits refactored code block and appends diagnostic entry to fix_history."),
            ("5. Completion Sentinel", "Routes safely to END sentinel when tests succeed or iteration cap is reached.")
        ],
        notes="Detail the 4-step cyclical feedback loop students implement in Lab 03."
    )

    # Slide 5: Monospace Code Container (TypedDict State Schema)
    code_sample = (
        'from typing import TypedDict, Annotated, List\n'
        'import operator\n\n'
        'class AgentState(TypedDict):\n'
        '    code: str\n'
        '    iteration: int\n'
        '    tests_passed: bool\n'
        '    fix_history: Annotated[List[str], operator.add]\n'
    )
    SlideEngine.build_code_slide(
        prs,
        badge="STATE DESIGN",
        title="LangGraph Centralized State Schema with Reducers",
        subtitle="Defining strongly-typed state transitions and non-destructive list accumulation",
        spec_title="Schema Components",
        spec_items=[
            ("TypedDict Structure", "Provides static typing and IDE autocompletion for all node functions."),
            ("State Reducer (operator.add)", "Appends new history entries without overwriting previous attempts."),
            ("Pure Node Functions", "Nodes take state and return partial updates matching the schema."),
            ("Deterministic Immutability", "State is safely isolated across asynchronous node executions.")
        ],
        code_snippet=code_sample,
        notes="Explain how Annotated with operator.add prevents destructive overwriting of historical notes during cycles."
    )

    # Slide 6: Two-Column Comparison (Persistence & HITL)
    SlideEngine.build_two_column(
        prs,
        badge="PRODUCTION SAFETY",
        title="Persistence, Checkpointing & Human-in-the-Loop",
        subtitle="Guaranteeing state durability across server restarts and enforcing safety approval gates",
        left_title="Checkpointing Architecture",
        left_items=[
            ("State Snapshots", "MemorySaver or SqliteSaver serializes state after every node step."),
            ("Thread Isolation", "Unique thread_id parameters isolate independent user sessions."),
            ("Time-Travel Debugging", "Roll back state to any historical checkpoint to test alternative branches."),
            ("Resilient Recovery", "Resume interrupted workflows instantly after process crashes.")
        ],
        right_title="Human-in-the-Loop (HITL) Gates",
        right_items=[
            ("Static Interrupts", "interrupt_before=['high_risk_node'] pauses graph before side effects."),
            ("Human Inspection", "Operator reviews generated SQL, API calls, or financial payouts."),
            ("Interactive Approval", "Operator can approve, modify state directly, or cancel execution."),
            ("Clean Resumption", "Graph resumes execution seamlessly via app.invoke(None, config).")
        ],
        notes="Conclude with production governance and safety patterns."
    )

    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        prs.save(p)
        print(f"[+] Saved Unit 03 Presentation deck: {p}")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
    targets = [
        os.path.join(base_dir, "presentations", "AINT_2050_Unit_03_Presentation.pptx"),
        os.path.join(base_dir, "units", "unit_03_code_first_stateful_graphs_langgraph", "lectures", "AINT_2050_Unit_03_Presentation.pptx")
    ]
    build_unit_03_deck(targets)
