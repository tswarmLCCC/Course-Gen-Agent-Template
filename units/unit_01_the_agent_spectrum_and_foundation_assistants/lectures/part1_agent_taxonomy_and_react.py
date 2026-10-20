"""
AINT 2050: Applied AI Agent Architectures
Unit 1 Lecture Demonstration - Part 1: Pure-Python ReAct Reasoning Engine
"""

import re
from typing import Dict, Any, Callable


# 1. Deterministic Tool Implementations
def tool_calculator(expression: str) -> str:
    """Safely evaluates basic arithmetic expressions."""
    try:
        # Sanitize input: allow only digits, operators, parens, spaces
        if not re.match(r"^[\d\s\+\-\*\/\(\)\.]+$", expression):
            return "Error: Invalid characters in arithmetic expression."
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error calculating: {e}"


def tool_database_lookup(query: str) -> str:
    """Mock database lookup for customer data."""
    mock_db = {
        "cust_101": "Customer: Alice Smith | Tier: Platinum | Balance: $450.00 | Status: Active",
        "cust_102": "Customer: Bob Jones | Tier: Standard | Balance: $12.50 | Status: Active",
        "cust_103": "Customer: Charlie Brown | Tier: Suspended | Balance: $0.00 | Status: Inactive"
    }
    q = query.strip().lower()
    return mock_db.get(q, f"Record not found for query '{query}'.")


# 2. Tool Registry
TOOL_REGISTRY: Dict[str, Callable[[str], str]] = {
    "calculate": tool_calculator,
    "lookup_customer": tool_database_lookup
}


# 3. Simulated LLM Engine (Demonstrating ReAct Trajectory)
def mock_llm_inference(prompt: str) -> str:
    """
    Simulates a foundation model (Gemini/Claude) generating a ReAct trajectory.
    In production, this calls the actual Gemini or Claude API.
    """
    if "Observation 1:" not in prompt:
        return "Thought 1: I need to check the customer record for 'cust_101' to see their balance.\nAction: lookup_customer(cust_101)"
    elif "Observation 2:" not in prompt:
        return "Thought 2: The balance is $450.00. The user requested 15% of this balance. I will calculate 450.00 * 0.15.\nAction: calculate(450.00 * 0.15)"
    else:
        return "Thought 3: The calculation returned 67.5. I have all information needed.\nFinal Answer: Alice Smith's current balance is $450.00, and 15% of that balance is $67.50."


# 4. Pure-Python ReAct Loop
def execute_react_agent(user_query: str, max_iterations: int = 5):
    print("=" * 65)
    print(f"USER QUERY: {user_query}")
    print("=" * 65)

    scratchpad = ""
    for step in range(1, max_iterations + 1):
        full_prompt = f"Objective: {user_query}\nTrajectory History:\n{scratchpad}\nGenerate next Thought/Action or Final Answer:"
        llm_response = mock_llm_inference(full_prompt)

        # Check for Final Answer termination
        if "Final Answer:" in llm_response:
            print(f"\n[STEP {step}] MODEL SYNTHESIS:")
            print(llm_response)
            final_answer = llm_response.split("Final Answer:")[-1].strip()
            print("\n" + "=" * 65)
            print(f"AGENT MISSION COMPLETE: {final_answer}")
            print("=" * 65)
            return final_answer

        # Extract Thought and Action
        print(f"\n[STEP {step}] AGENT REASONING & ACTION:")
        print(llm_response)
        scratchpad += f"\n{llm_response}"

        action_match = re.search(r"Action:\s*([a-zA-Z0-9_]+)\((.*)\)", llm_response)
        if action_match:
            tool_name = action_match.group(1).strip()
            tool_arg = action_match.group(2).strip()

            if tool_name in TOOL_REGISTRY:
                observation = TOOL_REGISTRY[tool_name](tool_arg)
            else:
                observation = f"Error: Tool '{tool_name}' is not registered."

            print(f"--> [ENVIRONMENT OBSERVATION]: {observation}")
            scratchpad += f"\nObservation {step}: {observation}"
        else:
            print("--> [ERROR]: No valid tool call action found.")
            break

    return "Agent terminated without final answer."


if __name__ == "__main__":
    execute_react_agent("What is 15% of the account balance for customer cust_101?")
