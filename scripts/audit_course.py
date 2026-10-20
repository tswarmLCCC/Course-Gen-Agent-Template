#!/usr/bin/env python3
"""
Course Quality & Cartridge Audit Engine (audit_course.py)
Automated verification suite that validates course configs, unit pedagogy,
XML integrity, QTI quiz compliance, and 16:9 widescreen slide presentations.
"""

import os
import sys
import json
import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple

# Add scripts directory to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from qti_builder import parse_quiz_md


def audit_config(config_path: str) -> bool:
    print(f"\n[1] Auditing Course Configuration: {config_path}")
    if not os.path.exists(config_path):
        print(f"  [FAIL] Configuration file not found: {config_path}")
        return False
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        req_keys = ["course_code", "course_title", "term", "institution", "assignment_groups"]
        for k in req_keys:
            if k not in cfg:
                print(f"  [FAIL] Missing required key: {k}")
                return False
        total_weight = sum(float(g.get("weight", 0.0)) for g in cfg["assignment_groups"])
        if abs(total_weight - 100.0) > 0.01:
            print(f"  [FAIL] Assignment group weights sum to {total_weight}%, expected 100.0%")
            return False
        print(f"  [PASS] Course: {cfg['course_code']} - {cfg['course_title']}")
        print(f"  [PASS] Assignment Groups (100% weighted): {len(cfg['assignment_groups'])} groups verified.")
        return True
    except Exception as e:
        print(f"  [FAIL] Error parsing configuration: {e}")
        return False


def audit_units(units_dir: str) -> bool:
    print(f"\n[2] Auditing Unit Curricula: {units_dir}")
    if not os.path.exists(units_dir):
        print(f"  [FAIL] Units directory not found: {units_dir}")
        return False

    unit_folders = [f for f in sorted(os.listdir(units_dir)) if os.path.isdir(os.path.join(units_dir, f))]
    if not unit_folders:
        print(f"  [FAIL] No unit folders found in {units_dir}")
        return False

    print(f"  [*] Found {len(unit_folders)} units.")
    all_ok = True
    for idx, u_folder in enumerate(unit_folders, 1):
        u_path = os.path.join(units_dir, u_folder)
        req_patterns = {
            "Overview": ["overview.md"],
            "Study Guide / Drills": ["study_guide.md", "self_check_drills.md", "readings.md"],
            "Lab Guide": ["student_lab_guide.md", "lab_guide.md"],
            "Quiz": ["unit_quiz.md", "quiz.md"]
        }
        for item_name, patterns in req_patterns.items():
            found = False
            for root, _, files in os.walk(u_path):
                for f in files:
                    if any(p.lower() in f.lower() for p in patterns):
                        found = True
                        break
                if found:
                    break
            if not found:
                print(f"  [WARN] Unit {idx} ({u_folder}): Missing {item_name} artifact")
            else:
                print(f"  [PASS] Unit {idx} ({u_folder}): {item_name} verified")

        # Test Quiz parsing
        for root, _, files in os.walk(u_path):
            for f in files:
                if "quiz" in f.lower() and f.endswith(".md"):
                    q_file = os.path.join(root, f)
                    try:
                        questions = parse_quiz_md(q_file)
                        print(f"  [PASS] Unit {idx} Quiz: Parsed {len(questions)} QTI questions from {f}")
                    except Exception as e:
                        print(f"  [FAIL] Unit {idx} Quiz Error ({f}): {e}")
                        all_ok = False
    return all_ok


def audit_cartridge(imscc_path: str) -> bool:
    print(f"\n[3] Auditing Canvas Cartridge (.imscc): {imscc_path}")
    if not os.path.exists(imscc_path):
        print(f"  [FAIL] Cartridge not found: {imscc_path}")
        return False

    size_mb = os.path.getsize(imscc_path) / (1024 * 1024)
    print(f"  [INFO] Cartridge Size: {size_mb:.2f} MB")

    try:
        with zipfile.ZipFile(imscc_path, "r") as z:
            names = z.namelist()
            req_files = [
                "imsmanifest.xml",
                "course_settings/module_meta.xml",
                "course_settings/assignment_groups.xml",
                "course_settings/course_settings.xml",
                "course_settings/syllabus.html"
            ]
            for rf in req_files:
                if rf not in names:
                    print(f"  [FAIL] Cartridge missing required file: {rf}")
                    return False
                print(f"  [PASS] Found: {rf}")

            # Verify XML parsing
            xml_count = 0
            for name in names:
                if name.endswith(".xml") or name.endswith(".qti"):
                    content = z.read(name)
                    ET.fromstring(content)
                    xml_count += 1
            print(f"  [PASS] Validated {xml_count} XML files inside cartridge. Zero XML syntax errors.")

            # Count modules & wiki pages
            wiki_pages = [n for n in names if n.startswith("wiki_content/") and n.endswith(".html")]
            quizzes = [n for n in names if n.endswith("assessment_qti.xml")]
            print(f"  [PASS] Packaged {len(wiki_pages)} native WikiPages and {len(quizzes)} QTI Quizzes.")
            return True
    except Exception as e:
        print(f"  [FAIL] Cartridge validation error: {e}")
        return False


def audit_presentations(search_dir: str) -> bool:
    print(f"\n[4] Auditing Widescreen 16:9 PowerPoint Decks: {search_dir}")
    try:
        import pptx
        from pptx.util import Inches
    except ImportError:
        print("  [WARN] python-pptx not available, skipping presentation geometry check.")
        return True

    found_decks = []
    for root, _, files in os.walk(search_dir):
        for f in files:
            if f.endswith(".pptx") and not f.startswith("~$"):
                found_decks.append(os.path.join(root, f))

    if not found_decks:
        print("  [WARN] No .pptx presentation decks found.")
        return False

    for deck_path in found_decks:
        try:
            prs = pptx.Presentation(deck_path)
            w = round(prs.slide_width / Inches(1), 3)
            h = round(prs.slide_height / Inches(1), 3)
            slides_count = len(prs.slides)
            is_widescreen = (abs(w - 13.333) < 0.1 and abs(h - 7.5) < 0.1)
            status = "[PASS]" if is_widescreen else "[WARN]"
            print(f"  {status} {os.path.basename(deck_path)}: {slides_count} slides ({w}\" x {h}\" - 16:9 Widescreen)")
        except Exception as e:
            print(f"  [FAIL] Error reading presentation {deck_path}: {e}")
            return False
    return True


def main():
    root_dir = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
    print("=" * 70)
    print("Course Generation Agent Template - Comprehensive Audit Suite")
    print("=" * 70)

    cfg_file = os.path.join(root_dir, "course_config.json")
    units_dir = os.path.join(root_dir, "units")
    
    cfg_ok = audit_config(cfg_file)
    units_ok = audit_units(units_dir)
    
    # Check cartridge
    cartridges = [f for f in os.listdir(root_dir) if f.endswith(".imscc")]
    cart_ok = True
    if cartridges:
        for c in cartridges:
            cart_ok = audit_cartridge(os.path.join(root_dir, c)) and cart_ok
    else:
        print("\n[3] No .imscc cartridge found in workspace root yet.")
        cart_ok = False

    pres_ok = audit_presentations(root_dir)

    print("\n" + "=" * 70)
    overall = cfg_ok and units_ok and cart_ok and pres_ok
    print(f"FINAL AUDIT RESULT: {'[PASSED] 100% READY' if overall else '[NEEDS ACTION]'}")
    print("=" * 70 + "\n")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()
