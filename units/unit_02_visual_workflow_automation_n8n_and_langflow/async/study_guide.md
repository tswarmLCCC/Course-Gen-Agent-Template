# Unit 02 Study Guide: Visual Workflow Automation with n8n and Langflow

## 1. Introduction: The Level 2 Agent Paradigm
In modern software engineering, writing raw Python loops for every automation creates significant operational friction:
- Every API endpoint change requires code refactoring, pull requests, CI/CD builds, and container deployments.
- Non-engineering stakeholders (operations managers, support leads, product owners) cannot inspect or adjust business logic.
- Visual debugging, real-time payload inspection, and retry loops must be engineered manually.

**Level 2 Visual Agent Orchestrators** solve these challenges by representing agent systems as visual, node-based directed acyclic graphs (DAGs) and stateful execution canvases. This unit examines the two industry-standard open-source platforms dominating this space: **n8n** and **Langflow**.

```
+---------------------------------------------------------------------------------------+
|                                THE AGENT MATURITY SPECTRUM                            |
+---------------------------------------------------------------------------------------+
|  LEVEL 1: Conversational Assist.  |  LEVEL 2: Visual Low-Code Orchestrators  |  LEVEL 3: Stateful Graphs |
|  - Gemini 1.5 Pro / Claude 3.5    |  - n8n (Enterprise Workflows & APIs)     |  - LangGraph (Code-First) |
|  - Single-turn or Chat Loop       |  - Langflow (Visual RAG & Prototyping)   |  - Typed State, Cycles    |
|  - Manual CLI Python scripts      |  - Visual Webhooks, Node Plugs           |  - Production Checkpoints |
+---------------------------------------------------------------------------------------+
```

---

## 2. n8n Architecture: Enterprise Workflow AI Agents
n8n is an extendable, fair-code workflow automation tool. In version 1.x+, n8n introduced dedicated **Advanced AI** nodes powered by LangChain under the hood.

```
       +-----------------------+
       |   Webhook / Chat      |  <-- Incoming Event Trigger (POST /webhook/support)
       +-----------+-----------+
                   |
                   v
       +-----------------------+
       |     AI Agent Node     | <---+ Memory Node (Window Buffer)
       | (Tools Agent / ReAct) | <---+ Model Node (Claude 3.5 / Gemini Pro)
       +-----------+-----------+
                   |
         +---------+---------+
         |                   |
         v                   v
   +-----------+       +-----------+
   | HTTP Tool |       | Code Tool |
   | (Zendesk) |       | (Python)  |
   +-----------+       +-----------+
```

### Key n8n Agent Components
1. **Chat / Webhook Trigger**: Initiates workflow execution upon HTTP POST requests from external systems (e.g., GitHub webhooks, Stripe events, Slack webhooks).
2. **AI Agent Node**: Acts as the central cognitive brain. It receives the prompt, calls connected language models, determines which attached tool nodes to invoke, and synthesizes answers.
3. **Chat Model Node**: Connects to foundation model providers (Google Gemini, Anthropic Claude, OpenAI, Ollama). Configures model temperature, top_p, and credential keys.
4. **Memory Node**: Manages conversational history across turns. Common implementations include:
   - *Window Buffer Memory*: Retains the last $N$ message pairs in memory.
   - *Redis Chat Memory*: Persists conversation turns across distributed worker nodes.
5. **Tool Nodes**: Sub-nodes plugged directly into the AI Agent node:
   - *HTTP Request Tool*: Executes arbitrary REST API calls based on agent-generated parameters.
   - *Custom Code Tool*: Runs JavaScript or Python snippets to parse or transform payloads.
   - *Vector Store Tool*: Queries Pinecone, Qdrant, or Supabase for contextual embeddings.

---

## 3. Langflow Architecture: Visual RAG & Agentic Prototyping
While n8n focuses on business process automation and external SaaS integrations, **Langflow** (created by Logspace, acquired by DataStax) is explicitly built for AI application prototyping, Retrieval-Augmented Generation (RAG), and component-level experimentation.

```
+---------------------------------------------------------------------------------------+
|                                LANGFLOW CANVAS TOPOLOGY                               |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|   +-------------------+       +--------------------+       +---------------------+    |
|   | Document Loader   | ----> | Recursive Splitter | ----> | Text Embeddings     |    |
|   | (PDF / Markdown)  |       | (Chunk: 500 tokens)|       | (text-embedding-3)  |    |
|   +-------------------+       +--------------------+       +----------+----------+    |
|                                                                       |               |
|                                                                       v               |
|   +-------------------+       +--------------------+       +---------------------+    |
|   | User Chat Input   | ----> | Prompt Template    | ----> | Vector Store        |    |
|   | (Natural Query)   |       | (System + Context) |       | (Chroma / Astra DB) |    |
|   +-------------------+       +---------+----------+       +----------+----------+    |
|                                         |                             |               |
|                                         +--------------+--------------+               |
|                                                        |                              |
|                                                        v                              |
|                                             +--------------------+                    |
|                                             | Language Model Node|                    |
|                                             | (Claude 3.5 Sonnet)|                    |
|                                             +----------+---------+                    |
|                                                        |                              |
|                                                        v                              |
|                                             +--------------------+                    |
|                                             | Chat Output        |                    |
|                                             +--------------------+                    |
+---------------------------------------------------------------------------------------+
```

### Key Differences: n8n vs. Langflow
| Architectural Dimension | n8n AI Workflows | Langflow Canvases |
| :--- | :--- | :--- |
| **Primary Focus** | Enterprise SaaS automation, webhooks, multi-step business logic | RAG pipelines, LLM experimentation, agent component visualizer |
| **Connectivity** | 400+ pre-built SaaS connectors (Slack, Jira, GitHub, Postgres) | Vector stores, embedding models, tokenizers, LLM providers |
| **Execution Trigger** | Event-driven webhooks, cron schedules, chat interfaces | Interactive playground, Python SDK export, REST API endpoints |
| **Underlying Engine** | Node.js runtime with LangChain integration | Pure Python FastAPI backend running LangChain / LlamaIndex |
| **Ideal Use Case** | Automated customer triage, alerting, automated DevOps pipelines | Custom corporate knowledge search, RAG evaluation, prompt chaining |

---

## 4. Production Webhook Security & Error Resilience
When exposing Level 2 agents to the internet via webhooks, three security and resilience patterns are mandatory:
1. **HMAC Signature Verification**: Compute and verify SHA-256 signatures on incoming webhook headers to prevent unauthorized payload spoofing.
2. **Error Trigger Nodes**: When a downstream tool (such as an external CRM API) fails, visual workflows route execution to dedicated error catch branches rather than dropping the transaction.
3. **Execution Timeouts**: Enforce maximum execution windows (e.g., 30 seconds) on agent nodes to prevent runaway costs from cyclical loops.
