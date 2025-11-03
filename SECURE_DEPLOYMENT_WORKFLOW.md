# Secure Deployment Workflow

**CRITICAL: Never hardcode API keys or secrets in files!**

This guide explains the secure deployment workflow to prevent API key exposure.

## Overview

```
┌──────────────────────────────────────────────────────────┐
│  Single Source of Truth: MONOREPO ONLY                   │
│  ~/.claude/plugins/marketplaces/mcp-servers-marketplace/ │
└──────────────────────────────────────────────────────────┘
                           ↓
        ┌─────────────────────────────────────┐
        │  Secure Sync with Secret Scanning   │
        │  ./scripts/sync-to-standalone-      │
        │          secure.sh                   │
        └─────────────────────────────────────┘
                           ↓
        ┌─────────────────────────────────────┐
        │  GitHub Repository                   │
        │  (with GitHub Secrets)               │
        └─────────────────────────────────────┘
                           ↓
        ┌─────────────────────────────────────┐
        │  FastMCP Cloud Auto-Deploy           │
        └─────────────────────────────────────┘
```

## Key Principles

1. **❌ NEVER** hardcode API keys in YAML/config files
2. **❌ NEVER** edit in `~/Projects/` directories
3. **❌ NEVER** commit `.env` files
4. **✅ ALWAYS** edit in monorepo only
5. **✅ ALWAYS** use GitHub Secrets for sensitive values
6. **✅ ALWAYS** use the secure sync script

## Step-by-Step Workflow

### 1. Edit Code in Monorepo

```bash
cd ~/.claude/plugins/marketplaces/mcp-servers-marketplace/
cd servers/business-productivity/signalhire/

# Edit your server code
vim server.py
```

### 2. Store Secrets Locally (Never Commit!)

Create `.env` file in your server directory:

```bash
# servers/business-productivity/signalhire/.env
SIGNALHIRE_API_KEY=202.R6cmAKCaf7FHPPstzfP2Vnh5XOBo
EXTERNAL_CALLBACK_URL=http://137.184.196.101:8000/signalhire/callback
```

**.env is gitignored - it will NEVER be synced to GitHub!**

### 3. Upload Secrets to GitHub

Use the secrets management script:

```bash
# Upload all secrets from .env file
./scripts/manage-github-secrets.sh set-from-env signalhire-mcp \
  servers/business-productivity/signalhire/.env

# Or set individual secrets
./scripts/manage-github-secrets.sh set signalhire-mcp \
  SIGNALHIRE_API_KEY "your-key-here"

# List all secrets for verification
./scripts/manage-github-secrets.sh list signalhire-mcp
```

### 4. Reference Secrets in YAML Files

**❌ WRONG (WILL BE BLOCKED):**
```yaml
envs:
  - key: SIGNALHIRE_API_KEY
    value: "202.R6cmAKCaf7FHPPstzfP2Vnh5XOBo"  # NEVER DO THIS
```

**✅ CORRECT:**
```yaml
envs:
  - key: SIGNALHIRE_API_KEY
    value: ${{ secrets.SIGNALHIRE_API_KEY }}
```

### 5. Sync to GitHub (Secure)

```bash
# Use the SECURE sync script
./scripts/sync-to-standalone-secure.sh signalhire-mcp
```

**What this script does:**
- ✅ Creates temp clone in `/tmp/` (not `~/Projects/`)
- ✅ Installs git hooks in temp clone
- ✅ Copies files (excludes `.env`)
- ✅ **Scans ALL files for secrets**
- ✅ **BLOCKS push if any secrets found**
- ✅ Pushes to GitHub if clean
- ✅ Deletes temp clone

**If secrets are detected:**
```
❌ SYNC BLOCKED: Secrets detected in files!

Files with potential secrets will NOT be synced to GitHub.

Solutions:
1. Remove hardcoded secrets from YAML/config files
2. Use GitHub Secrets instead:
   gh secret set SECRET_NAME -b"secret-value" -R vanman2024/signalhire-mcp
3. Update files to reference secrets:
   value: ${{ secrets.SECRET_NAME }}
```

