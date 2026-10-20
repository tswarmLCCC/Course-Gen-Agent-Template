"""
=============================================================================
NEXUS COGNITIVE SYSTEMS - PURE-PYTHON REACT AGENT ENGINE
Course: AINT 2050 - Applied AI Agent Architectures
Unit 1 Applied Programming Laboratory
=============================================================================
Student Name: [Your Name Here]
Date: [Current Date]
=============================================================================
ARCHITECTURAL ANALYSIS (GEMINI VS. CLAUDE):
1. Gemini Function Calling uses OpenAPI 3.0 schemas with native parallel tool dispatch
   and high token throughput, ideal for multimodal real-time stream analysis.
2. Anthropic Claude uses strict JSON Schema validation and excels at multi-step
   code generation and desktop GUI interaction through its Computer Use API.
3. Level 1 prompt assistants without Level 3 state graph guards risk infinite loops,
   hallucinated arguments, and unmonitored financial or data destruction.
=============================================================================
"""

import re
from typing import Dict, Any, Callable, Tuple, Optional


# =============================================================================
# Task 1: Tool Registry & Safe Execution Engine
# =============================================================================
class ToolRegistry:
    """Manages tool registration and safe, isolated execution."""

    def __init__(self):
        self._tools: Dict[str, Callable[[str], str]] = {}

    def register_tool(self, name: str, func: Callable[[str], str]):
        """Registers a named callable tool."""
        self._tools[name] = func

    def dispatch(self, tool_name: str, argument: str) -> str:
        """
        Safely dispatches a registered tool. Catches any exception
        and returns an error observation string without crashing.
        """
        if tool_name not in self._tools:
            return f"Error: Tool '{tool_name}' is not registered."
        try:
            return str(self._tools[tool_name](argument))
        except Exception as e:
            return f"Error executing tool '{tool_name}': {e}"


# Deterministic Core Tool Implementations
def tool_calculator(expression: str) -> str:
    """Safely evaluates basic arithmetic expressions."""
    cleaned = expression.strip()
    if not re.match(r"^[\d\s\+\-\*\/\(\)\.]+$", cleaned):
        return "Error: Invalid characters in arithmetic expression."
    try:
        val = eval(cleaned)
        return str(round(val, 4))
    except Exception as e:
        return f"Error calculating: {e}"


def tool_search_database(query: str) -> str:
    """Mock database lookup for enterprise account balances."""
    db = {
        "acc_101": "Account: ACC_101 | Owner: Nexus Corp | Balance: 15400.00 USD | Status: Active",
        "acc_102": "Account: ACC_102 | Owner: Acme Freight | Balance: 3250.50 USD | Status: Active",
        "acc_103": "Account: ACC_103 | Owner: Cyberdyne LLC | Balance: 0.00 USD | Status: Suspended"
    }
    q = query.strip().lower()
    return db.get(q, f"No record found for account query '{query}'.")


def tool_convert_currency(args_str: str) -> str:
    """
    Converts currency amount from USD to target currency (EUR, GBP, JPY).
    Format expected: 'amount_usd to target_currency' (e.g. '100 to EUR').
    """
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


# =============================================================================
# Task 2: ReAct Action Parser
# =============================================================================
def parse_agent_action(model_text: str) -> Tuple[bool, str, str]:
    """
    Parses LLM generation to detect Final Answer or Action calls.
    Returns: (is_final: bool, action_name: str, arguments: str)
    """
    if "Final Answer:" in model_text:
        answer = model_text.split("Final Answer:")[-1].strip()
        return True, "FINAL_ANSWER", answer

    match = re.search(r"Action:\s*([a-zA-Z0-9_]+)\((.*)\)", model_text)
    if match:
        tool_name = match.group(1).strip()
        args = match.group(2).strip()
        return False, tool_name, args

    return False, "MALFORMED_ACTION", model_text.strip()


