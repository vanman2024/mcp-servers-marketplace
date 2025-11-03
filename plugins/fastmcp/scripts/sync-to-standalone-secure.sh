#!/bin/bash
# Secure sync: Server from monorepo to standalone repo with secret scanning
# This prevents API keys and secrets from being pushed to GitHub

set -e

SERVER_NAME="$1"

if [ -z "$SERVER_NAME" ]; then
    echo "Usage: ./scripts/sync-to-standalone-secure.sh <server-name>"
    echo "Example: ./scripts/sync-to-standalone-secure.sh cats-mcp-server"
    exit 1
fi

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Map server name to paths
case "$SERVER_NAME" in
    "signalhire-mcp")
        MONOREPO_PATH="servers/business-productivity/signalhire"
        STANDALONE_REPO="https://github.com/vanman2024/signalhire-mcp.git"
        STANDALONE_DIR="/tmp/signalhire-mcp-sync"
        REPO_NAME="signalhire-mcp"
        ;;
    "cats-mcp-server")
        MONOREPO_PATH="servers/business-productivity/cats-mcp-server"
        STANDALONE_REPO="https://github.com/vanman2024/cats-mcp-server.git"
        STANDALONE_DIR="/tmp/cats-mcp-server-sync"
        REPO_NAME="cats-mcp-server"
        ;;
    *)
        echo -e "${RED}❌ Unknown server: $SERVER_NAME${NC}"
        echo "Add mapping in this script or DEPLOYED_SERVERS.md"
        exit 1
        ;;
esac

echo -e "${BLUE}🔄 Syncing $SERVER_NAME to standalone repo...${NC}"
echo "   Monorepo: $MONOREPO_PATH"
echo "   Standalone: $STANDALONE_REPO"
echo ""

# Clean up any previous sync directory
rm -rf "$STANDALONE_DIR"

# Clone standalone repo
echo -e "${BLUE}📥 Cloning standalone repo...${NC}"
git clone "$STANDALONE_REPO" "$STANDALONE_DIR"

# Install git hooks in the temp clone for secret scanning
echo -e "${BLUE}🔐 Installing security hooks in temp clone...${NC}"
MONOREPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$STANDALONE_DIR/.git/hooks"
cp "$MONOREPO_ROOT/.git/hooks/pre-commit" "$STANDALONE_DIR/.git/hooks/"
cp "$MONOREPO_ROOT/.git/hooks/pre-push" "$STANDALONE_DIR/.git/hooks/"
chmod +x "$STANDALONE_DIR/.git/hooks/"*

# Copy files from monorepo to standalone (excluding git, archive, cache, secrets)
echo -e "${BLUE}📋 Copying files from monorepo...${NC}"
rsync -av --delete \
    --exclude='.git' \
    --exclude='.archive' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.pytest_cache' \
    --exclude='.coverage' \
    --exclude='venv' \
    --exclude='.env' \
    --exclude='.env.local' \
    --exclude='.env.*.local' \
    "$MONOREPO_ROOT/$MONOREPO_PATH/" "$STANDALONE_DIR/"

# Navigate to standalone repo
cd "$STANDALONE_DIR"

# Check if there are changes
if git diff --quiet && git diff --staged --quiet; then
    echo -e "${GREEN}✅ No changes to sync${NC}"
    rm -rf "$STANDALONE_DIR"
    exit 0
fi

# Stage all changes
git add -A

# Show what changed
echo ""
echo -e "${YELLOW}📝 Changes to be committed:${NC}"
git status --short

# Manual secret scan before commit (additional layer)
echo ""
echo -e "${BLUE}🔍 Scanning for secrets in changed files...${NC}"

FOUND_SECRETS=0
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

# Secret patterns (matching pre-commit hook)
declare -a PATTERNS=(
  "AKIA[0-9A-Z]{16}"
  "api[_-]?key['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9]{20,}"
  "sk-[a-zA-Z0-9]{32,}"
  "sk-ant-[a-zA-Z0-9\-_]{95,}"
  "ctx7-[a-zA-Z0-9]{32,}"
  "Bearer [a-zA-Z0-9_\-\.]{20,}"
  "password['\"]?\s*[:=]\s*['\"]?[^ '\"]+"
  "secret['\"]?\s*[:=]\s*['\"]?[^ '\"]+"
  "token['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9]{20,}"
  "-----BEGIN (RSA |DSA )?PRIVATE KEY-----"
  "postgres://[^ '\"]*:[^ '\"]*@"
  "mongodb(\+srv)?://[^ '\"]*:[^ '\"]*@"
  "value:\s*['\"]?[0-9]{3}\.[a-zA-Z0-9]{20,}['\"]?"
)

for file in $STAGED_FILES; do
  # Skip binary files
  if file "$file" 2>/dev/null | grep -q "binary"; then
    continue
  fi

  # Skip safe files
  if [[ "$file" == "package-lock.json" ]] || [[ "$file" == "yarn.lock" ]]; then
    continue
  fi

  for pattern in "${PATTERNS[@]}"; do
    if grep -qE "$pattern" "$file" 2>/dev/null; then
      echo -e "${RED}✗ Potential secret found in: $file${NC}"
      echo -e "${YELLOW}  Pattern: $pattern${NC}"
      FOUND_SECRETS=1
    fi
  done
done

if [ $FOUND_SECRETS -eq 1 ]; then
  echo ""
  echo -e "${RED}❌ SYNC BLOCKED: Secrets detected in files!${NC}"
  echo ""
  echo "Files with potential secrets will NOT be synced to GitHub."
  echo ""
  echo "Solutions:"
  echo "1. Remove hardcoded secrets from YAML/config files"
  echo "2. Use GitHub Secrets instead:"
  echo "   ${BLUE}gh secret set SECRET_NAME -b\"secret-value\" -R vanman2024/$REPO_NAME${NC}"
  echo "3. Update files to reference secrets:"
  echo "   ${YELLOW}value: \${{ secrets.SECRET_NAME }}${NC}"
  echo ""

  # Clean up
  cd - > /dev/null
  rm -rf "$STANDALONE_DIR"
  exit 1
fi

echo -e "${GREEN}✓ No secrets detected${NC}"

# Commit with timestamp
COMMIT_MSG="sync: Update from monorepo ($(date '+%Y-%m-%d %H:%M:%S'))"
echo ""
echo -e "${BLUE}💾 Committing changes...${NC}"
git commit -m "$COMMIT_MSG"

# Push to main branch (pre-push hook will run here too)
echo ""
echo -e "${BLUE}🚀 Pushing to standalone repo...${NC}"
git push origin main

# Clean up
cd - > /dev/null
rm -rf "$STANDALONE_DIR"

echo ""
echo -e "${GREEN}✅ Sync complete!${NC}"
echo "   FastMCP Cloud will auto-deploy from: $STANDALONE_REPO"
echo ""
echo -e "${YELLOW}⚠️  Remember to set secrets in GitHub if needed:${NC}"
echo "   ${BLUE}gh secret set SECRET_NAME -b\"secret-value\" -R vanman2024/$REPO_NAME${NC}"
