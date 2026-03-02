---
name: send-message
description: Send messages and files via Telegram
disable-model-invocation: true
---

# /send-message — Telegram Messaging

## Usage
```
/send-message <message>                    # Quick notification
/send-message --ask <question>             # Ask and wait for reply
/send-message --file <path> [caption]      # Send a file
```

## Tools Available
- `mcp__telegram__notify_user` — Send a one-way notification
- `mcp__telegram__ask_user` — Send message and wait for reply
- `mcp__telegram__send_file` — Send a file with optional caption
- `mcp__telegram__zip_project` — Zip and send a project directory

## When to Use
- Task finished → notify with results
- Need a decision → ask and wait for reply
- Generated a file → send it directly
- Long-running task → periodic progress updates

## Examples
- "The build passed, 47 tests green" → `notify_user`
- "Should I deploy to production?" → `ask_user`, wait, act on response
- "Here's the report" → `send_file` with the PDF/CSV path
