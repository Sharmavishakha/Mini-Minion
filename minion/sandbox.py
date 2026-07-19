"""Manages the isolated Docker sandbox for the Minion."""

import docker
import os
import tarfile
import io
from pathlib import Path


class Sandbox:
    """Wraps a Docker container that serves as the agent's workspace."""

    def __init__(self, image: str = "minion-sandbox:latest", 
                 repo_path: str = "./sample_repo"):
        self.client = docker.from_env()
        self.image = image
        self.repo_path = Path(repo_path).resolve()
        self.container = None

    def start(self):
        """Start the sandbox with the repo mounted."""
        print(f"🐳 Starting sandbox from image {self.image}")
        self.container = self.client.containers.run(
            self.image,
            detach=True,
            volumes={
                str(self.repo_path): {
                    "bind": "/workspace",
                    "mode": "rw"
                }
            },
            working_dir="/workspace",
            tty=True,
            stdin_open=True,
            remove=False,
        )
        print(f"✅ Sandbox started: {self.container.short_id}")
        
        # Initialize git in the workspace for diff tracking
        self.exec("git init -q && git add -A && git commit -q -m 'initial' --allow-empty")
        return self

    def exec(self, command: str, workdir: str = "/workspace") -> dict:
        """Execute a shell command in the sandbox."""
        if not self.container:
            raise RuntimeError("Sandbox not started")
        
        exec_result = self.container.exec_run(
            cmd=["/bin/bash", "-c", command],
            workdir=workdir,
            demux=True,
        )
        stdout, stderr = exec_result.output
        return {
            "exit_code": exec_result.exit_code,
            "stdout": (stdout or b"").decode("utf-8", errors="replace"),
            "stderr": (stderr or b"").decode("utf-8", errors="replace"),
        }

    def stop(self):
        """Clean up the container."""
        if self.container:
            print(f"🧹 Stopping sandbox {self.container.short_id}")
            self.container.stop(timeout=5)
            self.container.remove()
            self.container = None


# Global sandbox instance (shared across tools)
_sandbox: Sandbox | None = None


def get_sandbox() -> Sandbox:
    global _sandbox
    if _sandbox is None:
        raise RuntimeError("Sandbox not initialized. Call init_sandbox() first.")
    return _sandbox


def init_sandbox(repo_path: str = "./sample_repo") -> Sandbox:
    global _sandbox
    _sandbox = Sandbox(repo_path=repo_path)
    _sandbox.start()
    return _sandbox


def destroy_sandbox():
    global _sandbox
    if _sandbox:
        _sandbox.stop()
        _sandbox = None