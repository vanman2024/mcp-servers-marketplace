#!/bin/bash
# FastMCP Server Environment Variable Verification Script
# Checks environment variables are properly configured for deployment

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SERVER_PATH="${1:-.}"
ENV_FILE="${ENV_FILE:-.env}"
CHECK_MODE="${CHECK_MODE:-all}"  # all, required, optional

# Check results tracking
CHECK_RESULTS=()
EXIT_CODE=0

echo -e "${BLUE}=== FastMCP Server Environment Variable Check ===${NC}"
echo "Server path: $SERVER_PATH"
echo "Env file: $ENV_FILE"
echo "Check mode: $CHECK_MODE"
echo ""

# Helper functions
log_pass() {
    echo -e "${GREEN}✓${NC} $1"
    CHECK_RESULTS+=("PASS: $1")
}

log_fail() {
    echo -e "${RED}✗${NC} $1"
    CHECK_RESULTS+=("FAIL: $1")
    EXIT_CODE=1
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    CHECK_RESULTS+=("WARN: $1")
}

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check 1: Verify .env.example exists
echo -e "${BLUE}[1/5] Checking documentation...${NC}"
if [[ -f "$SERVER_PATH/.env.example" ]]; then
    log_pass "Found .env.example template"

    # Count documented variables
    DOC_VAR_COUNT=$(grep -E "^[A-Z_]+" "$SERVER_PATH/.env.example" | wc -l)
    log_info "Documents $DOC_VAR_COUNT environment variable(s)"
else
    log_fail ".env.example not found - required for documentation"
    echo ""
    echo -e "${YELLOW}Tip: Create .env.example with all required environment variables${NC}"
    exit 1
fi
echo ""

# Check 2: Parse .env.example for variables
echo -e "${BLUE}[2/5] Parsing documented variables...${NC}"

declare -A REQUIRED_VARS
declare -A OPTIONAL_VARS
declare -A VAR_DESCRIPTIONS

