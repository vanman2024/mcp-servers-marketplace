# Deployed MCP Servers

This file tracks all MCP servers deployed to FastMCP Cloud and other platforms.

## FastMCP Cloud Deployments

### SignalHire MCP Server
- **Status**: ✅ Active
- **Platform**: FastMCP Cloud
- **GitHub**: https://github.com/vanman2024/signalhire-mcp
- **Local**: `~/Projects/mcp-servers/business-productivity/signalhire-mcp/`
- **Deployed**: Auto-deploy from main branch
- **Environment Variables**: Set in FastMCP Cloud
  - `SIGNALHIRE_API_KEY`
  - `PORT`

### CATS MCP Server
- **Status**: ✅ Active
- **Platform**: FastMCP Cloud
- **GitHub**: https://github.com/vanman2024/cats-mcp-server
- **Local**: `~/Projects/mcp-servers/business-productivity/cats-mcp-server/`
- **Deployed**: Auto-deploy from main branch
- **Environment Variables**: Set in FastMCP Cloud
  - `CATS_API_KEY`
  - `PORT`

### Multi-Lead MCP Server
- **Status**: 🔧 Configured (Ready for deployment)
- **Platform**: FastMCP Cloud
- **GitHub**: https://github.com/vanman2024/multilead-mcp
- **Local**: `~/Projects/mcp-servers/multilead-mcp/`
- **Server Entrypoint**: `server.py:mcp`
- **Deployed**: Auto-deploy from master branch
- **Deployment URL**: https://multilead-mcp.fastmcp.app/mcp (when deployed)
- **Health Check**: https://multilead-mcp.fastmcp.app/health (when deployed)
- **Environment Variables**: Set in FastMCP Cloud dashboard
  - `MULTILEAD_API_KEY` (required) - Get from https://app.multilead.co/settings/api
  - `TRANSPORT=http` (optional)
  - `LOG_LEVEL=INFO` (optional)
  - `LOG_FORMAT=json` (optional)
  - `RATE_LIMIT_PER_MINUTE=100` (optional)
  - `RATE_LIMIT_PER_HOUR=1000` (optional)
- **Capabilities**: 77 tools, 2 resources, 2 prompts
- **Tests**: ✅ 82 passing tests
- **Documentation**:
  - Quick Start: `FASTMCP_CLOUD_QUICK_START.md`
  - Complete Guide: `docs/deployment/FASTMCP_CLOUD_DEPLOYMENT.md`
  - Status: `DEPLOYMENT_STATUS.md`

## DigitalOcean Droplet Deployments

### SignalHire Callback Server
- **Status**: ✅ Active (running 4+ days)
- **Platform**: DigitalOcean Droplet
- **IP**: 137.184.196.101:8000
- **Local**: `~/Projects/mcp-servers/business-productivity/signalhire-mcp/`
- **Service**: systemd (`signalhire-callback`)
- **Environment Variables**: `/etc/signalhire/.env` (600 permissions)
  - `SIGNALHIRE_API_KEY` - **NEEDS ROTATION** (key exposed on 2025-11-02)
  - `PORT=8000`
- **Deployed**: Manual via `deploy-to-droplet.sh`
- **Logs**: `journalctl -u signalhire-callback -f`

## Deployment Commands

### FastMCP Cloud
```bash
# Servers auto-deploy when pushed to GitHub

# SignalHire MCP
cd ~/Projects/mcp-servers/business-productivity/signalhire-mcp
git push

# CATS MCP
cd ~/Projects/mcp-servers/business-productivity/cats-mcp-server
git push

# Multi-Lead MCP
cd ~/Projects/mcp-servers/multilead-mcp
git push

# FastMCP Cloud pulls latest and redeploys automatically
```

### DigitalOcean Droplet
```bash
# Deploy SignalHire callback server
deploy-to-droplet.sh ~/Projects/mcp-servers/business-productivity/signalhire-mcp 137.184.196.101 signalhire-callback

# Update secrets only
update-secrets.sh 137.184.196.101 signalhire-callback

# Check status
doctl compute ssh 137.184.196.101 --ssh-command 'systemctl status signalhire-callback'

# View logs
doctl compute ssh 137.184.196.101 --ssh-command 'journalctl -u signalhire-callback -n 50'
```

## Pending Actions

### Security
- [ ] **URGENT**: Rotate SignalHire API key (exposed key: `202.R6cmAKCaf7FHPPstzfP2Vnh5XOBo`)
  1. Generate new key in SignalHire dashboard
  2. Update FastMCP Cloud environment variables
  3. Update droplet: `ENV_FILE=.env.production update-secrets.sh 137.184.196.101 signalhire-callback`
  4. Verify both deployments working
  5. Revoke old key

### Planned Deployments
- [x] ~~Multi-Lead MCP server~~ - ✅ Configured and ready for FastMCP Cloud deployment
- [ ] CATS callback server (if needed)
- [ ] Ayrshare MCP server
- [ ] Google Workspace MCP server

## Notes

- **FastMCP Cloud**: Easiest deployment method, preferred for MCP servers
- **DigitalOcean Droplets**: Used for apps requiring custom server configuration (callbacks, webhooks, etc.)
- **No App Platform**: Not using DigitalOcean App Platform - only droplets and FastMCP Cloud

---

*Last Updated: 2025-11-07*
*Auto-managed by deployment scripts*
