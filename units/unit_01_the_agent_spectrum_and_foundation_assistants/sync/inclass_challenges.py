"""
AINT 2050: Applied AI Agent Architectures
Unit 1 Synchronous Active Learning Challenges
"""

import re
from typing import Dict, Any, Callable, Tuple


# =============================================================================
# Challenge 1: Tool Registry & Safe Dispatcher
# =============================================================================
class ToolRegistry:
    """Manages registered callable tools and safe execution."""

    def __init__(self):
        self._tools: Dict[str, Callable[[str], str]] = {}

    def register_tool(self, name: str, func: Callable[[str], str]):
        self._tools[name] = func

    def dispatch(self, tool_name: str, argument: str) -> str:
        """
        Safely executes a registered tool. If the tool is not found,
        returns an error string. If execution raises an exception,
        catches it and returns the error string.
        """
        if tool_name not in self._tools:
            return f"Error: Tool '{tool_name}' not found."
        try:
            return self._tools[tool_name](argument)
        except Exception as e:
            return f"Error executing '{tool_name}': {e}"


# =============================================================================
# Challenge 2: Action Parsing from Model Output
# =============================================================================
def parse_react_action(model_text: str) -> Tuple[bool, str, str]:
    """
    Parses a model response to determine if it is an Action or Final Answer.
    - If 'Final Answer: [text]' is present, returns (True, 'FINAL_ANSWER', text).
    - If 'Action: tool_name(arguments)' is present, returns (False, tool_name, arguments).
    - If neither is matched, returns (False, 'UNKNOWN', '').
    """
    if "Final Answer:" in model_text:
        ans = model_text.split("Final Answer:")[-1].strip()
        return (True, "FINAL_ANSWER", ans)

    match = re.search(r"Action:\s*([a-zA-Z0-9_]+)\((.*)\)", model_text)
    if match:
        tool_name = match.group(1).strip()
        args = match.group(2).strip()
        return (False, tool_name, args)

    return (False, "UNKNOWN", "")


# =============================================================================
# Automated Verification Suite
# =============================================================================
def run_verification_tests():
    print("Testing Unit 1 Active Learning Challenges...\n")

    # Test Challenge 1
    reg = ToolRegistry()
    reg.register_tool("echo", lambda x: f"Echo: {x}")
    reg.register_tool("failing_tool", lambda x: 1 / 0)

    assert reg.dispatch("echo", "hello") == "Echo: hello"
    assert "not found" in reg.dispatch("missing", "arg")
    assert "Error executing" in reg.dispatch("failing_tool", "arg")
    print("[PASS] Challenge 1: Safe Tool Registry & Dispatcher verified.")

    # Test Challenge 2
    is_final, action, args = parse_react_action("Thought: I need to query.\nAction: search(weather in Denver)")
    assert is_final is False and action == "search" and args == "weather in Denver"

    is_final_2, action_2, ans_2 = parse_react_action("Thought: Done.\nFinal Answer: 72 degrees and sunny.")
    assert is_final_2 is True and action_2 == "FINAL_ANSWER" and ans_2 == "72 degrees and sunny."
    print("[PASS] Challenge 2: ReAct Action & Final Answer parser verified.")

    print("\nALL IN-CLASS CHALLENGES PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_verification_tests()
