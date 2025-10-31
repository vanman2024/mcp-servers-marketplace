#!/bin/bash
# Start Figma MCP Server with enhanced error handling
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Navigate to script directory
cd "$(dirname "$0")"

echo -e "${BLUE}=== Figma MCP Server Startup ===${NC}"

# Load .env file if it exists
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ Loading .env file${NC}"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo -e "${YELLOW}⚠ No .env file found${NC}"
    echo "  You can copy .env.example to .env for easier configuration"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -q -r requirements.txt

# Run configuration validator if requested
if [ "$1" = "--validate" ] || [ "$VALIDATE_CONFIG" = "true" ]; then
    echo -e "${BLUE}Running configuration validator...${NC}"
    python validate_config.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}Configuration validation failed!${NC}"
        echo "Fix the issues above and try again."
        exit 1
    fi
    echo
fi

# Check required environment variables with better messages
echo -e "${BLUE}Checking environment variables...${NC}"

# Check for Figma token (either FIGMA_PAT or FIGMA_ACCESS_TOKEN)
if [ -z "$FIGMA_PAT" ] && [ -z "$FIGMA_ACCESS_TOKEN" ]; then
    echo -e "${RED}✗ Error: Figma authentication token not found!${NC}"
    echo
    echo "Please set one of the following environment variables:"
    echo "  export FIGMA_PAT=\"your-figma-personal-access-token\""
    echo "  export FIGMA_ACCESS_TOKEN=\"your-figma-token\""
    echo
    echo "Get a token from: https://www.figma.com/developers/access-tokens"
    echo "Make sure it has 'File content' read permission"
    echo
    echo "Example:"
    echo "  export FIGMA_PAT=\"figd_AbCdEfGhIjKlMnOpQrStUvWxYz\""
    exit 1
else
    if [ -n "$FIGMA_PAT" ]; then
        echo -e "${GREEN}✓ FIGMA_PAT detected${NC}"
    else
        echo -e "${GREEN}✓ FIGMA_ACCESS_TOKEN detected${NC}"
    fi
fi

if [ -z "$SUPABASE_URL" ]; then
    echo -e "${RED}✗ Error: SUPABASE_URL not found!${NC}"
    echo
    echo "Please set: export SUPABASE_URL=\"https://your-project.supabase.co\""
    echo
    echo "Get it from: Supabase Dashboard → Settings → API → Project URL"
    exit 1
else
    echo -e "${GREEN}✓ SUPABASE_URL detected: $SUPABASE_URL${NC}"
fi

if [ -z "$SUPABASE_SERVICE_KEY" ]; then
    echo -e "${RED}✗ Error: SUPABASE_SERVICE_KEY not found!${NC}"
    echo
    echo "Please set: export SUPABASE_SERVICE_KEY=\"your-service-key\""
    echo
    echo "Get it from: Supabase Dashboard → Settings → API → service_role key"
    echo "(NOT the anon/public key!)"
    exit 1
else
    echo -e "${GREEN}✓ SUPABASE_SERVICE_KEY detected${NC}"
fi

# Set default port if not provided
export FIGMA_MCP_PORT=${FIGMA_MCP_PORT:-8031}

# Show debug mode status
if [ "$FIGMA_DEBUG" = "true" ] || [ "$FIGMA_DEBUG" = "1" ]; then
    echo -e "${YELLOW}ℹ Debug mode enabled${NC}"
fi

# Reminder about database migrations
if [ -f "migrations/001_initial_schema.sql" ]; then
    echo
    echo -e "${YELLOW}📋 Database Setup Reminder:${NC}"
    echo "  If this is your first time running the server,"
    echo "  run the migration script in your Supabase dashboard:"
    echo "  → SQL Editor → New Query → Paste migrations/001_initial_schema.sql"
fi

# Start the server
echo
echo -e "${GREEN}🚀 Starting Figma MCP Server on port $FIGMA_MCP_PORT...${NC}"
echo -e "${BLUE}   Health check: http://localhost:$FIGMA_MCP_PORT/health${NC}"
echo

cd src
python figma_server.py