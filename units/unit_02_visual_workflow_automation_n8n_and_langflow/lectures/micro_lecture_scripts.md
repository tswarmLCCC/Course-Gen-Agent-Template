# Unit 02 Micro-Lecture Scripts: Visual Workflow Automation with n8n and Langflow

## Video 2.1: The Visual Node Paradigm: Why Low-Code Agents Matter (10 min)
**Instructor Teleprompter Script**:
"Hello and welcome to Unit 02 of Applied AI Agent Architectures. In our previous unit, we built a ReAct agent loop from scratch using pure Python. While writing imperative Python loops gives you complete control over every variable, consider what happens when you deploy that code into a large enterprise with dozens of teams.

Every time a business rule changes—say, an automatic refund threshold drops from one hundred dollars to fifty dollars—a software developer has to open a pull request, wait for automated tests to run, get peer code reviews, and redeploy containers. 

This is where Level 2 of the Agent Spectrum enters: Visual Workflow Automation. Tools like n8n and Langflow treat agent systems as directed acyclic graphs of nodes. Operations managers, support leads, and developers can visually see the flow of data, inspect intermediate payloads, and plug in pre-built connectors to enterprise software like Salesforce, Zendesk, and Stripe. Let's look at how visual execution topologies work."

---

## Video 2.2: n8n Architecture: AI Agent Node, Tools & Webhook Triggers (10 min)
**Instructor Teleprompter Script**:
"In this video, we dissect the internal architecture of n8n's Advanced AI system. At the core is the AI Agent node. If you look at the n8n canvas, the AI Agent node is not an isolated box; it features modular input connectors.

On the left side, you connect a Chat Model node—such as Anthropic Claude 3.5 Sonnet or Google Gemini 1.5 Pro. Below it, you connect a Memory node, such as Window Buffer Memory or Redis Memory. On the right, you attach Tool nodes, such as HTTP Request nodes or Custom Code nodes.

When an inbound webhook fires from an external service, the payload passes into the AI Agent node. The agent calls the connected language model, the model emits a tool call, n8n automatically executes that tool node, and feeds the observation back. Let's inspect a live customer triage example on the canvas."

---

## Video 2.3: Langflow Component Canvas: Visual RAG Pipelines (10 min)
**Instructor Teleprompter Script**:
"While n8n specializes in business workflows and SaaS integrations, Langflow is engineered specifically for AI application prototyping, RAG pipelines, and component evaluation.

In Langflow, each piece of an AI pipeline is an interactive visual block. You have Document Loaders that read PDF files, Text Splitters that chunk text with sliding overlaps, Embedding models that vectorize chunks, and Vector Stores like Chroma or Astra DB that index them. 

Connecting these blocks allows you to visually trace the exact path a user's question takes as it searches through documents before reaching the language model. Furthermore, Langflow allows you to export your entire visual canvas as clean Python code or serve it directly via a FastAPI endpoint."

---

## Video 2.4: Production Readiness: Webhooks, HMAC Security & Error Boundaries (10 min)
**Instructor Teleprompter Script**:
"Exposing an agent to the public internet via webhooks introduces critical security and reliability challenges. Anyone who discovers your webhook URL could spam it, consuming expensive model API credits or triggering unauthorized tools.

To secure your endpoints, you must implement HMAC SHA-256 signature verification. The sending system signs the payload using a shared secret, and your receiver computes the cryptographic hash. We use Python's constant-time comparison `hmac.compare_digest` to prevent timing attacks.

Additionally, we must design for failure. External APIs fail all the time with 500 server errors or 429 rate limits. In visual workflows, we use error trigger nodes and 'continue-on-fail' branches to ensure the agent reports problems gracefully rather than crashing."
