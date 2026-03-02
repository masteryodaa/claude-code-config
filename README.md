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

## How It Works — Two-Tier Config

Claude Code uses a **two-tier configuration** system:

```
~/CLAUDE.md                    ← GLOBAL (applies to every project)
~/.claude/                     ← GLOBAL (skills, hooks, MCP servers, registry)
    ├── settings.json
    ├── skills/
    ├── hooks/
    ├── playbooks/
    └── ...

your-project/.claude/          ← PROJECT (overrides/extends global for this project only)
    ├── CLAUDE.md
    ├── rules/
    ├── skills/
    └── hooks/
```

**Global config** (`~/CLAUDE.md` + `~/.claude/`) applies everywhere — every time you run `claude` in any directory, it picks up:
- Your identity, preferences, and workflow rules
- All 6 global skills (`/code-review`, `/debug`, `/research`, etc.)
- All hooks (auto-format, compaction safety net, notifications)
- All MCP servers (GitHub, Telegram, TTS, etc.)
- The capability registry

**Project config** (`your-project/.claude/`) adds project-specific rules on top. It can:
- Add project-specific skills (e.g., `/deploy`, `/test`)
- Add project-specific coding rules (e.g., "use pytest", "always type-hint")
- Override the global auto-format hook with a project-specific one
- Set project-specific compaction context

## Using in Any Project

### Option 1: Use the `/new-project` skill (recommended)

After setup, just `cd` into any project and run:

```bash
cd /path/to/your-project
claude
```

Then inside Claude Code:

```
/new-project python        # For a Python project
/new-project typescript    # For a TS project
/new-project go            # For a Go project
/new-project               # Generic (no language-specific rules)
```

This scaffolds the full `.claude/` directory for that project:

```
your-project/.claude/
├── CLAUDE.md                # Project charter — fill in project name, key commands, architecture
├── compaction-context.md    # Auto-updated before compaction (safety net)
├── context/                 # Drop API specs, protocol docs, reference material here
├── rules/                   # Language-specific coding rules (auto-generated)
│   └── python.md            # e.g., "use type hints", "pytest for testing", "Google docstrings"
├── skills/                  # Add project-specific slash commands here
└── hooks/                   # Project-level hooks (override global if needed)
```

### Option 2: Manual setup

If you prefer manual control, create the minimum:

```bash
mkdir -p your-project/.claude
```

Then create `your-project/.claude/CLAUDE.md`:

```markdown
# My Project — Claude Code Configuration

## Project
- **Language**: Python
- **Path**: /path/to/your-project

## Key Commands
- `pytest` — run tests
- `ruff check .` — lint
- `python -m myapp` — run the app

## Architecture
- FastAPI backend in `src/`
- PostgreSQL database
- Redis for caching

## Rules
- Always use type hints
- Write tests for new features
- Use Google-style docstrings
```

That's it. Claude Code reads this file automatically when you run `claude` inside the project.

### Option 3: Existing project — just start using it

You don't *need* a `.claude/` directory at all. The global config already gives you:

- `/code-review` — review any code in the current directory
- `/debug` — debug any bug in the current project
- `/research` — research anything and save findings
- Auto-formatting on every file save
- All MCP servers (GitHub, Telegram, TTS, etc.)

The project `.claude/` directory just makes Claude **smarter about your specific project** by giving it context about architecture, commands, and rules.

## What Each Global Skill Does

| Skill | Command | What it does |
|-------|---------|-------------|
| **new-project** | `/new-project [lang]` | Scaffolds `.claude/` with language-aware rules |
| **code-review** | `/code-review [target]` | 4-dimension review: security, performance, quality, tests. Gives APPROVE / REQUEST CHANGES / NEEDS DISCUSSION verdict |
| **debug** | `/debug [description]` | 6-step workflow: reproduce → isolate → root cause → fix → verify → document. Saves novel bugs to memory |
| **research** | `/research <topic>` | 4+ search angles, cross-references sources, saves structured findings to `~/.claude/plans/` |
| **send-message** | `/send-message <msg>` | Send Telegram notifications, ask for input, send files |
| **schedule** | `/schedule <task>` | Schedule Windows tasks, set reminders, run commands at specific times |

## Adding Project-Specific Skills

Create a skill file at `your-project/.claude/skills/my-skill/SKILL.md`:

```markdown
---
name: deploy
description: Deploy the app to production
---

# /deploy — Production Deployment

## Steps
1. Run tests: `pytest`
2. Build: `docker build -t myapp .`
3. Push: `docker push myapp:latest`
4. Deploy: `kubectl apply -f k8s/`
5. Verify: check health endpoint
```

Now `/deploy` works only inside that project.

## Hooks — What Runs Automatically

| Hook | When | What it does |
|------|------|-------------|
| **SessionStart (startup)** | Every `claude` launch | Shows git branch, recent commits, loads memory |
| **SessionStart (compact)** | After context compaction | Reloads compaction context and memory |
| **PreCompact** | Before context compaction | Saves git state, working directory, and reload instructions |
| **PostToolUse (Edit/Write)** | After any file edit | Auto-formats with ruff (Python) or prettier (JS/TS/CSS/JSON/MD/YAML) |
| **Notification** | When Claude sends a notification | Shows a Windows popup dialog |

The auto-format hook is smart: if your project has its own `.claude/hooks/auto-format.py`, the global one steps aside.

## Playbooks — When to Use What

| Situation | Playbook |
|-----------|----------|
| Need a tool Claude doesn't have | `capability-gap.md` — search, propose, install, register |
| Task has independent subtasks | `parallel-agents.md` — fan-out patterns, concurrency limits |
| Long-running command | `background-tasks.md` — async patterns, anti-patterns |
| Evaluating a technology | `deep-research.md` — multi-angle search methodology |
| MCP server issues | `mcp-servers.md` — capabilities, troubleshooting, DSN formats |

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
