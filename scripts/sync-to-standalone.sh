#!/bin/bash
# Sync server from monorepo to standalone repo for FastMCP Cloud deployment

set -e

SERVER_NAME="$1"

if [ -z "$SERVER_NAME" ]; then
    echo "Usage: ./scripts/sync-to-standalone.sh <server-name>"
    echo "Example: ./scripts/sync-to-standalone.sh cats-mcp-server"
    exit 1
fi

# Map server name to paths
case "$SERVER_NAME" in
    "cats-mcp-server")
        MONOREPO_PATH="servers/business-productivity/cats-mcp-server"
        STANDALONE_REPO="https://github.com/vanman2024/cats-mcp-server.git"
        STANDALONE_DIR="/tmp/cats-mcp-server-sync"
        ;;
    *)
        echo "❌ Unknown server: $SERVER_NAME"
        echo "Add mapping in this script or DEPLOYED_SERVERS.md"
        exit 1
        ;;
esac

echo "🔄 Syncing $SERVER_NAME to standalone repo..."
echo "   Monorepo: $MONOREPO_PATH"
echo "   Standalone: $STANDALONE_REPO"
echo ""

# Clean up any previous sync directory
rm -rf "$STANDALONE_DIR"

# Clone standalone repo
echo "📥 Cloning standalone repo..."
git clone "$STANDALONE_REPO" "$STANDALONE_DIR"

# Copy files from monorepo to standalone (excluding git, archive, cache)
echo "📋 Copying files from monorepo..."
rsync -av --delete \
    --exclude='.git' \
    --exclude='.archive' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.pytest_cache' \
    --exclude='.coverage' \
    --exclude='venv' \
    --exclude='.env' \
    "$MONOREPO_PATH/" "$STANDALONE_DIR/"

# Navigate to standalone repo
cd "$STANDALONE_DIR"

# Check if there are changes
if git diff --quiet && git diff --staged --quiet; then
    echo "✅ No changes to sync"
    rm -rf "$STANDALONE_DIR"
    exit 0
fi

# Stage all changes
git add -A

# Show what changed
echo ""
echo "📝 Changes to be committed:"
git status --short

# Commit with timestamp
COMMIT_MSG="sync: Update from monorepo ($(date '+%Y-%m-%d %H:%M:%S'))"
git commit -m "$COMMIT_MSG"

# Push to main branch
echo ""
echo "🚀 Pushing to standalone repo..."
git push origin main

# Clean up
cd -
rm -rf "$STANDALONE_DIR"

echo ""
echo "✅ Sync complete!"
echo "   FastMCP Cloud will auto-deploy from: $STANDALONE_REPO"
