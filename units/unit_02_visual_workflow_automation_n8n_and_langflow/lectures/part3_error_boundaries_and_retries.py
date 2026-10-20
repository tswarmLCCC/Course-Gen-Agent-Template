"""
AINT 2050: Applied AI Agent Architectures
Unit 2 Lecture Demonstration - Part 3: Error Boundaries, Retry Policies & Fallback Nodes
Demonstrates enterprise resilience patterns for API failures in visual orchestration workflows.
"""

import time
from typing import Callable, Any

def execute_with_exponential_backoff(operation: Callable[[], Any], max_retries: int = 3, initial_delay: float = 0.1) -> Any:
    """Executes a fallible API call with exponential backoff and jitter."""
    delay = initial_delay
    for attempt in range(1, max_retries + 1):
        try:
            print(f"  [ATTEMPT {attempt}] Executing API call...")
            return operation()
        except Exception as e:
            print(f"  [WARN] Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                print("  [ERROR] Exceeded maximum retry budget. Invoking fallback branch.")
                raise e
            time.sleep(delay)
            delay *= 2.0

class FlakyExternalService:
    def __init__(self, succeed_on_attempt: int = 3):
        self.attempts = 0
        self.succeed_on = succeed_on_attempt

    def query_crm(self) -> dict:
        self.attempts += 1
        if self.attempts < self.succeed_on:
            raise ConnectionError("503 Service Unavailable: Rate limit or gateway timeout")
        return {"customer_id": "C-109", "name": "Elena Rostova", "plan": "Enterprise"}

if __name__ == "__main__":
    print("--- Demonstrating Transient Error Resilience & Retries ---")
    service = FlakyExternalService(succeed_on_attempt=3)
    
    result = execute_with_exponential_backoff(service.query_crm, max_retries=4)
    print(f"Final Success Payload: {result}")
    assert result["plan"] == "Enterprise"
    print("Resilience tests passed successfully!")
