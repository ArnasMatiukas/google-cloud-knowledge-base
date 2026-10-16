#!/usr/bin/env bash
# ==============================================================================
# Antigravity 2.0 & ADK Coding Agent MCP Bootstrap Script
# Merges .agents/mcp_config.json into ~/.gemini/config/mcp_config.json
# and optionally installs official ADK coding skills via google-agents-cli.
# ==============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_MCP="$REPO_ROOT/.agents/mcp_config.json"
TARGET_DIR="$HOME/.gemini/config"
TARGET_MCP="$TARGET_DIR/mcp_config.json"

mkdir -p "$TARGET_DIR"

python3 - "$SOURCE_MCP" "$TARGET_MCP" <<'PYEOF'
import json
import os
import sys

src_path, dst_path = sys.argv[1], sys.argv[2]
with open(src_path, "r", encoding="utf-8") as f:
    src_cfg = json.load(f)

dst_cfg = {"mcpServers": {}}
if os.path.exists(dst_path):
    try:
        with open(dst_path, "r", encoding="utf-8") as f:
            dst_cfg = json.load(f) or {"mcpServers": {}}
    except Exception:
        dst_cfg = {"mcpServers": {}}

dst_servers = dst_cfg.setdefault("mcpServers", {})
for name, server_def in src_cfg.get("mcpServers", {}).items():
    dst_servers[name] = server_def

with open(dst_path, "w", encoding="utf-8") as f:
    json.dump(dst_cfg, f, indent=2)

print(f"[OK] Merged {len(src_cfg.get('mcpServers', {}))} MCP server configs into {dst_path}")
PYEOF

if [[ "${1:-}" == "--with-adk-skills" ]]; then
  if command -v uvx >/dev/null 2>&1; then
    echo "[INFO] Running 'uvx google-agents-cli setup' to install official ADK skills..."
    uvx google-agents-cli setup
  else
    echo "[WARN] 'uvx' is not installed. Install uv (https://docs.astral.sh/uv/) and run: uvx google-agents-cli setup"
  fi
else
  echo "[INFO] Tip: Run './scripts/setup_antigravity_mcp.sh --with-adk-skills' to also install official ADK CLI skills via uvx."
fi
