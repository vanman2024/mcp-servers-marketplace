---
description: Deploy MCP server from monorepo to FastMCP Cloud using sync workflow
argument-hint: <server-name>
allowed-tools: Bash, Read, Write, Glob, AskUserQuestion, TodoWrite, Skill
---

**Arguments**: $ARGUMENTS

Goal: Deploy an MCP server from the monorepo to its standalone repo, then to FastMCP Cloud

## Load Deployment Skill

INVOKE the deployment skill to load validation, testing, and verification patterns:

!{skill fastmcp-cloud-deployment}

This provides:
- Pre-deployment validation scripts
- Local testing patterns
- Environment variable verification
- Post-deployment health checks
- Deployment tracking templates

## Usage

```bash
/deploy-mcp-server cats-mcp-server
```

## Workflow

### Step 1: Validate Server Name

- Parse server name from $ARGUMENTS
- Check if server exists in DEPLOYED_SERVERS.md
- If not found, ask user if this is a new deployment

### Step 2: Check for Uncommitted Changes

```bash
cd servers/business-productivity/${SERVER_NAME}
git status --porcelain
```

- If uncommitted changes exist, ask user to commit first
- Show: "You have uncommitted changes. Commit them first?"

### Step 3: Sync to Standalone Repo

```bash
cd /path/to/monorepo
./scripts/sync-to-standalone.sh ${SERVER_NAME}
```

- Execute sync script
- Show sync output (files copied, commit message, push status)
- Mark as complete in todo list

### Step 4: FastMCP Cloud Status

Check deployment status:
- Read DEPLOYED_SERVERS.md to get FastMCP Cloud URL
- Show: "FastMCP Cloud is deploying from standalone repo"
- Show: "Watch deployment at: https://fastmcp.app"
- Show endpoint URL: "Your server will be at: https://${SERVER_NAME}.fastmcp.app/mcp"

### Step 5: Test Instructions

Provide testing commands:

```bash
# Test with MCP Inspector
mcp-inspector https://${SERVER_NAME}.fastmcp.app/mcp

# Test with curl
curl -X POST https://${SERVER_NAME}.fastmcp.app/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'
```

### Step 6: Update Tracking

- Update DEPLOYED_SERVERS.md with:
  - Last synced date (today)
  - Any status changes
- Commit tracking update to monorepo

## New Server Deployment

If server not in DEPLOYED_SERVERS.md:

1. **Ask for confirmation**: "This is a new server. Do you want to deploy it to FastMCP Cloud?"

2. **Check standalone repo exists**:
   ```bash
   gh repo view vanman2024/${SERVER_NAME} 2>/dev/null
   ```

3. **If repo doesn't exist**, guide user:
   ```
   ❌ Standalone repo not found

   Next steps:
   1. Create repo: https://github.com/new
      - Name: ${SERVER_NAME}
      - Private/Public: Your choice
      - Don't initialize with README

   2. Add to sync script: scripts/sync-to-standalone.sh
      - Add case entry for ${SERVER_NAME}

   3. Run this command again
   ```

4. **If repo exists**, continue with sync

5. **Guide FastMCP Cloud setup**:
   ```
   📋 FastMCP Cloud Setup Checklist:

   [ ] Go to https://fastmcp.app
   [ ] Click "New Project"
   [ ] Connect to: https://github.com/vanman2024/${SERVER_NAME}
   [ ] Set environment variables (API keys, etc.)
   [ ] Click "Deploy"
   [ ] Wait for build to complete

   Your server will be at: https://${SERVER_NAME}.fastmcp.app/mcp
   ```

6. **Add to DEPLOYED_SERVERS.md**:
   ```markdown
   ### ${SERVER_NAME}
   - **Monorepo Path**: `servers/category/${SERVER_NAME}/`
   - **Standalone Repo**: https://github.com/vanman2024/${SERVER_NAME}
   - **FastMCP Cloud**: https://fastmcp.app (project: ${SERVER_NAME})
   - **Status**: ✅ Active - X tools
   - **Last Synced**: ${TODAY}
   - **Sync Command**: `./scripts/sync-to-standalone.sh ${SERVER_NAME}`
   ```

## Error Handling

### "No such file or directory" (sync script)
- Ensure you're in monorepo root
- Run: `cd /path/to/mcp-servers-marketplace`

### "Permission denied (publickey)"
- Sync script uses HTTPS, not SSH
- Check git credentials: `gh auth status`

### "Standalone repo not found"
- Create standalone repo first
- Add to sync script mapping

### "Server not in DEPLOYED_SERVERS.md"
- Follow new server deployment flow
- Or add manually to tracking file

## Todo List Template

Use TodoWrite to create this list:

```
[ ] Validate server name and check tracking
[ ] Check for uncommitted changes
[ ] Sync to standalone repo
[ ] Verify FastMCP Cloud deployment
[ ] Provide testing instructions
[ ] Update tracking documentation
```

## Success Output

```
✅ Deployment Complete!

Server: ${SERVER_NAME}
Standalone Repo: https://github.com/vanman2024/${SERVER_NAME}
FastMCP Cloud: https://fastmcp.app

Endpoint: https://${SERVER_NAME}.fastmcp.app/mcp

Test it:
  mcp-inspector https://${SERVER_NAME}.fastmcp.app/mcp

Or use in Claude Desktop - add to config:
  {
    "mcpServers": {
      "${SERVER_NAME}": {
        "url": "https://${SERVER_NAME}.fastmcp.app/mcp",
        "transport": "http"
      }
    }
  }

Watch deployment: https://fastmcp.app
```

## Implementation Notes

- Always use TodoWrite for progress tracking
- Show sync script output (don't hide it)
- Verify sync completed before showing success
- Update DEPLOYED_SERVERS.md after every deployment
- Ask user to manually configure FastMCP Cloud (can't automate that yet)
