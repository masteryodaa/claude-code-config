"""Windows System Control MCP Server.

Provides clipboard, screenshots, process management, system info,
desktop notifications, and URL opening via PowerShell/Windows APIs.
"""

from mcp.server.fastmcp import FastMCP
import subprocess
import os
import tempfile

try:
    import pyperclip
except ImportError:
    pyperclip = None

mcp = FastMCP("Windows System Control")


@mcp.tool()
def clipboard_read() -> str:
    """Read current clipboard contents."""
    try:
        if pyperclip:
            return pyperclip.paste()
        result = subprocess.run(
            ["powershell", "-Command", "Get-Clipboard"],
            capture_output=True, text=True, timeout=5,
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error reading clipboard: {e}"


@mcp.tool()
def clipboard_write(text: str) -> str:
    """Write text to clipboard."""
    try:
        if pyperclip:
            pyperclip.copy(text)
        else:
            subprocess.run(
                ["powershell", "-Command", f"Set-Clipboard -Value '{text}'"],
                capture_output=True, timeout=5,
            )
        return f"Copied {len(text)} characters to clipboard"
    except Exception as e:
        return f"Error writing clipboard: {e}"


@mcp.tool()
def screenshot(filename: str = "") -> str:
    """Take a screenshot and save it. Returns the file path."""
    try:
        if not filename:
            filename = os.path.join(tempfile.gettempdir(), "claude_screenshot.png")
        ps_script = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; "
            "$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height); "
            "$graphics = [System.Drawing.Graphics]::FromImage($bitmap); "
            "$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size); "
            f"$bitmap.Save('{filename}'); "
            "$graphics.Dispose(); $bitmap.Dispose()"
        )
        subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True, timeout=15,
        )
        if os.path.exists(filename):
            return f"Screenshot saved to {filename}"
        return "Screenshot failed — file not created"
    except Exception as e:
        return f"Error taking screenshot: {e}"


@mcp.tool()
def process_list(filter_name: str = "") -> str:
    """List running processes. Optionally filter by name prefix."""
    try:
        cmd = ["tasklist", "/FO", "CSV", "/NH"]
        if filter_name:
            cmd.extend(["/FI", f"IMAGENAME eq {filter_name}*"])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        output = result.stdout.strip()
        lines = output.split("\n")
        if len(lines) > 50:
            return "\n".join(lines[:50]) + f"\n... ({len(lines) - 50} more)"
        return output
    except Exception as e:
        return f"Error listing processes: {e}"


@mcp.tool()
def process_kill(name_or_pid: str) -> str:
    """Kill a process by name (e.g. notepad.exe) or PID."""
    try:
        if name_or_pid.isdigit():
            cmd = ["taskkill", "/PID", name_or_pid, "/F"]
        else:
            cmd = ["taskkill", "/IM", name_or_pid, "/F"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return (result.stdout or result.stderr).strip()
    except Exception as e:
        return f"Error killing process: {e}"


@mcp.tool()
def system_info() -> str:
    """Get system information: OS, CPU, memory, disk usage."""
    try:
        ps_script = (
            "$os = Get-CimInstance Win32_OperatingSystem; "
            "$cpu = Get-CimInstance Win32_Processor | Select -First 1; "
            "$disk = Get-CimInstance Win32_LogicalDisk -Filter \"DeviceID='C:'\"; "
            "@{"
            "  OS = $os.Caption + ' ' + $os.Version;"
            "  TotalRAM_GB = [math]::Round($os.TotalVisibleMemorySize/1MB, 1);"
            "  FreeRAM_GB = [math]::Round($os.FreePhysicalMemory/1MB, 1);"
            "  CPU = $cpu.Name;"
            "  CPU_Cores = $cpu.NumberOfCores;"
            "  Disk_Total_GB = [math]::Round($disk.Size/1GB, 1);"
            "  Disk_Free_GB = [math]::Round($disk.FreeSpace/1GB, 1)"
            "} | ConvertTo-Json"
        )
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True, text=True, timeout=15,
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error getting system info: {e}"


@mcp.tool()
def desktop_notification(title: str, message: str) -> str:
    """Show a Windows desktop toast notification."""
    try:
        ps_script = (
            "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null; "
            "$notify = New-Object System.Windows.Forms.NotifyIcon; "
            "$notify.Icon = [System.Drawing.SystemIcons]::Information; "
            f"$notify.BalloonTipTitle = '{title.replace(chr(39), chr(39)+chr(39))}'; "
            f"$notify.BalloonTipText = '{message.replace(chr(39), chr(39)+chr(39))}'; "
            "$notify.Visible = $true; "
            "$notify.ShowBalloonTip(5000); "
            "Start-Sleep -Seconds 6; "
            "$notify.Dispose()"
        )
        subprocess.Popen(
            ["powershell", "-Command", ps_script],
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        return f"Notification shown: {title}"
    except Exception as e:
        return f"Error showing notification: {e}"


@mcp.tool()
def open_url(url: str) -> str:
    """Open a URL in the default browser."""
    try:
        subprocess.run(["cmd", "/c", "start", url], capture_output=True, timeout=5)
        return f"Opened {url}"
    except Exception as e:
        return f"Error opening URL: {e}"


if __name__ == "__main__":
    mcp.run()
