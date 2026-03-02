# Claude Code Config

Portable Claude Code setup with global skills, playbooks, hooks, MCP servers, and a capability registry.

## What's Included

| Component | Count | Description |
|-----------|-------|-------------|
| **Global Skills** | 6 | `/new-project`, `/code-review`, `/debug`, `/research`, `/send-message`, `/schedule` |
| **Playbooks** | 5 | Guides for capability gaps, parallel agents, background tasks, deep research, MCP servers |
| **Plan Templates** | 3 | Research, feature spec, and architecture decision (ADR) templates |
| **Hooks** | 2 | Auto-format (ruff/prettier) on file save, compaction context safety net |
| **MCP Servers** | 3 custom | System control (clipboard/screenshots/processes), TTS (300+ voices), Task scheduler |
| **Registry** | 1 | Central index of all capabilities, skills, plugins, and MCP servers |
| **Memory Templates** | 4 | Cross-session learning: debugging insights, patterns, tool notes |

## Quick Setup

```bash
git clone https://github.com/masteryodaa/claude-code-config.git
cd claude-code-config
bash setup.sh
```

Then complete the manual steps printed by the setup script (MCP tokens, paths, etc.).

## Structure

```
.
├── CLAUDE.md                              # Global config (goes to ~/CLAUDE.md)
├── mcp-config-template.json               # MCP server config template (merge into ~/.claude.json)
├── setup.sh                               # One-command setup script
└── .claude/
    ├── settings.json                      # Permissions, hooks, auto-updates
    ├── settings.local.json                # Local permission overrides
    ├── registry/index.json                # Capability registry
    ├── playbooks/                         # Decision guides
    │   ├── capability-gap.md
    │   ├── parallel-agents.md
    │   ├── background-tasks.md
    │   ├── deep-research.md
    │   └── mcp-servers.md
    ├── plans/templates/                   # Reusable templates
    │   ├── research-template.md
    │   ├── feature-spec-template.md
    │   └── architecture-decision-template.md
    ├── hooks/                             # Auto-triggered scripts
    │   ├── auto-format-global.py           # Format on save (ruff/prettier)
    │   └── save-compaction-context.py      # Pre-compaction safety net
    ├── skills/                            # Slash-command skills
    │   ├── code-review/SKILL.md
    │   ├── debug/SKILL.md
    │   ├── new-project/SKILL.md
    │   ├── research/SKILL.md
    │   ├── schedule/SKILL.md
    │   └── send-message/SKILL.md
    ├── mcp-servers/                       # Custom Python MCP servers
    │   ├── system-control/                # Clipboard, screenshots, processes
    │   ├── tts/                           # Text-to-speech (edge-tts)
    │   └── scheduler/                     # Windows Task Scheduler
    └── memory/                            # Cross-session memory templates
        ├── MEMORY.md
        ├── debugging.md
        ├── patterns.md
        └── tool-notes.md
```

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Python 3.10+
- Node.js 18+ (for npm-based MCP servers)
- Windows 11 (for system-control, scheduler, notification hooks)

## MCP Servers

| Server | Auth | Description |
|--------|------|-------------|
| **github-mcp** | GitHub PAT or OAuth | Code search, PRs, issues, repos |
| **telegram** | Bot token + Chat ID | Send/receive messages and files |
| **system-control** | None | Clipboard, screenshots, process control, notifications |
| **tts** | None | Text-to-speech with 300+ voices via edge-tts |
| **scheduler** | None | Windows Task Scheduler integration |
| **dbhub** | None | SQLite/Postgres/MySQL queries (npm package) |

## Customization

- Edit `CLAUDE.md` to change identity, active projects, and workflow preferences
- Add project-specific skills to any project's `.claude/skills/` directory
- Add new MCP servers and update `registry/index.json`
- Create new playbooks in `.claude/playbooks/` for recurring workflows
