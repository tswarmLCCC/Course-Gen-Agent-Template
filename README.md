# Course Generation Agent Template: Applied AI Agent Architectures

A turnkey, production-grade template and agentic toolchain for programmatically authoring, styling, packaging, and deploying accredited college and enterprise courses into **Canvas LMS** via **Common Cartridge (`.imscc`)**.

Equipped with zero-dependency Python build engines, progressive-disclosure agent skills under `.agents/`, DesignPLUS-compliant page renderers, native QTI 1.2 quiz compilers, and a 16:9 widescreen PowerPoint presentation engine.

---

## What This Template Solves

Building courses directly inside Canvas or through naive cartridge exports causes notorious bugs:
1. **The "Canvas HTML File Link" Bug:** Canvas imports pages as raw static file downloads rather than native interactive Canvas Pages (`WikiPage`). *This toolkit fixes this by synchronizing `<content_type>WikiPage</content_type>` across `module_meta.xml` and `imsmanifest.xml`.*
2. **Broken Canvas CSS Styling:** Custom stylesheets are frequently blocked by institution security policies. *This toolkit embeds self-contained, DesignPLUS-compliant responsive styles, ribbons, zebra tables, and dark syntax boxes directly into page HTML.*
3. **Manual Quiz Entry:** Manually typing 15 questions per unit into Canvas takes hours. *This toolkit compiles clean Markdown quiz files directly into Canvas-compliant QTI 1.2 XML with rationales and assessment metadata.*
4. **Disjointed Presentation Decks:** Lecture slides often lack accessibility or consistent branding. *This toolkit includes `SlideEngine`, a programmatic 16:9 widescreen PowerPoint generator supporting 5 universal slide archetypes with 100% speaker notes coverage.*
5. **Accredited Word Syllabi:** Automatically generates both a native Canvas HTML syllabus and a downloadable OpenXML Word document (`.docx`) conforming to higher-education accreditation standards.

---

## Sample Course: AINT 2050
**Applied AI Agent Architectures: From Conversational Spark to LangGraph Systems**  
An accelerated, hands-on exploration of the modern AI Agent spectrum across three foundational tiers:
- **Level 1 (Foundation Assistants & Conversational Spark)**: Google Gemini 1.5 Pro, Anthropic Claude 3.5 Sonnet, ReAct cognitive loops, and OpenAPI / JSON Schema tool calling contracts.
- **Level 2 (Visual Workflow Automation)**: Low-code visual node canvases (n8n, Langflow), incoming webhook triggers, HMAC SHA-256 security, modular memory buffers, and visual RAG pipelines.
- **Level 3 (Code-First Stateful Graphs)**: Cyclical state machine engineering with LangGraph, strongly-typed `TypedDict` schemas with reducers, conditional edge routing, checkpointer persistence (`MemorySaver`), and Human-in-the-Loop (HITL) approval breakpoints.

---

## Quick Start (3 Steps)

### Step 1: Clone & Launch Environment
Everything runs out-of-the-box in **GitHub Codespaces** or any local Python 3.11+ environment:
```bash
python3 -m pip install pytest python-pptx
```

### Step 2: Configure Your Course Metadata
Edit `course_config.json` to define your course code, title, term, institution, and 100% weighted gradebook groups:
```json
{
  "course_code": "AINT 2050",
  "course_title": "Applied AI Agent Architectures: From Conversational Spark to LangGraph Systems",
  "term": "Fall 2026",
  "institution": "Laramie County Community College",
  "domain": "lccc-wy.instructure.com",
  "credits": "3.0 Credit Hours (Hybrid / Active Learning)",
  "assignment_groups": [
    { "key": "labs", "name": "Hands-on Applied Agent Labs", "weight": 40.0 },
    { "key": "capstone", "name": "Comprehensive Agent Architecture Capstone", "weight": 30.0 },
    { "key": "quizzes", "name": "Unit Knowledge Checks & Architecture Quizzes", "weight": 20.0 },
    { "key": "prep", "name": "Asynchronous Preparation & Socratic AI Drills", "weight": 10.0 }
  ]
}
```

