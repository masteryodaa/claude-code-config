# Playbook: MCP Server Capabilities

## Active MCP Servers

### 1. GitHub (HTTP Remote)
**Tools**: Code search, PR management, issues, repo analysis, file contents
**Auth**: OAuth via browser (auto-prompted on first use)
**When to use**: Deep GitHub operations beyond what `gh` CLI offers — code search across repos, batch PR operations, automated issue management.

### 2. Telegram
**Tools**: notify_user, ask_user, send_file, zip_project
**Auth**: Bot token + Chat ID (configured in .claude.json)
**When to use**: Notify user of task completion, ask for decisions mid-task, send generated files.
**Pattern**: Use `ask_user` when you need input and the user isn't actively watching the session.

### 3. DBHub (Multi-Database)
**Tools**: Query any database with SQL
**Configured**: SQLite at `~/.claude/data/claude.db`
**When to use**: Store/query structured data, analyze datasets, create local databases for projects.
**Add more DBs**: Edit `~/.claude.json` → dbhub args → add more `--dsn` values.
**DSN formats**:
- SQLite: `file:/path/to/db.sqlite`
- PostgreSQL: `postgres://user:pass@host:5432/dbname`
- MySQL: `mysql://user:pass@host:3306/dbname`

### 4. System Control (Custom Python)
**Tools**: clipboard_read, clipboard_write, screenshot, process_list, process_kill, system_info, desktop_notification, open_url
**Auth**: None (local)
**When to use**: Read/write clipboard, take screenshots for debugging, check system resources, show notifications, open URLs.

### 5. TTS (Custom Python)
**Tools**: speak, save_speech, list_voices, get_voice_info
**Auth**: None (uses edge-tts, no API key)
**When to use**: Read text aloud, generate audio files, accessibility.
**Default voice**: en-US-GuyNeural (300+ voices available — use `list_voices` to browse).

### 6. Scheduler (Custom Python)
**Tools**: schedule_task, list_tasks, remove_task, set_reminder, run_at
**Auth**: None (uses Windows Task Scheduler)
**When to use**: Set reminders, schedule recurring tasks, run commands at specific times.
**Note**: All tasks prefixed with `Claude_` — survives reboots.

## Troubleshooting

### Server won't start
```bash
# Check server status
/mcp

# Test custom server directly
python ~/.claude/mcp-servers/system-control/server.py
# If it hangs waiting for stdin, it's working correctly (stdio transport)
```

### npm-based server fails
- Ensure `cmd /c` wrapper is in args (required on Windows)
- Check `npx` is available: `npx --version`
- Check network connectivity for package download

### Permission denied
- Custom Python servers need no special permissions
- `schtasks` (scheduler) needs normal user permissions
- `taskkill` may need elevation for system processes

## Adding New Database Connections
Edit the dbhub entry in `~/.claude.json` to add more DSNs:
```json
"args": ["/c", "npx", "-y", "@bytebase/dbhub",
  "--dsn", "file:~/.claude/data/claude.db",
  "--dsn", "postgres://user:pass@localhost:5432/mydb"
]
```