### 6. Auto-Deployment

- GitHub repo gets updated
- FastMCP Cloud auto-deploys
- Environment variables come from GitHub Secrets
- Your server is live with secure configuration!

## Quick Reference Commands

### Secrets Management

```bash
# List secrets
./scripts/manage-github-secrets.sh list signalhire-mcp

# Set from .env
./scripts/manage-github-secrets.sh set-from-env signalhire-mcp path/to/.env

# Set individual secret
./scripts/manage-github-secrets.sh set signalhire-mcp SECRET_NAME "value"

# Delete secret
./scripts/manage-github-secrets.sh delete signalhire-mcp SECRET_NAME
```

### Secure Sync

```bash
# Sync with secret scanning
./scripts/sync-to-standalone-secure.sh signalhire-mcp

# Check what's deployed
cat DEPLOYED_SERVERS.md
```

### Git Hooks (Automatic)

The post-commit hook automatically:
- Detects changed servers
- Runs secure sync with secret scanning
- Updates DEPLOYED_SERVERS.md
- Blocks if secrets detected

## What Gets Synced vs Excluded

### ✅ Synced to GitHub:
- Source code (`*.py`, `*.ts`)
- Configuration templates (`.env.example`)
- Documentation (`README.md`, `docs/`)
- YAML files (with `${{ secrets.* }}` references)
- Requirements/dependencies

### ❌ Excluded (Never Synced):
- `.env` (actual secrets)
- `.env.local`
- `.env.*.local`
- `__pycache__/`, `*.pyc`
- `venv/`
- `.git/` (monorepo git stays separate)

## Troubleshooting

### "Secrets detected in files"

1. Find the file mentioned in error
2. Remove hardcoded value
3. Upload to GitHub Secrets:
   ```bash
   ./scripts/manage-github-secrets.sh set server-name SECRET_NAME "value"
   ```
4. Update file to use `${{ secrets.SECRET_NAME }}`
5. Try sync again

### "No such server"

Add mapping to `scripts/sync-to-standalone-secure.sh`:
```bash
case "$SERVER_NAME" in
    "your-server")
        MONOREPO_PATH="servers/category/your-server"
        STANDALONE_REPO="https://github.com/username/your-server.git"
        STANDALONE_DIR="/tmp/your-server-sync"
        REPO_NAME="your-server"
        ;;
```

### Verify No Persistent Directories

```bash
# Should return empty or only legitimate projects
ls ~/Projects/ | grep -E "(mcp|production)"
```

If you see `*-production/` directories, they're leftovers - delete them:
```bash
trash-put ~/Projects/server-name-production
```

## Security Best Practices

1. **Never commit secrets** - Use `.env` files (gitignored)
2. **Always use GitHub Secrets** - For all sensitive values
3. **Run secure sync** - Let it scan for secrets
4. **Verify on GitHub** - Check repo has no exposed keys
5. **Rotate exposed keys** - If accidentally committed
6. **Use `.env.example`** - Template with dummy values

## Migration from Old Workflow

If you were using the old `sync-to-standalone.sh`:

1. Upload existing secrets to GitHub:
   ```bash
   ./scripts/manage-github-secrets.sh set-from-env server-name path/to/.env
   ```

2. Update all YAML files to use `${{ secrets.* }}`

3. Switch to secure script:
   ```bash
   ./scripts/sync-to-standalone-secure.sh server-name
   ```

4. Delete any `~/Projects/*-production/` directories

5. Update git hooks to use secure script (already done if you pulled latest)

## Summary

**The Golden Rule:** Edit in monorepo ONLY, use GitHub Secrets, sync with secret scanning.

This prevents API key exposure and keeps your deployment workflow secure and simple.
