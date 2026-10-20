"""
AINT 2050: Applied AI Agent Architectures
Unit 2 Lecture Demonstration - Part 2: Visual Workflow Node Execution Simulator
Demonstrates how visual node engines (n8n/Langflow) pass typed payloads between nodes.
"""

from typing import Dict, Any, List

class WorkflowContext:
    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.execution_log: List[str] = []

    def log(self, message: str):
        self.execution_log.append(message)
        print(f"  [NODE EXEC] {message}")

def node_webhook_trigger(ctx: WorkflowContext, payload: dict) -> dict:
    ctx.log(f"Received webhook event: {payload.get('event')}")
    ctx.state["raw_event"] = payload
    return {"status": "accepted", "event_id": payload.get("ticket_id")}

def node_classifier_agent(ctx: WorkflowContext) -> dict:
    text = ctx.state["raw_event"].get("message", "").lower()
    ctx.log("AI Model Node analyzing customer intent...")
    if "billing" in text or "refund" in text:
        category = "billing"
        priority = "high"
    elif "password" in text or "login" in text:
        category = "auth"
        priority = "critical"
    else:
        category = "general"
        priority = "medium"
    
    ctx.state["classification"] = {"category": category, "priority": priority}
    ctx.log(f"Classification result: category={category}, priority={priority}")
    return ctx.state["classification"]

def node_dispatch_router(ctx: WorkflowContext) -> str:
    category = ctx.state["classification"]["category"]
    ctx.log(f"Routing to target handler: {category}")
    if category == "auth":
        return "route_security_team"
    elif category == "billing":
        return "route_finance_queue"
    return "route_general_support"

if __name__ == "__main__":
    context = WorkflowContext()
    event_payload = {
        "event": "ticket.submitted",
        "ticket_id": "T-809",
        "message": "User locked out after password reset attempt."
    }
    print("--- Executing Visual Node Pipeline Simulation ---")
    node_webhook_trigger(context, event_payload)
    node_classifier_agent(context)
    destination = node_dispatch_router(context)
    print(f"Final Execution Route: {destination}")
    assert destination == "route_security_team"
    print("Pipeline simulation completed successfully.")
