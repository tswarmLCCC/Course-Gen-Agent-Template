# Unit 02 Self-Check Drills: Visual Workflow Automation (n8n & Langflow)

Test your understanding of visual agent architectures, n8n node topologies, and Langflow RAG pipelines before attending synchronous lab.

---

### Drill 1: Incoming Webhook Payload Extraction in n8n
**Scenario**: An external e-commerce platform posts a refund request payload to an n8n Webhook node:
```json
{
  "event": "customer.dispute",
  "data": {
    "customer_id": "cust_88219",
    "amount": 249.50,
    "reason": "Damaged goods on arrival"
  }
}
```
In an n8n expression connected to a downstream Claude 3.5 Sonnet AI Agent prompt, which syntax correctly extracts the customer's dispute reason?

* A) `{{ $json.data.reason }}`
* B) `{{ document.getElementById("reason") }}`
* C) `{{ customer.dispute.reason }}`
* D) `{{ params["reason"] }}`

<details>
<summary>Check Answer & Explanation</summary>

**Correct Answer**: **A) `{{ $json.data.reason }}`**

**Explanation**: In n8n, data emitted by an incoming node is exposed on the `$json` root object. Traversing nested keys follows standard JavaScript object notation: `$json.data.reason` extracts `"Damaged goods on arrival"`.
</details>

---

### Drill 2: Memory Buffer Capacity vs. Context Window Overflow
**Scenario**: You configure an n8n AI Agent with a "Window Buffer Memory" node set to `k = 30` (30 previous conversation turns). The connected language model has a context window limit of 8,000 tokens. The agent interacts with a user exchanging long technical logs (500 tokens per message).

What will occur on turn 18?

* A) n8n will automatically upgrade the LLM context window to 32k tokens.
* B) The context will exceed 8,000 tokens (18 turns * 500 tokens = 9,000+ tokens), resulting in a context length limit error from the LLM API provider.
* C) n8n will automatically summarize the previous turns without user intervention.
* D) The AI Agent node will delete the user's database records.

<details>
<summary>Check Answer & Explanation</summary>

**Correct Answer**: **B) Context length limit error from the LLM provider.**

**Explanation**: Window Buffer Memory only limits the count of message pairs (`k`), not the total token volume. If individual messages are large, a fixed message-count window can easily overflow an LLM's token context window. In production, developers use token-capped memory buffers or summarizer memory nodes.
</details>

---

### Drill 3: Langflow RAG Component Ordering
**Scenario**: You are assembling a visual RAG assistant in Langflow to answer questions from internal PDF compliance policies.

What is the correct sequential order of components required to index the documents into a searchable vector store?

* A) Vector Store -> Prompt Template -> Document Loader -> Text Splitter
* B) Text Embeddings -> User Input -> Language Model -> Text Splitter
* C) Document Loader -> Text Splitter -> Text Embeddings -> Vector Store
* D) Chat Output -> Vector Store -> Document Loader -> API Call

<details>
<summary>Check Answer & Explanation</summary>

**Correct Answer**: **C) Document Loader -> Text Splitter -> Text Embeddings -> Vector Store**

**Explanation**: The document pipeline must first ingest raw documents (`Document Loader`), partition them into semantically meaningful chunks (`Text Splitter`), generate mathematical vector representations for each chunk (`Text Embeddings`), and store both vectors and text chunks into the searchable database (`Vector Store`).
</details>

---

### Drill 4: Error Handling in Enterprise Visual Workflows
**Scenario**: An n8n AI Agent node calls an external CRM Tool node to retrieve a customer's contract tier. The CRM API returns an HTTP 503 "Service Unavailable" response.

How should the visual workflow be architected to ensure the agent does not hang or deliver a false hallucination to the customer?

* A) Disable all error notifications in n8n preferences.
* B) Configure "Continue On Fail" on the tool node, routing execution to a fallback node or passing the 503 error string back to the agent as an observation so it can inform the user gracefully.
* C) Reboot the n8n Docker container immediately whenever an HTTP 500 error occurs.
* D) Hardcode the customer tier as "Enterprise Tier 1" for all users.

<details>
<summary>Check Answer & Explanation</summary>

**Correct Answer**: **B) Configure "Continue On Fail" and route to fallback or return error observation.**

**Explanation**: Robust visual workflows catch tool errors at the node boundary. Passing the failure status back to the agent as an environment observation allows the LLM to explain the transient outage to the user or try an alternate cached data source.
</details>

---

### Drill 5: Architecture Selection: n8n vs. Langflow vs. LangGraph
**Scenario**: An enterprise fintech client requires an automated fraud triage pipeline that:
1. Ingests webhook alerts from Stripe and Datadog.
2. Cross-references records across Salesforce and HubSpot CRM.
3. Automatically posts triage summaries into dedicated Slack incident channels.
4. Requires zero code changes by operational staff when modifying Slack notification channels.

Which platform is the most appropriate architectural choice?

* A) Langflow
* B) n8n
* C) Pure C++ command-line loop
* D) LangGraph

<details>
<summary>Check Answer & Explanation</summary>

**Correct Answer**: **B) n8n**

**Explanation**: n8n is engineered specifically for multi-SaaS enterprise integrations, webhook ingestion, and low-code configurability. Non-engineering operational teams can easily reconfigure Slack channels or CRM credentials directly in the visual UI without redeploying code.
</details>
