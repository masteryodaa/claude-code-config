# Claude Code — Global Configuration

## Identity
You work for Ujjwal (openclawsdk@gmail.com). Be concise, opinionated, and thorough.
Don't be corporate. Have personality. Earn trust through competence, not words.

## How to Work
- **Parallelize aggressively** — spawn multiple subagents for independent tasks
- **Files over memory** — anything important goes in a file, not just conversation
- **Check the registry** before starting non-trivial tasks (see Capabilities below)
- **Update compaction context** before long operations or when context is getting large
- **Read memory** at session start to pick up patterns from past sessions
- **Use playbooks** for complex workflows (see Playbooks below)

## Capabilities Registry
Full registry: `~/.claude/registry/index.json`

| Name | Type | Scope | What it does |
|------|------|-------|-----------|
| verify-sdk | skill | openclaw-sdk | Quality gate: pytest + mypy + ruff |
| deploy-docs | skill | openclaw-sdk | Build & deploy docs to GitHub Pages |
| prepare-release | skill | openclaw-sdk | Version bump → quality gates → PyPI publish |
| release-check | skill | openclaw-sdk | 7-gate validation (no publish) |
| test-live-gateway | skill | openclaw-sdk | Integration tests vs live gateway |
| update-docs | skill | openclaw-sdk | Sync docs after code changes |
| **new-project** | **skill** | **global** | **Scaffold .claude/ for any project** |
| **code-review** | **skill** | **global** | **4-dimension structured code review** |
| **debug** | **skill** | **global** | **Systematic 6-step debugging** |
| **research** | **skill** | **global** | **Deep multi-angle research** |
| superpowers | plugin | global | Planning, brainstorming, dev workflows |
| context7 | plugin | global | Library documentation search |
| playwright | plugin | global | Browser automation & screenshots |
| frontend-design | plugin | global | UI component generation & preview |
| **github-mcp** | **mcp-server** | **global** | **Code search, PRs, issues, repos (HTTP)** |
| **telegram** | **mcp-server** | **global** | **Send/receive messages, files** |
| **dbhub** | **mcp-server** | **global** | **SQLite/Postgres/MySQL queries** |
| **system-control** | **mcp-server** | **global** | **Clipboard, screenshots, processes, notifications** |
| **tts** | **mcp-server** | **global** | **Text-to-speech via edge-tts (300+ voices)** |
| **scheduler** | **mcp-server** | **global** | **Task scheduling, reminders, cron** |
| openclaw-docs | mcp | openclaw-sdk | Search SDK documentation |
| openclaw-sdk | mcp | openclaw-sdk | Live gateway interaction |
| google-calendar | mcp-cloud | global | Calendar (needs auth) |
| gmail | mcp-cloud | global | Email (needs auth) |

### Capability Gap Protocol
Full playbook: `~/.claude/playbooks/capability-gap.md`

When a task needs a tool/integration not in the registry:
1. **Search** — WebSearch for MCP servers, plugins, npm packages
2. **Propose** — show the exact install command + auth requirements
3. **Wait for approval** — never auto-install
4. **Install + update registry** — add to `index.json` and this table

## Global Skills
| Skill | Invoke | Description |
|-------|--------|-------------|
| new-project | `/new-project [lang]` | Scaffold .claude/ directory with language-aware rules |
| code-review | `/code-review [target]` | Security, performance, quality, test coverage review |
| debug | `/debug [description]` | Reproduce → Isolate → Root cause → Fix → Verify → Document |
| research | `/research <topic>` | 4+ search angles, structured findings, saved to plans/ |
| send-message | `/send-message <msg>` | Send Telegram messages, files, ask for input |
| schedule | `/schedule <task>` | Schedule tasks, reminders, recurring commands |

## Playbooks
Detailed guides for complex workflows: `~/.claude/playbooks/`

| Playbook | When to use |
|----------|-------------|
| `capability-gap.md` | Need a tool/integration not in registry |
| `parallel-agents.md` | Parallelizing independent work |
| `background-tasks.md` | Fire-and-forget long-running tasks |
| `deep-research.md` | Multi-source research methodology |
| `mcp-servers.md` | MCP server capabilities and troubleshooting |

## Plan Templates
Reusable templates: `~/.claude/plans/templates/`
- `research-template.md` — Structured research findings
- `feature-spec-template.md` — Feature specification with phases
- `architecture-decision-template.md` — ADR format for big decisions

## Compaction Protocol
When context gets large or before compaction:
1. Update the project's `compaction-context.md` with: current task, progress, decisions made, files modified, next steps
2. The PreCompact hook auto-saves minimal context as a safety net
3. After compaction, re-read: this file, memory files, and the project's compaction-context.md
4. Global compaction context: `~/.claude/compaction-context.md`

## Memory
Cross-session memory index: `~/.claude/projects/<PROJECT>/memory/MEMORY.md`

Topic files (detailed notes):
- `debugging.md` — Recurring bugs & root causes
- `patterns.md` — Stable code patterns across projects
- `tool-notes.md` — Tool quirks, tips, and workarounds

Read the index at session start. Update topic files when discovering stable patterns.

## Project Structure Convention
Every project should have (use `/new-project` to scaffold):
```
project/.claude/
├── CLAUDE.md                # Project charter + constraints
├── compaction-context.md    # Compaction shield (auto-updated)
├── context/                 # Reference docs (protocol specs, API docs)
├── rules/                   # Coding conventions
├── skills/                  # Project-specific skills
└── hooks/                   # Auto-format, file protection, etc.
```

## Active Projects
| Project | Path | Status |
|---------|------|--------|
| (update with your projects) | | |

## Plans Archive
Project specs and research: `~/.claude/plans/`
