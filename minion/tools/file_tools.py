"""Tools for reading and writing files in the sandbox."""

from minion.sandbox import get_sandbox


def read_file(file_path: str) -> str:
    """Read the contents of a file from the sandbox.
    
    Args:
        file_path: Path to the file relative to /workspace
    
    Returns:
        File contents as string, or error message
    """
    sb = get_sandbox()
    result = sb.exec(f"cat {file_path}")
    if result["exit_code"] != 0:
        return f"ERROR reading {file_path}: {result['stderr']}"
    return result["stdout"]


def write_file(file_path: str, content: str) -> str:
    """Write content to a file in the sandbox (overwrites existing).
    
    Args:
        file_path: Path relative to /workspace
        content: Full content to write
    
    Returns:
        Success or error message
    """
    sb = get_sandbox()
    # Use base64 to avoid shell escaping issues
    import base64
    b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")
    cmd = f"echo '{b64}' | base64 -d > {file_path}"
    result = sb.exec(cmd)
    if result["exit_code"] != 0:
        return f"ERROR writing {file_path}: {result['stderr']}"
    return f"✅ Wrote {len(content)} chars to {file_path}"


def list_files(directory: str = ".") -> str:
    """List files in a directory (recursive, excluding .git).
    
    Args:
        directory: Path relative to /workspace
    
    Returns:
        Newline-separated file list
    """
    sb = get_sandbox()
    result = sb.exec(
        f"find {directory} -type f -not -path '*/\\.git/*' | head -100"
    )
    return result["stdout"] or "(no files found)"