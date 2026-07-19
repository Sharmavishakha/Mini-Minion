"""Tools for executing shell commands safely."""

from minion.sandbox import get_sandbox

# Block these commands for safety
FORBIDDEN_PATTERNS = [
    "rm -rf /",
    ":(){ :|:& };:",  # fork bomb
    "> /dev/sda",
    "mkfs",
    "dd if=",
]


def run_shell_command(command: str) -> str:
    """Execute a shell command in the sandbox. 
    Use this for running tests, linters, or exploring the environment.
    
    Args:
        command: Shell command to execute
    
    Returns:
        stdout + stderr + exit code
    """
    # Safety check
    for pattern in FORBIDDEN_PATTERNS:
        if pattern in command:
            return f"❌ BLOCKED: Command contains forbidden pattern: {pattern}"
    
    sb = get_sandbox()
    result = sb.exec(command)
    
    output = f"--- EXIT CODE: {result['exit_code']} ---\n"
    if result["stdout"]:
        output += f"--- STDOUT ---\n{result['stdout']}\n"
    if result["stderr"]:
        output += f"--- STDERR ---\n{result['stderr']}\n"
    return output[:5000]  # Truncate to avoid blowing up context


def run_tests(test_path: str = "tests/") -> str:
    """Run pytest on the given path.
    
    Args:
        test_path: Path to test directory or file
    
    Returns:
        Test results
    """
    sb = get_sandbox()
    result = sb.exec(f"python -m pytest {test_path} -v --tb=short 2>&1")
    output = result["stdout"] + result["stderr"]
    status = "✅ PASSED" if result["exit_code"] == 0 else "❌ FAILED"
    return f"{status}\n{output[:4000]}"