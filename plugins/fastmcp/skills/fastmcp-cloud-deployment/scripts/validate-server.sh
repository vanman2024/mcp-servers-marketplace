#!/bin/bash
# FastMCP Server Pre-Deployment Validation Script
# Validates server syntax, dependencies, and fastmcp.json configuration

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SERVER_PATH="${1:-.}"
VERBOSE="${VERBOSE:-0}"
EXIT_CODE=0

# Validation results tracking
VALIDATION_RESULTS=()

echo -e "${BLUE}=== FastMCP Server Pre-Deployment Validation ===${NC}"
echo "Server path: $SERVER_PATH"
echo ""

# Helper functions
log_pass() {
    echo -e "${GREEN}✓${NC} $1"
    VALIDATION_RESULTS+=("PASS: $1")
}

log_fail() {
    echo -e "${RED}✗${NC} $1"
    VALIDATION_RESULTS+=("FAIL: $1")
    EXIT_CODE=1
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    VALIDATION_RESULTS+=("WARN: $1")
}

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Validation 1: Check server file exists
echo -e "${BLUE}[1/7] Checking server file...${NC}"
if [[ -f "$SERVER_PATH/server.py" ]]; then
    log_pass "Found Python server file: server.py"
    SERVER_FILE="$SERVER_PATH/server.py"
    SERVER_LANG="python"
elif [[ -f "$SERVER_PATH/server.ts" ]]; then
    log_pass "Found TypeScript server file: server.ts"
    SERVER_FILE="$SERVER_PATH/server.ts"
    SERVER_LANG="typescript"
elif [[ -f "$SERVER_PATH/index.ts" ]]; then
    log_pass "Found TypeScript server file: index.ts"
    SERVER_FILE="$SERVER_PATH/index.ts"
    SERVER_LANG="typescript"
else
    log_fail "No server file found (expected server.py, server.ts, or index.ts)"
fi
echo ""

# Validation 2: Syntax check
echo -e "${BLUE}[2/7] Validating syntax...${NC}"
if [[ "$SERVER_LANG" == "python" ]]; then
    if command -v python3 &> /dev/null; then
        if python3 -m py_compile "$SERVER_FILE" 2>/dev/null; then
            log_pass "Python syntax is valid"
        else
            log_fail "Python syntax errors detected"
            if [[ $VERBOSE -eq 1 ]]; then
                python3 -m py_compile "$SERVER_FILE" 2>&1 | head -10
            fi
        fi
    else
        log_warn "Python3 not found - skipping syntax check"
    fi
elif [[ "$SERVER_LANG" == "typescript" ]]; then
    if command -v tsc &> /dev/null; then
        if tsc --noEmit "$SERVER_FILE" 2>/dev/null; then
            log_pass "TypeScript syntax is valid"
        else
            log_fail "TypeScript syntax errors detected"
            if [[ $VERBOSE -eq 1 ]]; then
                tsc --noEmit "$SERVER_FILE" 2>&1 | head -10
            fi
        fi
    else
        log_warn "TypeScript compiler not found - skipping syntax check"
    fi
fi
echo ""

# Validation 3: Check dependencies
echo -e "${BLUE}[3/7] Checking dependencies...${NC}"
if [[ "$SERVER_LANG" == "python" ]]; then
    if [[ -f "$SERVER_PATH/requirements.txt" ]]; then
        log_pass "Found requirements.txt"

        # Check if fastmcp is listed
        if grep -q "fastmcp" "$SERVER_PATH/requirements.txt"; then
            log_pass "FastMCP dependency declared in requirements.txt"
        else
            log_fail "FastMCP not found in requirements.txt"
        fi

        # Check for version pinning
        UNPINNED_DEPS=$(grep -v "==" "$SERVER_PATH/requirements.txt" | grep -v "^#" | grep -v "^$" | wc -l)
        if [[ $UNPINNED_DEPS -gt 0 ]]; then
            log_warn "Found $UNPINNED_DEPS unpinned dependencies (recommend using == for production)"
        fi
    else
        log_fail "requirements.txt not found"
    fi
elif [[ "$SERVER_LANG" == "typescript" ]]; then
    if [[ -f "$SERVER_PATH/package.json" ]]; then
        log_pass "Found package.json"

        # Check if @fastmcp/core is listed
        if grep -q "@fastmcp/core" "$SERVER_PATH/package.json"; then
            log_pass "FastMCP dependency declared in package.json"
        else
            log_fail "FastMCP not found in package.json dependencies"
        fi
    else
        log_fail "package.json not found"
    fi
fi
echo ""

