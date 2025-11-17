  # Airtable MCP Sync - FastMCP Data Mapping

**Automatic sync of all MCP server configurations from Airtable to GitHub**

## What This Syncs

✅ **All MCP Servers** from Airtable MCP Servers table
✅ **FastMCP plugins** from Plugins table
✅ **Server configurations** (.mcp.json compatible)
✅ **Deployment metadata** (STDIO, HTTP, FastMCP Cloud)
✅ **Environment variables** and connection details
✅ **Available tools** and agent relationships

## Output Structure

```
airtable-mcp-sync/
├── servers/                          # Markdown for each MCP server
│   ├── supabase.md
│   ├── github.md
│   ├── postman.md
│   └── ...
├── plugins/                          # FastMCP plugin data
│   └── fastmcp-plugins.json
├── configs/                          # Ready-to-use .mcp.json configs
│   ├── stdio-servers.mcp.json       # npx/Python servers
│   ├── http-servers.mcp.json        # HTTP/local servers
│   └── fastmcp-cloud-servers.json   # Cloud-deployed servers
├── mcp-servers.json                  # Full table export
└── MCP-SYNC-REPORT.md               # Summary statistics
```

## Quick Setup (3 Steps)

### Step 1: Get Airtable Token
1. https://airtable.com/create/tokens
2. Scopes: `data.records:read` + `schema.bases:read`
3. Grant access to: **Claude Plugins** (`appHbSB7WhT1TxEQb`)
4. Copy token

### Step 2: Add GitHub Secrets
GitHub → **Settings** → **Secrets** → Add:
- `AIRTABLE_TOKEN` = your token
- `AIRTABLE_BASE_ID` = `appHbSB7WhT1TxEQb`

### Step 3: Enable Workflow Permissions
GitHub → **Settings** → **Actions** → **General**
- Select "Read and write permissions"
- Save

## Run the Sync

### Manual Trigger
1. **Actions** tab → **"Sync Airtable MCP Data to GitHub"**
2. **Run workflow** → **Run workflow**
3. Wait ~30 seconds
4. Check commit for synced files

### Automatic Schedule
- Runs **every hour** automatically
- Only commits when data changes

## Generated Configuration Files

### STDIO Servers Config (`stdio-servers.mcp.json`)

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-supabase"],
      "env": {
        "SUPABASE_URL": "${SUPABASE_URL}",
        "SUPABASE_ANON_KEY": "${SUPABASE_ANON_KEY}"
      }
    }
  }
}
```

### HTTP Servers Config (`http-servers.mcp.json`)

```json
{
  "mcpServers": {
    "figma": {
      "type": "http",
      "url": "http://localhost:8031",
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_ACCESS_TOKEN}"
      }
    }
  }
}
```

### FastMCP Cloud Servers (`fastmcp-cloud-servers.json`)

```json
[
  {
    "name": "My FastMCP Server",
    "url": "https://my-server.fastmcp.cloud",
    "status": "Deployed",
    "description": "Production MCP server"
  }
]
```

## Server Markdown Example

Each server gets a comprehensive markdown file:

```markdown
# Supabase

## Overview

**Description**: Database and backend platform with built-in auth, storage, and realtime

**Purpose**: Database operations, auth management, and backend services

## Configuration

| Property | Value |
|----------|-------|
| **Server Type** | HTTP (Remote) |
| **Deployment Method** | External Service |
| **FastMCP Cloud Status** | N/A (External) |
| **Agent Count** | 15 |

## Connection Details

**Connection URL**: `https://mcp.supabase.com/mcp`

## Environment Variables

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
```

## Available Tools

- list_tables
- execute_sql
- apply_migration
- generate_types
```

## Use Cases

### 1. Copy MCP Server Config

```bash
# Copy STDIO servers to your project
cp airtable-mcp-sync/configs/stdio-servers.mcp.json .mcp.json
```

### 2. Reference Server Details

```bash
# Check Supabase server configuration
cat airtable-mcp-sync/servers/supabase.md
```

### 3. Audit Deployments

```bash
# See which servers are deployed to FastMCP Cloud
cat airtable-mcp-sync/configs/fastmcp-cloud-servers.json | jq '.'
```

### 4. Generate Documentation

Use the synced data to auto-generate:
- Server catalogs
- Configuration guides
- Deployment manifests

## What Gets Mapped

For each MCP server:
- ✅ Name and description
- ✅ Server type (STDIO/HTTP/Cloud)
- ✅ Deployment method (npx/Python/HTTP/External)
- ✅ Connection details (URLs, commands, ports)
- ✅ Environment variables
- ✅ Available tools
- ✅ Security notes
- ✅ Agent relationships
- ✅ FastMCP Cloud deployment status

## Integration Examples

### Use in Scripts

```python
import json

# Load all servers
with open('airtable-mcp-sync/mcp-servers.json') as f:
    servers = json.load(f)

# Filter STDIO servers
stdio = [s for s in servers
         if s['fields'].get('Deployment Method') == 'npx']

# Generate .mcp.json
config = {"mcpServers": {}}
for server in stdio:
    name = server['fields']['MCP Server Name'].lower()
    config["mcpServers"][name] = {
        "command": "npx",
        "args": ["-y", server['fields']['Package/Source']]
    }
```

### Use in CI/CD

```yaml
# .github/workflows/deploy.yml
- name: Sync latest MCP configs
  run: |
    # Pull latest sync data
    git pull origin main

    # Copy production configs
    cp airtable-mcp-sync/configs/http-servers.mcp.json .mcp.json

    # Deploy with configs
    ./deploy.sh
```

## Customization

### Change Sync Frequency

Edit `.github/workflows/sync-airtable-mcp.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  - cron: '0 0 * * *'    # Daily at midnight
```

### Filter Servers

Edit `scripts/sync-airtable-mcp.py`:

```python
# Only sync production servers
production_servers = [
    s for s in servers_data
    if s['fields'].get('Status') == 'Production'
]
```

## Monitoring

Check sync status:
1. **Actions** tab → **Sync Airtable MCP Data**
2. View recent runs and logs
3. Check `MCP-SYNC-REPORT.md` for stats

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No commits | Data hasn't changed (normal) |
| Token error | Add AIRTABLE_TOKEN secret |
| Permission denied | Enable workflow write permissions |
| Missing servers | Check Airtable table filtering |

---

**Ready to use!** Your MCP server configurations are now automatically mapped from Airtable to GitHub. 🚀
