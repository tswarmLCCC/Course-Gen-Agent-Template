# Unit 02 Assessment: Visual Workflow Automation with n8n and Langflow

Welcome to the Unit 02 Quiz. This assessment evaluates your mastery of Level 2 visual agent architectures, n8n node topologies, Langflow component canvases, event-driven webhooks, memory buffers, and visual RAG systems.

---

### Question 1
What is the core conceptual differentiator between Level 1 foundation assistants and Level 2 visual workflow orchestrators?
* A) Level 1 models do not have token context limits.
* B) Level 2 orchestrators connect models to visual directed acyclic graphs (DAGs), webhooks, and pre-built SaaS tool nodes without requiring custom imperative code for every connector.
* C) Level 2 systems operate purely offline without network access.
* D) Level 1 assistants can only be queried through Microsoft Excel spreadsheets.

---

### Question 2
In the n8n Advanced AI architecture, what role does the "Chat Trigger" or "Webhook Trigger" node perform?
* A) It stores the persistent vector embeddings in a Chroma database.
* B) It acts as the event entry point, initiating workflow execution upon receipt of an HTTP request or user chat interaction.
* C) It compiles TypeScript code into machine language.
* D) It monitors local CPU temperatures during model inference.

---

### Question 3
When configuring an AI Agent node in n8n, how are tools made accessible to the language model?
* A) By typing Python function definitions directly into the operating system shell.
* B) By connecting modular Tool nodes (e.g., HTTP Request Tool, Custom Code Tool) directly to the "Tool" input plug of the AI Agent node.
* C) By emailing tool documentation to the LLM vendor.
* D) Tools cannot be connected to n8n AI Agent nodes.

---

### Question 4
In Langflow, what is the primary function of a "Recursive Character Text Splitter" component within a RAG pipeline?
* A) To delete duplicate characters across raw text files.
* B) To partition large source documents into smaller, semantically coherent chunks with optional overlap prior to embedding generation.
* C) To compress audio recordings into MP3 files.
* D) To encrypt database passwords using MD5.

---

### Question 5
Why is constant-time comparison (`hmac.compare_digest`) strongly recommended when validating incoming webhook signatures?
* A) It increases server CPU clock speed by 15%.
* B) Standard string equality (`==`) terminates early upon finding the first mismatched character, exposing the application to timing side-channel attacks.
* C) Python standard string equality raises a SyntaxError when comparing hex digests.
* D) It reduces network latency across cloud regions.

---

### Question 6
In an n8n AI workflow, how does a "Window Buffer Memory" node retain conversational state?
* A) It keeps a sliding window of the last $k$ conversational interaction turns in local memory.
* B) It downloads the entire chat history as an uncompressed CSV file to the desktop.
* C) It queries the Wikipedia API for historical facts.
* D) It retrains the foundation model's neural network weights on every message.

---

### Question 7
Which of the following enterprise scenarios is best suited for Langflow rather than n8n?
* A) Automatically syncing contacts between Salesforce CRM and Mailchimp upon webhook notification.
* B) Rapidly prototyping, visualizing, and evaluating a custom multi-stage RAG pipeline with varying vector databases, embedding models, and prompt templates.
* C) Sending automated SMS alerts via Twilio when an AWS EC2 instance fails.
* D) Scheduling a nightly cron job to backup a PostgreSQL database.

---

### Question 8
When an n8n AI Agent calls an external HTTP Request Tool and receives an HTTP 429 status code, what does this indicate?
* A) The destination server is permanently offline.
* B) The agent has exceeded the downstream API provider's rate limit.
* C) The user entered an invalid email address.
* D) The n8n license key has expired.

---

### Question 9
What is the advantage of using Langflow's Python code export feature?
* A) It converts the visual component graph into clean, executable Python/LangChain code that can be embedded into custom microservices or CI/CD pipelines.
* B) It eliminates the need for Python runtime environments.
* C) It increases GPU VRAM on the host server.
* D) It prevents any further modifications to the prompt templates.

---

### Question 10
In visual workflow design, what is an "Error Trigger" or "Continue on Fail" pattern?
* A) A configuration that causes the server to reboot whenever a calculation error happens.
* B) A resilience pattern that catches downstream node exceptions, preventing total workflow failure and routing execution to fallback logic or telemetry logging.
* C) A tool that deliberately introduces bugs into production code.
* D) A rule that automatically deletes all student submissions.

