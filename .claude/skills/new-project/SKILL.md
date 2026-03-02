---
name: new-project
description: Scaffold a .claude/ directory for any project
disable-model-invocation: true
---

# /new-project — Project Scaffolding

## Usage
```
/new-project [language]
```
Language: `python`, `javascript`, `typescript`, `go`, or omit for generic.

## What to Create

Create the following structure in the current working directory:

```
.claude/
├── CLAUDE.md                # Project charter (fill with project name + language)
├── compaction-context.md    # Empty template
├── context/                 # Empty dir (for API docs, specs)
├── rules/                   # Language-specific rules
├── skills/                  # Empty dir (for project skills)
└── hooks/                   # Empty dir (for project hooks)
```

### CLAUDE.md Template
```markdown
# [Project Name] — Claude Code Configuration

## Project
- **Language**: [detected or specified]
- **Path**: [current directory]

## How to Work
- Read this file at session start
- Follow rules in `.claude/rules/`
- Update `compaction-context.md` before long operations

## Key Commands
(To be filled as project develops)

## Architecture
(To be filled as project develops)
```

### compaction-context.md Template
```markdown
# Compaction Context

*No active context. Update this file before compaction or long operations.*

## Current Task
(none)

## Progress
(none)

## Next Steps
(none)
```

### Language-Specific Rules

**Python** → `.claude/rules/python.md`:
- Use type hints everywhere
- Prefer pathlib over os.path
- Use ruff for linting, black for formatting
- pytest for testing
- Docstrings: Google style

**JavaScript/TypeScript** → `.claude/rules/js-ts.md`:
- Use ESM imports
- Prefer const, avoid var
- Use prettier for formatting
- Descriptive variable names, no abbreviations

**Go** → `.claude/rules/go.md`:
- Follow effective Go conventions
- Use gofmt/goimports
- Error handling: always check, never ignore
- Prefer table-driven tests

**Generic** (no language specified) → `.claude/rules/general.md`:
- Keep functions small and focused
- Write tests for new functionality
- Document non-obvious decisions

## After Creation
Print a summary of what was created and suggest next steps:
1. Add project-specific commands to CLAUDE.md
2. Add any reference docs to context/
3. Create project-specific skills in skills/
