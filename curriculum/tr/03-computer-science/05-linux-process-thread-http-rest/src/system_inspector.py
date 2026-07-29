"""Small, testable Linux process and concurrency utilities."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from pathlib import Path
from threading import Lock
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Serializable result of a child process execution."""

    returncode: int
    stdout: str
    stderr: str


class CommandTimeoutError(RuntimeError):
    """Raised when a child process exceeds its deadline."""


def _truncate(text: str, limit: int) -> str:
    if limit < 1:
        raise ValueError("limit must be positive")
    if len(text) <= limit:
        return text
    return f"{text[:limit]}...<truncated>"


def run_command(
    args: list[str],
    *,
    timeout_seconds: float = 5.0,
    max_output_chars: int = 10_000,
    env: dict[str, str] | None = None,
) -> CommandResult:
    """Run a command without a shell and capture bounded text output.

    The caller receives non-zero exit codes as data. Timeouts are converted to
    a domain-specific exception so service code can handle them consistently.
    """

    if not args or any(not isinstance(arg, str) or not arg for arg in args):
        raise ValueError("args must contain non-empty strings")
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")

    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_seconds,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        raise CommandTimeoutError(
            f"command exceeded {timeout_seconds:.2f} seconds"
        ) from exc

    return CommandResult(
        returncode=completed.returncode,
        stdout=_truncate(completed.stdout, max_output_chars),
        stderr=_truncate(completed.stderr, max_output_chars),
    )


def parallel_map(
    function: Callable[[T], R],
    items: Iterable[T],
    *,
    max_workers: int = 4,
) -> list[R]:
    """Apply an I/O-oriented function with an explicit concurrency bound."""

    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")
    with ThreadPoolExecutor(
        max_workers=max_workers,
        thread_name_prefix="lesson-worker",
    ) as executor:
        return list(executor.map(function, items))


class ThreadSafeCounter:
    """Minimal example of protecting shared mutable state with a lock."""

    def __init__(self) -> None:
        self._value = 0
        self._lock = Lock()

    def increment(self, amount: int = 1) -> int:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        with self._lock:
            self._value += amount
            return self._value

    @property
    def value(self) -> int:
        with self._lock:
            return self._value


def collect_runtime_info() -> dict[str, object]:
    """Return non-secret runtime facts useful for diagnostics."""

    return {
        "pid": os.getpid(),
        "parent_pid": os.getppid(),
        "cwd": str(Path.cwd()),
        "python": platform.python_version(),
        "platform": platform.system(),
        "cpu_count": os.cpu_count(),
    }


def main() -> None:
    runtime = collect_runtime_info()
    command = run_command([sys.executable, "--version"])
    print(json.dumps(runtime, indent=2, sort_keys=True))
    print(json.dumps(asdict(command), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
