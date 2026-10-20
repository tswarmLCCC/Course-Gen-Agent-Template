# Learn with AI: Exploring Visual Agent Architectures (n8n & Langflow)

Use the following structured Socratic prompts with an advanced foundation assistant (such as Anthropic Claude 3.5 Sonnet or Google Gemini 1.5 Pro) to deepen your understanding of Level 2 visual agent workflows.

---

## Exercise 1: Visual Orchestration vs. Code-First Trade-Offs

Copy and paste the following prompt into your AI assistant:

```markdown
You are a Principal Cloud Enterprise Architect specializing in autonomous systems and workflow automation. 

I am evaluating whether our organization should build our automated customer support and incident routing agent using:
Option A: A low-code visual platform like n8n with AI Agent nodes and Webhook triggers.
Option B: A visual component canvas like Langflow connected to our vector database.
Option C: A code-first stateful framework like LangGraph written in Python.

Our requirements:
1. We process 50,000 webhook events per day from Stripe, GitHub, and Zendesk.
2. We need business support leads to easily update canned response templates without opening GitHub pull requests.
3. We need strict audit logging and data residency compliance.
4. We need to query a knowledge base of 2,000 PDF troubleshooting manuals.

Please conduct a Socratic interview with me:
- Ask me 2 targeted questions about our team's engineering velocity and infrastructure constraints.
- Provide a comparative decision matrix evaluating Developer Velocity, Maintainability, Failure Recovery, and Long-Term Extensibility across the three options.
- Conclude with a hybrid architecture recommendation if applicable.
```

---

## Exercise 2: Auditing an n8n JSON Workflow Schema

Copy and paste the following prompt to analyze visual node configuration contracts:

```markdown
You are an expert n8n workflow engineer.

I want to understand how an n8n AI Agent node binds to an HTTP Request Tool node at the underlying JSON schema level.

Please explain:
1. How does n8n serialize the parameters that the AI model outputs into the HTTP Request node's query parameters or JSON body?
2. How does n8n handle parameter type mismatches (for example, if the LLM outputs a string `"25"` when the downstream API endpoint expects an integer `25`)?
3. What happens under the hood when "Return Intermediate Steps" is enabled on the AI Agent node?

Provide a minimal valid n8n workflow JSON snippet showing a Webhook Trigger connected to an AI Agent with an attached HTTP Request tool node, and explain how data flows across the node boundaries.
```
