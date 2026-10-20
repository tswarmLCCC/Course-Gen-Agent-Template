#!/usr/bin/env python3
"""
Applied Lab 02 Starter: Automated Customer Operations Visual Dispatcher
Course: AINT 2050 - Applied AI Agent Architectures
Unit: Unit 02 - Visual Workflow Automation with n8n and Langflow

Student Instructions:
Complete the marked TODO sections:
1. verify_webhook_signature (HMAC SHA-256 verification)
2. SlidingWindowMemory (FIFO buffer retaining last k turns)
3. VisualAgentDispatcher.process_event (event routing and tool execution)
"""

import hmac
import hashlib
import json
from typing import Dict, List, Any, Optional, Callable


# =====================================================================
# TASK 1: HMAC Webhook Signature Verification
# =====================================================================
def verify_webhook_signature(payload_bytes: bytes, secret: str, signature_header: str) -> bool:
    """
    Verifies that the incoming webhook payload was signed by an authorized client.
    
    Args:
        payload_bytes: Raw bytes of the inbound HTTP request body.
        secret: Shared secret key between the client and webhook receiver.
        signature_header: Expected hex digest received in HTTP header (e.g., 'sha256=abcdef...')
        
    Returns:
        bool: True if signature is cryptographically valid, False otherwise.
    """
    # Clean 'sha256=' prefix if present
    expected_hex = signature_header.replace("sha256=", "").strip()
    
    # Calculate computed HMAC SHA-256
    computed = hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
    
    # Use hmac.compare_digest to prevent timing attacks
    return hmac.compare_digest(computed, expected_hex)


# =====================================================================
# TASK 2: Sliding Window Memory Buffer
# =====================================================================
class SlidingWindowMemory:
    """Manages short-term conversation turns with a sliding window cap."""
    
    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self.history: List[Dict[str, str]] = []

    def add_turn(self, role: str, content: str):
        """Appends a turn to history."""
        self.history.append({"role": role, "content": content})

    def get_context(self) -> List[Dict[str, str]]:
        """Returns the most recent max_turns messages."""
        return self.history[-self.max_turns:] if len(self.history) > self.max_turns else list(self.history)


# =====================================================================
# TASK 3: Visual Agent Workflow Dispatcher
# =====================================================================
class VisualAgentDispatcher:
    """Simulates an n8n / Langflow visual agent execution engine."""
    
    def __init__(self, webhook_secret: str):
        self.secret = webhook_secret
        self.tools: Dict[str, Callable] = {}
        self.memories: Dict[str, SlidingWindowMemory] = {}

    def register_tool(self, name: str, func: Callable):
        self.tools[name] = func

    def get_or_create_memory(self, session_id: str) -> SlidingWindowMemory:
        if session_id not in self.memories:
            self.memories[session_id] = SlidingWindowMemory(max_turns=6)
        return self.memories[session_id]

    def process_event(self, raw_body: bytes, sig_header: str) -> Dict[str, Any]:
        """Processes inbound webhook payload, routes through AI Agent logic and tools."""
        if not verify_webhook_signature(raw_body, self.secret, sig_header):
            return {"status": "error", "code": 401, "message": "Unauthorized: Invalid HMAC signature."}

        payload = json.loads(raw_body.decode("utf-8"))
        customer_id = payload.get("customer_id", "unknown")
        intent = payload.get("intent", "general_inquiry")
        data = payload.get("data", {})

        memory = self.get_or_create_memory(customer_id)
        memory.add_turn("user", f"Intent: {intent}, Data: {json.dumps(data)}")

        # Visual Agent Node Routing Logic
        action_taken = "none"
        response_text = ""

        try:
            if intent == "billing_inquiry":
                if "lookup_customer_tier" in self.tools:
                    tier_info = self.tools["lookup_customer_tier"](customer_id)
                    action_taken = "lookup_customer_tier"
                    response_text = f"Customer {customer_id} is in {tier_info.get('tier')} tier."
            elif intent == "refund_request":
                amount = data.get("amount", 0.0)
                tier_info = self.tools.get("lookup_customer_tier", lambda cid: {"tier": "STANDARD"})(customer_id)
                tier = tier_info.get("tier", "STANDARD")
                
                # Rule: Auto-issue credit if <= $100 for VIP or ENTERPRISE
                if amount <= 100.0 and tier in ["VIP", "ENTERPRISE"] and "issue_temporary_credit" in self.tools:
                    credit_res = self.tools["issue_temporary_credit"](customer_id, amount)
                    action_taken = "issue_temporary_credit"
                    response_text = f"Issued ${amount:.2f} credit to {customer_id} (Ref: {credit_res.get('ref_id')})."
                else:
                    # Escalate high value or standard tiers
                    if "escalate_to_human" in self.tools:
                        esc_res = self.tools["escalate_to_human"](customer_id, f"Refund request of ${amount} requires manual review.")
                        action_taken = "escalate_to_human"
                        response_text = f"Escalated to human supervisor: Ticket #{esc_res.get('ticket_id')}."
            else:
                response_text = "General inquiry logged for review."

        except Exception as ex:
            action_taken = "error_fallback"
            response_text = f"Tool failure intercepted: {str(ex)}"

        memory.add_turn("assistant", response_text)

        return {
            "status": "success",
            "customer_id": customer_id,
            "action_taken": action_taken,
            "response": response_text,
            "memory_turns": len(memory.get_context())
        }


