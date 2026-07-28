from __future__ import annotations

import subprocess
from pathlib import Path


FORBIDDEN_TRACKED_PATTERNS = (
    ".env",
    ".venv/",
    "__pycache__/",
    ".ipynb_checkpoints/",
)


def run_git(*args: str, cwd: Path) -> str:
    """Run a Git command and return stripped standard output."""
    completed = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def tracked_files(repo: Path) -> list[str]:
    output = run_git("ls-files", cwd=repo)
    return [line for line in output.splitlines() if line]


def repository_issues(repo: Path) -> list[str]:
    issues: list[str] = []

    try:
        inside = run_git("rev-parse", "--is-inside-work-tree", cwd=repo)
    except subprocess.CalledProcessError:
        return ["Directory is not a Git repository."]

    if inside != "true":
        issues.append("Directory is not a Git work tree.")

    files = tracked_files(repo)
    for file_name in files:
        normalized = file_name.replace("\\", "/")
        if any(
            normalized == pattern.rstrip("/") or pattern in normalized
            for pattern in FORBIDDEN_TRACKED_PATTERNS
        ):
            issues.append(f"Forbidden tracked path: {file_name}")

    status = run_git("status", "--porcelain", cwd=repo)
    if status:
        issues.append("Working tree is not clean.")

    try:
        run_git("log", "-1", "--oneline", cwd=repo)
    except subprocess.CalledProcessError:
        issues.append("Repository has no commits.")

    return issues


def main() -> int:
    repo = Path.cwd()
    issues = repository_issues(repo)

    if issues:
        print("Repository check failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("Repository check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