### Step 3: Compile Cartridge & Slide Decks
Run the master CLI compiler:
```bash
# 1. Compile Canvas Common Cartridge (.imscc)
python build_course.py

# 2. Generate 16:9 Widescreen Lecture Presentation Deck (.pptx)
python scripts/generate_sample_slides.py

# 3. Run Comprehensive Quality & XML Audit Suite
python scripts/audit_course.py
```
Output: Generates `AINT_2050_Complete.imscc` and `presentations/AINT_2050_Unit_01_Presentation.pptx`, fully audited and ready to import into Canvas!

---

## Repository Architecture

```text
.
├── .agents/                               # Agent Customization Roots
│   ├── rules/
│   │   ├── emoticon_usage.md             # Strict professional emoticon/emoji policy
│   │   ├── pedagogical_standards.md      # 14-artifact unit framework & 300m contact model
│   │   └── video_mapping.md              # Dynamic video lecture & lab walkthrough router
│   └── skills/
│       ├── canvas-course-builder/        # End-to-end .imscc builder & DesignPLUS styler
│       ├── slide-deck-generator/         # 16:9 widescreen PowerPoint generator (5 archetypes)
│       ├── course-intake-scanner/        # Scans knowledge drops to scaffold courses
│       └── syllabus-docx-cloner/         # Accredited OpenXML Word (.docx) cloner
│
├── course_config.json                     # Master declarative course specification
├── build_course.py                        # Master CLI builder (also mirrored in scripts/)
├── AINT_2050_Complete.imscc               # Compiled Canvas Cartridge package (verified zero XML errors)
│
├── course_specs/                          # Master Institutional Governance
│   ├── course_learning_outcomes.md       # CLOs 1–6 mapped to Bloom's taxonomy & competencies
│   ├── syllabus_master.md                # 8-week modular hybrid schedule (300 min/week budget)
│   ├── grading_and_assessment_policy.md  # Weighted grading scale, loop guards & AI policy
│   ├── external_resources_guide.md       # Curated documentation, papers & video links
│   └── AINT_2050_Master_Syllabus.docx    # Auto-generated accredited Word syllabus
│
├── units/                                 # Modular Curricula (The 14-Artifact Standard)
│   ├── unit_01_the_agent_spectrum_and_foundation_assistants/ # Level 1: Gemini & Claude
│   ├── unit_02_visual_workflow_automation_n8n_and_langflow/  # Level 2: n8n & Langflow
│   └── unit_03_code_first_stateful_graphs_langgraph/         # Level 3: LangGraph Graphs
│
├── presentations/                         # Standalone Slide Decks
│   └── AINT_2050_Unit_01_Presentation.pptx# Widescreen 16:9 PowerPoint deck with speaker notes
│
├── scripts/                               # Core Python Automation Suite
│   ├── build_course.py                   # Master course compiler CLI
│   ├── build_cartridge.py                # Pure Python Canvas Common Cartridge synthesizer
│   ├── html_styler.py                    # DesignPLUS markdown-to-HTML converter
│   ├── qti_builder.py                    # Markdown to QTI 1.2 XML quiz compiler
│   ├── docx_syllabus.py                  # OpenXML Word (.docx) syllabus generator
│   ├── slide_engine.py                   # 16:9 PowerPoint engine (5 universal archetypes)
│   ├── generate_sample_slides.py         # Programmatic slide generator for Unit 1
│   ├── intake_scanner.py                 # Knowledge drop-zone scanner and scaffolder
│   └── audit_course.py                   # Comprehensive verification test suite
│
├── shared_assets/                         # Course Datasets & Media Index
│   └── VideoMap.md                       # Master index of YouTube/video lecture embeds
│
└── archive/                               # Backups & Archives
    └── cartridge_backups/                # Automated timestamped .imscc package backups
```

