# Deployment Workflow - Dual-Repo Pattern

## Overview

This project uses a **dual-repo pattern** to balance development convenience with deployment requirements.

### The Problem

FastMCP Cloud requires each MCP server to be at the **root of its own GitHub repository**. However, we want to develop all servers together in a **monorepo** for easier management, shared tooling, and code reuse.

### The Solution

**Two types of repositories:**

1. **Development Monorepo** (this repo)
   - Contains all MCP servers in organized folders
   - Where you do all development work
   - Single place for issues, PRs, documentation
   - Repo: `mcp-servers-marketplace`

2. **Deployment Repos** (standalone repos)
   - One repository per deployed server
   - Server files at root level (no subdirectories)
   - Connected to FastMCP Cloud for auto-deployment
   - Example: `cats-mcp-server` standalone repo

The sync script bridges these two repos automatically.

---

## Daily Development Workflow

### Making Changes to a Deployed Server

```bash
# 1. Work in the monorepo
cd servers/business-productivity/cats-mcp-server/
vim server_all_tools.py
# ... make your changes ...

# 2. Test locally (optional but recommended)
python server_all_tools.py

# 3. Commit to monorepo
git add -A
git commit -m "feat: add new candidate search filters"
git push origin main

# 4. Sync to standalone repo (triggers deployment)
./scripts/sync-to-standalone.sh cats-mcp-server

# 5. FastMCP Cloud auto-deploys
# Watch deployment at https://fastmcp.app
```

**That's it!** The sync script handles:
- Cloning the standalone repo
- Copying updated files
- Committing with timestamp
- Pushing to trigger FastMCP Cloud deployment
- Cleanup

---

## What Gets Synced

