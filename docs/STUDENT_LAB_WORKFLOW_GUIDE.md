# Student Guide: How to Complete & Submit Weekly Programming Labs

**Course:** COSC 1010: Introduction to Computer Science & Python Programming  
**Environment:** Python 3.11+ Sandbox (GitHub Codespaces / VS Code)

---

## 1. Quick Start with GitHub Codespaces

Every programming lab runs directly in your browser—no local Python or software installation required:

1. Click **Code** (green button on your repo page) $\rightarrow$ **Codespaces** $\rightarrow$ **Create codespace on main**.
2. Wait ~60 seconds for the automated Python container to initialize.
3. Open a terminal (`Ctrl + ~` or `Cmd + ~`) and verify Python:
   ```bash
   python3 --version
   ```

---

## 2. Weekly Lab Completion Workflow

Each week follows a simple, structured 5-step workflow:

```text
├── 1. Review Lab Specifications (guides/student_lab_guide.md)
├── 2. Open Starter Script (guides/labX_starter.py)
├── 3. Write & Execute Code (python3 guides/labX_starter.py)
├── 4. Run Automated Self-Verification (pytest or assertion blocks)
└── 5. Save as labX_yourlastname.py & Upload to Canvas Assignment
```

### Step 1: Review Lab Specifications
Open `guides/student_lab_guide.md` in your unit folder (or the **Unit X: Applied Lab Guide** in Canvas) to review the technical scenario, tasks, point breakdowns, and grading rubric.

### Step 2: Open the Starter Script
Open `guides/labX_starter.py`. This template contains function headers, type annotations, descriptive docstrings, and structured `TODO` blocks.

### Step 3: Write and Test Your Code
Write your solution directly inside the specified function blocks. Test interactively in your terminal:
```bash
python3 units/unit_01_computational_thinking_and_python_basics/guides/lab1_starter.py
```

### Step 4: Run Self-Verification Tests
Every starter script includes built-in verification assertions or test functions. Run pytest to check all test cases:
```bash
pytest units/unit_01_computational_thinking_and_python_basics/
```
> **The Verification Rule:** Never submit code you haven't executed! All submitted scripts must run cleanly with **zero syntax or runtime errors**.

### Step 5: Submit to Canvas
1. Save your completed file with your last name: `labX_yourlastname.py` (e.g. `lab1_smith.py`).
2. Open Canvas, navigate to the weekly **Unit X Applied Lab Assignment**, and upload your `.py` file.

---

## 3. Python Code Quality & Grading Standards

All code submissions are evaluated against four core criteria:
1. **Functionality (40 pts):** All challenge requirements met, edge cases handled, automated test assertions pass.
2. **Code Architecture (30 pts):** Modular functional design, proper variable scope, no global variable mutations, no magic numbers.
3. **PEP-8 Formatting (20 pts):** Descriptive `snake_case` naming, 4-space indentation, clear variable names, type annotations.
4. **Documentation (10 pts):** Informative docstrings (`"""..."""`) explaining parameters, return values, and algorithm rationale.
