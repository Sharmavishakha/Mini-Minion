"""Tools for searching the codebase."""

from minion.sandbox import get_sandbox


def search_code(pattern: str, file_glob: str = "*") -> str:
    """Search for a pattern in the codebase using ripgrep.
    
    Args:
        pattern: Regex pattern to search
        file_glob: Glob to restrict files (e.g. '*.py')
    
    Returns:
        Matching lines with file:line prefixes
    """
    sb = get_sandbox()
    # Escape quotes in pattern
    safe_pattern = pattern.replace("'", "'\\''")
    result = sb.exec(
        f"rg --line-number --max-count 20 -g '{file_glob}' '{safe_pattern}' || true"
    )
    return result["stdout"][:3000] or "(no matches)"