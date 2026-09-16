#!/usr/bin/env python3
"""
CLI Utility to auto-format and type-check all Python files in the repository
without opening them individually in VS Code.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Helper to run shell commands and display output."""
    print(f"\n⚡ {description}...")
    result = subprocess.run(cmd, check=False)
    if result.returncode == 0:
        print(f"✅ {description} completed successfully.")
        return True
    else:
        print(
            f"❌ {description} found issues or failed (Exit code: {result.returncode})."
        )
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Format and type-check all Python files in current directory."
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check formatting without writing changes.",
    )
    args = parser.parse_args()

    root_dir = Path.cwd()
    print(f"🔍 Running auto-formatter and type-checker in: {root_dir}")

    # 1. Run Ruff Formatter
    format_cmd = ["ruff", "format"]
    if args.check_only:
        format_cmd.append("--check")
    format_cmd.append(".")

    # 2. Run Ruff Import Sorter / Linter
    lint_cmd = (
        ["ruff", "check", "--fix", "."]
        if not args.check_only
        else ["ruff", "check", "."]
    )

    # 3. Run Pyright / Pylance Type Checker
    typecheck_cmd = ["pyright", "."]

    # Execute workflow
    fmt_ok = run_command(format_cmd, "Formatting code with Ruff")
    lint_ok = run_command(lint_cmd, "Organizing imports and linting with Ruff")
    type_ok = run_command(typecheck_cmd, "Running Pyright type checker")

    if not (fmt_ok and lint_ok and type_ok):
        sys.exit(1)


if __name__ == "__main__":
    main()
