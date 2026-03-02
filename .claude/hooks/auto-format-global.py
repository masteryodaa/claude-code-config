#!/usr/bin/env python3
"""Global PostToolUse auto-formatter for Claude Code.

Maps file extensions to formatters (ruff, prettier).
Skips if the project has its own auto-format.py hook.
"""

import json
import os
import shutil
import subprocess
import sys

FORMATTER_MAP = {
    # Python → ruff
    ".py": ("ruff", ["ruff", "format", "--quiet"]),
    # Web/JS/TS → prettier
    ".js": ("prettier", ["prettier", "--write", "--log-level", "silent"]),
    ".ts": ("prettier", ["prettier", "--write", "--log-level", "silent"]),
    ".jsx": ("prettier", ["prettier", "--write", "--log-level", "silent"]),
    ".tsx": ("prettier", ["prettier", "--write", "--log-level", "silent"]),
    ".css": ("prettier", ["prettier", "--write", "--log-level", "silent"]),
    ".json": ("prettier", ["prettier", "--write", "--log-level", "silent"]),
    ".md": ("prettier", ["prettier", "--write", "--log-level", "silent"]),
    ".yaml": ("prettier", ["prettier", "--write", "--log-level", "silent"]),
    ".yml": ("prettier", ["prettier", "--write", "--log-level", "silent"]),
    ".html": ("prettier", ["prettier", "--write", "--log-level", "silent"]),
}


def main():
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = hook_input.get("tool_name", "")
    if tool_name not in ("Edit", "Write"):
        return

    file_path = hook_input.get("tool_params", {}).get("file_path", "")
    if not file_path or not os.path.isfile(file_path):
        return

    # Skip if project has its own auto-format hook
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if project_dir:
        project_hook = os.path.join(project_dir, ".claude", "hooks", "auto-format.py")
        if os.path.isfile(project_hook):
            return

    # Find the right formatter
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    if ext not in FORMATTER_MAP:
        return

    formatter_name, cmd = FORMATTER_MAP[ext]

    # Check if formatter is installed
    if not shutil.which(formatter_name):
        return

    # Run formatter
    try:
        subprocess.run(
            cmd + [file_path],
            capture_output=True,
            timeout=10,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass  # Fail silently — formatting is best-effort


if __name__ == "__main__":
    main()
