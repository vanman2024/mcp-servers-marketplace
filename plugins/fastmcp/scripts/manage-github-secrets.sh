#!/bin/bash
# GitHub Secrets Management for MCP Servers
# Uses gh CLI to securely manage secrets for standalone repos

set -e

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

COMMAND="$1"
SERVER_NAME="$2"

# Map server names to GitHub repos
get_repo_name() {
    case "$1" in
        "signalhire-mcp")
            echo "vanman2024/signalhire-mcp"
            ;;
        "cats-mcp-server")
            echo "vanman2024/cats-mcp-server"
            ;;
        *)
            echo ""
            ;;
    esac
}

# List secrets for a server
list_secrets() {
    local repo=$(get_repo_name "$1")
    if [ -z "$repo" ]; then
        echo -e "${RED}❌ Unknown server: $1${NC}"
        exit 1
    fi

    echo -e "${BLUE}🔐 Secrets for $repo:${NC}"
    gh secret list -R "$repo"
}

# Set a secret for a server
set_secret() {
    local repo=$(get_repo_name "$SERVER_NAME")
    if [ -z "$repo" ]; then
        echo -e "${RED}❌ Unknown server: $SERVER_NAME${NC}"
        exit 1
    fi

    local secret_name="$3"
    local secret_value="$4"

    if [ -z "$secret_name" ] || [ -z "$secret_value" ]; then
        echo -e "${RED}❌ Usage: $0 set <server-name> <SECRET_NAME> <secret-value>${NC}"
        exit 1
    fi

    echo -e "${BLUE}Setting secret $secret_name for $repo...${NC}"
    echo -n "$secret_value" | gh secret set "$secret_name" -R "$repo"
    echo -e "${GREEN}✅ Secret $secret_name set successfully${NC}"
}

# Delete a secret for a server
delete_secret() {
    local repo=$(get_repo_name "$SERVER_NAME")
    if [ -z "$repo" ]; then
        echo -e "${RED}❌ Unknown server: $SERVER_NAME${NC}"
        exit 1
    fi

    local secret_name="$3"

    if [ -z "$secret_name" ]; then
        echo -e "${RED}❌ Usage: $0 delete <server-name> <SECRET_NAME>${NC}"
        exit 1
    fi

    echo -e "${YELLOW}Deleting secret $secret_name from $repo...${NC}"
    gh secret delete "$secret_name" -R "$repo"
    echo -e "${GREEN}✅ Secret $secret_name deleted${NC}"
}

# Set secret from .env file
set_from_env() {
    local repo=$(get_repo_name "$SERVER_NAME")
    if [ -z "$repo" ]; then
        echo -e "${RED}❌ Unknown server: $SERVER_NAME${NC}"
        exit 1
    fi

    local env_file="$3"

    if [ -z "$env_file" ] || [ ! -f "$env_file" ]; then
        echo -e "${RED}❌ .env file not found: $env_file${NC}"
        exit 1
    fi

    echo -e "${BLUE}📄 Reading secrets from $env_file...${NC}"
    echo ""

    # Read .env file and set secrets
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" ]] && continue

        # Remove quotes from value
        value="${value%\"}"
        value="${value#\"}"
        value="${value%\'}"
        value="${value#\'}"

        echo -e "${BLUE}Setting $key...${NC}"
        echo -n "$value" | gh secret set "$key" -R "$repo"
        echo -e "${GREEN}✅ $key set${NC}"
    done < "$env_file"

    echo ""
    echo -e "${GREEN}✅ All secrets from $env_file set in $repo${NC}"
}

# Show usage
show_usage() {
    echo "GitHub Secrets Management for MCP Servers"
    echo ""
    echo "Usage:"
    echo "  $0 list <server-name>"
    echo "  $0 set <server-name> <SECRET_NAME> <secret-value>"
    echo "  $0 delete <server-name> <SECRET_NAME>"
    echo "  $0 set-from-env <server-name> <path-to-.env>"
    echo ""
    echo "Examples:"
    echo "  $0 list signalhire-mcp"
    echo "  $0 set signalhire-mcp SIGNALHIRE_API_KEY \"202.abc123...\""
    echo "  $0 set-from-env signalhire-mcp servers/business-productivity/signalhire/.env"
    echo "  $0 delete signalhire-mcp OLD_SECRET"
    echo ""
    echo "Supported servers:"
    echo "  - signalhire-mcp (vanman2024/signalhire-mcp)"
    echo "  - cats-mcp-server (vanman2024/cats-mcp-server)"
}

# Main command router
case "$COMMAND" in
    "list")
        list_secrets "$SERVER_NAME"
        ;;
    "set")
        set_secret "$@"
        ;;
    "delete")
        delete_secret "$@"
        ;;
    "set-from-env")
        set_from_env "$@"
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
