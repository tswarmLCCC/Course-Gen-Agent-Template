# Unit 02 Instructor Lecture Notes: Visual Workflow Automation

## 1. Pedagogical Framing & Conceptual Anchor
- **Transition from Unit 1 to Unit 2**: Students just finished writing raw Python ReAct loops. Emphasize that while coding raw loops provides complete foundational comprehension, modern enterprise velocity requires visual abstractions.
- **The Core Analogy**: Think of Level 1 (raw code) as writing custom assembly or C code, Level 2 (visual workflows) as high-level visual scripting like Unreal Engine Blueprints or LabVIEW, and Level 3 (LangGraph) as structured systems programming in Rust/Go.

---

## 2. Common Student Misconceptions & Pitfalls
1. **"Visual low-code means no real programming."**
   - *Correction*: Emphasize that visual workflows still require rigorous algorithmic thinking: schema design, JSON manipulation, error handling, and API authentication. In n8n and Langflow, developers frequently write inline JavaScript or Python code within custom nodes.
2. **"Memory Buffer retains everything forever."**
   - *Correction*: Remind students that `WindowBufferMemory` only holds the last $k$ interactions. If students send massive payloads (e.g. 5,000 token system logs), they will overflow context windows even with small $k$.
3. **"Webhooks are secure by default."**
   - *Correction*: Webhook URLs are public endpoints. Without cryptographic HMAC signature checking or bearer token auth, bad actors can trigger infinite billable loops.

---

## 3. Synchronous Lab Demonstration Tips
- During the live demo, show how to inspect the `$json` data inspector in n8n.
- Intentionally send a malformed webhook payload and show how the node graph flags the syntax error in red.
- Demonstrate setting up a fallback branch that logs errors to a mock file or terminal.