# Validation 4: Check fastmcp.json configuration
echo -e "${BLUE}[4/7] Validating fastmcp.json...${NC}"
if [[ -f "$SERVER_PATH/fastmcp.json" ]]; then
    log_pass "Found fastmcp.json"

    # Validate JSON syntax
    if command -v jq &> /dev/null; then
        if jq empty "$SERVER_PATH/fastmcp.json" 2>/dev/null; then
            log_pass "fastmcp.json has valid JSON syntax"

            # Check required fields
            NAME=$(jq -r '.name // empty' "$SERVER_PATH/fastmcp.json")
            VERSION=$(jq -r '.version // empty' "$SERVER_PATH/fastmcp.json")
            ENTRY_POINT=$(jq -r '.entryPoint // empty' "$SERVER_PATH/fastmcp.json")

            [[ -n "$NAME" ]] && log_pass "Server name: $NAME" || log_fail "Missing 'name' field"
            [[ -n "$VERSION" ]] && log_pass "Version: $VERSION" || log_warn "Missing 'version' field"
            [[ -n "$ENTRY_POINT" ]] && log_pass "Entry point: $ENTRY_POINT" || log_fail "Missing 'entryPoint' field"

            # Check environment variables
            ENV_VARS=$(jq -r '.env // [] | length' "$SERVER_PATH/fastmcp.json")
            if [[ $ENV_VARS -gt 0 ]]; then
                log_info "Declared $ENV_VARS environment variables"
            fi
        else
            log_fail "fastmcp.json has invalid JSON syntax"
        fi
    else
        log_warn "jq not installed - skipping JSON validation"
    fi
else
    log_warn "fastmcp.json not found (required for FastMCP Cloud deployment)"
fi
echo ""

# Validation 5: Check for common issues
echo -e "${BLUE}[5/7] Checking for common issues...${NC}"

# Check for hardcoded secrets
if grep -rE "(api[_-]?key|secret|password|token)\\s*=\\s*['\"][^'\"]+['\"]" "$SERVER_FILE" 2>/dev/null; then
    log_warn "Potential hardcoded secrets detected - use environment variables"
else
    log_pass "No obvious hardcoded secrets detected"
fi

# Check for localhost references
if grep -rE "(localhost|127\\.0\\.0\\.1)" "$SERVER_FILE" 2>/dev/null; then
    log_warn "Found localhost references - may cause issues in production"
fi

# Check for debug mode
if grep -rE "(debug\\s*=\\s*True|DEBUG\\s*=\\s*True)" "$SERVER_FILE" 2>/dev/null; then
    log_warn "Debug mode enabled - should be disabled for production"
fi

echo ""

# Validation 6: Check environment variables
echo -e "${BLUE}[6/7] Checking environment configuration...${NC}"
if [[ -f "$SERVER_PATH/.env.example" ]]; then
    log_pass "Found .env.example template"

    # Check if .env exists
    if [[ -f "$SERVER_PATH/.env" ]]; then
        log_warn ".env file found - ensure it's in .gitignore"

        # Check .gitignore
        if [[ -f "$SERVER_PATH/.gitignore" ]] && grep -q "^\.env$" "$SERVER_PATH/.gitignore"; then
            log_pass ".env is in .gitignore"
        else
            log_fail ".env is NOT in .gitignore - risk of committing secrets!"
        fi
    fi
else
    log_warn ".env.example not found (recommended for documenting required env vars)"
fi
echo ""

# Validation 7: Check project metadata
echo -e "${BLUE}[7/7] Checking project metadata...${NC}"
if [[ -f "$SERVER_PATH/README.md" ]]; then
    log_pass "Found README.md"
else
    log_warn "README.md not found (recommended for deployment documentation)"
fi

if [[ -f "$SERVER_PATH/.gitignore" ]]; then
    log_pass "Found .gitignore"
else
    log_warn ".gitignore not found"
fi

if [[ "$SERVER_LANG" == "python" ]] && [[ -f "$SERVER_PATH/pyproject.toml" ]]; then
    log_info "Found pyproject.toml (modern Python project)"
fi

echo ""
echo -e "${BLUE}=== Validation Summary ===${NC}"
echo ""

# Count results
PASS_COUNT=$(printf '%s\n' "${VALIDATION_RESULTS[@]}" | grep -c "^PASS:" || true)
FAIL_COUNT=$(printf '%s\n' "${VALIDATION_RESULTS[@]}" | grep -c "^FAIL:" || true)
WARN_COUNT=$(printf '%s\n' "${VALIDATION_RESULTS[@]}" | grep -c "^WARN:" || true)

echo "Results: $PASS_COUNT passed, $FAIL_COUNT failed, $WARN_COUNT warnings"
echo ""

if [[ $EXIT_CODE -eq 0 ]]; then
    echo -e "${GREEN}✓ Server passed validation - ready for deployment${NC}"
    if [[ $WARN_COUNT -gt 0 ]]; then
        echo -e "${YELLOW}⚠ Address warnings before production deployment${NC}"
    fi
else
    echo -e "${RED}✗ Server validation failed - fix errors before deploying${NC}"
    echo ""
    echo "Failed checks:"
    printf '%s\n' "${VALIDATION_RESULTS[@]}" | grep "^FAIL:" | sed 's/^FAIL: /  - /'
fi

echo ""
exit $EXIT_CODE
