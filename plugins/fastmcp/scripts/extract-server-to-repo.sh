#!/bin/bash
# extract-server-to-repo.sh - Extract an MCP server from monorepo to separate repository
# Usage: ./scripts/extract-server-to-repo.sh <server-path> [target-dir]
#
# Example: ./scripts/extract-server-to-repo.sh servers/business-productivity/cats-mcp-server ../cats-mcp-server

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Parse arguments
SERVER_PATH="$1"
TARGET_DIR="${2:-}"

if [ -z "$SERVER_PATH" ]; then
    echo -e "${RED}Error: Server path required${NC}"
    echo "Usage: $0 <server-path> [target-dir]"
    echo ""
    echo "Examples:"
    echo "  $0 servers/business-productivity/cats-mcp-server"
    echo "  $0 servers/business-productivity/cats-mcp-server ../cats-mcp-server"
    exit 1
fi

# Validate source exists
if [ ! -d "$SERVER_PATH" ]; then
    echo -e "${RED}Error: Server path not found: $SERVER_PATH${NC}"
    exit 1
fi

# Get server name from path
SERVER_NAME=$(basename "$SERVER_PATH")

# Determine target directory
if [ -z "$TARGET_DIR" ]; then
    TARGET_DIR="../${SERVER_NAME}"
fi

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}MCP Server Extraction to Separate Repo${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}Source:${NC} $SERVER_PATH"
echo -e "${GREEN}Target:${NC} $TARGET_DIR"
echo -e "${GREEN}Server:${NC} $SERVER_NAME"
echo ""

# Check if target exists
if [ -d "$TARGET_DIR" ]; then
    echo -e "${YELLOW}Warning: Target directory already exists: $TARGET_DIR${NC}"
    read -p "Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
    trash-put "$TARGET_DIR"
fi

# Create target directory
echo -e "${BLUE}[1/6] Creating target directory...${NC}"
mkdir -p "$TARGET_DIR"

# Copy server files (excluding archive and cache)
echo -e "${BLUE}[2/6] Copying server files...${NC}"
rsync -av --exclude='archive/' --exclude='__pycache__/' --exclude='*.pyc' "$SERVER_PATH/" "$TARGET_DIR/"

# Initialize git repository
echo -e "${BLUE}[3/6] Initializing git repository...${NC}"
cd "$TARGET_DIR"
git init
git branch -M main

# Create .gitignore if it doesn't exist
echo -e "${BLUE}[4/6] Creating .gitignore...${NC}"
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.local
.env.*.local

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log

# Archive/backup files
archive/
EOF
fi

# Verify required files
echo -e "${BLUE}[5/6] Verifying required files...${NC}"

MISSING_FILES=()

if [ ! -f "server.py" ] && [ ! -f "src/server.py" ]; then
    MISSING_FILES+=("server.py")
fi

if [ ! -f "fastmcp.json" ]; then
    echo -e "${YELLOW}  Warning: fastmcp.json not found (required for FastMCP Cloud)${NC}"
fi

if [ ! -f "README.md" ]; then
    echo -e "${YELLOW}  Warning: README.md not found${NC}"
fi

if [ ! -f "requirements.txt" ] && [ ! -f "pyproject.toml" ]; then
    echo -e "${YELLOW}  Warning: No requirements.txt or pyproject.toml found${NC}"
fi

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo -e "${RED}Error: Required files missing:${NC}"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - $file"
    done
    exit 1
fi

# Initial commit
echo -e "${BLUE}[6/6] Creating initial commit...${NC}"
git add .
git commit -m "Initial commit: Extract ${SERVER_NAME} from monorepo

Extracted from mcp-servers-marketplace monorepo for FastMCP Cloud deployment.

Original location: ${SERVER_PATH}"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Extraction Complete${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}Repository:${NC} $TARGET_DIR"
echo -e "${GREEN}Branch:${NC} main"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Review extracted files:"
echo "   cd $TARGET_DIR"
echo "   ls -la"
echo ""
echo "2. Create GitHub repository:"
echo "   gh repo create ${SERVER_NAME} --public --source=. --remote=origin"
echo ""
echo "3. Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "4. Deploy to FastMCP Cloud:"
echo "   - Visit https://fastmcp.app"
echo "   - Create new project"
echo "   - Connect GitHub repository"
echo "   - Configure environment variables"
echo "   - Deploy!"
echo ""
echo -e "${YELLOW}Note: Original server in monorepo remains unchanged${NC}"
echo ""
