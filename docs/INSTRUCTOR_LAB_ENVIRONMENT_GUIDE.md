# Instructor Guide: Lab Delivery Architectures & Infrastructure Strategy

**Audience:** Instructor / Course Author  
**Target Environments:** GitHub Codespaces (Cloud / Hybrid) vs. Local Campus Computer Lab  
**Last Updated:** Academic Year 2026–2027  

---

## Executive Summary & Strategic Architecture

For technical courses combining synchronous active learning with asynchronous guided study, infrastructure must guarantee:
1. **Zero-install onboarding** (preventing Week 1 tech support overhead).
2. **Deterministic execution environments** across student hardware (Mac, Windows, Linux, Chromebooks).
3. **Automated test verification** and native Canvas LMS submission.

### The Dual-Track Infrastructure Recommendation
* **Primary Daily Driver: GitHub Codespaces (Cloud Dev Containers)**
  - Cloud-native container per student (browser-based VS Code).
  - Pre-configured Python runtime, test runners (`pytest`), and standard packages.
  - Native integration with Git for student portfolio building and version control.
  - Zero local software dependencies.
* **Secondary / On-Premises: Campus Computer Lab (Direct or Proxmox VE)**
  - Local physical machines or virtual appliances.
  - Ideal for zero-latency in-person active learning or air-gapped exams.

---

## Technical Specifications for Dev Containers

Every student sandbox is defined declaratively in `.devcontainer/devcontainer.json`:
- **Base Image:** `mcr.microsoft.com/devcontainers/python:3.11`
- **Security:** Runs as unprivileged user (`vscode`), with `no-new-privileges:true`.
- **Pre-installed Tooling:** Python 3.11, `pytest`, `python-pptx`, code formatting extensions.
- **Workflow:** Students write code in `units/unit_XX/guides/`, execute test suites, and submit clean `.py` files to Canvas SpeedGrader.
