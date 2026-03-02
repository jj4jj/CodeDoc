"""
cmd_agent.py — low-level subprocess runner for CLI-based LLM agents.

Usage:
    output = run_agent_cmd("claude --dangerously-skip-permissions -p", prompt, cwd="/docs/out")
"""

import logging
import os
import shlex
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)


def run_agent_cmd(
    cmd: str,
    prompt: str,
    cwd: Optional[str] = None,
    timeout: int = 600,
    env: Optional[dict] = None,
) -> str:
    """
    Run a CLI agent command, pipe *prompt* to its stdin, return stdout.

    Args:
        cmd:     Full command string, e.g. "claude --dangerously-skip-permissions -p"
        prompt:  The text prompt to pass via stdin.
        cwd:     Working directory for the subprocess (the output docs dir is useful
                 so agents that write files land in the right place).
        timeout: Maximum seconds to wait (default 10 min).
        env:     Extra environment variables merged with os.environ.

    Returns:
        Captured stdout as a string.

    Raises:
        RuntimeError: if the process exits with a non-zero return code.
        TimeoutError: if the process exceeds *timeout* seconds.
    """
    parts = shlex.split(cmd)
    merged_env = {**os.environ, **(env or {})}

    logger.debug(f"Running agent cmd: {parts!r}  cwd={cwd!r}")

    try:
        result = subprocess.run(
            parts,
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=cwd,
            env=merged_env,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError(
            f"Agent command timed out after {timeout}s: {cmd!r}"
        ) from exc

    if result.stderr:
        logger.debug(f"Agent stderr:\n{result.stderr[:2000]}")

    if result.returncode != 0:
        raise RuntimeError(
            f"Agent command exited with code {result.returncode}: {cmd!r}\n"
            f"stderr: {result.stderr[:1000]}"
        )

    return result.stdout
