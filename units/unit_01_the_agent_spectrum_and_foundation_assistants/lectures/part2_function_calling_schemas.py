"""
AINT 2050: Applied AI Agent Architectures
Unit 1 Lecture Demonstration - Part 2: JSON Tool Schemas & Parameter Validation
"""

import json
from typing import Dict, Any


# 1. Defining Standard JSON Schemas for Gemini / Claude Tools
TOOL_SCHEMAS = [
    {
        "name": "query_database",
        "description": "Executes a read-only query against the customer database.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The unique customer string ID (e.g. 'cust_101')."
                },
                "fields": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of fields to retrieve (e.g. ['balance', 'status'])."
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "send_email_notification",
        "description": "Sends an email alert to a customer. Gated action requiring confirmation.",
        "parameters": {
            "type": "object",
            "properties": {
                "recipient": {"type": "string", "description": "Valid email address."},
                "subject": {"type": "string", "description": "Email subject line."},
                "body": {"type": "string", "description": "Email body content."}
            },
            "required": ["recipient", "subject", "body"]
        }
    }
]


# 2. Client-Side Validation Function
def validate_tool_call(tool_name: str, arguments: Dict[str, Any]) -> Tuple_or_Result := bool:
    schema = next((s for s in TOOL_SCHEMAS if s["name"] == tool_name), None)
    if not schema:
        return False, f"Unknown tool: '{tool_name}'"

    required_fields = schema["parameters"].get("required", [])
    for field in required_fields:
        if field not in arguments:
            return False, f"Missing required parameter: '{field}' for tool '{tool_name}'"

    return True, "Valid payload"


if __name__ == "__main__":
    print("=" * 60)
    print("DEMO: JSON Tool Schemas & Client Validation")
    print("=" * 60)
    print("Declared Tool Schemas:\n", json.dumps(TOOL_SCHEMAS, indent=2))

    # Test Validation
    valid, msg = validate_tool_call("query_database", {"customer_id": "cust_101"})
    print(f"\nTest 1 (Valid Payload): {valid} -> {msg}")

    invalid, err = validate_tool_call("send_email_notification", {"recipient": "user@test.com"})
    print(f"Test 2 (Missing Fields): {invalid} -> {err}")
