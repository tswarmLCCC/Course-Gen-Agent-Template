"""
=============================================================================
NEXUS COGNITIVE SYSTEMS - PURE-PYTHON REACT AGENT ENGINE
Course: AINT 2050 - Applied AI Agent Architectures
Unit 1 Applied Programming Laboratory — MASTER INSTRUCTOR SOLUTION KEY
=============================================================================
Author: Tim Swarm (Course Lead)
Institution: Laramie County Community College
[FOR INSTRUCTORS ONLY — UNPUBLISHED CANVAS RESOURCE]
=============================================================================
"""

import re
from typing import Dict, Any, Callable, Tuple, Optional


class ToolRegistry:
    """Production tool registry with error isolation and schema metadata."""

    def __init__(self):
        self._tools: Dict[str, Callable[[str], str]] = {}

    def register_tool(self, name: str, func: Callable[[str], str]):
        self._tools[name] = func

    def dispatch(self, tool_name: str, argument: str) -> str:
        if tool_name not in self._tools:
            return f"Error: Tool '{tool_name}' is not registered."
        try:
            return str(self._tools[tool_name](argument))
        except Exception as e:
            return f"Error executing tool '{tool_name}': {e}"


def tool_calculator(expression: str) -> str:
    cleaned = expression.strip()
    if not re.match(r"^[\d\s\+\-\*\/\(\)\.]+$", cleaned):
        return "Error: Invalid characters in arithmetic expression."
    try:
        val = eval(cleaned)
        return str(round(val, 4))
    except Exception as e:
        return f"Error calculating: {e}"


def tool_search_database(query: str) -> str:
    db = {
        "acc_101": "Account: ACC_101 | Owner: Nexus Corp | Balance: 15400.00 USD | Status: Active",
        "acc_102": "Account: ACC_102 | Owner: Acme Freight | Balance: 3250.50 USD | Status: Active",
        "acc_103": "Account: ACC_103 | Owner: Cyberdyne LLC | Balance: 0.00 USD | Status: Suspended"
    }
    q = query.strip().lower()
    return db.get(q, f"No record found for account query '{query}'.")


def tool_convert_currency(args_str: str) -> str:
    rates = {"EUR": 0.92, "GBP": 0.78, "JPY": 155.20}
    parts = args_str.split(" to ")
    if len(parts) != 2:
        return "Error: Expected format 'amount to CURRENCY' (e.g. '100 to EUR')."
    try:
        amt = float(parts[0].strip())
        target = parts[1].strip().upper()
        if target not in rates:
            return f"Error: Unsupported target currency '{target}'."
        converted = amt * rates[target]
        return f"{converted:.2f} {target}"
    except ValueError:
        return "Error: Invalid numeric amount."


def parse_agent_action(model_text: str) -> Tuple[bool, str, str]:
    if "Final Answer:" in model_text:
        answer = model_text.split("Final Answer:")[-1].strip()
        return True, "FINAL_ANSWER", answer

    match = re.search(r"Action:\s*([a-zA-Z0-9_]+)\((.*)\)", model_text)
    if match:
        tool_name = match.group(1).strip()
        args = match.group(2).strip()
        return False, tool_name, args

    return False, "MALFORMED_ACTION", model_text.strip()


class ReActAgent:
    def __init__(self, registry: ToolRegistry, llm_engine: Optional[Callable[[str], str]] = None):
        self.registry = registry
        self.llm_engine = llm_engine or self._mock_llm

    def _mock_llm(self, prompt: str) -> str:
        if "Observation 1:" not in prompt:
            return "Thought 1: I need to query the account balance for 'acc_101'.\nAction: search_database(acc_101)"
        elif "Observation 2:" not in prompt:
            return "Thought 2: The balance is 15400.00 USD. Now I will convert this amount to EUR.\nAction: convert_currency(15400.00 to EUR)"
        else:
            return "Thought 3: The converted balance is 14168.00 EUR. I have satisfied the request.\nFinal Answer: Nexus Corp's balance of $15,400.00 USD is equivalent to 14,168.00 EUR."

    def run(self, user_query: str, max_iterations: int = 6) -> str:
        scratchpad = ""
        for step in range(1, max_iterations + 1):
            prompt = f"User Query: {user_query}\nTrajectory:\n{scratchpad}\nGenerate next Thought/Action or Final Answer:"
            response = self.llm_engine(prompt)

            is_final, tool_name, args = parse_agent_action(response)
            if is_final:
                return args

            if tool_name == "MALFORMED_ACTION":
                scratchpad += f"\nObservation {step}: Error: Could not parse Action syntax."
                continue

            scratchpad += f"\n{response}"
            obs = self.registry.dispatch(tool_name, args)
            scratchpad += f"\nObservation {step}: {obs}"

        return "Error: Agent reached maximum recursion limit (possible loop detected)."


if __name__ == "__main__":
    reg = ToolRegistry()
    reg.register_tool("calculator", tool_calculator)
    reg.register_tool("search_database", tool_search_database)
    reg.register_tool("convert_currency", tool_convert_currency)
    agent = ReActAgent(reg)
    print("Master Instructor Solution Execution Output:\n", agent.run("What is Nexus Corp's balance in EUR?"))