The sync script copies everything **except**:
- `.git/` (preserves standalone repo's git history)
- `.archive/` (historical docs not needed in production)
- `__pycache__/`, `*.pyc` (Python cache files)
- `.pytest_cache/`, `.coverage` (test artifacts)
- `venv/` (virtual environments)
- `.env` (secrets stay local)

Everything else (code, docs, configs, tests) is synced exactly as-is.

---

## Tracking Deployed Servers

All deployed servers are tracked in:

**`DEPLOYED_SERVERS.md`** (repo root)
```markdown
### cats-mcp-server
- **Monorepo Path**: `servers/business-productivity/cats-mcp-server/`
- **Standalone Repo**: https://github.com/vanman2024/cats-mcp-server
- **FastMCP Cloud**: https://fastmcp.app (project: cats-mcp-server)
- **Status**: ✅ Active - 164 tools
- **Last Synced**: 2025-11-01
- **Sync Command**: `./scripts/sync-to-standalone.sh cats-mcp-server`
```

**Always update this file when:**
- Deploying a new server
- Changing standalone repo URLs
- Updating tool counts or status

---

## Deploying a New Server

### Step 1: Develop in Monorepo

Build your server in the appropriate category:
```
servers/
├── business-productivity/
├── ai-llm/
├── cloud-infrastructure/
├── content-media/
├── design-tools/
└── ... (your new server here)
```

### Step 2: Create Standalone Repo

```bash
# On GitHub, create new repo (e.g., "my-mcp-server")
# Don't initialize with README/license (we'll push from monorepo)
```

### Step 3: Add to Sync Script

Edit `scripts/sync-to-standalone.sh`:

```bash
case "$SERVER_NAME" in
    "cats-mcp-server")
        MONOREPO_PATH="servers/business-productivity/cats-mcp-server"
        STANDALONE_REPO="https://github.com/vanman2024/cats-mcp-server.git"
        STANDALONE_DIR="/tmp/cats-mcp-server-sync"
        ;;
    "my-new-server")  # ADD THIS
        MONOREPO_PATH="servers/category/my-new-server"
        STANDALONE_REPO="https://github.com/vanman2024/my-new-server.git"
        STANDALONE_DIR="/tmp/my-new-server-sync"
        ;;
    *)
        echo "❌ Unknown server: $SERVER_NAME"
        exit 1
        ;;
esac
```

### Step 4: Initial Sync

```bash
# First sync pushes everything to standalone repo
./scripts/sync-to-standalone.sh my-new-server
```

### Step 5: Connect to FastMCP Cloud

1. Go to https://fastmcp.app
2. Create new project
3. Connect to standalone repo: `https://github.com/vanman2024/my-new-server`
4. Set environment variables (e.g., API keys)
5. Deploy!

### Step 6: Update Tracking Doc

Add entry to `DEPLOYED_SERVERS.md`:

```markdown
### my-new-server
- **Monorepo Path**: `servers/category/my-new-server/`
- **Standalone Repo**: https://github.com/vanman2024/my-new-server
- **FastMCP Cloud**: https://fastmcp.app (project: my-new-server)
- **Status**: ✅ Active - X tools
- **Last Synced**: 2025-XX-XX
- **Sync Command**: `./scripts/sync-to-standalone.sh my-new-server`
```

---

## Troubleshooting

### "Permission denied (publickey)" Error

The sync script uses HTTPS (not SSH). If you see this error:
1. Check the URL in sync script uses `https://` not `git@`
2. Verify you're logged into GitHub CLI: `gh auth status`

### FastMCP Cloud Not Deploying

1. Check deployment logs at https://fastmcp.app
2. Verify `fastmcp.json` is present and valid
3. Check environment variables are set
4. Ensure standalone repo received the push: `git log` in standalone repo

### Sync Script Shows "No changes to sync"

This means monorepo and standalone repo are already in sync. This is normal if you:
- Haven't made changes since last sync
- Forgot to commit changes to monorepo first

Solution: Make sure to commit changes to monorepo before syncing.

### Files Not Syncing

Check if files are in the exclude list in `sync-to-standalone.sh`:
```bash
rsync -av --delete \
    --exclude='.git' \
    --exclude='.archive' \
    --exclude='__pycache__' \
    # ... etc
```

If a file pattern is excluded but shouldn't be, remove it from the script.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    DEVELOPMENT                           │
│                                                          │
│  mcp-servers-marketplace (monorepo)                     │
│  ├── servers/                                           │
│  │   ├── business-productivity/                        │
│  │   │   └── cats-mcp-server/  ◄─── You work here     │
│  │   ├── ai-llm/                                       │
│  │   └── ...                                            │
│  ├── scripts/sync-to-standalone.sh                     │
│  └── DEPLOYED_SERVERS.md                               │
└─────────────────────────────────────────────────────────┘
                           │
                           │ ./scripts/sync-to-standalone.sh
                           │ (automatic sync)
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    DEPLOYMENT                            │
│                                                          │
│  cats-mcp-server (standalone repo)                     │
│  ├── server_all_tools.py                               │
│  ├── toolsets_*.py                                      │
│  ├── fastmcp.json                                       │
│  └── docs/                                              │
│                                                          │
│  Connected to: FastMCP Cloud                            │
└─────────────────────────────────────────────────────────┘
                           │
                           │ Auto-deploy on push
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  PRODUCTION                              │
│                                                          │
│  FastMCP Cloud (https://fastmcp.app)                   │
│  ├── Builds Docker container                           │
│  ├── Runs server on HTTP                               │
│  └── Public endpoint: https://*.fastmcp.app/mcp        │
└─────────────────────────────────────────────────────────┘
```

---

## Best Practices

### ✅ Do This

- **Always commit to monorepo first**, then sync
- **Test locally** before syncing (if possible)
- **Update DEPLOYED_SERVERS.md** when deploying new servers
- **Use descriptive commit messages** (they appear in standalone repo)
- **Run sync after every meaningful change** (not every tiny commit)

### ❌ Don't Do This

- **Don't commit directly to standalone repos** (always go through monorepo)
- **Don't edit standalone repos manually** (sync will overwrite)
- **Don't skip updating DEPLOYED_SERVERS.md** (you'll forget what's deployed)
- **Don't sync secrets/credentials** (they should be in FastMCP Cloud env vars)

---

## Quick Reference

```bash
# Sync a deployed server
./scripts/sync-to-standalone.sh cats-mcp-server

# View deployed servers
cat DEPLOYED_SERVERS.md

# Check sync script mapping
grep -A 3 "cats-mcp-server" scripts/sync-to-standalone.sh

# View standalone repo without cloning
gh repo view vanman2024/cats-mcp-server --web
```

---

## Related Documentation

- **[DEPLOYED_SERVERS.md](../DEPLOYED_SERVERS.md)** - List of all deployed servers
- **[FASTMCP_CLOUD.md](FASTMCP_CLOUD.md)** - FastMCP Cloud deployment guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributing guidelines for new servers
