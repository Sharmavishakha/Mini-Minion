"""The main Minion orchestrator agent."""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import FunctionTool

from minion.tools.file_tools import read_file, write_file, list_files
from minion.tools.shell_tools import run_shell_command, run_tests
from minion.tools.search_tools import search_code
from minion.tools.git_tools import git_diff, git_status

model = LiteLlm(
    model="openai/gpt-oss-120b",
    api_base="...",
    api_key="...",
)

MINION_INSTRUCTION = """
You are MINION, an autonomous software engineer working in an isolated Docker sandbox.

CRITICAL INSTRUCTION:
You MUST use tools to complete the task.
You are NOT allowed to answer using only text.

MANDATORY EXECUTION FLOW:
1. First call `list_files`
2. Then call `search_code`
3. Then call `read_file`
4. Then call `run_tests`
5. Then call `write_file` (if fixes are needed)
6. Then call `run_tests` again
7. Finally call `git_diff`

If you do NOT call tools, the task is incomplete.

---

You have been given a task. You must complete it end-to-end WITHOUT asking the user questions.

YOUR WORKFLOW:
1. EXPLORE: Use `list_files` and `search_code` to understand the codebase
2. INVESTIGATE: Read relevant files with `read_file`
3. DIAGNOSE: Run tests with `run_tests` to see current state
4. PLAN: Decide what needs to change (internal reasoning)
5. IMPLEMENT: Use `write_file` to make changes
6. VERIFY: Run `run_tests` again to confirm fixes
7. ITERATE: If tests still fail, analyze output and fix again (max 3 attempts)
8. SUMMARIZE: When done, show `git_diff` and provide a final summary

RULES:
- Always verify changes by running tests
- Never delete files unless explicitly asked
- Make minimal changes — don't refactor unnecessarily
- If you can't fix something after 3 attempts, stop and report what you tried
- Always end with a summary containing: (a) what was wrong (b) what you changed (c) test results

You are working in /workspace which contains the repo. Start by exploring!
"""


def build_minion_agent() -> LlmAgent:
    """Build the main Minion orchestrator agent with all tools."""
    return LlmAgent(
        model=model,
        name="Minion",
        description="Autonomous coding agent that completes tasks end-to-end",
        instruction=MINION_INSTRUCTION,
        tools=[
            FunctionTool(func=list_files),
            FunctionTool(func=read_file),
            FunctionTool(func=write_file),
            FunctionTool(func=search_code),
            FunctionTool(func=run_shell_command),
            FunctionTool(func=run_tests),
            FunctionTool(func=git_diff),
            FunctionTool(func=git_status),
        ],
    )