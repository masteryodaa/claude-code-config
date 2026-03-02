# Playbook: Background Tasks

## What Are Background Tasks?
Commands or agents that run asynchronously while you continue other work. You get notified when they complete.

## When to Use
- **Long-running tests**: `pytest`, `npm test`, build commands
- **Deployments**: `npm run deploy`, `poetry publish`
- **Research agents**: Deep WebSearch that takes time
- **File processing**: Large file operations, bulk transformations

## Bash Background Tasks
```
Use run_in_background: true on the Bash tool.
You'll be notified when it completes — no need to poll.
```

### Examples
- Running a full test suite while continuing to write code
- Building documentation while reviewing other files
- Starting a dev server while working on code changes

## Agent Background Tasks
```
Use run_in_background: true on the Agent tool.
The agent runs independently and returns results when done.
```

### Examples
- Research agent fetching multiple URLs while you write code
- Explore agent searching a large codebase while you work on a known file

## Anti-Patterns
- **Don't poll**: You'll be notified — no `sleep` loops
- **Don't background short tasks**: If it takes <5s, just wait
- **Don't background dependent tasks**: If you need the result to continue, run foreground
- **Don't background file edits**: Multiple writers = race conditions

## Checking Background Tasks
- Use `TaskOutput` with the task ID to check status
- Use `block: false` for non-blocking status check
- Use `block: true` (default) to wait for completion
