"""Git operations for tracking Minion's changes."""

from minion.sandbox import get_sandbox


def git_diff() -> str:
    """Show the diff of all changes made by the Minion.
    
    Returns:
        Unified diff output
    """
    sb = get_sandbox()
    result = sb.exec("git add -A && git diff --cached")
    return result["stdout"] or "(no changes)"


def git_status() -> str:
    """Show git status."""
    sb = get_sandbox()
    result = sb.exec("git status --short")
    return result["stdout"] or "(clean)"