# Playbook: Parallel Agents

## When to Parallelize
- **Independent searches**: Looking for multiple unrelated things in a codebase
- **Multi-file analysis**: Reading/analyzing files that don't depend on each other
- **Research from multiple angles**: Different WebSearch queries for the same topic
- **Independent subtasks**: Tasks that don't share state or dependencies

## When NOT to Parallelize
- One task's output is another's input (sequential dependency)
- Tasks that modify the same files (race conditions)
- Tasks where you need to decide the next step based on the first result

## Patterns

### Fan-out Search
```
Spawn 3 Explore agents in parallel:
- Agent 1: Find all API endpoints
- Agent 2: Find all database models
- Agent 3: Find all test files
```

### Parallel Research
```
Spawn 2-3 agents in parallel:
- Agent 1: WebSearch for "topic best practices"
- Agent 2: WebSearch for "topic vs alternatives"
- Agent 3: WebSearch for "topic common issues"
```

### Independent File Operations
```
In a single message, call multiple tools:
- Read file A
- Read file B
- Glob for pattern C
```

## Best Practices
1. **Use background agents for slow tasks**: `run_in_background: true` for tasks >30s
2. **Limit concurrency**: 3-4 parallel agents max — more adds overhead without speed
3. **Aggregate results**: After parallel work completes, synthesize in the main context
4. **Use worktree isolation** for agents that modify files: `isolation: "worktree"`
5. **Prefer haiku model** for simple search/read agents to minimize cost
