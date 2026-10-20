# Course Generation Agent Guidelines & Architectural Rules

Welcome to the **Course Generation Agent Template** repository. This environment equips AI pair-programming agents and instructional developers with a production-grade, zero-dependency Python toolchain and progressive-disclosure skills to author, scaffold, format, compile, and deploy accredited college and enterprise courses.

---

## 1. Core Architecture & Agent Skills

Agents operating in this repository have access to four specialized skills under `.agents/skills/`:

1. **`canvas-course-builder`** ([.agents/skills/canvas-course-builder/SKILL.md](file:///.agents/skills/canvas-course-builder/SKILL.md)):
   - Compiles production-grade Canvas Common Cartridge (`.imscc`) packages.
   - Converts Markdown files into DesignPLUS-compliant Canvas WikiPages.
   - Compiles Markdown assessments into native QTI 1.2 XML quizzes with Canvas metadata.
   - Generates native SpeedGrader assignments with weighted gradebook groups.
   - Validates all generated XML with `xml.etree.ElementTree`.

2. **`slide-deck-generator`** ([.agents/skills/slide-deck-generator/SKILL.md](file:///.agents/skills/slide-deck-generator/SKILL.md)):
   - Generates 16:9 widescreen, WCAG 2.1 AAA high-contrast PowerPoint (`.pptx`) decks.
   - Implements the 5 universal slide archetypes (Split-Hero, Section Divider, Two-Column, Process Flow, Monospace Code Container).
   - Injects comprehensive speaker notes on 100% of slides.

3. **`course-intake-scanner`** ([.agents/skills/course-intake-scanner/SKILL.md](file:///.agents/skills/course-intake-scanner/SKILL.md)):
   - Scans unstructured curriculum assets, legacy decks, lecture transcripts, and notes across `knowledge_dump/` drop zones to scaffold course plans.

4. **`syllabus-docx-cloner`** ([.agents/skills/syllabus-docx-cloner/SKILL.md](file:///.agents/skills/syllabus-docx-cloner/SKILL.md)):
   - Generates institutional Microsoft Word (`.docx`) syllabi adhering to college accreditation standards.

---

## 2. Pedagogical Standards: The 14-Artifact Unit Model
Governed by [.agents/rules/pedagogical_standards.md](file:///.agents/rules/pedagogical_standards.md).
Every modular unit under `units/` must follow the 14-artifact standard:
- Governance: `overview.md` (DesignPLUS ribbon banner, contact hour budget, CLO mapping)
- Async Guided Study (150 min): `async/study_guide.md`, `async/self_check_drills.md`, `async/learn_with_ai.md`
- Synchronous Lab (150 min): `sync/lesson_plan.md`, `sync/inclass_challenges.py`
- Practical Laboratory: `guides/student_lab_guide.md`, `guides/labX_starter.py`, `guides/instructor_solution.py`
- Assessments: `assessments/lab_rubric.md`, `assessments/unit_quiz.md` (QTI 1.2 compatible)
- Lectures & Presentations: `lectures/slides.md`, `lectures/micro_lecture_scripts.md`, `lectures/instructor_lecture_notes.md`, `lectures/partX_*.py`, `lectures/*_Presentation.pptx`

---

## 3. Video Integration Rule
Governed by [.agents/rules/video_mapping.md](file:///.agents/rules/video_mapping.md).
All custom course videos produced by the instructor are indexed in `shared_assets/VideoMap.md`.
- Format: `<Video Label / Pattern> - <URL>`
- Course Orientation: Embedded in `wiki_content/start-here.html` and linked in `course_settings/syllabus.html`.
- Unit Lectures: Embedded in `unit-XX-readings.html` under Section 4.
- Unit Labs: Embedded in `unit-XX-applied-lab-guide.html`.
- The cartridge build engine (`scripts/build_course.py`) dynamically reads `shared_assets/VideoMap.md` during cartridge synthesis.

---

## 4. Emoticon & Emoji Policy
Governed by [.agents/rules/emoticon_usage.md](file:///.agents/rules/emoticon_usage.md).
- Emoticons and emojis are eliminated across assistant responses, Canvas pages, course guides, and code scripts.
- May only be used VERY sparingly for great effect.