---

## The 14-Artifact Modular Unit Standard

Every unit in `units/` strictly implements the **14-Artifact Standard** governed by [.agents/rules/pedagogical_standards.md](file:///.agents/rules/pedagogical_standards.md):

| # | Artifact Name | Relative Path | Target Audience & Canvas Item Type |
| :-: | :--- | :--- | :--- |
| **1** | Unit Overview | `overview.md` | Student-facing `WikiPage` with DesignPLUS Banner Ribbon |
| **2** | Study Guide | `async/study_guide.md` | Student-facing `WikiPage` (Required Readings & Videos) |
| **3** | Self-Check Drills | `async/self_check_drills.md` | Student-facing `WikiPage` with collapsible `<details>` cards |
| **4** | Socratic AI Drill | `async/learn_with_ai.md` | Student-facing `WikiPage` (Roleplay prompt & debrief) |
| **5** | Lecture Outline | `lectures/slides.md` | Instructor & student assertion-evidence outline |
| **6** | Micro-Lecture Scripts | `lectures/micro_lecture_scripts.md` | Instructor verbatim recording scripts with timestamps |
| **7** | Instructor Runbook | `lectures/instructor_lecture_notes.md` | Instructor delivery guide with common student traps |
| **8** | Lecture Code Demos | `lectures/partX_*.py` | Runnable demonstration scripts |
| **9** | Slide Presentation | `lectures/*_Presentation.pptx` | 16:9 widescreen PowerPoint deck with speaker notes |
| **10** | Synchronous Lesson Plan| `sync/lesson_plan.md` | Active learning delivery plan (75m / 150m tracks) |
| **11** | In-Class Challenges | `sync/inclass_challenges.py` | Pair-programming drills with assert verification |
| **12** | Student Lab Guide | `guides/student_lab_guide.md` | Student-facing `WikiPage` with DesignPLUS rubric table |
| **13** | Lab Starter Code | `guides/labX_starter.py` | Student starter script with type hints & assert tests |
| **14** | Master Solution Key | `guides/instructor_solution.py` | Master answer key for instructors |
| **15** | Analytic Lab Rubric | `assessments/lab_rubric.md` | SpeedGrader 4-criterion grading matrix (100 pts) |
| **16** | QTI 1.2 Unit Quiz | `assessments/unit_quiz.md` | Native `Quizzes::Quiz` assessment with rationales (15 questions) |

---

## Programmatic Slide Generation (`SlideEngine`)

The template includes an advanced presentation engine in `scripts/slide_engine.py` that builds PowerPoint decks programmatically via `python-pptx` adhering to **WCAG 2.1 AAA high-contrast standards** (`13.333" x 7.5"`):

1. **Split-Hero Title Slide:** Hero badge container, vibrant gold accent stripe, assertion headline.
2. **High-Contrast Section Divider:** Deep Navy background (`#002055`), vertical gold accent bar, section numbering.
3. **Two-Column Comparison Cards:** Ice blue (`#F3F7FC`) and warm cream (`#FFFDF0`) rounded cards with dark navy and amber accents.
4. **Full-Width Sequential Flow:** Structured process timeline card.
5. **Monospace Code Container:** Midnight Slate (`#111827`) code syntax card with strict left-aligned Consolas text and cyan highlighting (`#8AD4FF`).
6. **100% Speaker Notes Coverage:** Injects delivery commentary and live-coding prompts into PowerPoint presenter notes.

---

## Importing into Canvas LMS

1. Open your Canvas course shell.
2. Navigate to **Settings** (bottom left navigation).
3. Click **Import Course Content** (right sidebar).
4. Select **Common Cartridge 1.x Package** under Content Type.
5. Choose `AINT_2050_Complete.imscc`.
6. Select **All content** and click **Import**.
7. In ~30 seconds, Canvas imports all Modules, WikiPages, SpeedGrader Assignments, Gradebook Groups, and QTI Quizzes formatted and live!