# =====================================================================
# Automated Unit Test Suite
# =====================================================================
def run_tests():
    print("Executing Applied Lab 02 Unit Tests...")
    test_secret = "secret_enterprise_token_9981"
    dispatcher = VisualAgentDispatcher(test_secret)

    # Mock tool implementations
    mock_db = {
        "cust_101": {"tier": "VIP", "balance": 0.0},
        "cust_202": {"tier": "STANDARD", "balance": 50.0}
    }

    def mock_tier_lookup(cid: str) -> Dict[str, Any]:
        return mock_db.get(cid, {"tier": "STANDARD", "balance": 0.0})

    def mock_issue_credit(cid: str, amount: float) -> Dict[str, Any]:
        return {"status": "CREDIT_ISSUED", "ref_id": f"CR-{cid}-99"}

    def mock_escalate(cid: str, reason: str) -> Dict[str, Any]:
        return {"ticket_id": 9941, "assigned_queue": "tier_2_support"}

    dispatcher.register_tool("lookup_customer_tier", mock_tier_lookup)
    dispatcher.register_tool("issue_temporary_credit", mock_issue_credit)
    dispatcher.register_tool("escalate_to_human", mock_escalate)

    # Test 1: Signature Verification Success & Failure
    payload = json.dumps({"customer_id": "cust_101", "intent": "billing_inquiry"}).encode("utf-8")
    valid_sig = hmac.new(test_secret.encode(), payload, hashlib.sha256).hexdigest()
    
    assert verify_webhook_signature(payload, test_secret, valid_sig) is True
    assert verify_webhook_signature(payload, test_secret, "bad_hex_signature") is False
    print("  [+] Test 1: HMAC Signature verification passed.")

    # Test 2: Process Billing Inquiry Event
    res1 = dispatcher.process_event(payload, valid_sig)
    assert res1["status"] == "success"
    assert res1["action_taken"] == "lookup_customer_tier"
    assert "VIP" in res1["response"]
    print("  [+] Test 2: Billing inquiry routing passed.")

    # Test 3: Auto-credit for VIP under threshold
    payload_refund = json.dumps({
        "customer_id": "cust_101",
        "intent": "refund_request",
        "data": {"amount": 75.00}
    }).encode("utf-8")
    sig_refund = hmac.new(test_secret.encode(), payload_refund, hashlib.sha256).hexdigest()

    res2 = dispatcher.process_event(payload_refund, sig_refund)
    assert res2["action_taken"] == "issue_temporary_credit"
    assert "CR-cust_101-99" in res2["response"]
    print("  [+] Test 3: VIP automated credit routing passed.")

    # Test 4: Escalation for Standard Tier refund
    payload_std = json.dumps({
        "customer_id": "cust_202",
        "intent": "refund_request",
        "data": {"amount": 75.00}
    }).encode("utf-8")
    sig_std = hmac.new(test_secret.encode(), payload_std, hashlib.sha256).hexdigest()

    res3 = dispatcher.process_event(payload_std, sig_std)
    assert res3["action_taken"] == "escalate_to_human"
    assert "9941" in res3["response"]
    print("  [+] Test 4: Human escalation routing passed.")

    # Test 5: Sliding Window Memory Retention
    mem = dispatcher.get_or_create_memory("cust_101")
    assert len(mem.get_context()) >= 4
    print("  [+] Test 5: Sliding window memory persistence passed.")

    print("\nAll 5 Applied Lab 02 tests PASSED successfully!")


if __name__ == "__main__":
    run_tests()
