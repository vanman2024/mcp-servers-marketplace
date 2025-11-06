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
cd ~/Projects/mcp-servers/business-productivity/signalhire-mcp
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
- [ ] CATS callback server (if needed)
- [ ] Ayrshare MCP server
- [ ] Google Workspace MCP server

## Notes

- **FastMCP Cloud**: Easiest deployment method, preferred for MCP servers
- **DigitalOcean Droplets**: Used for apps requiring custom server configuration (callbacks, webhooks, etc.)
- **No App Platform**: Not using DigitalOcean App Platform - only droplets and FastMCP Cloud

---

*Last Updated: 2025-11-02*
*Auto-managed by deployment scripts*
