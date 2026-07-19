"""The Minion blueprint: a Sequential workflow."""

from google.adk.agents import LlmAgent, SequentialAgent, LoopAgent
from google.adk.tools import FunctionTool

from google.adk.models.lite_llm import LiteLlm
from minion.agent import build_minion_agent
from minion.tools.git_tools import git_diff
from minion.tools.shell_tools import run_tests


model = LiteLlm(
    model="openai/gpt-oss-120b",
    api_base="...",
    api_key="...",
)


def build_final_reporter() -> LlmAgent:
    """Agent that produces the final PR-style summary."""
    return LlmAgent(
        model=model,
        name="FinalReporter",
        description="Generates final report with diff and test results",
        instruction="""
        Your job is to create a final "PR-style" report.
        
        Steps:
        1. Call `git_diff` to get all changes
        2. Call `run_tests` to confirm final test status
        3. Produce a report with sections:
           ## Summary
           ## Changes (the diff)
           ## Test Results
           ## Notes for Reviewer
        """,
        tools=[
            FunctionTool(func=git_diff),
            FunctionTool(func=run_tests),
        ],
    )


def build_minion_workflow() -> SequentialAgent:
    """Build the full Minion blueprint: work → report."""
    minion = build_minion_agent()
    reporter = build_final_reporter()

    return SequentialAgent(
        name="MinionBlueprint",
        description="End-to-end Mini Minion: solves task then reports",
        sub_agents=[minion, reporter],
    )