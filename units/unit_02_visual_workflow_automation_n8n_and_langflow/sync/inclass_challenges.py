#!/usr/bin/env python3
"""
Unit 02 In-Class Challenge: Visual Node Workflow Simulator
AINT 2050 - Applied AI Agent Architectures

In this challenge, students simulate how visual orchestrators like n8n and Langflow
execute node graphs under the hood:
1. Parse a graph of nodes and connections.
2. Route incoming webhook payloads into an AI Agent node.
3. Validate and execute attached tool nodes.
4. Catch errors and return structured execution telemetry.
"""

import json
from typing import Dict, List, Any, Optional


class WorkflowNode:
    def __init__(self, node_id: str, node_type: str, name: str, parameters: Dict[str, Any]):
        self.node_id = node_id
        self.node_type = node_type
        self.name = name
        self.parameters = parameters


class VisualWorkflowEngine:
    def __init__(self):
        self.nodes: Dict[str, WorkflowNode] = {}
        self.connections: Dict[str, List[str]] = {}  # source_id -> [target_ids]
        self.tools: Dict[str, Any] = {}

    def add_node(self, node_id: str, node_type: str, name: str, parameters: Optional[Dict[str, Any]] = None):
        self.nodes[node_id] = WorkflowNode(node_id, node_type, name, parameters or {})

    def add_connection(self, source_id: str, target_id: str):
        if source_id not in self.connections:
            self.connections[source_id] = []
        self.connections[source_id].append(target_id)

    def register_tool(self, tool_name: str, handler):
        self.tools[tool_name] = handler

    def execute_webhook(self, webhook_node_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Simulates incoming webhook event triggering downstream nodes."""
        if webhook_node_id not in self.nodes:
            raise ValueError(f"Webhook node {webhook_node_id} does not exist.")

        webhook_node = self.nodes[webhook_node_id]
        if webhook_node.node_type != "WebhookTrigger":
            raise ValueError(f"Node {webhook_node_id} is not a WebhookTrigger.")

        execution_log = [f"Triggered: {webhook_node.name} with event {payload.get('event', 'unknown')}"]
        current_data = payload

        # Traverse downstream connections
        targets = self.connections.get(webhook_node_id, [])
        agent_result = {}

        for target_id in targets:
            node = self.nodes[target_id]
            if node.node_type == "AIAgent":
                agent_result = self._execute_agent_node(node, current_data, execution_log)

        return {
            "status": "success",
            "execution_log": execution_log,
            "result": agent_result
        }

    def _execute_agent_node(self, node: WorkflowNode, input_data: Dict[str, Any], log: List[str]) -> Dict[str, Any]:
        log.append(f"AI Agent Node '{node.name}' processing input...")
        event_type = input_data.get("event")
        data = input_data.get("data", {})

        # Simulate agent reasoning and tool invocation
        if event_type == "customer.ticket":
            category = data.get("category")
            if category == "billing" and "query_billing_db" in self.tools:
                log.append("Agent reasoned: Billing issue detected -> invoking query_billing_db")
                tool_output = self.tools["query_billing_db"](data.get("customer_id"))
                log.append(f"Observation: {tool_output}")
                return {
                    "action_taken": "query_billing_db",
                    "response": f"Customer billing status retrieved: {tool_output.get('status')}",
                    "details": tool_output
                }
            elif "default_faq" in self.tools:
                log.append("Agent reasoned: General issue -> invoking default_faq")
                tool_output = self.tools["default_faq"](data.get("query", ""))
                return {
                    "action_taken": "default_faq",
                    "response": tool_output.get("answer", "No answer found."),
                    "details": tool_output
                }

        return {"action_taken": "none", "response": "Unhandled event type."}


# =====================================================================
# Synchronous In-Class Paired Challenge Verification
# =====================================================================
def run_challenge():
    print("Testing VisualWorkflowEngine simulation...")
    engine = VisualWorkflowEngine()

    # 1. Define Visual Topology
    engine.add_node("node_1", "WebhookTrigger", "Incoming Ticket Webhook", {"path": "/webhook/support"})
    engine.add_node("node_2", "AIAgent", "Support Triage Agent", {"model": "claude-3-5-sonnet", "temperature": 0.2})
    engine.add_connection("node_1", "node_2")

    # 2. Register Tool Handlers
    def mock_billing_tool(customer_id: str):
        return {"customer_id": customer_id, "balance_due": 0.00, "status": "ACTIVE_PAID"}

    def mock_faq_tool(query: str):
        return {"query": query, "answer": "To reset password, navigate to /auth/reset."}

    engine.register_tool("query_billing_db", mock_billing_tool)
    engine.register_tool("default_faq", mock_faq_tool)

    # 3. Simulate Incoming Event
    test_event = {
        "event": "customer.ticket",
        "data": {
            "customer_id": "cust_4091",
            "category": "billing",
            "query": "Why was I charged twice?"
        }
    }

    result = engine.execute_webhook("node_1", test_event)

    print("\nExecution Telemetry:")
    for entry in result["execution_log"]:
        print(f"  [>] {entry}")
    print(f"Agent Final Output: {result['result']['response']}")

    # Assertions
    assert result["status"] == "success"
    assert result["result"]["action_taken"] == "query_billing_db"
    assert result["result"]["details"]["status"] == "ACTIVE_PAID"
    print("\nAll in-class challenge assertions PASSED successfully!")


if __name__ == "__main__":
    run_challenge()
