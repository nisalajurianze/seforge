#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

EXCLUDED_DIRS = {
    ".git", ".engineering", ".agents", ".claude", ".cursor", ".github",
    "__pycache__", ".venv", "venv", "env", "node_modules", "vendor",
    "build", "dist", "target", ".tox", ".nox", ".pytest_cache", ".mypy_cache",
}


def iter_python_files(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in EXCLUDED_DIRS]
        current_path = Path(current)
        for name in files:
            if name.endswith(".py"):
                yield current_path / name


def main() -> int:
    parser = argparse.ArgumentParser(description="Syntax-check project Python files without importing them or creating bytecode.")
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    failures = []
    count = 0
    for path in iter_python_files(root):
        count += 1
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec", dont_inherit=True)
        except (SyntaxError, UnicodeDecodeError, OSError) as exc:
            failures.append(f"{path.relative_to(root)}: {exc}")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        print(f"Python syntax check failed: {len(failures)} of {count} files.", file=sys.stderr)
        return 1

    print(f"Python syntax check passed: {count} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
