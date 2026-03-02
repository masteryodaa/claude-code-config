---
name: schedule
description: Schedule tasks, reminders, and recurring commands
disable-model-invocation: true
---

# /schedule — Task Scheduling

## Usage
```
/schedule reminder "meeting in 10 min" in 10 minutes
/schedule task "git pull" daily at 09:00
/schedule list
/schedule remove <task-name>
```

## Tools Available
- `mcp__scheduler__schedule_task` — Create a scheduled task (ONCE, DAILY, HOURLY, MINUTE)
- `mcp__scheduler__list_tasks` — List all Claude-created tasks
- `mcp__scheduler__remove_task` — Delete a scheduled task
- `mcp__scheduler__set_reminder` — Quick reminder with popup notification
- `mcp__scheduler__run_at` — Run a command at a specific time

## Task Types
| Type | Example |
|------|--------|
| One-time | `schedule_task("backup", "...", "ONCE", time="14:00")` |
| Daily | `schedule_task("standup", "...", "DAILY", time="09:00")` |
| Hourly | `schedule_task("check", "...", "HOURLY")` |
| Every N min | `schedule_task("ping", "...", "MINUTE", interval_minutes=30)` |

## Notes
- All tasks are prefixed with `Claude_` for easy identification
- Tasks survive reboots (uses Windows Task Scheduler)
- Use `set_reminder` for quick fire-and-forget notifications
- Reminders show a Windows popup dialog
