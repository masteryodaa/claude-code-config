# Tool & Workflow Notes

Quirks, tips, and workarounds for tools and workflows. Things that aren't in the docs but matter in practice.

## Claude Code
- Compaction loses context — always keep compaction-context.md updated
- Hooks run synchronously — keep them fast (<10s)
- settings.json hooks use bash syntax even on Windows (Git Bash)

## MCP Servers
- npm-based servers (telegram, dbhub) need `cmd /c` wrapper on Windows — `/c` gets mangled to `C:/` by `claude mcp add`, must fix manually in .claude.json
- Custom Python servers at `~/.claude/mcp-servers/` use `mcp.server.fastmcp.FastMCP` — no wrapper needed
- GitHub MCP uses HTTP transport (remote, no local process) — OAuth prompts on first use
- Scheduler uses Windows `schtasks` — all tasks prefixed with `Claude_`
- TTS uses edge-tts (no API key needed, 300+ voices, default: en-US-GuyNeural)

## Git
(To be populated as issues arise)

## Package Managers
(To be populated as issues arise)

---

*Updated when tool quirks are discovered and verified.*