---

### Question 11
In an n8n expression, what does the syntax `{{ $json.body.user_id }}` represent?
* A) An HTML CSS selector for styling buttons.
* B) A dynamic variable expression extracting the `user_id` property from the incoming JSON payload of the preceding node.
* C) A cryptographic hash of the current user's password.
* D) A system command that runs in the Linux bash shell.

---

### Question 12
How does a Vector Store node operate within a visual RAG flow in Langflow?
* A) It generates graphic design SVG vector images for web pages.
* B) It performs approximate nearest-neighbor (ANN) similarity search across embedded document vectors and returns the most relevant text chunks to the prompt template.
* C) It calculates the mathematical vector dot product of RGB pixel values in images.
* D) It compiles C++ code into binary dynamic link libraries (.dll).

---

### Question 13
Why might an enterprise choose a Level 2 visual platform over building a custom Level 3 Python codebase for customer service triage?
* A) Visual platforms do not require internet access.
* B) Visual platforms enable non-engineering business leads to audit, modify, and manage workflow business rules and canned responses without deploying code changes.
* C) Level 3 codebases cannot connect to language models.
* D) Visual platforms are completely immune to any security vulnerabilities.

---

### Question 14
What is the primary architectural limitation of pure DAG-based visual workflows when implementing iterative reasoning agents?
* A) Directed acyclic graphs cannot natively represent arbitrary cyclical loops, stateful conditional backtracking, or complex multi-agent state machines without cumbersome workaround nodes.
* B) DAGs cannot process JSON data payloads.
* C) DAGs can only execute on Apple macOS operating systems.
* D) DAGs do not support string variables.

---

### Question 15
When deploying an n8n workflow to production handling sensitive PII (Personally Identifiable Information), which security measure should always be enforced?
* A) Printing all decrypted webhook payloads to public console logs.
* B) Running with credential encryption enabled, securing webhook endpoints with authentication/HMAC, and isolating execution in a private VPC.
* C) Sharing administrative dashboard URLs publicly on social media.
* D) Disabling TLS/SSL encryption to maximize throughput.

---

## Answer Key

| Question # | Correct Answer | Concept Tested & Rationale |
| :--- | :--- | :--- |
| **1** | **B** | Level 2 visual orchestrators provide low-code node DAGs, visual connectors, and pre-built integrations for rapid enterprise deployment. |
| **2** | **B** | Webhook and chat trigger nodes ingest external HTTP requests or user interactions to start the workflow execution. |
| **3** | **B** | In n8n, tools are modular nodes attached directly to the AI Agent node's tool input socket. |
| **4** | **B** | Text splitters chunk source documents into smaller segments to fit within LLM embedding and context windows. |
| **5** | **B** | `hmac.compare_digest` prevents timing attacks by taking constant time regardless of where mismatches occur. |
| **6** | **A** | Window Buffer Memory maintains the last $k$ interaction pairs in memory to provide conversational continuity. |
| **7** | **B** | Langflow specializes in visual experimentation, RAG component assembly, and evaluating document retrieval pipelines. |
| **8** | **B** | HTTP 429 Too Many Requests indicates that the rate limit of the third-party API has been reached. |
| **9** | **A** | Langflow allows visual prototypes to be exported as Python scripts for deployment into production microservices. |
| **10** | **B** | Error nodes and fallback branches ensure that failures in downstream APIs do not cause catastrophic pipeline outages. |
| **11** | **B** | n8n uses handlebars syntax `{{ $json... }}` to reference JSON data emitted by upstream nodes. |
| **12** | **B** | Vector store nodes perform semantic similarity search to retrieve relevant text chunks for the LLM. |
| **13** | **B** | Low-code visual platforms empower cross-functional teams to adjust routing rules and prompts without requiring engineering deployments. |
| **14** | **A** | DAGs are acyclic by definition, making cyclical agent reasoning loops, state rollback, and complex branching difficult without graph frameworks like LangGraph. |
| **15** | **B** | Enterprise compliance mandates credential encryption, VPC isolation, and endpoint authentication for handling PII. |
