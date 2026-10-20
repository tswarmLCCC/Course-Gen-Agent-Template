# Pedagogical Standards & Course Architecture Rule

## 1. Modular Unit Architecture (The 14-Artifact Standard)
Every modular course unit developed in this template adheres to the complete, production-grade 14-artifact pedagogical framework:

| Category | Artifact | Path Convention | Purpose & Content |
| :--- | :--- | :--- | :--- |
| **Governance** | Unit Overview | `overview.md` | Weekly roadmap, contact hour budget (150m study / 150m lab), CLO alignment. Uses DesignPLUS banner ribbon. |
| **Asynchronous Study** | Study Guide | `async/study_guide.md` | 150-minute async guided roadmap, core concept breakdowns, required readings with concise chapter summaries. |
| **Asynchronous Study** | Self-Check Drills | `async/self_check_drills.md` | Conceptual focus questions and code-tracing exercises with interactive `<details>/<summary>` collapsible answer keys. |
| **Asynchronous Study** | Socratic AI Practice | `async/learn_with_ai.md` | Roleplay persona prompt ("Dr. Guido" or course expert), interactive practice drill, and debrief discussion prompt. |
| **Lectures & Media** | Slide Outline | `lectures/slides.md` | Assertion-Evidence slide outline mapped to the 5 universal slide archetypes. |
| **Lectures & Media** | Micro-Lecture Scripts | `lectures/micro_lecture_scripts.md` | Verbatim delivery scripts (5–10 mins each) with timestamps, code demonstrations, and pedagogical pauses. |
| **Lectures & Media** | Instructor Notes | `lectures/instructor_lecture_notes.md` | Delivery runbook, common misconceptions, active learning prompts, live-coding tips. |
| **Lectures & Media** | Code Demonstrations | `lectures/partX_*.py` | Modular, runnable demo scripts used during lecture presentations. |
| **Lectures & Media** | Slide Presentation | `lectures/*_Presentation.pptx` | Programmatic 16:9 widescreen PowerPoint deck with 100% speaker notes coverage. |
| **Synchronous Lab** | Lesson Plan | `sync/lesson_plan.md` | Minute-by-minute active learning delivery plan for 75-min or 150-min class meetings. |
| **Synchronous Lab** | In-Class Challenges | `sync/inclass_challenges.py` | Scaffolded pair-programming drills with assert tests for live classroom delivery. |
| **Practical Guides** | Student Lab Guide | `guides/student_lab_guide.md` | Scenario-driven laboratory instructions, step-by-step technical specifications, and native HTML rubric table. |
| **Practical Guides** | Student Starter Code | `guides/labX_starter.py` | Commented starter script with type hints, docstrings, and structured TODO blocks. |
| **Practical Guides** | Instructor Master Key | `guides/instructor_solution.py` | Complete reference solution with PEP-8 compliance and architectural comments. (Unpublished in Canvas). |
| **Assessments** | Analytic Lab Rubric | `assessments/lab_rubric.md` | 100-point 4-criterion grading matrix: Functionality (40%), Architecture (30%), Validation (20%), Documentation (10%). |
| **Assessments** | Unit Quiz (QTI 1.2) | `assessments/unit_quiz.md` | 15-question multiple-choice assessment with distractor rationales and markdown Answer Key table. |

---

## 2. Contact Hour Model (300 Minutes/Week)
Every unit is budgeted for a rigorous 300 minutes of weekly instructional engagement:
- **150 Minutes of Asynchronous Guided Learning**:
  - Bite-sized video micro-lectures (5–10 mins each).
  - Curated readings with chapter summaries.
  - Formative self-check knowledge checks before class.
  - Socratic AI practice drills.
- **150 Minutes of Synchronous Active Learning & Practical Lab**:
  - Concept reinforcement and live-coding demonstrations.
  - Collaborative pair-programming challenges.
  - Hands-on applied laboratory work with instructor coaching.

---

## 3. Visual & Technical Standards
- **Selective Banner Ribbon Policy**: DesignPLUS banner ribbons (`dp-header dp-basic-bar`) are applied exclusively to Home Page, Orientation, and Unit Overviews. All subpages use the clean, professional standard layout with navy blue headers (`#1e3a8a`) and slate lead cards (`#f8fafc`).
- **Zero-Dependency Python Architecture**: Cartridge compilation, QTI generation, syllabus generation, and markdown styling require only the Python standard library. Slide generation uses `python-pptx`.
- **Accreditation-Compliant Syllabus**: Syllabi are generated in both native Canvas HTML and standalone Microsoft Word (`.docx`) format adhering to institutional standards.
