#!/usr/bin/env python3
"""
=============================================================================
Course Generation Agent Template - Canvas Common Cartridge (.imscc) Builder
=============================================================================
Production-grade Canvas Common Cartridge compiler that dynamically transforms
modular unit folders, course configuration, and video mapping into a fully
accredited, DesignPLUS-compliant Canvas LMS package (.imscc).

Guarantees 100% Canvas Import Compliance:
1. Native WikiPages: Injects full HTML documents with <head><meta name="identifier"/>
   so Canvas imports pages as native Pages (WikiPages), NOT raw files in "Files".
2. Front Page Home: Sets <meta name="front_page" content="true"/> and
   <default_view>wiki</default_view> with dynamic Module Accordion navigation.
3. Course Orientation Module: Compiles Start Here, Syllabus, Socratic AI Guidelines,
   Student Lab Workflow, Dev Environment Setup, and External Resources.
4. Modular 9-Item Units: Assembles Overview, Readings & Video Lectures, Async Prep
   Drills, Applied Lab Guide with Rubric table, SpeedGrader Assignment, Native
   QTI 1.2 Knowledge Check Quiz, Discussion Topic, Learn with AI, and unpublished
   Instructor Teaching Notes.
5. Automated Validation & Backups: Performs xml.etree.ElementTree validation on all
   generated XML files and automatically archives timestamped backups in
   archive/cartridge_backups/.
=============================================================================
"""

import os
import sys
import re
import hashlib
import zipfile
import html
import shutil
import datetime
import json
import argparse
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UNITS_DIR = os.path.join(BASE_DIR, "units")
COURSE_SPECS_DIR = os.path.join(BASE_DIR, "course_specs")
OUTPUT_BUILD_DIR = os.path.join(BASE_DIR, "build", "canvas_cartridge")

def make_id(seed: str) -> str:
    """Generate a deterministic 32-char hex identifier matching Canvas format."""
    return "g" + hashlib.md5(seed.encode("utf-8")).hexdigest()[1:]

def load_course_config() -> dict:
    """Loads course configuration JSON or provides institutional defaults."""
    config_path = os.path.join(BASE_DIR, "course_config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "course_code": "COURSE 1010",
        "course_title": "Applied Systems Architecture",
        "term": "Fall 2026",
        "institution": "Laramie County Community College",
        "domain": "lccc-wy.instructure.com",
        "credits": "3.0 Credit Hours",
        "contact_hours_weekly": "300 Minutes",
        "description": "Comprehensive applied active-learning curriculum.",
        "outcomes": [
            "CLO 1: Master core theoretical paradigms and operational mental models.",
            "CLO 2: Construct, test, and debug applied systems using industry tools.",
            "CLO 3: Evaluate tradeoffs, security governance, and system performance."
        ],
        "assignment_groups": [
            {"key": "labs", "name": "Hands-on Applied Labs", "weight": 40.0},
            {"key": "quizzes", "name": "Unit Knowledge Checks & Quizzes", "weight": 20.0},
            {"key": "prep", "name": "Asynchronous Preparation & Drills", "weight": 10.0},
            {"key": "capstone", "name": "Comprehensive Course Capstone", "weight": 30.0}
        ],
        "grading_scale": "A: 90.0% – 100% | B: 80.0% – 89.9% | C: 70.0% – 79.9% | D: 60.0% – 69.9% | F: Below 60.0%"
    }

