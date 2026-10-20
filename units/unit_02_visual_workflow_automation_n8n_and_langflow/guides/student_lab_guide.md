# Applied Lab 02 Guide: Automated Customer Operations Agent with Visual Workflow Dispatcher

## Assignment Overview
- **Course**: AINT 2050 - Applied AI Agent Architectures
- **Unit**: Unit 02 - Visual Workflow Automation with n8n and Langflow
- **Deliverable**: `lab2_starter.py` (Completed Python script passing 100% assertions)
- **Time Commitment**: 60–90 minutes
- **Grade Weight**: Part of the 40% Applied Labs category

---

## 1. Architectural Mission
In this laboratory, you will build the backend runtime engine that powers Level 2 visual workflow tools like n8n and Langflow. Your engine will:
1. **Verify Inbound Webhooks**: Compute and validate HMAC SHA-256 signatures on inbound HTTP payloads.
2. **Execute Visual Node DAGs**: Traverse node connections (`WebhookTrigger` -> `AIAgentNode` -> `ToolNodes`).
3. **Manage Conversational Memory**: Maintain a sliding-window message buffer (`k = 5`) across customer sessions.
4. **Dispatch Structured Tools**: Route agent requests to registered tools (`lookup_customer_tier`, `issue_temporary_credit`, `escalate_to_human`).
5. **Handle Transient Failures**: Catch tool exceptions and return error observations back to the agent without crashing the pipeline.

```
Incoming Webhook (POST) 
      |
      v
+-------------------------------+
|  HMAC Signature Verification  | ---> Invalid -> Return HTTP 401 Unauthorized
+---------------+---------------+
                | Valid
                v
+-------------------------------+
|   Sliding Window Memory (k=5) |
+---------------+---------------+
                |
                v
+-------------------------------+
|       AI Agent Node Brain     |
|   (Classifies & Picks Tool)   |
+---------------+---------------+
                |
     +----------+----------+
     |                     |
     v                     v
[ Tool: Tier Lookup ]  [ Tool: Credit Issue ]
     |                     |
     +----------+----------+
                |
                v
+-------------------------------+
|   Synthesize Final Response   |
+-------------------------------+
```

---

## 2. Technical Requirements & TODOs

Open [lab2_starter.py](file:///c:/dev/Course-Gen-Agent-Template/units/unit_02_visual_workflow_automation_n8n_and_langflow/guides/lab2_starter.py) and implement the marked sections:

### Task 1: `verify_webhook_signature(payload_bytes, secret, signature_header)`
- Calculate `hmac.new(secret.encode(), payload_bytes, hashlib.sha256).hexdigest()`.
- Compare using `hmac.compare_digest` to prevent timing attacks.
- Return `True` if valid, `False` otherwise.

### Task 2: `SlidingWindowMemory` Class
- Implement `add_turn(role, content)` and `get_context(max_turns=5)`.
- Ensure it retains only the most recent $k$ message pairs without mutating the historical archive.

### Task 3: `VisualAgentDispatcher` Class
- Implement `register_tool(name, schema, func)`.
- Implement `process_event(webhook_payload, customer_id)`.
- Route triage logic deterministically based on intent:
  - If intent is `billing_inquiry`, call `lookup_customer_tier`.
  - If refund amount <= $100.00 and tier is `VIP` or `ENTERPRISE`, call `issue_temporary_credit`.
  - If error or high risk, route to `escalate_to_human`.

---

## 3. Automated Verification & Testing
Execute the starter script directly:
```bash
python units/unit_02_visual_workflow_automation_n8n_and_langflow/guides/lab2_starter.py
```
Or run via pytest:
```bash
pytest units/unit_02_visual_workflow_automation_n8n_and_langflow/guides/lab2_starter.py
```
All 5 test assertions must exit with status `0` before submission.