while IFS= read -r line; do
    # Skip comments and empty lines
    [[ "$line" =~ ^#.*$ ]] && continue
    [[ -z "$line" ]] && continue

    # Extract variable name and value
    if [[ "$line" =~ ^([A-Z_][A-Z0-9_]*)=(.*)$ ]]; then
        VAR_NAME="${BASH_REMATCH[1]}"
        VAR_VALUE="${BASH_REMATCH[2]}"

        # Check if it's required (no default value or placeholder)
        if [[ -z "$VAR_VALUE" ]] || [[ "$VAR_VALUE" == "your-"* ]] || [[ "$VAR_VALUE" == "<"*">" ]]; then
            REQUIRED_VARS["$VAR_NAME"]=1
            log_info "Required: $VAR_NAME"
        else
            OPTIONAL_VARS["$VAR_NAME"]="$VAR_VALUE"
            log_info "Optional: $VAR_NAME (default: $VAR_VALUE)"
        fi
    fi

    # Extract inline comments as descriptions
    if [[ "$line" =~ #(.*)$ ]]; then
        DESC="${BASH_REMATCH[1]}"
        if [[ -n "$VAR_NAME" ]]; then
            VAR_DESCRIPTIONS["$VAR_NAME"]="$DESC"
        fi
    fi
done < "$SERVER_PATH/.env.example"

REQUIRED_COUNT=${#REQUIRED_VARS[@]}
OPTIONAL_COUNT=${#OPTIONAL_VARS[@]}

echo ""
log_info "Found $REQUIRED_COUNT required and $OPTIONAL_COUNT optional variables"
echo ""

# Check 3: Verify local .env file
echo -e "${BLUE}[3/5] Checking local environment file...${NC}"
if [[ -f "$SERVER_PATH/$ENV_FILE" ]]; then
    log_pass "Found $ENV_FILE"

    # Source the .env file to get values
    set -a
    source "$SERVER_PATH/$ENV_FILE" 2>/dev/null || true
    set +a

    # Check required variables
    MISSING_REQUIRED=()
    for var in "${!REQUIRED_VARS[@]}"; do
        if [[ -z "${!var}" ]]; then
            MISSING_REQUIRED+=("$var")
        fi
    done

    if [[ ${#MISSING_REQUIRED[@]} -eq 0 ]]; then
        log_pass "All required variables are set"
    else
        log_fail "Missing ${#MISSING_REQUIRED[@]} required variable(s):"
        for var in "${MISSING_REQUIRED[@]}"; do
            echo "  - $var"
            if [[ -n "${VAR_DESCRIPTIONS[$var]}" ]]; then
                echo "    ${VAR_DESCRIPTIONS[$var]}"
            fi
        done
    fi

    # Check optional variables
    MISSING_OPTIONAL=()
    for var in "${!OPTIONAL_VARS[@]}"; do
        if [[ -z "${!var}" ]]; then
            MISSING_OPTIONAL+=("$var")
        fi
    done

    if [[ ${#MISSING_OPTIONAL[@]} -gt 0 ]]; then
        log_info "${#MISSING_OPTIONAL[@]} optional variable(s) using defaults"
    fi
else
    log_fail "$ENV_FILE not found"
    echo ""
    echo -e "${YELLOW}Create $ENV_FILE from template:${NC}"
    echo "  cp $SERVER_PATH/.env.example $SERVER_PATH/$ENV_FILE"
    echo "  # Then edit $ENV_FILE with your values"
fi
echo ""

# Check 4: Validate fastmcp.json env declarations
echo -e "${BLUE}[4/5] Checking fastmcp.json declarations...${NC}"
if [[ -f "$SERVER_PATH/fastmcp.json" ]] && command -v jq &> /dev/null; then
    FASTMCP_ENV_COUNT=$(jq -r '.env // [] | length' "$SERVER_PATH/fastmcp.json")

    if [[ $FASTMCP_ENV_COUNT -gt 0 ]]; then
        log_info "fastmcp.json declares $FASTMCP_ENV_COUNT environment variable(s)"

        # Check if all are documented in .env.example
        UNDOCUMENTED=()
        while IFS= read -r var; do
            if ! grep -q "^${var}=" "$SERVER_PATH/.env.example"; then
                UNDOCUMENTED+=("$var")
            fi
        done < <(jq -r '.env[]?.name // empty' "$SERVER_PATH/fastmcp.json")

        if [[ ${#UNDOCUMENTED[@]} -eq 0 ]]; then
            log_pass "All fastmcp.json variables documented in .env.example"
        else
            log_warn "Variables in fastmcp.json missing from .env.example:"
            for var in "${UNDOCUMENTED[@]}"; do
                echo "  - $var"
            done
        fi

        # Show fastmcp.json env configuration
        echo ""
        log_info "Environment variables from fastmcp.json:"
        jq -r '.env[]? | "  - \(.name): \(.description // "No description") [\(.required // false | if . then "required" else "optional" end)]"' "$SERVER_PATH/fastmcp.json"
    else
        log_info "No environment variables declared in fastmcp.json"
    fi
else
    if [[ ! -f "$SERVER_PATH/fastmcp.json" ]]; then
        log_warn "fastmcp.json not found (required for FastMCP Cloud)"
    else
        log_warn "jq not installed - skipping fastmcp.json validation"
    fi
fi
echo ""

# Check 5: Security validation
echo -e "${BLUE}[5/5] Checking security...${NC}"

# Check if .env is in .gitignore
if [[ -f "$SERVER_PATH/.gitignore" ]]; then
    if grep -qE "^\.env$|^\.env\..*$" "$SERVER_PATH/.gitignore"; then
        log_pass ".env files properly excluded from git"
    else
        log_fail ".env not in .gitignore - SECURITY RISK!"
        echo ""
        echo -e "${RED}Add to .gitignore immediately:${NC}"
        echo "  echo '.env' >> .gitignore"
        echo "  echo '.env.*' >> .gitignore"
        echo "  echo '!.env.example' >> .gitignore"
    fi
else
    log_fail ".gitignore not found"
fi

# Check for common security issues
if [[ -f "$SERVER_PATH/$ENV_FILE" ]]; then
    # Check for placeholder values
    PLACEHOLDERS=$(grep -E "your-|<.*>|CHANGEME|TODO|FIXME" "$SERVER_PATH/$ENV_FILE" || true)
    if [[ -n "$PLACEHOLDERS" ]]; then
        log_warn "Found placeholder values in $ENV_FILE - replace before deployment:"
        echo "$PLACEHOLDERS" | sed 's/^/  /'
    else
        log_pass "No obvious placeholder values detected"
    fi

    # Check for empty required values
    for var in "${!REQUIRED_VARS[@]}"; do
        VALUE="${!var}"
        if [[ -z "$VALUE" ]]; then
            log_fail "Required variable $var is empty"
        fi
    done
fi

echo ""

# Summary
echo -e "${BLUE}=== Environment Check Summary ===${NC}"
echo ""

PASS_COUNT=$(printf '%s\n' "${CHECK_RESULTS[@]}" | grep -c "^PASS:" || true)
FAIL_COUNT=$(printf '%s\n' "${CHECK_RESULTS[@]}" | grep -c "^FAIL:" || true)
WARN_COUNT=$(printf '%s\n' "${CHECK_RESULTS[@]}" | grep -c "^WARN:" || true)

echo "Results: $PASS_COUNT passed, $FAIL_COUNT failed, $WARN_COUNT warnings"
echo ""

# Show what needs to be configured
if [[ ${#MISSING_REQUIRED[@]} -gt 0 ]]; then
    echo -e "${YELLOW}Action Required - Set these variables in $ENV_FILE:${NC}"
    for var in "${MISSING_REQUIRED[@]}"; do
        echo "  $var=${VAR_DESCRIPTIONS[$var]:-<value>}"
    done
    echo ""
fi

if [[ $EXIT_CODE -eq 0 ]]; then
    echo -e "${GREEN}✓ Environment configuration validated${NC}"
    if [[ $WARN_COUNT -gt 0 ]]; then
        echo -e "${YELLOW}⚠ Address warnings before production deployment${NC}"
    fi
else
    echo -e "${RED}✗ Environment configuration has errors${NC}"
    echo ""
    echo "Failed checks:"
    printf '%s\n' "${CHECK_RESULTS[@]}" | grep "^FAIL:" | sed 's/^FAIL: /  - /'
fi

echo ""
exit $EXIT_CODE
