# Extracted MCP Servers

Tracking of servers extracted from monorepo to standalone GitHub repos for FastMCP Cloud deployment.

## Extracted & Ready for Deployment

### signalhire-mcp
- **Monorepo Path**: `servers/business-productivity/signalhire/`
- **Standalone Repo**: https://github.com/vanman2024/signalhire-mcp
- **FastMCP Cloud**: https://signalhire.fastmcp.app (deploying)
- **Status**: 🟡 Deploying to FastMCP Cloud (commit 0d48b69)
- **Capabilities**: 13 tools, 7 resources, 8 prompts
- **Extracted**: 2025-11-02
- **Last Synced**: 2025-11-02 16:36
- **Sync Command**: `./scripts/sync-to-standalone.sh signalhire-mcp`
- **Workflow**: ⚠️ Edit in monorepo ONLY, then sync to GitHub

### cats-mcp-server
- **Monorepo Path**: `servers/business-productivity/cats-mcp-server/`
- **Standalone Repo**: https://github.com/vanman2024/cats-mcp-server
- **Production Dir**: N/A
- **FastMCP Cloud**: https://fastmcp.app (project: cats-mcp-server)
- **Status**: ✅ Deployed & Active - 164 tools
- **Last Synced**: 2025-11-01
- **Sync Command**: `./scripts/sync-to-standalone.sh cats-mcp-server`

---

## Sync Workflow

When you make changes to a deployed server in the monorepo:

1. Make changes in monorepo: `servers/business-productivity/cats-mcp-server/`
2. Test locally
3. Commit to monorepo: `git commit -m "feat: ..."`
4. Sync to standalone repo: `./scripts/sync-to-standalone.sh cats-mcp-server`
5. FastMCP Cloud auto-deploys from standalone repo

## Adding New Deployments

When deploying a new server to FastMCP Cloud:

1. Create standalone repo on GitHub
2. Run: `./scripts/setup-standalone-repo.sh <server-path> <repo-url>`
3. Add entry to this file
4. Push to standalone repo
5. Connect to FastMCP Cloud
