---
allowed-tools: Bash
description: Test MCP server (simple version)
---

# Test MCP Server: $ARGUMENTS

!`echo "🧪 Testing MCP server: $ARGUMENTS"`
!`cd /home/gotime2022/mcp-kernel-new/servers/http/$ARGUMENTS-http-mcp && python3 -m src.${ARGUMENTS}_server 2>&1 | head -5`
!`ps aux | grep "$ARGUMENTS.*server" | grep -v grep | head -1`

## Usage Examples:
- `/mcp-test-simple github`
- `/mcp-test-simple supabase`
- `/mcp-test-simple vercel-v0`