def extract_unit_topic(overview_text: str, folder_name: str, num: int) -> str:
    """Extracts high-level topic title from overview.md or folder name."""
    m = re.search(r"^#\s*Unit\s*0?%d\s*(?:Overview)?[:\-]\s*(.+)$" % num, overview_text, re.MULTILINE | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m2 = re.search(r"^#\s*(.+)$", overview_text, re.MULTILINE)
    if m2:
        cand = m2.group(1).strip()
        cand = re.sub(r"^Unit\s*0?\d+\s*(?:Overview)?[:\-]\s*", "", cand, flags=re.IGNORECASE).strip()
        if cand:
            return cand
    clean_folder = re.sub(r"^unit_0?\d+_", "", folder_name)
    return clean_folder.replace("_", " ").title()

def extract_readings(study_guide_text: str, unit_num: int, topic: str) -> list:
    """Extracts curated readings tuples [(name, url, desc), ...] from study_guide.md or external_resources_guide.md."""
    readings = []
    for line in study_guide_text.splitlines():
        line = line.strip()
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            for idx, c in enumerate(cells):
                m = re.search(r'\[([^\]]+)\]\((https?://[^)]+)\)', c)
                if m:
                    r_title = m.group(1).strip()
                    r_url = m.group(2).strip()
                    r_desc = ""
                    for d_idx in range(idx + 1, len(cells)):
                        if cells[d_idx] and not cells[d_idx].startswith("http"):
                            r_desc = cells[d_idx]
                            break
                    if not r_desc:
                        r_desc = f"Authoritative documentation and reference guide for {r_title}."
                    readings.append((r_title, r_url, r_desc))
    
    if not readings:
        for m in re.finditer(r'[-*]\s+\*\*\[?([^\]]+?)\]?\*\*:\s*(?:\[([^\]]+)\]\((https?://[^\)]+)\)|(https?://\S+))\s*(?:—|-)?\s*(.*)', study_guide_text):
            r_title = m.group(1).strip()
            r_url = m.group(3) or m.group(4)
            r_desc = m.group(5).strip() or f"Official guide for {r_title}."
            readings.append((r_title, r_url, r_desc))

    if not readings:
        ext_guide_path = os.path.join(COURSE_SPECS_DIR, "external_resources_guide.md")
        if os.path.exists(ext_guide_path):
            with open(ext_guide_path, "r", encoding="utf-8") as egf:
                eg_text = egf.read()
            keywords = []
            if unit_num == 1:
                keywords = ["react", "gemini", "claude", "foundation"]
            elif unit_num == 2:
                keywords = ["n8n", "langflow", "webhook"]
            elif unit_num == 3:
                keywords = ["langgraph", "langsmith", "stategraph"]
            else:
                keywords = [topic.split()[0].lower()]
            for m in re.finditer(r'\[([^\]]+)\]\((https?://[^\)]+)\)\s*(?:—|-)?\s*(.*)', eg_text):
                r_title = m.group(1).strip()
                r_url = m.group(2).strip()
                r_desc = m.group(3).strip() or f"Official framework documentation for {r_title}."
                block = f"{r_title} {r_url} {r_desc}".lower()
                if any(kw in block for kw in keywords):
                    readings.append((r_title, r_url, r_desc))

    if not readings:
        for m in re.finditer(r'\[([^\]]+)\]\((https?://[^\)]+)\)', study_guide_text):
            r_title = m.group(1).strip()
            r_url = m.group(2).strip()
            if len(r_title) > 3 and not r_url.endswith((".png", ".jpg")):
                readings.append((r_title, r_url, f"Recommended reading for {r_title}."))
                if len(readings) >= 4:
                    break
    return readings

def detect_code_type(unit_dir: str) -> tuple:
    """Detects primary language of unit starter files: returns (lang, allowed_extensions)."""
    for root, _, files in os.walk(unit_dir):
        for f in files:
            if f.endswith(".py"):
                return "python", "py,txt,pdf,zip"
            if f.endswith(".sql"):
                return "sql", "sql,txt,pdf"
    return "python", "py,txt,pdf,zip"

def load_learn_with_ai_data(unit_num: int, folder: str, topic: str) -> dict:
    """Dynamically parses async/learn_with_ai.md for the Socratic drill."""
    ai_path = os.path.join(UNITS_DIR, folder, "async", "learn_with_ai.md")
    persona = "Autonomous Systems Architect"
    drill_topic = topic
    prompt = ""
    discussion_prompt = f"In the Unit {unit_num} Discussion, share your findings, traps, and breakthrough insights from your Socratic AI practice session."

    if os.path.exists(ai_path):
        with open(ai_path, "r", encoding="utf-8") as f:
            content = f.read()

        m_persona = re.search(r'\*\*Persona:\*\*\s*(.+)', content)
        if m_persona:
            persona = m_persona.group(1).strip()

        m_topic = re.search(r'\*\*(?:Target )?Topic:\*\*\s*(.+)', content)
        if m_topic:
            drill_topic = m_topic.group(1).strip()

        m_prompt = re.search(r'```(?:text|markdown)?\s*\n(.*?)\n```', content, re.DOTALL)
        if m_prompt:
            prompt = m_prompt.group(1).strip()

        m_disc = re.search(r'##\s*(?:3\.\s*)?Weekly Discussion.*?\n(.*)', content, re.DOTALL | re.IGNORECASE)
        if m_disc:
            disc_text = m_disc.group(1).strip()
            if disc_text:
                discussion_prompt = disc_text

    if not prompt:
        prompt = f"Act as a strict, Socratic technical mentor. Challenge me on core architectural concepts, failure modes, and implementation patterns for {topic}."

    return {
        "persona": persona,
        "drill_topic": drill_topic,
        "prompt": prompt,
        "discussion_prompt": discussion_prompt
    }

def load_teacher_guide_data(unit_num: int, folder: str, topic: str) -> dict:
    """Dynamically parses lectures/micro_lecture_scripts.md and sync/lesson_plan.md."""
    scripts_path = os.path.join(UNITS_DIR, folder, "lectures", "micro_lecture_scripts.md")
    videos = []
    if os.path.exists(scripts_path):
        with open(scripts_path, "r", encoding="utf-8") as f:
            content = f.read()
        for m in re.finditer(r'##\s*(Micro-Video\s*[\d\.]+:\s*[^\n]+)', content):
            v_title = m.group(1).strip()
            start_pos = m.end()
            chunk = content[start_pos:start_pos+300]
            m_dur = re.search(r'\*\s*\*\*Duration:\*\*\s*([^\n]+)', chunk)
            v_dur = m_dur.group(1).strip() if m_dur else "5-8 mins"
            videos.append((v_title, v_dur, f"Instructional micro-video covering core concepts for {v_title}."))

    if not videos:
        videos = [
            (f"Micro-Video {unit_num}.1: Core Concepts & Mental Models", "5-7 mins", f"Introduce core principles of {topic}."),
            (f"Micro-Video {unit_num}.2: Live Coding Demonstration", "6-8 mins", f"Demonstrate step-by-step implementation in live environment."),
            (f"Micro-Video {unit_num}.3: Applied Lab Walkthrough", "4-5 mins", f"Tour lab starter code, scenarios, and submission criteria.")
        ]

    lesson_plan_path = os.path.join(UNITS_DIR, folder, "sync", "lesson_plan.md")
    sync_agenda = "0:00-0:20 Concept Debrief & Warm-up | 0:20-0:50 Live Demo & Trap Analysis | 0:50-1:40 Paired Challenges | 1:40-2:20 Lab Execution | 2:20-2:30 Practical Turn-in Debrief"
    if os.path.exists(lesson_plan_path):
        with open(lesson_plan_path, "r", encoding="utf-8") as f:
            lp_text = f.read()
            m_opt_b = re.search(r'##\s*Delivery Track Option B: Single 150-Minute Block\s*\n(.*?)(?=\n##|\Z)', lp_text, re.DOTALL)
            if m_opt_b:
                sync_agenda = m_opt_b.group(1).strip()
            else:
                m_opt_a = re.search(r'###\s*Session 1:(.*?)(?=\n###|\n##|\Z)', lp_text, re.DOTALL)
                if m_opt_a:
                    sync_agenda = m_opt_a.group(1).strip()

    return {
        "videos": videos,
        "sync_agenda": sync_agenda
    }

def load_and_clean_unit_overview(unit_num: int, folder: str = "") -> str:
    """Loads and cleans the curated instructor Unit Overview markdown file."""
    if not folder:
        for f in os.listdir(UNITS_DIR):
            if re.search(r"unit_0?%d\b" % unit_num, f):
                folder = f
                break
    if not folder:
        return ""

    file_path = os.path.join(UNITS_DIR, folder, "overview.md")
    if not os.path.exists(file_path):
        file_path = os.path.join(UNITS_DIR, folder, "async", "study_guide.md")
    if not os.path.exists(file_path):
        return ""

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    text = re.sub(r'\\([*_#!\[\]\.\-+=\<\>~|`])', r'\1', text)
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        if line.strip().startswith('# **Unit') or line.strip().startswith('# Unit'):
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()

def parse_unit_overview_sections(overview_text: str, unit_num: int, topic: str) -> tuple:
    """Parses overview.md to extract executive lead, objectives, roadmap, and time budget."""
    cleaned = re.sub(r'<div class="dp-header.*?</div>\s*---', '', overview_text, flags=re.DOTALL)

    m_exec = re.search(r'##\s*(?:\d+\.\s*)?Executive Summary[^\n]*\n(.*?)(?=\n\s*---\s*\n|\n\s*##|\Z)', cleaned, re.DOTALL)
    if m_exec:
        lead = m_exec.group(1).strip()
    else:
        m_title = re.search(r'^#\s*Unit\s*\d+\s*(?:Overview)?\s*[:\-]\s*(.*)', cleaned, re.MULTILINE | re.IGNORECASE)
        after_title = cleaned[m_title.end():] if m_title else cleaned
        m_lead = re.search(r'^\s*([A-Za-z0-9*].*?)(?=\n\s*---\s*\n|\n\s*##|\Z)', after_title, re.DOTALL | re.MULTILINE)
        lead = m_lead.group(1).strip() if m_lead else f"Welcome to Unit {unit_num}: {topic}."

    m_obj = re.search(r'##\s*(?:\d+\.\s*)?(?:Course Learning Outcomes|Weekly Learning Objectives)[^\n]*\n(.*?)(?=\n\s*---\s*\n|\n\s*##|\Z)', cleaned, re.DOTALL)
    objectives_md = m_obj.group(1).strip() if m_obj else f"<p>Master production skills and architectural principles for {topic}.</p>"

    m_road = re.search(r'##\s*(?:\d+\.\s*)?(?:Weekly Roadmap|Weekly Deliverables)[^\n]*\n(.*?)(?=\n\s*---\s*\n|\n\s*##|\Z)', cleaned, re.DOTALL)
    roadmap_md = m_road.group(1).strip() if m_road else """<ol>
  <li><strong>Required Readings &amp; Embedded Videos:</strong> Master core conceptual models and view lecture demonstrations.</li>
  <li><strong>Asynchronous Preparation &amp; Drills:</strong> Complete the formative reflection questions and self-check drills.</li>
  <li><strong>Applied Laboratory Assignment:</strong> Implement and verify your solution against live challenges.</li>
  <li><strong>Canvas Lab Turn-in:</strong> Submit your verified code or scripts through SpeedGrader.</li>
  <li><strong>Learn with AI:</strong> Complete the interactive roleplay drill and discuss findings.</li>
  <li><strong>Unit Knowledge Check:</strong> Take the 15-question multiple-choice assessment.</li>
</ol>"""

    m_time = re.search(r'##\s*(?:\d+\.\s*)?Instructional Time Budget[^\n]*\n(.*?)(?=\n\s*---\s*\n|\n\s*##|\Z)', cleaned, re.DOTALL)
    time_md = m_time.group(1).strip() if m_time else "<p><strong>150 Minutes Guided Self-Study:</strong> Video micro-lectures, authoritative readings, and formative self-check drills.<br/><strong>150 Minutes Applied Practice:</strong> Hands-on implementation, debugging scenarios, and unit assessments.</p>"

    return lead, objectives_md, roadmap_md, time_md

def discover_unit_metadata(units_dir: str, config: dict, custom_videos: list) -> list:
    """Dynamically scans units/ directory and discovers all units in numerical order."""
    units = []
    if not os.path.exists(units_dir):
        return units

    folders = [f for f in sorted(os.listdir(units_dir)) if os.path.isdir(os.path.join(units_dir, f))]
    for folder in folders:
        m = re.search(r"unit_(\d+)", folder)
        if not m:
            continue
        num = int(m.group(1))
        u_dir = os.path.join(units_dir, folder)

        ov_path = os.path.join(u_dir, "overview.md")
        ov_text = ""
        if os.path.exists(ov_path):
            with open(ov_path, "r", encoding="utf-8") as f:
                ov_text = f.read()
        topic = extract_unit_topic(ov_text, folder, num)

        sg_path = os.path.join(u_dir, "async", "study_guide.md")
        sg_text = ""
        if os.path.exists(sg_path):
            with open(sg_path, "r", encoding="utf-8") as f:
                sg_text = f.read()
        readings = extract_readings(sg_text, num, topic)

        unit_vids = [v for v in custom_videos if v.get("unit_num") == num]
        videos = []
        for v in unit_vids:
            if v.get("video_id"):
                videos.append((v["label"], v["video_id"], 0, "0:00"))

        base_date = datetime.date(2026, 10, 23) + datetime.timedelta(days=(num - 1) * 7)
        due_iso = f"{base_date.isoformat()}T23:59:00"
        due_str = f"{base_date.strftime('%A, %B %d, %Y')} at 11:59 PM (Midnight MT)"

        units.append({
            "num": num,
            "folder": folder,
            "short_title": f"Unit {num}",
            "title": f"Unit {num}: {topic}",
            "topic": topic,
            "due_date_str": due_str,
            "due_iso": due_iso,
            "readings": readings,
            "videos": videos
        })
    return units

def format_inline(s: str) -> str:
    """Formats inline markdown syntax to HTML."""
    s = re.sub(r'\\([*_#!\\[\\]\.\-+=\<\>~|`])', r'\1', s)

    def replace_inline_code(match):
        code_text = html.escape(match.group(1))
        return f'<code style="background: #f1f5f9; color: #0369a1; padding: 0.15rem 0.35rem; border-radius: 3px; font-size: 0.9em; font-family: Consolas, monospace; font-weight: 600;">{code_text}</code>'

    s = re.sub(r'`([^`]+)`', replace_inline_code, s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = s.replace(r'$\rightarrow$', '&rarr;')
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = s.replace('⚠️', '').replace('❌', '')
    return s

def parse_markdown_to_html(md: str) -> str:
    """Converts structured markdown (tables, code blocks, lists, details) into clean styled HTML."""
    if not md:
        return ""

    # Strip decorative emojis
    md = md.replace('⚠️', '').replace('❌', '')

    # Unescape markdown punctuation and operators first (\+, \=, \*, 1\., \_, etc.)
    md = re.sub(r'\\([*_#!\\[\\]\.\-+=\<\>~|`])', r'\1', md)

    code_blocks = []
    def code_block_sub(match):
        lang = match.group(1) or ''
        code = match.group(2)
        idx = len(code_blocks)
        code_html = f'<div style="background: #0f172a; color: #f8fafc; padding: 1rem 1.25rem; border-radius: 6px; overflow-x: auto; margin: 1.25rem 0; font-family: Consolas, Monaco, monospace; font-size: 0.9em; line-height: 1.5;"><pre style="margin: 0; background: transparent; color: inherit;"><code>{html.escape(code.strip())}</code></pre></div>'
        code_blocks.append(code_html)
        return f'__CODE_BLOCK_{idx}__'

    text = re.sub(r'^[ \t]*```([a-zA-Z0-9_-]*)\r?\n(.*?)\r?\n[ \t]*```', code_block_sub, md, flags=re.DOTALL | re.MULTILINE)

    lines = text.splitlines()
    output = []
    in_table = False
    table_rows = []
    in_list = False
    list_type = None

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            in_table = False
            return ''
        html_table = ['<div style="overflow-x: auto; margin: 1.25rem 0;"><table style="width: 100%; border-collapse: collapse; border: 1px solid #cbd5e1; font-size: 0.95em;">']
        header_cells = table_rows[0]
        html_table.append('<thead><tr style="background-color: #1e3a8a; color: #ffffff;">')
        for c in header_cells:
            html_table.append(f'<th style="padding: 10px 14px; border: 1px solid #94a3b8; font-weight: 600;">{format_inline(c)}</th>')
        html_table.append('</tr></thead><tbody>')
        for row_idx, row in enumerate(table_rows[1:]):
            bg = '#f8fafc' if row_idx % 2 == 0 else '#ffffff'
            html_table.append(f'<tr style="background-color: {bg};">')
            for c in row:
                html_table.append(f'<td style="padding: 8px 14px; border: 1px solid #cbd5e1;">{format_inline(c)}</td>')
            html_table.append('</tr>')
        html_table.append('</tbody></table></div>')
        in_table = False
        table_rows = []
        return ''.join(html_table)

    def flush_list():
        nonlocal in_list, list_type
        if not in_list:
            return ''
        tag = list_type
        in_list = False
        list_type = None
        return f'</{tag}>\n'

    for line in lines:
        trimmed = line.strip()

        if trimmed.startswith('|') and trimmed.endswith('|'):
            cells = [c.strip() for c in trimmed[1:-1].split('|')]
            if re.match(r'^[:\- ]+$', ''.join(cells)):
                pass
            else:
                if not in_table:
                    if in_list:
                        output.append(flush_list())
                    in_table = True
                    table_rows = [cells]
                else:
                    table_rows.append(cells)
            continue
        elif in_table:
            output.append(flush_table())

        if not trimmed:
            if in_list:
                output.append(flush_list())
            continue

        cb_match = re.match(r'^__CODE_BLOCK_(\d+)__$', trimmed)
        if cb_match:
            if in_list:
                output.append(flush_list())
            idx = int(cb_match.group(1))
            output.append(code_blocks[idx])
            continue

        h_match = re.match(r'^(#{1,6})\s+(.*)$', trimmed)
        if h_match:
            if in_list:
                output.append(flush_list())
            level = len(h_match.group(1))
            h_text = format_inline(h_match.group(2).strip())
            if level == 1:
                output.append(f'<h2 style="color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.4rem; margin-top: 1.5rem; margin-bottom: 0.75rem;">{h_text}</h2>')
            elif level == 2:
                output.append(f'<h3 style="color: #1e3a8a; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.3rem; margin-top: 1.5rem; margin-bottom: 0.75rem;">{h_text}</h3>')
            elif level == 3:
                output.append(f'<h4 style="color: #0f172a; margin-top: 1.25rem; margin-bottom: 0.5rem; font-size: 1.15em;">{h_text}</h4>')
            else:
                output.append(f'<h5 style="color: #334155; margin-top: 1rem; margin-bottom: 0.5rem; font-size: 1.05em;">{h_text}</h5>')
            continue

        if trimmed in ('---', '***', '___'):
            if in_list:
                output.append(flush_list())
            output.append('<hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 1.5rem 0;"/>')
            continue

        if trimmed.startswith('<details>'):
            if in_list:
                output.append(flush_list())
            output.append('<details style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 0.75rem 1.25rem; margin: 1rem 0;">')
            continue
        if trimmed.startswith('</details>'):
            if in_list:
                output.append(flush_list())
            output.append('</details>')
            continue
        if trimmed.startswith('<summary>') and trimmed.endswith('</summary>'):
            if in_list:
                output.append(flush_list())
            sum_text = trimmed[9:-10].strip()
            sum_text = re.sub(r'<\/?b>', '', sum_text)
            output.append(f'<summary style="cursor: pointer; font-weight: 600; color: #1e3a8a; padding: 0.25rem 0;">{format_inline(sum_text)}</summary><div style="margin-top: 0.75rem; padding-top: 0.5rem; border-top: 1px dashed #cbd5e1;">')
            continue
        if trimmed.startswith('</summary>'):
            continue

        if trimmed.startswith('>'):
            if in_list:
                output.append(flush_list())
            bq_text = format_inline(trimmed.lstrip('>').strip())
            output.append(f'<div style="background: #eff6ff; border-left: 4px solid #3b82f6; padding: 0.75rem 1.25rem; margin: 1rem 0; border-radius: 0 4px 4px 0; color: #1e3a8a;">{bq_text}</div>')
            continue

        ul_match = re.match(r'^[*•-]\s+(.*)$', trimmed)
        ol_match = re.match(r'^\d+\.\s+(.*)$', trimmed)
        if ul_match:
            if not in_list or list_type != 'ul':
                if in_list:
                    output.append(flush_list())
                in_list = True
                list_type = 'ul'
                output.append('<ul style="padding-left: 1.5rem; margin: 0.75rem 0;">')
            output.append(f'<li style="margin-bottom: 0.35rem;">{format_inline(ul_match.group(1))}</li>')
            continue
        elif ol_match:
            item_text = ol_match.group(1).strip()
            # Strip redundant internal numbering like "1. ", "**1. ", "**1.**" to prevent double numbering (e.g. "1. 1.")
            item_text = re.sub(r'^(\*\*)?\d+[\.\)]\s*(\*\*)?\s*', '', item_text)
            if not in_list or list_type != 'ol':
                if in_list:
                    output.append(flush_list())
                in_list = True
                list_type = 'ol'
                output.append('<ol style="padding-left: 1.5rem; margin: 0.75rem 0;">')
            output.append(f'<li style="margin-bottom: 0.35rem;">{format_inline(item_text)}</li>')
            continue

        if in_list:
            output.append(flush_list())
        
        output.append(f'<p style="margin: 0.75rem 0; line-height: 1.6;">{format_inline(trimmed)}</p>')

    if in_table:
        output.append(flush_table())
    if in_list:
        output.append(flush_list())

    result = '\n'.join(output)
    result = result.replace('</details>', '</div></details>')

    for idx, cb in enumerate(code_blocks):
        result = result.replace(f'__CODE_BLOCK_{idx}__', cb)
    return result

def render_standard_page_html(title: str, lead_html: str, sections: list, page_id: str, workflow_state: str = "active") -> str:
    """
    Renders clean, modern, native Canvas HTML pages without the ribbon header,
    ideal for lab guides, reading pages, study drills, and AI practice.
    """
    sections_html = []
    for heading, content in sections:
        sec = f"""  <div style="margin-bottom: 2rem;">
    <h2 style="color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.4rem; margin-top: 1.75rem; margin-bottom: 1rem;">{html.escape(heading)}</h2>
    <div style="line-height: 1.6; color: #1e293b;">
      {content}
    </div>
  </div>"""
        sections_html.append(sec)

    body_sections = "\n".join(sections_html)
    lead_block = ""
    if lead_html:
        lead_block = f"""  <div style="background: #f8fafc; border-left: 4px solid #1e3a8a; padding: 1rem 1.25rem; margin-bottom: 1.75rem; border-radius: 0 4px 4px 0; font-size: 1.05em; line-height: 1.5; color: #334155;">
    {lead_html}
  </div>"""

    return f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>{html.escape(title)}</title>
<meta name="identifier" content="{page_id}"/>
<meta name="editing_roles" content="teachers"/>
<meta name="workflow_state" content="{workflow_state}"/>
<meta name="editor_type" content="rce"/>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; padding: 1.5rem; max-width: 1000px; margin: 0 auto;">
  <h1 style="color: #1e3a8a; margin-top: 0; margin-bottom: 1.25rem;">{html.escape(title)}</h1>
{lead_block}
{body_sections}
</body>
</html>"""

def render_designplus_html(title: str, lead_html: str, panels: list, page_id: str, workflow_state: str = "active") -> str:
    """Renders HTML strictly adhering to DesignPLUS styles for Unit Overviews, Home, and Start Here."""
    panels_html = []
    for heading, content in panels:
        panels_html.append(f"""    <div class="dp-panel-group">
      <h2 class="dp-panel-heading ">{html.escape(heading)}</h2>
      <div class="dp-panel-content ">
        {content}
      </div>
    </div>""")

    body_panels = "\n".join(panels_html)

    return f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>{html.escape(title)}</title>
<meta name="identifier" content="{page_id}"/>
<meta name="editing_roles" content="teachers"/>
<meta name="workflow_state" content="{workflow_state}"/>
<meta name="editor_type" content="rce"/>
</head>
<body>
<div id="dp-wrapper" class="dp-wrapper dp-hdg-i-cp-brdr-h2-dp-primary dp-hdg-txt-h3-dp-primary dp-hdg-txt-h4-dp-primary dp-hdg-txt-h5-dp-primary dp-hdg-i-cp-brdr-h5-dp-primary dp-hdg-b-h2-brdr-b dp-hdg-txt-h6-dp-primary dp-hdg-i-cp-brdr-h6-dp-primary dp-hdg-i-styl-h2-pill dp-hdg-i-styl-h3-pill dp-hdg-cp-brdr-h3-dp-secondary dp-hdg-cp-brdr-h2-dp-secondary dp-hdg-brdr-h2-1 dp-hdg-brdr-h3-1 dp-hdg-brdr-h4-1 dp-hdg-brdr-h5-1 dp-hdg-brdr-h6-1 dp-hdg-i-sz-h2-fill dp-hdg-i-sz-h3-fill dp-hdg-i-sz-h5-fill dp-hdg-i-sz-h6-fill dp-hdg-i-brdr-h5-2 dp-hdg-i-brdr-h6-2 dp-hdg-b-h3-brdr-b dp-hdg-txt-h2-dp-primary dp-hdg-i-brdr-h2-1 dp-hdg-i-brdr-h3-1 dp-hdg-i-sz-h4-fill dp-hdg-i-cp-brdr-h3-dp-primary dp-hdg-i-brdr-h4-1 dp-hdg-i-bg-h2-dp-primary dp-hdg-i-bg-h3-dp-primary dp-hdg-b-h4-brdr-b dp-hdg-d-h4-table-l dp-hdg-i-styl-h4-pill dp-hdg-i-cp-brdr-h4-dp-primary">
  <header class="dp-header dp-basic-bar dp-header-s-brdr-l dp-header-brdr-w-4 dp-header-out-dp-secondary dp-header-pre-s-brdr-r dp-header-pre-font-sm dp-header-pre-out-dp-secondary dp-header-sub-brdr-w-0 dp-header-desc-txt-dp-primary dp-header-desc-out-dp-primary dp-header-sub-bg-dp-white dp-header-sub-txt-dp-primary dp-header-sub-out-dp-primary">
    <h2 class="dp-heading dp-locked"><span class="dp-header-title">{html.escape(title)}</span></h2>
    <p>&nbsp;</p>
  </header>
  <div class="dp-content-block">
    {lead_html}
  </div>
  <div class="dp-panels-wrapper dp-accordion-plus dp-panel-color-dp-primary dp-panel-active-color-dp-accent dp-panel-hover-color-dp-accent">
{body_panels}
  </div>
</div>
</body>
</html>"""

def render_ribbon_sections_page_html(title: str, lead_html: str, sections: list, page_id: str, workflow_state: str = "active") -> str:
    """
    Renders HTML pages with DesignPLUS ribbon headers for each major section/chapter,
    with an overall descriptive lead card on top.
    """
    sections_html = []
    for heading, content in sections:
        sec = f"""  <div class="dp-header-wrapper" style="margin-top: 2.5rem; margin-bottom: 1.25rem;">
    <header class="dp-header dp-basic-bar dp-header-s-brdr-l dp-header-brdr-w-4 dp-header-out-dp-secondary dp-header-pre-s-brdr-r dp-header-pre-font-sm dp-header-pre-out-dp-secondary dp-header-sub-brdr-w-0 dp-header-desc-txt-dp-primary dp-header-desc-out-dp-primary dp-header-sub-bg-dp-white dp-header-sub-txt-dp-primary dp-header-sub-out-dp-primary">
      <h2 class="dp-heading dp-locked"><span class="dp-header-title">{html.escape(heading)}</span></h2>
    </header>
  </div>
  <div class="dp-section-body" style="line-height: 1.6; color: #1e293b; margin-bottom: 2rem; padding: 0 0.25rem;">
    {content}
  </div>"""
        sections_html.append(sec)

    body_sections = "\n".join(sections_html)
    lead_block = ""
    if lead_html:
        lead_block = f"""  <div class="dp-content-block" style="background: #f8fafc; border-left: 4px solid #1e3a8a; padding: 1.25rem 1.5rem; margin-top: 1.5rem; margin-bottom: 2rem; border-radius: 0 6px 6px 0; font-size: 1.05em; line-height: 1.6; color: #334155;">
    {lead_html}
  </div>"""

    return f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>{html.escape(title)}</title>
<meta name="identifier" content="{page_id}"/>
<meta name="editing_roles" content="teachers"/>
<meta name="workflow_state" content="{workflow_state}"/>
<meta name="editor_type" content="rce"/>
</head>
<body>
<div id="dp-wrapper" class="dp-wrapper dp-hdg-i-cp-brdr-h2-dp-primary dp-hdg-txt-h3-dp-primary dp-hdg-txt-h4-dp-primary dp-hdg-txt-h5-dp-primary dp-hdg-i-cp-brdr-h5-dp-primary dp-hdg-b-h2-brdr-b dp-hdg-txt-h6-dp-primary dp-hdg-i-cp-brdr-h6-dp-primary dp-hdg-i-styl-h2-pill dp-hdg-i-styl-h3-pill dp-hdg-cp-brdr-h3-dp-secondary dp-hdg-cp-brdr-h2-dp-secondary dp-hdg-brdr-h2-1 dp-hdg-brdr-h3-1 dp-hdg-brdr-h4-1 dp-hdg-brdr-h5-1 dp-hdg-brdr-h6-1 dp-hdg-i-sz-h2-fill dp-hdg-i-sz-h3-fill dp-hdg-i-sz-h5-fill dp-hdg-i-sz-h6-fill dp-hdg-i-brdr-h5-2 dp-hdg-i-brdr-h6-2 dp-hdg-b-h3-brdr-b dp-hdg-txt-h2-dp-primary dp-hdg-i-brdr-h2-1 dp-hdg-i-brdr-h3-1 dp-hdg-i-sz-h4-fill dp-hdg-i-cp-brdr-h3-dp-primary dp-hdg-i-brdr-h4-1 dp-hdg-i-bg-h2-dp-primary dp-hdg-i-bg-h3-dp-primary dp-hdg-b-h4-brdr-b dp-hdg-d-h4-table-l dp-hdg-i-styl-h4-pill dp-hdg-i-cp-brdr-h4-dp-primary">
  <header class="dp-header dp-basic-bar dp-header-s-brdr-l dp-header-brdr-w-4 dp-header-out-dp-secondary dp-header-pre-s-brdr-r dp-header-pre-font-sm dp-header-pre-out-dp-secondary dp-header-sub-brdr-w-0 dp-header-desc-txt-dp-primary dp-header-desc-out-dp-primary dp-header-sub-bg-dp-white dp-header-sub-txt-dp-primary dp-header-sub-out-dp-primary">
    <h1 class="dp-heading dp-locked"><span class="dp-header-title">{html.escape(title)}</span></h1>
    <p>&nbsp;</p>
  </header>
{lead_block}
{body_sections}
</div>
</body>
</html>"""

def render_video_embed(title: str, video_id: str, start_sec: int) -> str:
    """Generates a clean responsive 16:9 embedded YouTube player."""
    mins = start_sec // 60
    secs = start_sec % 60
    return f"""<div style="margin-bottom: 2rem;">
  <h4 style="margin-bottom: 0.5rem; color: #1e293b;">{html.escape(title)} <span style="font-size: 0.9em; font-weight: normal; color: #64748b;">(Starts at {mins}:{secs:02d})</span></h4>
  <div class="dp-embed-wrapper" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 6px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 0.5rem;">
    <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" title="{html.escape(title)}" src="https://www.youtube.com/embed/{video_id}?start={start_sec}" loading="lazy" allowfullscreen="allowfullscreen" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"></iframe>
  </div>
  <p style="font-size: 0.85em; color: #64748b; margin-top: 0.25rem;"><a href="https://www.youtube.com/watch?v={video_id}&amp;t={start_sec}s" target="_blank" rel="noopener">Open video segment in new tab ({mins}:{secs:02d})</a></p>
</div>"""

def load_video_map():
    """Parses shared_assets/VideoMap.md to extract custom instructor videos."""
    video_map_path = os.path.join(BASE_DIR, "shared_assets", "VideoMap.md")
    videos = []
    if not os.path.exists(video_map_path):
        return videos
    
    with open(video_map_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            # Find the URL anywhere in the line
            m_url = re.search(r'(https?://\S+)', line)
            if not m_url:
                continue
            url = m_url.group(1).strip()
            label_text = line[:m_url.start()].strip().rstrip("-").strip()
            
            # Extract YouTube video id
            yt_id = None
            m_short = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
            m_watch = re.search(r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)', url)
            m_embed = re.search(r'youtube\.com/embed/([a-zA-Z0-9_-]+)', url)
            if m_short:
                yt_id = m_short.group(1)
            elif m_watch:
                yt_id = m_watch.group(1)
            elif m_embed:
                yt_id = m_embed.group(1)
            
            embed_url = f"https://www.youtube.com/embed/{yt_id}" if yt_id else url

            # Determine type, unit number, and specific page target
            vtype = "custom"
            unit_num = None
            
            label_lower = label_text.lower()
            if "orientation" in label_lower:
                vtype = "orientation"
            elif "codespace" in label_lower or "github" in label_lower:
                vtype = "codespaces"
            else:
                u_match = re.search(r'(?:unit|week)\s*(\d+)', label_lower)
                if u_match:
                    unit_num = int(u_match.group(1))
                    if "lab" in label_lower:
                        vtype = "unit_lab"
                    else:
                        vtype = "unit_lecture"
                elif "lab" in label_lower:
                    lab_match = re.search(r'lab\s*(\d+)', label_lower)
                    if lab_match:
                        unit_num = int(lab_match.group(1))
                    vtype = "unit_lab"
            
            display_title = label_text.split(" - ")[-1] if " - " in label_text else label_text

            videos.append({
                "raw_label": label_text,
                "label": display_title,
                "url": url,
                "video_id": yt_id,
                "embed_url": embed_url,
                "type": vtype,
                "unit_num": unit_num
            })
    return videos

def render_custom_video_card(title: str, url: str, embed_url: str) -> str:
    """Generates DesignPLUS-compliant responsive 16:9 card for custom instructor videos."""
    return f"""<div style="margin: 1.5rem 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
  <div style="background: #1e3a8a; color: #ffffff; padding: 0.6rem 1rem; font-weight: 600; font-size: 0.95em;">
    <i class="fas fa-play-circle"></i> {html.escape(title)}
  </div>
  <div class="dp-embed-wrapper" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%;">
    <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" 
            src="{embed_url}" 
            title="{html.escape(title)}" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen="allowfullscreen" 
            loading="lazy"></iframe>
  </div>
  <div style="padding: 0.5rem 1rem; background: #f8fafc; font-size: 0.85em; color: #64748b;">
    <a href="{url}" target="_blank" rel="noopener">Open {html.escape(title)} in new tab</a>
  </div>
</div>"""

def parse_quiz_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = re.split(r'#+\s*Answer Key', content, flags=re.IGNORECASE)
    questions_part = parts[0]
    key_part = parts[1] if len(parts) > 1 else ""

    key_map = {}
    for line in key_part.splitlines():
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 3:
            q_num_match = re.search(r'\d+', cells[0])
            ans_match = re.search(r'[A-D]', cells[1], re.IGNORECASE)
            if q_num_match and ans_match:
                q_num = int(q_num_match.group(0))
                ans = ans_match.group(0).upper()
                rationale = cells[2]
                key_map[q_num] = (ans, rationale)

    q_blocks = re.split(r'###\s*Question\s+(\d+)', questions_part)
    questions = []
    for i in range(1, len(q_blocks), 2):
        q_num = int(q_blocks[i])
        block_text = q_blocks[i+1].strip()

        opt_matches = list(re.finditer(r'^[ \t]*[*•-][ \t]+([A-D])\)[ \t]*', block_text, flags=re.MULTILINE))
        if len(opt_matches) == 4:
            prompt_end = opt_matches[0].start()
            prompt = block_text[:prompt_end].strip()
            sep_idx = block_text.find('\n---', opt_matches[-1].end())
            last_end = sep_idx if sep_idx != -1 else len(block_text)
            options = []
            for j, m in enumerate(opt_matches):
                opt_letter = m.group(1).upper()
                start = m.end()
                end = opt_matches[j + 1].start() if j + 1 < 4 else last_end
                opt_text = block_text[start:end].strip()
                options.append((opt_letter, opt_text))
        elif opt_matches:
            prompt_end = opt_matches[0].start()
            prompt = block_text[:prompt_end].strip()
            options = []
            for m in opt_matches:
                opt_letter = m.group(1).upper()
                opt_text = block_text[m.end():].splitlines()[0].strip()
                options.append((opt_letter, opt_text))
        else:
            prompt = block_text
            options = []

        correct_ans, rationale = key_map.get(q_num, ('A', ''))
        prompt = clean_quiz_text(prompt)
        options = [(opt_letter, clean_quiz_text(opt_text)) for opt_letter, opt_text in options]
        rationale = clean_quiz_text(rationale)
        questions.append({
            'num': q_num,
            'prompt': prompt,
            'options': options,
            'correct_answer': correct_ans,
            'rationale': rationale
        })

    return questions

def clean_quiz_text(s: str) -> str:
    """Cleans up escape characters, LaTeX arrows, and markdown escapes in quiz text."""
    if not s:
        return ""
    # LaTeX arrows and math symbols
    s = s.replace(r'$\rightarrow$', '→').replace(r'\rightarrow', '→')
    s = s.replace(r'\|\|', '||')
    s = s.replace(r'$A \le x \le B$', 'A <= x <= B').replace(r'\le', '<=')
    s = s.replace(r'$M \times N$', 'M × N').replace(r'\times', '×')
    s = s.replace(r'$4 \times 5 = 20$', '4 × 5 = 20')
    s = s.replace(r'\{1, 2, 3, 4\} \ \{3, 4, 5, 6\} = \{1, 2\}', '{1, 2, 3, 4} - {3, 4, 5, 6} = {1, 2}')
    s = s.replace(r'$X \rightarrow Y \rightarrow Z$', 'X → Y → Z')
    s = s.replace(r'$O(\log N)$', 'O(log N)').replace(r'\log', 'log')
    # Strip backslashes before special characters
    s = re.sub(r'\\([*_#!\\[\\]\.\-+=\<\>~|`])', r'\1', s)
    return s

def format_quiz_prompt_html(prompt: str) -> str:
    """Formats markdown quiz prompt into clean, DesignPLUS-compatible HTML."""
    prompt = clean_quiz_text(prompt)

    # 1. Code blocks ```sql ... ``` or ``` ... ```
    def replace_code_block(match):
        code_content = match.group(2).strip()
        escaped_code = html.escape(code_content)
        return f'<div style="background: #0f172a; color: #f8fafc; padding: 0.75rem 1rem; border-radius: 4px; font-family: Consolas, Monaco, monospace; font-size: 0.9em; line-height: 1.45; margin: 0.75rem 0; overflow-x: auto;"><pre style="margin: 0; background: transparent; color: inherit; font-family: inherit;"><code>{escaped_code}</code></pre></div>'

    prompt = re.sub(r'```([a-zA-Z0-9_-]*)\n(.*?)```', replace_code_block, prompt, flags=re.DOTALL)

    # 2. Markdown tables
    def replace_table(match):
        table_text = match.group(0).strip()
        lines = [line.strip() for line in table_text.splitlines() if line.strip()]
        if len(lines) < 2:
            return table_text
        
        headers = [c.strip() for c in lines[0].split('|')[1:-1]]
        data_rows = []
        for line in lines[2:]:
            if line.startswith('|'):
                data_rows.append([c.strip() for c in line.split('|')[1:-1]])
        
        th_html = "".join(f'<th style="border: 1px solid #cbd5e1; padding: 6px 12px; background: #1e3a8a; color: #ffffff; text-align: left; font-size: 0.9em;">{html.escape(h)}</th>' for h in headers)
        tr_rows = []
        for row_idx, row in enumerate(data_rows):
            bg = "#f8fafc" if row_idx % 2 == 1 else "#ffffff"
            tds = "".join(f'<td style="border: 1px solid #cbd5e1; padding: 6px 12px; background: {bg}; font-size: 0.9em;">{html.escape(c)}</td>' for c in row)
            tr_rows.append(f'<tr>{tds}</tr>')
        
        return f'<table style="border-collapse: collapse; margin: 0.75rem 0; width: auto; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;"><thead><tr>{th_html}</tr></thead><tbody>{"".join(tr_rows)}</tbody></table>'

    table_pattern = re.compile(r'(?:^[ \t]*\|.+?\|[ \t]*\n)+(?:^[ \t]*\|[-: |]+\|[ \t]*\n)(?:^[ \t]*\|.+?\|[ \t]*\n*)+', re.MULTILINE)
    prompt = table_pattern.sub(replace_table, prompt)

    # 3. Inline code
    def replace_inline_code(match):
        code_text = html.escape(match.group(1))
        return f'<code style="background: #f1f5f9; color: #0369a1; padding: 0.15rem 0.35rem; border-radius: 3px; font-family: Consolas, monospace; font-size: 0.9em; font-weight: 600;">{code_text}</code>'

    prompt = re.sub(r'`([^`\n]+)`', replace_inline_code, prompt)

    # 4. Bold and italics
    prompt = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', prompt)
    prompt = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', prompt)

    # 5. Convert paragraphs and line breaks
    blocks = re.split(r'\n{2,}', prompt.strip())
    html_blocks = []
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        if b.startswith('<div') or b.startswith('<table') or b.startswith('<pre'):
            html_blocks.append(b)
        else:
            b_clean = b.replace('\n', '<br/>')
            html_blocks.append(f'<p style="margin: 0.5rem 0; line-height: 1.6;">{b_clean}</p>')

    return f'<div style="font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif; font-size: 1rem; line-height: 1.6; color: #1e293b;">{"".join(html_blocks)}</div>'

def build_qti_xml(quiz_id: str, quiz_title: str, questions: list) -> str:
    """Generates standard QTI 1.2 XML matching the exact Canvas Multiple Choice profile."""
    items_xml = []
    for q in questions:
        q_num = q["num"]
        item_id = make_id(f"{quiz_id}_q_{q_num}")
        
        opt_labels = []
        correct_opt_id = None
        for opt_letter, opt_text in q["options"]:
            opt_id = make_id(f"{item_id}_opt_{opt_letter}")
            clean_text = clean_quiz_text(opt_text)
            if "```" in clean_text or "\n" in clean_text:
                opt_html = format_quiz_prompt_html(clean_text)
                opt_labels.append(f"""              <response_label ident="{opt_id}">
                <material>
                  <mattext texttype="text/html">{html.escape(opt_html)}</mattext>
                </material>
              </response_label>""")
            else:
                opt_labels.append(f"""              <response_label ident="{opt_id}">
                <material>
                  <mattext texttype="text/plain">{html.escape(clean_text)}</mattext>
                </material>
              </response_label>""")
            
            if opt_letter == q["correct_answer"]:
                correct_opt_id = opt_id

        if not correct_opt_id:
            correct_opt_id = make_id(f"{item_id}_opt_A")

        options_block = "\n".join(opt_labels)
        prompt_html = format_quiz_prompt_html(q["prompt"])

        items_xml.append(f"""      <item ident="{item_id}" title="Question {q_num}">
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>question_type</fieldlabel>
              <fieldentry>multiple_choice_question</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>points_possible</fieldlabel>
              <fieldentry>2.0</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>assessment_question_identifierref</fieldlabel>
              <fieldentry>{item_id}</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>cc_profile</fieldlabel>
              <fieldentry>cc.multiple_choice.v0p1</fieldentry>
            </qtimetadatafield>
          </qtimetadata>
        </itemmetadata>
        <presentation>
          <material>
            <mattext texttype="text/html">{html.escape(prompt_html)}</mattext>
          </material>
          <response_lid ident="response1" rcardinality="Single">
            <render_choice>
{options_block}
            </render_choice>
          </response_lid>
        </presentation>
        <resprocessing>
          <outcomes>
            <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
          </outcomes>
          <respcondition continue="No">
            <conditionvar>
              <varequal respident="response1">{correct_opt_id}</varequal>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
          </respcondition>
        </resprocessing>
      </item>""")

    items_joined = "\n".join(items_xml)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/profile/cc/ccv1p1/ccv1p1_qtiasiv1p2p1_v1p0.xsd">
  <assessment ident="{quiz_id}" title="{html.escape(quiz_title)}">
    <qtimetadata>
      <qtimetadatafield>
        <fieldlabel>cc_profile</fieldlabel>
        <fieldentry>cc.exam.v0p1</fieldentry>
      </qtimetadatafield>
      <qtimetadatafield>
        <fieldlabel>qmd_assessmenttype</fieldlabel>
        <fieldentry>Examination</fieldentry>
      </qtimetadatafield>
      <qtimetadatafield>
        <fieldlabel>qmd_scoretype</fieldlabel>
        <fieldentry>Percentage</fieldentry>
      </qtimetadatafield>
      <qtimetadatafield>
        <fieldlabel>cc_maxattempts</fieldlabel>
        <fieldentry>3</fieldentry>
      </qtimetadatafield>
    </qtimetadata>
    <section ident="root_section">
{items_joined}
    </section>
  </assessment>
</questestinterop>
"""

def build_assessment_meta_xml(quiz_id: str, quiz_title: str, quiz_group_id: str, due_at: str = None, lock_at: str = None) -> str:
    """Builds Canvas assessment_meta.xml."""
    assign_id = make_id(f"assign_{quiz_id}")
    due_block = f"  <due_at>{due_at}</due_at>\n  <lock_at>{lock_at}</lock_at>\n" if due_at else ""
    assign_due_block = f"    <due_at>{due_at}</due_at>\n    <lock_at>{lock_at}</lock_at>\n" if due_at else ""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<quiz xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd" identifier="{quiz_id}">
  <title>{html.escape(quiz_title)}</title>
  <description>&lt;p&gt;This weekly assessment tests your mastery of the relational SQL concepts, syntax, and query patterns covered in this unit.&lt;/p&gt;&lt;p&gt;The quiz consists of 15 multiple-choice questions (30 points total, 2 points each). You have 3 attempts; your highest score will be kept.&lt;/p&gt;</description>
{due_block}  <shuffle_questions>false</shuffle_questions>
  <shuffle_answers>false</shuffle_answers>
  <scoring_policy>keep_highest</scoring_policy>
  <quiz_type>assignment</quiz_type>
  <points_possible>30.0</points_possible>
  <allowed_attempts>3</allowed_attempts>
  <show_correct_answers>true</show_correct_answers>
  <assignment identifier="{assign_id}">
    <title>{html.escape(quiz_title)}</title>
{assign_due_block}    <workflow_state>published</workflow_state>
    <quiz_identifierref>{quiz_id}</quiz_identifierref>
    <points_possible>30.0</points_possible>
    <grading_type>points</grading_type>
    <submission_types>online_quiz</submission_types>
    <assignment_group_identifierref>{quiz_group_id}</assignment_group_identifierref>
  </assignment>
</quiz>
"""

def build_assignment_settings_xml(assign_id: str, title: str, group_id: str, points: float = 100.0, due_at: str = None, lock_at: str = None) -> str:
    """Generates standard Canvas assignment_settings.xml matching institutional format."""
    due_block = f"  <due_at>{due_at}</due_at>\n  <lock_at>{lock_at}</lock_at>\n" if due_at else ""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<assignment identifier="{assign_id}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>{html.escape(title)}</title>
  <time_zone_edited>Mountain Time (US &amp; Canada)</time_zone_edited>
  <module_locked>false</module_locked>
  <assignment_group_identifierref>{group_id}</assignment_group_identifierref>
  <workflow_state>published</workflow_state>
{due_block}  <assignment_overrides>
  </assignment_overrides>
  <allowed_extensions>sql,txt,pdf</allowed_extensions>
  <has_group_category>false</has_group_category>
  <points_possible>{points:.1f}</points_possible>
  <grading_type>points</grading_type>
  <submission_types>online_text_entry,online_upload</submission_types>
  <turnitin_enabled>false</turnitin_enabled>
  <vericite_enabled>false</vericite_enabled>
  <peer_reviews>false</peer_reviews>
  <automatic_peer_reviews>false</automatic_peer_reviews>
  <anonymous_peer_reviews>false</anonymous_peer_reviews>
  <freeze_on_copy>false</freeze_on_copy>
  <omit_from_final_grade>false</omit_from_final_grade>
  <hide_in_gradebook>false</hide_in_gradebook>
  <post_policy>
    <post_manually>false</post_manually>
  </post_policy>
</assignment>
"""


def main():
    config = load_course_config()
    c_code = config.get("course_code", "COURSE 1010")
    c_title = config.get("course_title", "Applied Systems")
    c_code_clean = c_code.replace(" ", "_")
    imscc_output_file = os.path.join(BASE_DIR, f"{c_code_clean}_Complete.imscc")

    print("=" * 65)
    print(f"{c_code}: {c_title} - Canvas Course Cartridge Builder")
    print("=" * 65)

    # 1. Prepare directories
    os.makedirs(OUTPUT_BUILD_DIR, exist_ok=True)
    wiki_dir = os.path.join(OUTPUT_BUILD_DIR, "wiki_content")
    settings_dir = os.path.join(OUTPUT_BUILD_DIR, "course_settings")
    non_cc_dir = os.path.join(OUTPUT_BUILD_DIR, "non_cc_assessments")
    web_res_dir = os.path.join(OUTPUT_BUILD_DIR, "web_resources")
    syllabi_dir = os.path.join(web_res_dir, "syllabi")
    images_dir = os.path.join(web_res_dir, "images")
    os.makedirs(wiki_dir, exist_ok=True)
    os.makedirs(settings_dir, exist_ok=True)
    os.makedirs(non_cc_dir, exist_ok=True)
    os.makedirs(syllabi_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    # 2. Assignment Groups
    groups_cfg = config.get("assignment_groups", [
        {"key": "labs", "name": "Hands-on Applied Labs", "weight": 40.0},
        {"key": "quizzes", "name": "Unit Knowledge Checks & Quizzes", "weight": 20.0},
        {"key": "prep", "name": "Asynchronous Preparation & Drills", "weight": 10.0},
        {"key": "capstone", "name": "Comprehensive Course Capstone", "weight": 30.0}
    ])
    group_map = {}
    ag_items = []
    for pos, g in enumerate(groups_cfg, 1):
        gid = make_id(f"group_{g['key']}")
        group_map[g['key']] = gid
        ag_items.append(f"""  <assignmentGroup identifier="{gid}">
    <title>{html.escape(g['name'])}</title>
    <position>{pos}</position>
    <group_weight>{float(g['weight']):.1f}</group_weight>
  </assignmentGroup>""")

    group_labs_id = group_map.get("labs", list(group_map.values())[0])
    group_quizzes_id = group_map.get("quizzes", list(group_map.values())[1] if len(group_map) > 1 else group_labs_id)

    assign_groups_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<assignmentGroups xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
{chr(10).join(ag_items)}
</assignmentGroups>
"""
    with open(os.path.join(settings_dir, "assignment_groups.xml"), "w", encoding="utf-8") as f:
        f.write(assign_groups_xml)

    # 3. Canvas Course Export Signature Files
    with open(os.path.join(settings_dir, "canvas_export.txt"), "w", encoding="utf-8") as f:
        f.write("Q: What did the panda say when he was forced out of his natural habitat?\nA: This is un-BEAR-able\n")

    context_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<context_info xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <course_name>{html.escape(c_code)}: {html.escape(c_title)}</course_name>
  <root_account_id>105390000000000001</root_account_id>
  <root_account_name>{html.escape(config.get("institution", "Laramie County Community College"))}</root_account_name>
  <canvas_domain>{html.escape(config.get("domain", "lccc-wy.instructure.com"))}</canvas_domain>
</context_info>
"""
    with open(os.path.join(settings_dir, "context.xml"), "w", encoding="utf-8") as f:
        f.write(context_xml)

    with open(os.path.join(settings_dir, "files_meta.xml"), "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<fileMeta xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <folders></folders>
  <files></files>
</fileMeta>
""")

    course_id = make_id(f"{c_code_clean.lower()}_course")
    course_settings_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<course identifier="{course_id}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>{html.escape(c_code)}: {html.escape(c_title)}</title>
  <course_code>{html.escape(c_code)}</course_code>
  <is_public>false</is_public>
  <default_view>wiki</default_view>
  <license>private</license>
  <grading_standard_enabled>true</grading_standard_enabled>
</course>
"""
    with open(os.path.join(settings_dir, "course_settings.xml"), "w", encoding="utf-8") as f:
        f.write(course_settings_xml)

    # Copy Word Document Syllabus to web_resources/syllabi
    dst_docx_name = f"{c_code_clean}_Master_Syllabus.docx"
    dst_docx_path = os.path.join(syllabi_dir, dst_docx_name)
    src_docx = os.path.join(COURSE_SPECS_DIR, dst_docx_name)
    if not os.path.exists(src_docx):
        for f in os.listdir(COURSE_SPECS_DIR) if os.path.exists(COURSE_SPECS_DIR) else []:
            if f.endswith(".docx"):
                src_docx = os.path.join(COURSE_SPECS_DIR, f)
                break
    syllabus_docx_res_id = make_id("res_syllabus_docx")
    if os.path.exists(src_docx):
        with open(src_docx, "rb") as sf, open(dst_docx_path, "wb") as df:
            df.write(sf.read())
    else:
        # Create minimal placeholder docx if not present
        with zipfile.ZipFile(dst_docx_path, "w") as zf:
            zf.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')

    # Load custom instructor videos from shared_assets/VideoMap.md
    custom_videos = load_video_map()
    orient_videos = [v for v in custom_videos if v["type"] == "orientation"]
    orient_video = orient_videos[0] if orient_videos else None
    orient_syllabus_link = ""
    if orient_video:
        orient_syllabus_link = f'\n<p style="margin-top: 0.75rem;"><strong>Course Orientation Video:</strong> <a href="{orient_video["url"]}" target="_blank" rel="noopener">Watch Course Orientation Video on YouTube</a></p>'

    # Build Native Syllabus HTML
    grading_lis = "".join([f"<li><strong>{html.escape(g['name'])} ({float(g['weight']):.0f}%):</strong> Evaluated according to course criteria.</li>" for g in groups_cfg])
    syllabus_body = f"""<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><title>Syllabus</title></head>
<body>
<div id="dp-wrapper" class="dp-wrapper">
<header class="dp-header dp-basic-bar" style="background: #1e3a8a; color: #ffffff; padding: 1.5rem; border-radius: 6px; margin-bottom: 1.5rem;">
  <h2 style="margin: 0; color: #ffffff; font-size: 1.8rem;">{html.escape(c_code)}: {html.escape(c_title)}</h2>
  <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Institutional Course Syllabus &amp; Policies</p>
</header>
<h3>Downloadable Master Syllabus</h3>
<p>The syllabus is a comprehensive guide to this course. Review your syllabus carefully, and ask questions of your instructor to make sure your understanding is clear.</p>
<p><a class="instructure_file_link" title="{dst_docx_name}" href="$IMS-CC-FILEBASE$/syllabi/{dst_docx_name.replace(' ', '%20')}?canvas_=1&amp;canvas_qs_wrap=1" target="_blank" rel="noopener">Download Master Syllabus (Word .docx)</a></p>{orient_syllabus_link}
<hr/>
<h3>Grade Scale &amp; Evaluation Breakdown</h3>
<ul>
{grading_lis}
</ul>
<p><strong>Standard Grading Scale:</strong> {html.escape(config.get("grading_scale", "A: 90.0% – 100% | B: 80.0% – 89.9% | C: 70.0% – 79.9% | D: 60.0% – 69.9% | F: Below 60.0%"))}</p>
<hr/>
<h3>Late Work &amp; Academic Integrity Policy</h3>
<p>Assignments, projects, and lab work should be turned in by the designated due date. All submitted work must adhere to college academic integrity standards.</p>
</div>
</body>
</html>"""
    with open(os.path.join(settings_dir, "syllabus.html"), "w", encoding="utf-8") as f:
        f.write(syllabus_body)

    # 4. Discover Units
    units = discover_unit_metadata(UNITS_DIR, config, custom_videos)
    print(f"[*] Discovered {len(units)} units dynamically from units/")

    pages_manifest = []
    modules_data = []
    assignment_manifest = []
    quiz_manifest = []
    discussions_manifest = []

    mod_orient_id = make_id("module_orientation")
    unit_mod_ids = {u["num"]: make_id(f"module_u{u['num']}") for u in units}

    # Orientation Module: Start Here
    p_start_here_id = make_id("page_start_here")
    p_start_here_file = "start-here.html"
    orient_video_embed = render_custom_video_card(orient_video["label"], orient_video["url"], orient_video["embed_url"]) if orient_video else ""

    start_here_html = f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>Start Here: Course Overview &amp; Orientation</title>
<meta name="identifier" content="{p_start_here_id}"/>
<meta name="workflow_state" content="active"/>
</head>
<body>
<div id="dp-wrapper" class="dp-wrapper">
  <header class="dp-header dp-basic-bar" style="background: #1e3a8a; color: #ffffff; padding: 1.5rem; border-radius: 6px; margin-bottom: 1.5rem;">
    <h2 style="margin: 0; color: #ffffff; font-size: 1.8rem;">Course Overview &amp; Orientation</h2>
  </header>
  <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1e293b;">
    <p><strong>Welcome to {html.escape(c_code)}: {html.escape(c_title)}!</strong></p>
    <p>{html.escape(config.get("description", ""))}</p>
    {orient_video_embed}
  </div>
</div>
</body>
</html>"""
    with open(os.path.join(wiki_dir, p_start_here_file), "w", encoding="utf-8") as f:
        f.write(start_here_html)
    pages_manifest.append((p_start_here_file, "Start Here: Course Overview & Orientation", p_start_here_id))

    # Front Page: home-page.html
    p_home_id = make_id("page_home_front")
    p_home_file = "home-page.html"
    mod_links_lis = [
        f'<li><a class="list-group-item" href="$CANVAS_OBJECT_REFERENCE$/modules/{mod_orient_id}">Getting Started - Course Orientation</a></li>'
    ]
    for unit in units:
        u_num = unit["num"]
        u_title = unit["title"]
        m_id = unit_mod_ids[u_num]
        mod_links_lis.append(f'<li><a class="list-group-item" href="$CANVAS_OBJECT_REFERENCE$/modules/{m_id}">{html.escape(u_title)}</a></li>')
    mod_links_joined = "\n".join(mod_links_lis)

    home_html = f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>Home Page</title>
<meta name="identifier" content="{p_home_id}"/>
<meta name="workflow_state" content="active"/>
<meta name="front_page" content="true"/>
</head>
<body>
<div id="dp-wrapper" class="dp-wrapper">
  <header class="dp-header dp-basic-bar" style="background: #1e3a8a; color: #ffffff; padding: 1.5rem; border-radius: 6px; margin-bottom: 1.5rem;">
    <h1 style="margin: 0; color: #ffffff; font-size: 1.8rem;">{html.escape(c_code)}: {html.escape(c_title)}</h1>
  </header>
  <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1e293b;">
    <p><strong>Welcome to {html.escape(c_code)}! Access your modules, syllabus, and course resources below.</strong></p>
    <ul style="line-height: 2;">
{mod_links_joined}
    </ul>
  </div>
</div>
</body>
</html>"""
    with open(os.path.join(wiki_dir, p_home_file), "w", encoding="utf-8") as f:
        f.write(home_html)
    pages_manifest.append((p_home_file, "Home Page", p_home_id))

    # Add Orientation Module
    modules_data.append({
        "id": mod_orient_id,
        "title": "Getting Started - Course Orientation",
        "items": [
            {"type": "WikiPage", "title": "Start Here: Course Overview & Orientation", "ref": p_start_here_id, "indent": 0, "state": "active"},
            {"type": "Attachment", "title": f"Master Course Syllabus (Word .docx)", "ref": syllabus_docx_res_id, "indent": 1, "state": "active"}
        ]
    })

    # 5. Process Weekly Instructional Units
    for unit in units:
        u_num = unit["num"]
        u_folder = unit["folder"]
        u_title = unit["title"]
        u_short = unit["short_title"]
        u_topic = unit["topic"]
        u_dir = os.path.join(UNITS_DIR, u_folder)

        print(f"  [+] Processing {u_short}: {u_folder}")
        code_lang, allowed_ext = detect_code_type(u_dir)
        ai_data = load_learn_with_ai_data(u_num, u_folder, u_topic)
        tg_info = load_teacher_guide_data(u_num, u_folder, u_topic)

        # 1. Overview Page
        overview_id = make_id(f"page_u{u_num}_overview")
        overview_file = f"unit-{u_num:02d}-overview.html"
        ov_raw = load_and_clean_unit_overview(u_num, u_folder)
        lead, obj_md, road_md, time_md = parse_unit_overview_sections(ov_raw, u_num, u_topic)
        ov_panels = [
            ("Course Learning Outcomes & Objectives", parse_markdown_to_html(obj_md)),
            ("Weekly Learning Sequence & Roadmap", parse_markdown_to_html(road_md)),
            ("Instructional Time Budget (300 Min/Week)", parse_markdown_to_html(time_md))
        ]
        with open(os.path.join(wiki_dir, overview_file), "w", encoding="utf-8") as f:
            f.write(render_designplus_html(f"{u_short} Overview: {u_topic}", f"<p>{html.escape(lead)}</p>", ov_panels, overview_id))
        pages_manifest.append((overview_file, f"{u_short} Overview: {u_topic}", overview_id))

        # 2. Readings & Video Lectures Page
        reading_id = make_id(f"page_u{u_num}_readings")
        reading_file = f"unit-{u_num:02d}-readings-and-media.html"
        readings_lis = [f"<li style='margin-bottom: 0.75rem;'><strong><a href='{r[1]}' target='_blank' rel='noopener'>{html.escape(r[0])}</a></strong>: {html.escape(r[2])}</li>" for r in unit["readings"]]
        readings_body = f"<ul style='line-height: 1.7;'>{''.join(readings_lis)}</ul>" if readings_lis else "<p>Review recommended materials in the course study guide.</p>"
        
        unit_lectures = [v for v in custom_videos if v.get("unit_num") == u_num and v.get("type") == "unit_lecture"]
        u_video_cards = "\n".join([render_custom_video_card(v["label"], v["url"], v["embed_url"]) for v in unit_lectures]) if unit_lectures else "<p>See VideoMap.md for video recordings.</p>"

        r_panels = [
            ("Required Readings & Technical Documentation", readings_body),
            ("Micro-Video Lectures (Embedded)", u_video_cards)
        ]
        with open(os.path.join(wiki_dir, reading_file), "w", encoding="utf-8") as f:
            f.write(render_standard_page_html(f"{u_short}: Required Readings & Video Lectures", "<p>Review required reading modules and instructional micro-lectures.</p>", r_panels, reading_id))
        pages_manifest.append((reading_file, f"{u_short}: Required Readings & Video Lectures", reading_id))

        # 3. Asynchronous Preparation & Drills Page
        study_id = make_id(f"page_u{u_num}_async_study")
        study_file = f"unit-{u_num:02d}-async-study.html"
        drills_path = os.path.join(u_dir, "async", "self_check_drills.md")
        drills_html = "<p>Complete the self-check drills in your study guide.</p>"
        if os.path.exists(drills_path):
            with open(drills_path, "r", encoding="utf-8") as df:
                drills_html = parse_markdown_to_html(df.read())
        study_panels = [("Formative Self-Check Drills & Practice", drills_html)]
        with open(os.path.join(wiki_dir, study_file), "w", encoding="utf-8") as f:
            f.write(render_standard_page_html(f"{u_short}: Asynchronous Preparation & Drills", "<p>Formative reflection questions and self-check drills.</p>", study_panels, study_id))
        pages_manifest.append((study_file, f"{u_short}: Asynchronous Preparation & Drills", study_id))

        # 4. Applied Lab Guide Page
        lab_guide_id = make_id(f"page_u{u_num}_applied_lab_guide")
        lab_guide_file = f"unit-{u_num:02d}-applied-lab-guide.html"
        lab_path = os.path.join(u_dir, "guides", "student_lab_guide.md")
        lab_content_html = "<p>Refer to course guides for lab specifications.</p>"
        if os.path.exists(lab_path):
            with open(lab_path, "r", encoding="utf-8") as lf:
                lab_content_html = parse_markdown_to_html(lf.read())
        rubric_path = os.path.join(u_dir, "assessments", "lab_rubric.md")
        rubric_html = "<p>Refer to the grading rubric for scoring criteria.</p>"
        if os.path.exists(rubric_path):
            with open(rubric_path, "r", encoding="utf-8") as rf:
                rubric_html = parse_markdown_to_html(rf.read())
        lab_panels = [
            ("Laboratory Scenario & Task Specifications", lab_content_html),
            ("Grading Rubric & Scoring Criteria", rubric_html)
        ]
        with open(os.path.join(wiki_dir, lab_guide_file), "w", encoding="utf-8") as f:
            f.write(render_standard_page_html(f"{u_short}: Applied Lab Guide", "<p>Hands-on technical scenario, tasks, and rubric criteria.</p>", lab_panels, lab_guide_id))
        pages_manifest.append((lab_guide_file, f"{u_short}: Applied Lab Guide", lab_guide_id))

        # 5. Native Canvas Assignment
        assign_id = make_id(f"canvas_assignment_u{u_num}")
        assign_folder = os.path.join(OUTPUT_BUILD_DIR, assign_id)
        os.makedirs(assign_folder, exist_ok=True)
        assign_title = f"{u_short} Applied Lab Assignment"
        assign_html_filename = f"unit-{u_num:02d}-lab-assignment.html"
        assign_settings_xml = build_assignment_settings_xml(
            assign_id, assign_title, group_labs_id, points=50.0,
            due_at=unit.get("due_iso"), lock_at=unit.get("due_iso")
        )
        with open(os.path.join(assign_folder, "assignment_settings.xml"), "w", encoding="utf-8") as af:
            af.write(assign_settings_xml)

        assign_desc_html = f"""<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><title>{html.escape(assign_title)}</title></head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1e293b; padding: 1rem; max-width: 900px;">
  <h2 style="color: #1e3a8a; border-bottom: 2px solid #1e3a8a; padding-bottom: 0.3rem;">{html.escape(assign_title)} (50 Points)</h2>
  <p>Complete the exercises in the <strong>{u_short}: Applied Lab Guide</strong> and upload your completed solution file below.</p>
  <div style="margin-top: 1rem;">{rubric_html}</div>
</body>
</html>"""
        with open(os.path.join(assign_folder, assign_html_filename), "w", encoding="utf-8") as ahf:
            ahf.write(assign_desc_html)
        assignment_manifest.append((assign_id, assign_html_filename, assign_title))

        # 6. Learn with AI Page
        ai_page_id = make_id(f"page_u{u_num}_learn_with_ai")
        ai_page_file = f"unit-{u_num:02d}-learn-with-ai.html"
        prompt_box_html = f"""<div style="background: #0f172a; color: #f8fafc; padding: 1rem 1.25rem; border-radius: 6px; font-family: Consolas, monospace; margin: 1rem 0;"><pre style="margin: 0; white-space: pre-wrap; color: inherit;"><code>{html.escape(ai_data['prompt'])}</code></pre></div>"""
        ai_panels = [
            ("Roleplay Persona & Instructions", f"<p><strong>Persona:</strong> {html.escape(ai_data['persona'])}</p><p>Copy the prompt below into ChatGPT, Claude, or Gemini:</p>{prompt_box_html}"),
            ("Reflection Debrief", f"<p>{html.escape(ai_data['discussion_prompt'])}</p>")
        ]
        with open(os.path.join(wiki_dir, ai_page_file), "w", encoding="utf-8") as f:
            f.write(render_standard_page_html(f"{u_short}: Learn with AI — Supplemental Practice Drill", "<p>AI-assisted Socratic drill to test conceptual depth.</p>", ai_panels, ai_page_id))
        pages_manifest.append((ai_page_file, f"{u_short}: Learn with AI — Supplemental Practice Drill", ai_page_id))

        # 7. Discussion Topic
        disc_id = make_id(f"disc_u{u_num}")
        disc_title = f"{u_short} Discussion: Learn with AI Debrief"
        disc_dir = os.path.join(OUTPUT_BUILD_DIR, disc_id)
        os.makedirs(disc_dir, exist_ok=True)
        disc_html = f"<p>{html.escape(ai_data['discussion_prompt'])}</p>"
        disc_xml_str = f"""<?xml version="1.0" encoding="UTF-8"?>
<topic xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1 http://www.imsglobal.org/xsd/imsccv1p1/ccv1p1_imsdt_v1p1.xsd">
  <title>{html.escape(disc_title)}</title>
  <text texttype="text/html">{html.escape(disc_html)}</text>
</topic>
"""
        with open(os.path.join(disc_dir, "discussion_topic.xml"), "w", encoding="utf-8") as df:
            df.write(disc_xml_str)
        discussions_manifest.append((disc_id, disc_title, f"{disc_id}/discussion_topic.xml"))

        # 8. QTI Quiz
        quiz_path = os.path.join(u_dir, "assessments", "unit_quiz.md")
        questions = parse_quiz_md(quiz_path) if os.path.exists(quiz_path) else []
        quiz_id = make_id(f"quiz_u{u_num}")
        quiz_meta_id = make_id(f"quiz_meta_u{u_num}")
        quiz_title = f"{u_short} Knowledge Check: {u_topic}"
        q_dir = os.path.join(OUTPUT_BUILD_DIR, quiz_id)
        os.makedirs(q_dir, exist_ok=True)
        if questions:
            qti_xml_str = build_qti_xml(quiz_id, quiz_title, questions)
            with open(os.path.join(q_dir, "assessment_qti.xml"), "w", encoding="utf-8") as qf:
                qf.write(qti_xml_str)
            meta_xml_str = build_assessment_meta_xml(
                quiz_id, quiz_title, group_quizzes_id,
                due_at=unit.get("due_iso"), lock_at=unit.get("due_iso")
            )
            with open(os.path.join(q_dir, "assessment_meta.xml"), "w", encoding="utf-8") as mf:
                mf.write(meta_xml_str)
            with open(os.path.join(non_cc_dir, f"{quiz_id}.xml.qti"), "w", encoding="utf-8") as ncf:
                ncf.write(qti_xml_str)
            quiz_manifest.append((quiz_id, quiz_meta_id, quiz_title))

        # 9. Instructor Guide (Unpublished)
        teacher_id = make_id(f"page_u{u_num}_teacher_guide")
        teacher_file = f"unit-{u_num:02d}-instructor-guide.html"
        sol_path = os.path.join(u_dir, "guides", "instructor_solution.py")
        if not os.path.exists(sol_path):
            sol_path = os.path.join(u_dir, "guides", "instructor_solution.sql")
        sol_html = "<p>Refer to course repository for instructor solution keys.</p>"
        if os.path.exists(sol_path):
            with open(sol_path, "r", encoding="utf-8") as sf:
                sol_html = f"<div style='background: #0f172a; color: #f8fafc; padding: 1rem 1.25rem; border-radius: 6px; overflow-x: auto; font-family: Consolas, monospace; font-size: 0.9em;'><pre style='margin: 0; background: transparent; color: inherit;'><code>{html.escape(sf.read().strip())}</code></pre></div>"

        teacher_panels = [
            ("Lecture Walkthrough Blueprint", f"<pre style='background: #f8fafc; padding: 1rem; border: 1px solid #cbd5e1;'><code>{html.escape(tg_info['sync_agenda'])}</code></pre>"),
            ("Instructor Master Solution Key", sol_html)
        ]
        with open(os.path.join(wiki_dir, teacher_file), "w", encoding="utf-8") as f:
            f.write(render_standard_page_html(f"[Instructor Guide] {u_short} Teaching Notes & Solutions", "<p><strong>[FOR INSTRUCTORS ONLY — UNPUBLISHED]</strong></p>", teacher_panels, teacher_id, workflow_state="unpublished"))
        pages_manifest.append((teacher_file, f"[Instructor Guide] {u_short} Teaching Notes & Solutions", teacher_id))

        # Module assembly
        u_mod_items = [
            {"type": "WikiPage", "title": f"{u_short} Overview: {u_topic}", "ref": overview_id, "indent": 0, "state": "active"},
            {"type": "WikiPage", "title": f"{u_short}: Required Readings & Video Lectures", "ref": reading_id, "indent": 1, "state": "active"},
            {"type": "WikiPage", "title": f"{u_short}: Asynchronous Preparation & Drills", "ref": study_id, "indent": 1, "state": "active"},
            {"type": "WikiPage", "title": f"{u_short}: Applied Lab Guide", "ref": lab_guide_id, "indent": 1, "state": "active"},
            {"type": "Assignment", "title": assign_title, "ref": assign_id, "indent": 1, "state": "active"},
            {"type": "WikiPage", "title": f"{u_short}: Learn with AI — Supplemental Practice Drill", "ref": ai_page_id, "indent": 1, "state": "active"},
            {"type": "DiscussionTopic", "title": disc_title, "ref": disc_id, "indent": 1, "state": "active"}
        ]
        if questions:
            u_mod_items.append({"type": "Quizzes::Quiz", "title": quiz_title, "ref": quiz_id, "indent": 1, "state": "active"})
        u_mod_items.append({"type": "WikiPage", "title": f"[Instructor Guide] {u_short} Teaching Notes & Solutions", "ref": teacher_id, "indent": 1, "state": "unpublished"})

        modules_data.append({
            "id": unit_mod_ids[u_num],
            "title": u_title,
            "items": u_mod_items
        })

    # 6. Generate course_settings/module_meta.xml
    modules_xml_items = []
    org_items = []
    for pos, mod in enumerate(modules_data, 1):
        mod_id = mod["id"]
        mod_title = mod["title"]
        m_items_xml = []
        m_man_items = []
        for i_pos, item in enumerate(mod["items"], 1):
            shared_item_id = make_id(f"item_{mod_id}_{item['ref']}")
            item_state = item.get("state", "active")
            item_indent = item.get("indent", 0)
            m_items_xml.append(f"""      <item identifier="{shared_item_id}">
        <content_type>{item['type']}</content_type>
        <workflow_state>{item_state}</workflow_state>
        <title>{html.escape(item['title'])}</title>
        <identifierref>{item['ref']}</identifierref>
        <position>{i_pos}</position>
        <new_tab>false</new_tab>
        <indent>{item_indent}</indent>
        <link_settings_json>null</link_settings_json>
      </item>""")
            m_man_items.append(f"""          <item identifier="{shared_item_id}" identifierref="{item['ref']}">
            <title>{html.escape(item['title'])}</title>
          </item>""")

        items_joined = "\n".join(m_items_xml)
        modules_xml_items.append(f"""  <module identifier="{mod_id}">
    <title>{html.escape(mod_title)}</title>
    <workflow_state>active</workflow_state>
    <position>{pos}</position>
    <require_sequential_progress>false</require_sequential_progress>
    <locked>false</locked>
    <items>
{items_joined}
    </items>
  </module>""")

        man_items_joined = "\n".join(m_man_items)
        org_items.append(f"""        <item identifier="{mod_id}">
          <title>{html.escape(mod_title)}</title>
{man_items_joined}
        </item>""")

    modules_meta_joined = "\n".join(modules_xml_items)
    modules_meta_str = f"""<?xml version="1.0" encoding="UTF-8"?>
<modules xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
{modules_meta_joined}
</modules>
"""
    with open(os.path.join(settings_dir, "module_meta.xml"), "w", encoding="utf-8") as f:
        f.write(modules_meta_str)

    # 7. Generate imsmanifest.xml
    manifest_id = make_id(f"{c_code_clean.lower()}_manifest")
    org_items_joined = "\n".join(org_items)
    resources_xml = [
        f"""    <resource identifier="{course_id}_syllabus" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="course_settings/syllabus.html" intendeduse="syllabus">
      <file href="course_settings/syllabus.html"/>
    </resource>
    <resource identifier="{course_id}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="course_settings/canvas_export.txt">
      <file href="course_settings/course_settings.xml"/>
      <file href="course_settings/module_meta.xml"/>
      <file href="course_settings/assignment_groups.xml"/>
      <file href="course_settings/context.xml"/>
      <file href="course_settings/canvas_export.txt"/>
      <file href="course_settings/files_meta.xml"/>
    </resource>
    <resource identifier="{syllabus_docx_res_id}" type="webcontent" href="web_resources/syllabi/{dst_docx_name}">
      <file href="web_resources/syllabi/{dst_docx_name}"/>
    </resource>"""
    ]

    for p_file, p_title, p_id in pages_manifest:
        resources_xml.append(f"""    <resource identifier="{p_id}" type="webcontent" href="wiki_content/{p_file}">
      <file href="wiki_content/{p_file}"/>
    </resource>""")

    for a_id, a_html_file, a_title in assignment_manifest:
        resources_xml.append(f"""    <resource identifier="{a_id}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="{a_id}/{a_html_file}">
      <file href="{a_id}/{a_html_file}"/>
      <file href="{a_id}/assignment_settings.xml"/>
    </resource>""")

    for q_id, q_meta_id, q_title in quiz_manifest:
        resources_xml.append(f"""    <resource identifier="{q_id}" type="imsqti_xmlv1p2/imscc_xmlv1p1/assessment">
      <file href="{q_id}/assessment_qti.xml"/>
      <dependency identifierref="{q_meta_id}"/>
    </resource>
    <resource identifier="{q_meta_id}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="{q_id}/assessment_meta.xml">
      <file href="{q_id}/assessment_meta.xml"/>
      <file href="non_cc_assessments/{q_id}.xml.qti"/>
    </resource>""")

    for d_id, d_title, d_file in discussions_manifest:
        resources_xml.append(f"""    <resource identifier="{d_id}" type="imsdt_xmlv1p1">
      <file href="{d_file}"/>
    </resource>""")

    resources_xml_joined = "\n".join(resources_xml)
    imsmanifest_str = f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{manifest_id}" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource" xmlns:lomimscc="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1 http://www.imsglobal.org/profile/cc/ccv1p1/ccv1p1_imscp_v1p2_v1p0.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lomresource_v1p0.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lommanifest_v1p0.xsd">
  <metadata>
    <schema>IMS Common Cartridge</schema>
    <schemaversion>1.1.0</schemaversion>
    <lomimscc:lom>
      <lomimscc:general>
        <lomimscc:title>
          <lomimscc:string>{html.escape(c_code)}: {html.escape(c_title)}</lomimscc:string>
        </lomimscc:title>
      </lomimscc:general>
    </lomimscc:lom>
  </metadata>
  <organizations>
    <organization identifier="org_1" structure="rooted-hierarchy">
      <item identifier="LearningModules">
{org_items_joined}
      </item>
    </organization>
  </organizations>
  <resources>
{resources_xml_joined}
  </resources>
</manifest>
"""
    with open(os.path.join(OUTPUT_BUILD_DIR, "imsmanifest.xml"), "w", encoding="utf-8") as f:
        f.write(imsmanifest_str)

    # 8. Schema & XML Verification Suite
    print("\n--- Running XML Validation Suite ---")
    xml_files_tested = 0
    for root, dirs, files in os.walk(OUTPUT_BUILD_DIR):
        for file in files:
            if file.endswith(".xml") or file.endswith(".qti"):
                file_path = os.path.join(root, file)
                try:
                    ET.parse(file_path)
                    xml_files_tested += 1
                except Exception as e:
                    print(f"ERROR in XML file {file_path}: {e}")
                    sys.exit(1)
    print(f"SUCCESS: Verified {xml_files_tested} XML files. Zero syntax errors!")

    # 9. Backup previous build
    if os.path.exists(imscc_output_file):
        backup_dir = os.path.join(BASE_DIR, "archive", "cartridge_backups")
        os.makedirs(backup_dir, exist_ok=True)
        mtime = os.path.getmtime(imscc_output_file)
        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"{c_code_clean}_Complete_{mtime_str}.imscc")
        if not os.path.exists(backup_path):
            shutil.copy2(imscc_output_file, backup_path)
            print(f"[Backup] Preserved previous cartridge to: {backup_path}")

    # 10. Package into .imscc
    print(f"\n--- Packaging into {imscc_output_file} ---")
    total_files = 0
    with zipfile.ZipFile(imscc_output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(OUTPUT_BUILD_DIR):
            for file in files:
                abs_path = os.path.join(root, file)
                arc_name = os.path.relpath(abs_path, OUTPUT_BUILD_DIR)
                zipf.write(abs_path, arc_name)
                total_files += 1

    size_mb = os.path.getsize(imscc_output_file) / (1024 * 1024)
    print(f"SUCCESS: Created {imscc_output_file} ({total_files} files, {size_mb:.2f} MB)")
    print("Canvas Native Course Export Package build complete!\n")

if __name__ == "__main__":
    main()