# =============================================================================
# Task 3: Autonomous ReAct Agent Loop
# =============================================================================
class ReActAgent:
    """Autonomous ReAct agent implementing Thought-Action-Observation loops."""

    def __init__(self, registry: ToolRegistry, llm_engine: Optional[Callable[[str], str]] = None):
        self.registry = registry
        self.llm_engine = llm_engine or self._default_mock_llm

    def _default_mock_llm(self, prompt: str) -> str:
        """Simulates LLM response based on scratchpad history."""
        if "Observation 1:" not in prompt:
            return "Thought 1: I need to query the account balance for 'acc_101'.\nAction: search_database(acc_101)"
        elif "Observation 2:" not in prompt:
            return "Thought 2: The balance is 15400.00 USD. Now I will convert this amount to EUR.\nAction: convert_currency(15400.00 to EUR)"
        else:
            return "Thought 3: The converted balance is 14168.00 EUR. I have satisfied the request.\nFinal Answer: Nexus Corp's balance of $15,400.00 USD is equivalent to 14,168.00 EUR."

    def run(self, user_query: str, max_iterations: int = 6) -> str:
        """
        Executes the autonomous reasoning loop up to max_iterations.
        Maintains the scratchpad across steps.
        """
        scratchpad = ""
        for step in range(1, max_iterations + 1):
            prompt = f"User Query: {user_query}\nTrajectory:\n{scratchpad}\nGenerate next Thought/Action or Final Answer:"
            response = self.llm_engine(prompt)

            is_final, tool_name, args = parse_agent_action(response)
            if is_final:
                return args

            if tool_name == "MALFORMED_ACTION":
                scratchpad += f"\nObservation {step}: Error: Could not parse Action syntax. Use 'Action: tool(arg)'."
                continue

            scratchpad += f"\n{response}"
            obs = self.registry.dispatch(tool_name, args)
            scratchpad += f"\nObservation {step}: {obs}"

        return "Error: Agent reached maximum recursion limit (possible loop detected)."


# =============================================================================
# Automated Self-Verification Suite
# =============================================================================
def run_tests():
    print("Running Unit 1 ReAct Agent Self-Verification Suite...\n")

    # 1. Test Tool Registry & Tools
    reg = ToolRegistry()
    reg.register_tool("calculator", tool_calculator)
    reg.register_tool("search_database", tool_search_database)
    reg.register_tool("convert_currency", tool_convert_currency)

    calc_res = reg.dispatch("calculator", "100 * 4.5 + 50")
    assert calc_res == "500.0", f"Calculator error: {calc_res}"

    db_res = reg.dispatch("search_database", "acc_101")
    assert "15400.00 USD" in db_res

    curr_res = reg.dispatch("convert_currency", "100 to EUR")
    assert "92.00 EUR" in curr_res
    print("[PASS] Task 1: Tool Registry & deterministic tools verified.")

    # 2. Test Action Parser
    is_f, act, arg = parse_agent_action("Thought: compute.\nAction: calculator(25 * 4)")
    assert is_f is False and act == "calculator" and arg == "25 * 4"

    is_f2, act2, ans2 = parse_agent_action("Thought: finished.\nFinal Answer: Task succeeded.")
    assert is_f2 is True and ans2 == "Task succeeded."
    print("[PASS] Task 2: ReAct Action Parser verified.")

    # 3. Test Full Autonomous Agent Execution
    agent = ReActAgent(reg)
    final_output = agent.run("What is Nexus Corp's balance in EUR?")
    assert "14,168.00 EUR" in final_output
    print("[PASS] Task 3: Autonomous multi-step ReAct agent verified.")

    # 4. Test Recursion Guard
    looping_llm = lambda p: "Thought: I am looping.\nAction: calculator(1+1)"
    looping_agent = ReActAgent(reg, looping_llm)
    guard_res = looping_agent.run("Force loop", max_iterations=3)
    assert "maximum recursion limit" in guard_res
    print("[PASS] Task 4: Recursion guard prevents infinite looping.")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED! Sample Agent Trajectory Output:")
    print("=" * 60)
    print(final_output)


if __name__ == "__main__":
    run_tests()
