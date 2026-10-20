# Applied Lab 2 Assessment Rubric: Visual Workflow Dispatcher

## Overview
- **Course**: AINT 2050 - Applied AI Agent Architectures
- **Unit**: Unit 02 - Visual Workflow Automation with n8n and Langflow
- **Assignment**: Lab 02 - Event-Driven Customer Operations Agent with Webhook Dispatcher
- **Total Points**: 100
- **Grading Weight**: Included in the 40% Applied Labs category

---

## Analytic Grading Matrix

| Performance Dimension | Exemplary (90-100%) | Proficient (80-89%) | Developing (70-79%) | Inadequate (0-69%) | Score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Webhook HMAC Cryptographic Verification** (25 pts) | Implements constant-time HMAC SHA-256 validation (`hmac.compare_digest`) ensuring unauthorized or spoofed payloads are rejected with HTTP 401. (23-25 pts) | HMAC validation is functional and rejects invalid tokens, but uses standard equality (`==`) rather than constant-time comparison. (20-22 pts) | Signature verification partially implemented; fails on prefixed headers or non-ASCII characters. (17-19 pts) | Signature check omitted or always returns True regardless of key validity. (0-16 pts) | /25 |
| **2. Visual Node Routing & Tool Binding** (25 pts) | Node graph routes customer intents cleanly to registered tools (`lookup_customer_tier`, `issue_temporary_credit`, `escalate_to_human`) matching business policies. (23-25 pts) | Tool routing is successful for primary cases; minor discrepancies in secondary threshold validation. (20-22 pts) | Tools are registered but hardcoded conditional branching misroutes tier validations. (17-19 pts) | Agent fails to dispatch to registered tools or unhandled exceptions crash the workflow. (0-16 pts) | /25 |
| **3. Memory Buffering & Context Windows** (25 pts) | Correctly implements FIFO sliding-window memory buffer (`k=5`) maintaining context continuity across session turns without token overflow. (23-25 pts) | Memory buffer maintains turn sequence but mutates raw history array unexpectedly. (20-22 pts) | Memory does not enforce the sliding-window cap, allowing unbounded list growth. (17-19 pts) | Conversation turns are dropped or session states collide across different customer IDs. (0-16 pts) | /25 |
| **4. Error Interception & Code Architecture** (25 pts) | Intercepts downstream tool exceptions gracefully, returning diagnostic telemetry observations without halting the process. Passes 100% automated assertions. (23-25 pts) | Exceptions are caught, but error payload lacks diagnostic clarity. Passes all test assertions. (20-22 pts) | Tool errors occasionally bubble up uncaught. Passes 4 of 5 automated test cases. (17-19 pts) | Code fails multiple automated test assertions or contains syntax errors. (0-16 pts) | /25 |

---

## Grading Scale
- **93.0% - 100.0%**: Grade A (Mastery of webhook security and visual node dispatching)
- **90.0% - 92.9%**: Grade A-
- **87.0% - 89.9%**: Grade B+
- **83.0% - 86.9%**: Grade B (Proficient implementation)
- **80.0% - 82.9%**: Grade B-
- **77.0% - 79.9%**: Grade C+
- **70.0% - 76.9%**: Grade C (Baseline functionality)
- **Below 70.0%**: Grade F (Non-functional engine or missing core components)
