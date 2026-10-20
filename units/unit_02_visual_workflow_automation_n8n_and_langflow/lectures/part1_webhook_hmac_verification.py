"""
AINT 2050: Applied AI Agent Architectures
Unit 2 Lecture Demonstration - Part 1: Inbound Webhook HMAC SHA-256 Verification
Demonstrates cryptographic signature verification for securing public webhooks in n8n/Langflow.
"""

import hmac
import hashlib
import json
from typing import Tuple

def generate_signed_payload(secret: str, data: dict) -> Tuple[bytes, str]:
    """Serializes payload and generates HMAC SHA-256 hex digest."""
    payload_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
    sig = hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
    return payload_bytes, f"sha256={sig}"

def verify_webhook_signature(payload_bytes: bytes, secret: str, sig_header: str) -> bool:
    """
    Verifies incoming webhook payload signature using constant-time comparison
    to prevent timing attacks.
    """
    if not sig_header or not sig_header.startswith("sha256="):
        return False
    expected_hex = sig_header.split("sha256=", 1)[1].strip()
    computed_hex = hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed_hex, expected_hex)

if __name__ == "__main__":
    SHARED_SECRET = "corp_secret_key_9948271048"
    sample_event = {
        "event": "customer.ticket_created",
        "ticket_id": "TCK-1094",
        "customer_id": "CUST-441",
        "message": "Account login fails with error 403 on billing page."
    }

    raw_body, header_sig = generate_signed_payload(SHARED_SECRET, sample_event)
    print(f"Generated Payload: {raw_body.decode('utf-8')}")
    print(f"Signature Header:  {header_sig}")

    is_valid = verify_webhook_signature(raw_body, SHARED_SECRET, header_sig)
    print(f"Verification Result (Genuine): {is_valid}")
    assert is_valid is True

    # Tampered test
    tampered_body = raw_body + b" "
    is_valid_tampered = verify_webhook_signature(tampered_body, SHARED_SECRET, header_sig)
    print(f"Verification Result (Tampered): {is_valid_tampered}")
    assert is_valid_tampered is False
    print("All HMAC security assertions passed successfully!")
