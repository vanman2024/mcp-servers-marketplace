# FastMCP Cloud Deployment Guide

Complete guide for deploying MCP servers to FastMCP Cloud managed hosting.

## What is FastMCP Cloud?

FastMCP Cloud (https://fastmcp.app) is a managed hosting platform specifically designed for FastMCP servers.

**Benefits:**
- ✅ **Automatic deployments** - Push to GitHub → Auto-deploy
- ✅ **Managed infrastructure** - No servers to manage
- ✅ **Environment variables** - Secure storage for API keys
- ✅ **HTTP endpoints** - Public URL for your MCP server
- ✅ **Preview deployments** - Pull requests get preview URLs
- ✅ **Custom domains** - Use your own domain (optional)
- ✅ **Zero config** - Works with `fastmcp.json`

**Cost:** Free tier available, see https://fastmcp.app/pricing

---

## Prerequisites

Before deploying to FastMCP Cloud:

1. **FastMCP server** - Working MCP server using FastMCP framework
2. **GitHub account** - Server must be in a GitHub repo
3. **FastMCP Cloud account** - Sign up at https://fastmcp.app
4. **fastmcp.json** - Deployment manifest in repo root

---

## Quick Start

### 1. Create `fastmcp.json`

In your server's root directory:

```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",
  "source": {
    "type": "filesystem",
    "path": "server_all_tools.py",
    "entrypoint": "mcp"
  },
  "environment": {
    "type": "uv",
    "python": ">=3.10",
    "dependencies": [
      "fastmcp>=2.0.0",
      "httpx>=0.27.0",
      "python-dotenv>=1.0.0"
    ]
  },
  "deployment": {
    "transport": "http",
    "host": "0.0.0.0",
    "port": 3000,
    "path": "/mcp/",
    "log_level": "INFO",
    "env": {
      "API_KEY": "${API_KEY}"
    }
  }
}
```

### 2. Push to GitHub

```bash
git add fastmcp.json
git commit -m "feat: add FastMCP Cloud config"
git push origin main
```

### 3. Connect to FastMCP Cloud

1. Go to https://fastmcp.app
2. Sign in with GitHub
3. Click **"New Project"**
4. Select your repository
5. FastMCP Cloud auto-detects `fastmcp.json`
6. Click **"Deploy"**

### 4. Set Environment Variables

In FastMCP Cloud dashboard:
1. Go to **Settings → Environment Variables**
2. Add your secrets (e.g., `API_KEY`)
3. Click **"Save"**
4. Redeploy if needed

### 5. Access Your Server

Your server is now live at:
```
https://your-project-name.fastmcp.app/mcp
```

---

## fastmcp.json Configuration

### Full Schema

```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",

  "source": {
    "type": "filesystem",           // or "package"
    "path": "server.py",            // Main server file
    "entrypoint": "mcp"             // FastMCP instance variable name
  },

  "environment": {
    "type": "uv",                   // Python package manager
    "python": ">=3.10",             // Python version requirement
    "dependencies": [               // Python packages
      "fastmcp>=2.0.0",
      "httpx>=0.27.0"
    ]
  },

  "deployment": {
    "transport": "http",            // Transport mode
    "host": "0.0.0.0",             // Bind host
    "port": 3000,                   // Port (3000 is standard)
    "path": "/mcp/",               // URL path
    "log_level": "INFO",           // DEBUG, INFO, WARNING, ERROR
    "env": {                        // Environment variables
      "API_KEY": "${API_KEY}",     // Reference from FastMCP Cloud settings
      "BASE_URL": "https://api.example.com"
    }
  }
}
```

### Source Types

**Filesystem** (most common):
```json
"source": {
  "type": "filesystem",
  "path": "server.py",
  "entrypoint": "mcp"
}
```

**Package** (for published packages):
```json
"source": {
  "type": "package",
  "package": "my-mcp-server",
  "entrypoint": "mcp"
}
```

### Environment Types

**uv** (recommended - fastest):
```json
"environment": {
  "type": "uv",
  "python": ">=3.10"
}
```

**pip** (traditional):
```json
"environment": {
  "type": "pip",
  "python": "3.10"
}
```

---

## Environment Variables

### Setting Secrets

Secrets (API keys, tokens) should **never** be in code or `fastmcp.json`.

**In FastMCP Cloud:**
1. Project → Settings → Environment Variables
2. Add variable: `CATS_API_KEY` = `your_secret_key_here`
3. Save

**In fastmcp.json:**
```json
"env": {
  "CATS_API_KEY": "${CATS_API_KEY}"  // References FastMCP Cloud setting
}
```

**In your server code:**
```python
import os
CATS_API_KEY = os.getenv("CATS_API_KEY")
```

### Common Environment Variables

```json
"env": {
  // API Keys
  "API_KEY": "${API_KEY}",
  "OPENAI_API_KEY": "${OPENAI_API_KEY}",

  // Base URLs
  "API_BASE_URL": "https://api.example.com/v3",

  // Feature flags
  "ENABLE_CACHING": "true",
  "DEBUG_MODE": "false",

  // Configuration
  "MAX_RETRIES": "3",
  "TIMEOUT_SECONDS": "30"
}
```

---

## Deployment Process

### What Happens When You Deploy

1. **GitHub webhook triggered** - Push to main branch or PR
2. **Clone repository** - FastMCP Cloud clones your repo
3. **Read fastmcp.json** - Parse configuration
4. **Install dependencies** - Using uv or pip
5. **Build Docker image** - Container with your server
6. **Start server** - Run on HTTP at specified port
7. **Health check** - Verify server responds
8. **Route traffic** - Public URL goes live

**Build time:** Usually 1-3 minutes

### Viewing Logs

FastMCP Cloud dashboard:
1. Project → **Deployments**
2. Click on deployment
3. View **Build Logs** and **Runtime Logs**

### Deployment Status

- 🟡 **Building** - Installing dependencies, building image
- 🟢 **Live** - Deployed and serving traffic
- 🔴 **Failed** - Build or runtime error (check logs)
- 🟠 **Suspended** - Manually stopped

---

## Automatic Deployments

### Main Branch

Every push to `main` triggers deployment:

```bash
git commit -m "feat: add new tools"
git push origin main
# ➡️ FastMCP Cloud auto-deploys
```

### Pull Request Previews

Every PR gets a preview URL:

```bash
git checkout -b feature/new-tools
# ... make changes ...
git push origin feature/new-tools
# ➡️ Create PR on GitHub
# ➡️ FastMCP Cloud deploys to preview URL
```

Preview URL: `https://your-project-name-pr-123.fastmcp.app/mcp`

---

## Troubleshooting

### Build Failures

**Dependency errors:**
```
ERROR: Could not find a version that satisfies the requirement fastmcp>=2.0.0
```

**Fix:** Check `fastmcp.json` dependencies match your `requirements.txt`

**Python version errors:**
```
ERROR: Python 3.9 found, but >=3.10 required
```

**Fix:** Update `environment.python` in `fastmcp.json`

### Runtime Errors

**Server not starting:**
```
ERROR: No module named 'mcp'
```

**Fix:** Check `source.entrypoint` matches your FastMCP instance variable name

**Import errors:**
```
ModuleNotFoundError: No module named 'httpx'
```

**Fix:** Add missing dependency to `environment.dependencies`

### Environment Variable Issues

**Variable not found:**
```python
CATS_API_KEY = os.getenv("CATS_API_KEY")  # Returns None
```

**Fix:**
1. Check variable is set in FastMCP Cloud settings
2. Check `env` section in `fastmcp.json` references it: `"CATS_API_KEY": "${CATS_API_KEY}"`
3. Redeploy after adding variables

### Connection Issues

**504 Gateway Timeout:**
- Server taking too long to respond
- Check for blocking operations in tool functions
- Add timeout limits to HTTP requests

**502 Bad Gateway:**
- Server crashed or not running
- Check runtime logs for errors
- Verify `port` in `fastmcp.json` matches server binding

---

## Best Practices

### ✅ Do This

- **Use uv** for faster builds (vs pip)
- **Keep dependencies minimal** (faster builds, smaller images)
- **Set proper log levels** (INFO for production, DEBUG for development)
- **Use environment variables** for all secrets
- **Test locally first** with same `fastmcp.json`
- **Monitor logs** after deployment
- **Version your dependencies** (e.g., `fastmcp==2.1.0` not `fastmcp>=2.0.0`)

### ❌ Don't Do This

- **Don't commit secrets** to `fastmcp.json` or code
- **Don't use blocking operations** in tool functions (use async)
- **Don't ignore build warnings** (they may cause runtime issues)
- **Don't skip testing** before deploying
- **Don't use development dependencies** in production

---

## Advanced Configuration

### Custom Domains

In FastMCP Cloud:
1. Settings → Domains
2. Add custom domain: `api.example.com`
3. Add DNS record: `CNAME api your-project.fastmcp.app`
4. Wait for SSL certificate provisioning

### Health Check Endpoints

FastMCP automatically provides:
- `/health` - Health check (200 if server is up)
- `/mcp/` - MCP endpoint

### CORS Configuration

For browser-based clients:

```python
from fastmcp import FastMCP

mcp = FastMCP("My Server")

# Add CORS middleware if needed
# (FastMCP Cloud handles this automatically for standard use cases)
```

### Rate Limiting

Implement in your server code:

```python
from fastmcp import FastMCP
import time
from collections import defaultdict

mcp = FastMCP("My Server")

# Simple rate limiter
rate_limit = defaultdict(list)
RATE_LIMIT = 100  # requests per minute

@mcp.tool()
def my_tool():
    client_ip = "..." # Get from request context
    now = time.time()
    rate_limit[client_ip] = [t for t in rate_limit[client_ip] if now - t < 60]

    if len(rate_limit[client_ip]) >= RATE_LIMIT:
        raise Exception("Rate limit exceeded")

    rate_limit[client_ip].append(now)
    # ... tool logic
```

---

## Migration from Other Platforms

### From Heroku

1. Keep same `requirements.txt`
2. Create `fastmcp.json` with your server config
3. Set environment variables in FastMCP Cloud
4. Deploy to FastMCP Cloud
5. Update DNS to point to new URL

### From Docker/Self-Hosted

1. Your server already works with FastMCP
2. Create `fastmcp.json` based on your Docker config
3. Push to GitHub
4. Deploy to FastMCP Cloud
5. Migrate environment variables

---

## Support

- **Documentation**: https://gofastmcp.com/docs
- **Discord**: https://discord.gg/fastmcp
- **GitHub Issues**: https://github.com/jlowin/fastmcp/issues
- **Email**: support@fastmcp.app

---

## Related Documentation

- **[DEPLOYMENT_WORKFLOW.md](DEPLOYMENT_WORKFLOW.md)** - Dual-repo development workflow
- **[DEPLOYED_SERVERS.md](../DEPLOYED_SERVERS.md)** - List of deployed servers
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Adding new servers
