# Playbook: Capability Gap Resolution

## Trigger
A task requires a tool, integration, or service that is NOT in `~/.claude/registry/index.json`.

## Steps

### 1. Confirm the gap
- Read `~/.claude/registry/index.json`
- Search by name, tags, and description — make sure it's actually missing
- Check if an existing capability can cover the need (e.g., playwright can handle basic web scraping)

### 2. Search for a solution
- **WebSearch** for: `"<service> MCP server"` or `"<service> claude code plugin"`
- Check these known sources:
  - Official MCP servers: https://github.com/modelcontextprotocol/servers
  - Anthropic plugin marketplace: `/plugin` → Discover tab
  - npm: `npx -y <package>-mcp-server`
  - Community lists: search `awesome-mcp-servers`

### 3. Evaluate what you find
- Prefer **official/first-party** MCP servers (e.g., Notion's own MCP > community fork)
- Prefer **HTTP transport** over SSE or stdio (remote, no local process)
- Check if auth is required (API key, OAuth) — note this for the user
- If multiple options exist, present top 2 with pros/cons

### 4. Propose to user
Format:
```
Found: <name> — <what it does>
Install: claude mcp add --transport <type> <name> <url>
Auth needed: <yes/no — details>
Want me to install it?
```

### 5. Install (after user approval only)
```bash
# HTTP (preferred)
claude mcp add --transport http <name> <url>

# Stdio (npm package)
claude mcp add --transport stdio <name> -- npx -y <package>

# With env vars for auth
claude mcp add --transport stdio <name> --env API_KEY=xxx -- npx -y <package>
```

### 6. Update registry
Add the new capability to `~/.claude/registry/index.json` with:
- name, type, scope, description, tags, status
- transport/source info

### 7. Update CLAUDE.md
Add a row to the capabilities table in `~/CLAUDE.md`.

## Rules
- **NEVER auto-install** — always get user approval first
- **NEVER store API keys** in the registry — only in MCP config or env vars
- If nothing exists for the need, say so honestly — don't force a bad fit
- If a plugin/MCP is found but looks unmaintained or sketchy, flag the risk
