#!/bin/bash
# Claude Code Config Setup Script
# Run this on a new machine to install the full Claude Code setup.
#
# Usage:
#   git clone https://github.com/masteryodaa/claude-code-config.git
#   cd claude-code-config
#   bash setup.sh

set -e

HOME_DIR="$HOME"
CLAUDE_DIR="$HOME_DIR/.claude"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Claude Code Config Setup ==="
echo "Home: $HOME_DIR"
echo "Claude dir: $CLAUDE_DIR"
echo ""

# 1. Copy CLAUDE.md to home directory
echo "[1/7] Copying CLAUDE.md to home directory..."
cp "$SCRIPT_DIR/CLAUDE.md" "$HOME_DIR/CLAUDE.md"

# 2. Create directory structure
echo "[2/7] Creating .claude directory structure..."
mkdir -p "$CLAUDE_DIR/registry"
mkdir -p "$CLAUDE_DIR/playbooks"
mkdir -p "$CLAUDE_DIR/plans/templates"
mkdir -p "$CLAUDE_DIR/hooks"
mkdir -p "$CLAUDE_DIR/skills"
mkdir -p "$CLAUDE_DIR/mcp-servers/system-control"
mkdir -p "$CLAUDE_DIR/mcp-servers/tts"
mkdir -p "$CLAUDE_DIR/mcp-servers/scheduler"
mkdir -p "$CLAUDE_DIR/data"

# 3. Copy settings (don't overwrite if exists)
echo "[3/7] Copying settings..."
if [ ! -f "$CLAUDE_DIR/settings.json" ]; then
    cp "$SCRIPT_DIR/.claude/settings.json" "$CLAUDE_DIR/settings.json"
    echo "  Created settings.json"
else
    echo "  settings.json already exists, skipping (check for updates manually)"
fi

if [ ! -f "$CLAUDE_DIR/settings.local.json" ]; then
    cp "$SCRIPT_DIR/.claude/settings.local.json" "$CLAUDE_DIR/settings.local.json"
fi

# 4. Copy registry
echo "[4/7] Copying registry..."
cp "$SCRIPT_DIR/.claude/registry/index.json" "$CLAUDE_DIR/registry/index.json"

# 5. Copy all content
echo "[5/7] Copying playbooks, templates, hooks, skills, and MCP servers..."
cp "$SCRIPT_DIR"/.claude/playbooks/*.md "$CLAUDE_DIR/playbooks/"
cp "$SCRIPT_DIR"/.claude/plans/templates/*.md "$CLAUDE_DIR/plans/templates/"
cp "$SCRIPT_DIR"/.claude/hooks/*.py "$CLAUDE_DIR/hooks/"

# Copy skills (each skill is a directory with SKILL.md)
for skill_dir in "$SCRIPT_DIR"/.claude/skills/*/; do
    skill_name=$(basename "$skill_dir")
    mkdir -p "$CLAUDE_DIR/skills/$skill_name"
    cp "$skill_dir"/* "$CLAUDE_DIR/skills/$skill_name/" 2>/dev/null || true
done

# Copy MCP servers
for server_dir in "$SCRIPT_DIR"/.claude/mcp-servers/*/; do
    server_name=$(basename "$server_dir")
    mkdir -p "$CLAUDE_DIR/mcp-servers/$server_name"
    cp "$server_dir"/* "$CLAUDE_DIR/mcp-servers/$server_name/" 2>/dev/null || true
done

# Copy memory templates (into a generic project memory dir)
echo "  Copying memory templates..."
# Memory files are per-project; these are templates for reference
mkdir -p "$CLAUDE_DIR/memory-templates"
cp "$SCRIPT_DIR"/.claude/memory/*.md "$CLAUDE_DIR/memory-templates/"

# 6. Install dependencies
echo "[6/7] Installing dependencies..."

# Python MCP server deps
for req_file in "$CLAUDE_DIR"/mcp-servers/*/requirements.txt; do
    server_name=$(basename "$(dirname "$req_file")")
    echo "  Installing $server_name deps..."
    pip install -r "$req_file" --quiet 2>/dev/null || python -m pip install -r "$req_file" --quiet 2>/dev/null || echo "  WARNING: Failed to install $server_name deps"
done

# Global formatters (for auto-format hook)
echo "  Installing formatters..."
pip install ruff --quiet 2>/dev/null || echo "  WARNING: Failed to install ruff"
npm install -g prettier 2>/dev/null || echo "  WARNING: Failed to install prettier"

# 7. Post-setup
echo "[7/7] Post-setup..."
echo ""
echo "=== Setup Complete ==="
echo ""
echo "MANUAL STEPS REMAINING:"
echo ""
echo "1. MCP Servers - Add to your ~/.claude.json:"
echo "   See mcp-config-template.json for the mcpServers block."
echo "   Replace <PLACEHOLDERS> with your actual values:"
echo "   - <HOME>: your home directory path (e.g., C:/Users/yourname)"
echo "   - <YOUR_GITHUB_PAT>: GitHub personal access token"
echo "   - <YOUR_TELEGRAM_BOT_TOKEN>: Telegram bot token"
echo "   - <YOUR_TELEGRAM_CHAT_ID>: Your Telegram chat ID"
echo ""
echo "2. GitHub MCP binary:"
echo "   Download github-mcp-server from GitHub releases or use:"
echo "   claude mcp add --transport http github-mcp https://api.githubcopilot.com/mcp/"
echo ""
echo "3. Update paths in CLAUDE.md:"
echo "   - Update 'Active Projects' with your project paths"
echo "   - Update memory path if your username differs"
echo ""
echo "4. Plugins will auto-install on first use:"
echo "   superpowers, context7, playwright, frontend-design"
echo ""
echo "Done! Start Claude Code and it will pick up the config automatically."
