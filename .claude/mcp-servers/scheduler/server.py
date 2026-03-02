"""Task Scheduler MCP Server for Windows.

Uses Windows Task Scheduler (schtasks.exe) for persistent scheduling
that survives reboots. All Claude-created tasks are prefixed with
'Claude_' for easy identification and cleanup.
"""

from mcp.server.fastmcp import FastMCP
import subprocess
import os
import re
from datetime import datetime, timedelta

mcp = FastMCP("Task Scheduler")

TASK_PREFIX = "Claude_"


def _sanitize_name(name: str) -> str:
    """Sanitize task name for Windows Task Scheduler."""
    clean = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
    if not clean.startswith(TASK_PREFIX):
        clean = TASK_PREFIX + clean
    return clean[:50]


@mcp.tool()
def schedule_task(
    name: str,
    command: str,
    schedule_type: str = "ONCE",
    time: str = "",
    date: str = "",
    interval_minutes: int = 0,
) -> str:
    """Schedule a Windows task.

    Args:
        name: Task name (auto-prefixed with 'Claude_')
        command: Shell command to run
        schedule_type: ONCE, DAILY, HOURLY, or MINUTE
        time: Time in HH:MM format (24h). Defaults to 1 minute from now for ONCE.
        date: Date in YYYY-MM-DD format. Defaults to today for ONCE.
        interval_minutes: Interval for MINUTE schedule type.
    """
    try:
        task_name = _sanitize_name(name)

        if schedule_type == "ONCE" and not time:
            future = datetime.now() + timedelta(minutes=1)
            time = future.strftime("%H:%M")
        if schedule_type == "ONCE" and not date:
            date = datetime.now().strftime("%Y/%m/%d")
        elif date:
            date = date.replace("-", "/")

        cmd = [
            "schtasks", "/Create", "/TN", task_name,
            "/TR", command, "/F",
        ]

        if schedule_type == "ONCE":
            cmd.extend(["/SC", "ONCE", "/ST", time, "/SD", date])
        elif schedule_type == "DAILY":
            if not time:
                return "Error: time (HH:MM) required for DAILY schedule"
            cmd.extend(["/SC", "DAILY", "/ST", time])
        elif schedule_type == "HOURLY":
            cmd.extend(["/SC", "HOURLY"])
        elif schedule_type == "MINUTE":
            if not interval_minutes:
                return "Error: interval_minutes required for MINUTE schedule"
            cmd.extend(["/SC", "MINUTE", "/MO", str(interval_minutes)])
        else:
            return f"Error: unknown schedule_type '{schedule_type}'. Use ONCE, DAILY, HOURLY, or MINUTE."

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return f"Task '{task_name}' scheduled ({schedule_type} at {time or 'interval'})"
        return f"Error: {result.stderr or result.stdout}"
    except Exception as e:
        return f"Error scheduling task: {e}"


@mcp.tool()
def list_tasks() -> str:
    """List all Claude-created scheduled tasks."""
    try:
        result = subprocess.run(
            ["schtasks", "/Query", "/FO", "LIST", "/V"],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0:
            return f"Error: {result.stderr}"

        # Filter to only Claude_ tasks
        blocks = result.stdout.split("\n\n")
        claude_tasks = []
        for block in blocks:
            if TASK_PREFIX in block:
                claude_tasks.append(block.strip())

        if not claude_tasks:
            return "No Claude-created scheduled tasks found."
        return "\n\n---\n\n".join(claude_tasks)
    except Exception as e:
        return f"Error listing tasks: {e}"


@mcp.tool()
def remove_task(name: str) -> str:
    """Remove a Claude-created scheduled task."""
    try:
        task_name = _sanitize_name(name) if not name.startswith(TASK_PREFIX) else name
        result = subprocess.run(
            ["schtasks", "/Delete", "/TN", task_name, "/F"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            return f"Task '{task_name}' removed."
        return f"Error: {result.stderr or result.stdout}"
    except Exception as e:
        return f"Error removing task: {e}"


@mcp.tool()
def set_reminder(message: str, minutes_from_now: int = 5) -> str:
    """Set a quick reminder that shows a Windows notification.

    Args:
        message: Reminder message text
        minutes_from_now: Minutes until reminder fires (default: 5)
    """
    try:
        future = datetime.now() + timedelta(minutes=minutes_from_now)
        time_str = future.strftime("%H:%M")
        date_str = future.strftime("%Y/%m/%d")
        task_name = _sanitize_name(f"Reminder_{future.strftime('%H%M%S')}")

        safe_msg = message.replace("'", "''").replace('"', '\\"')
        ps_cmd = (
            f"powershell -Command \""
            f"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null; "
            f"[System.Windows.Forms.MessageBox]::Show('{safe_msg}', 'Claude Reminder', 'OK', 'Information')"
            f"\""
        )

        cmd = [
            "schtasks", "/Create", "/TN", task_name,
            "/TR", ps_cmd,
            "/SC", "ONCE", "/ST", time_str, "/SD", date_str, "/F",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return f"Reminder set for {time_str}: '{message}'"
        return f"Error: {result.stderr or result.stdout}"
    except Exception as e:
        return f"Error setting reminder: {e}"


@mcp.tool()
def run_at(command: str, time: str, date: str = "") -> str:
    """Run a shell command at a specific future time.

    Args:
        command: Shell command to execute
        time: Time in HH:MM format (24h)
        date: Date in YYYY-MM-DD format (defaults to today)
    """
    try:
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        task_name = _sanitize_name(f"RunAt_{time.replace(':', '')}_{datetime.now().strftime('%S')}")
        return schedule_task(
            name=task_name.replace(TASK_PREFIX, ""),
            command=command,
            schedule_type="ONCE",
            time=time,
            date=date,
        )
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    mcp.run()
