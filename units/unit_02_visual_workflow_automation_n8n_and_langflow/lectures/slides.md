# Unit 02 Lecture Slides Outline: Visual Workflow Automation with n8n and Langflow

## Slide 1: Split-Hero Title
- **Title**: AINT 2050: Applied AI Agent Architectures
- **Subtitle**: Unit 02: Visual Workflow Automation with n8n and Langflow
- **Presenter**: Applied AI Engineering Faculty
- **Notes**: Welcome to Unit 02. Today we step up from Level 1 foundation assistants into Level 2: Visual Workflow Orchestration with n8n and Langflow.

## Slide 2: Section Divider
- **Category**: Section 1
- **Title**: The Visual Node Paradigm
- **Subtitle**: Why modern enterprise operations need low-code AI workflows
- **Notes**: We explore why raw Python scripts do not scale across cross-functional operations teams and how visual DAGs solve deployment velocity.

## Slide 3: Two-Column Comparison
- **Title**: Imperative Python vs. Visual Node Graphs
- **Column 1 Header**: Imperative Code (Level 1 / 3)
  - Full algorithmic control over memory and threads.
  - Requires git pull requests, CI/CD, and developer deployments.
  - Opaque runtime state for non-engineering stakeholders.
  - Custom error handling required for every API integration.
- **Column 2 Header**: Visual Node Canvases (Level 2)
  - Rapid drag-and-drop assembly of complex pipelines.
  - 400+ pre-built SaaS connectors and standard webhooks.
  - Visual execution telemetry and step-by-step payload inspection.
  - Business leads can adjust prompts and routing logic safely.
- **Notes**: Both paradigms have distinct strengths. Production organizations frequently use hybrid topologies: visual flows for SaaS ingestion and stateful code graphs for deep reasoning.

## Slide 4: Process Flow Architecture
- **Title**: End-to-End n8n AI Agent Workflow
- **Step 1**: Inbound Webhook (`POST /webhook/ticket`) receives external event.
- **Step 2**: HMAC Validator verifies SHA-256 signature against enterprise secret.
- **Step 3**: AI Agent Node parses payload with Claude 3.5 Sonnet / Gemini Pro.
- **Step 4**: Modular Tool Nodes query internal CRM or issue refund credits.
- **Step 5**: Response Dispatcher posts synthesized response to Slack or ticketing API.
- **Notes**: Walk through the lifecycle of a real-time webhook transaction through the node graph.

## Slide 5: Two-Column Comparison
- **Title**: n8n vs. Langflow: Choosing the Right Tool
- **Column 1 Header**: n8n Workflows
  - Best for: Multi-SaaS enterprise automations and event triggers.
  - Connectivity: Hundreds of enterprise connectors (Salesforce, Stripe, Jira).
  - Triggers: HTTP webhooks, cron schedules, app event streams.
  - Execution: Node.js engine with LangChain core.
- **Column 2 Header**: Langflow Canvases
  - Best for: RAG pipeline prototyping and document retrieval evaluation.
  - Connectivity: Native vector databases (Chroma, Astra, Pinecone).
  - Triggers: Interactive chat playground, FastAPI endpoints, Python SDK.
  - Execution: Pure Python backend with LangChain / LlamaIndex.
- **Notes**: Contrast the operational focus of n8n with the AI experimentation focus of Langflow.

## Slide 6: Monospace Code Syntax Container
- **Title**: Inbound Webhook HMAC SHA-256 Verification
- **Code Block**:
```python
import hmac, hashlib

def verify_webhook_signature(payload_bytes: bytes, secret: str, sig_header: str) -> bool:
    expected_hex = sig_header.replace("sha256=", "").strip()
    computed = hmac.new(secret.encode(), payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, expected_hex)
```
- **Notes**: Explain why `hmac.compare_digest` is mandatory to avoid timing vulnerability attacks.
