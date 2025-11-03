#!/bin/bash
# FastMCP Server Local Testing Script
# Tests server locally with health checks before deployment

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SERVER_PATH="${1:-.}"
TEST_DURATION="${TEST_DURATION:-10}"
PORT="${PORT:-8000}"
TRANSPORT="${TRANSPORT:-stdio}"  # stdio, http, or both

# Test results tracking
TEST_RESULTS=()
EXIT_CODE=0

echo -e "${BLUE}=== FastMCP Server Local Testing ===${NC}"
echo "Server path: $SERVER_PATH"
echo "Transport: $TRANSPORT"
echo "Test duration: ${TEST_DURATION}s"
echo ""

# Helper functions
log_pass() {
    echo -e "${GREEN}✓${NC} $1"
    TEST_RESULTS+=("PASS: $1")
}

log_fail() {
    echo -e "${RED}✗${NC} $1"
    TEST_RESULTS+=("FAIL: $1")
    EXIT_CODE=1
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    TEST_RESULTS+=("WARN: $1")
}

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

cleanup() {
    if [[ -n "$SERVER_PID" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
        log_info "Stopping server (PID: $SERVER_PID)..."
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
}

trap cleanup EXIT

# Detect server language and file
if [[ -f "$SERVER_PATH/server.py" ]]; then
    SERVER_FILE="$SERVER_PATH/server.py"
    SERVER_LANG="python"
    SERVER_CMD="python3"
elif [[ -f "$SERVER_PATH/server.ts" ]]; then
    SERVER_FILE="$SERVER_PATH/server.ts"
    SERVER_LANG="typescript"
    SERVER_CMD="tsx"
elif [[ -f "$SERVER_PATH/index.ts" ]]; then
    SERVER_FILE="$SERVER_PATH/index.ts"
    SERVER_LANG="typescript"
    SERVER_CMD="tsx"
else
    log_fail "No server file found"
    exit 1
fi

log_info "Detected $SERVER_LANG server: $SERVER_FILE"
echo ""

# Test 1: Import/Require Check
echo -e "${BLUE}[1/5] Testing module imports...${NC}"
if [[ "$SERVER_LANG" == "python" ]]; then
    if python3 -c "import sys; sys.path.insert(0, '$SERVER_PATH'); import $(basename ${SERVER_FILE%.py})" 2>/dev/null; then
        log_pass "Python imports successful"
    else
        log_fail "Python import errors detected"
        python3 -c "import sys; sys.path.insert(0, '$SERVER_PATH'); import $(basename ${SERVER_FILE%.py})" 2>&1 | head -5
    fi
elif [[ "$SERVER_LANG" == "typescript" ]]; then
    if command -v tsx &> /dev/null; then
        log_pass "TypeScript runtime (tsx) available"
    else
        log_warn "tsx not found - install with: npm install -g tsx"
    fi
fi
echo ""

# Test 2: STDIO Transport Test
if [[ "$TRANSPORT" == "stdio" ]] || [[ "$TRANSPORT" == "both" ]]; then
    echo -e "${BLUE}[2/5] Testing STDIO transport...${NC}"

    # Start server in background
    log_info "Starting server in STDIO mode..."

    if [[ "$SERVER_LANG" == "python" ]]; then
        timeout ${TEST_DURATION}s python3 "$SERVER_FILE" > /tmp/fastmcp-test-stdio.log 2>&1 &
    else
        timeout ${TEST_DURATION}s tsx "$SERVER_FILE" > /tmp/fastmcp-test-stdio.log 2>&1 &
    fi

    SERVER_PID=$!

    # Wait for server to initialize
    sleep 2

    if kill -0 "$SERVER_PID" 2>/dev/null; then
        log_pass "Server started successfully (PID: $SERVER_PID)"

        # Check if it's producing MCP messages
        if grep -q "jsonrpc" /tmp/fastmcp-test-stdio.log 2>/dev/null; then
            log_pass "Server is producing MCP protocol messages"
        else
            log_warn "No MCP messages detected yet (may need more time)"
        fi

        # Let it run for a bit
        sleep 3

        if kill -0 "$SERVER_PID" 2>/dev/null; then
            log_pass "Server running stable for 5 seconds"
        else
            log_fail "Server crashed during test"
            cat /tmp/fastmcp-test-stdio.log
        fi

        # Cleanup
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
        SERVER_PID=""
    else
        log_fail "Server failed to start"
        cat /tmp/fastmcp-test-stdio.log
    fi
    echo ""
fi

# Test 3: HTTP Transport Test
if [[ "$TRANSPORT" == "http" ]] || [[ "$TRANSPORT" == "both" ]]; then
    echo -e "${BLUE}[3/5] Testing HTTP transport...${NC}"

    # Check if port is already in use
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        log_fail "Port $PORT already in use"
    else
        log_info "Starting server on http://localhost:$PORT..."

        # Start server with HTTP transport
        if [[ "$SERVER_LANG" == "python" ]]; then
            # Assume FastMCP server supports HTTP via uvicorn
            timeout ${TEST_DURATION}s python3 "$SERVER_FILE" --transport http --port $PORT > /tmp/fastmcp-test-http.log 2>&1 &
        else
            timeout ${TEST_DURATION}s tsx "$SERVER_FILE" --transport http --port $PORT > /tmp/fastmcp-test-http.log 2>&1 &
        fi

        SERVER_PID=$!

        # Wait for server to start
        sleep 3

        if kill -0 "$SERVER_PID" 2>/dev/null; then
            log_pass "HTTP server started (PID: $SERVER_PID)"

            # Test health endpoint if available
            if command -v curl &> /dev/null; then
                if curl -s "http://localhost:$PORT/health" > /dev/null 2>&1; then
                    log_pass "Health endpoint responding"
                elif curl -s "http://localhost:$PORT/" > /dev/null 2>&1; then
                    log_pass "Root endpoint responding"
                else
                    log_warn "HTTP endpoints not responding (may not be configured)"
                fi
            fi

            # Cleanup
            kill "$SERVER_PID" 2>/dev/null || true
            wait "$SERVER_PID" 2>/dev/null || true
            SERVER_PID=""
        else
            log_fail "HTTP server failed to start"
            cat /tmp/fastmcp-test-http.log
        fi
    fi
    echo ""
fi

# Test 4: Environment Variables
echo -e "${BLUE}[4/5] Testing environment variables...${NC}"
if [[ -f "$SERVER_PATH/.env.example" ]]; then
    log_pass "Found .env.example"

    # Check if all vars in .env.example are documented
    ENV_VARS=$(grep -E "^[A-Z_]+" "$SERVER_PATH/.env.example" | cut -d= -f1 || true)
    if [[ -n "$ENV_VARS" ]]; then
        log_info "Documented environment variables:"
        echo "$ENV_VARS" | while read -r var; do
            echo "  - $var"
        done

        # Check if .env exists for testing
        if [[ -f "$SERVER_PATH/.env" ]]; then
            log_pass ".env file exists for local testing"

            # Check if all required vars are set
            MISSING_VARS=""
            for var in $ENV_VARS; do
                if ! grep -q "^${var}=" "$SERVER_PATH/.env"; then
                    MISSING_VARS="$MISSING_VARS $var"
                fi
            done

            if [[ -n "$MISSING_VARS" ]]; then
                log_warn "Missing variables in .env:$MISSING_VARS"
            else
                log_pass "All documented variables present in .env"
            fi
        else
            log_warn ".env not found - create from .env.example for testing"
        fi
    fi
else
    log_warn ".env.example not found"
fi
echo ""

# Test 5: FastMCP.json Configuration
echo -e "${BLUE}[5/5] Testing fastmcp.json configuration...${NC}"
if [[ -f "$SERVER_PATH/fastmcp.json" ]]; then
    log_pass "Found fastmcp.json"

    if command -v jq &> /dev/null; then
        # Check environment variables are documented
        ENV_COUNT=$(jq -r '.env // [] | length' "$SERVER_PATH/fastmcp.json")
        if [[ $ENV_COUNT -gt 0 ]]; then
            log_info "fastmcp.json declares $ENV_COUNT environment variables"

            # List them
            jq -r '.env[]? | "\(.name): \(.description // "No description")"' "$SERVER_PATH/fastmcp.json" | while read -r line; do
                echo "  - $line"
            done
        fi

        # Check for health check configuration
        if jq -e '.healthCheck' "$SERVER_PATH/fastmcp.json" > /dev/null 2>&1; then
            log_pass "Health check configured in fastmcp.json"
        else
            log_warn "No health check configuration found"
        fi
    fi
else
    log_warn "fastmcp.json not found (required for FastMCP Cloud)"
fi
echo ""

# Summary
echo -e "${BLUE}=== Test Summary ===${NC}"
echo ""

PASS_COUNT=$(printf '%s\n' "${TEST_RESULTS[@]}" | grep -c "^PASS:" || true)
FAIL_COUNT=$(printf '%s\n' "${TEST_RESULTS[@]}" | grep -c "^FAIL:" || true)
WARN_COUNT=$(printf '%s\n' "${TEST_RESULTS[@]}" | grep -c "^WARN:" || true)

echo "Results: $PASS_COUNT passed, $FAIL_COUNT failed, $WARN_COUNT warnings"
echo ""

if [[ $EXIT_CODE -eq 0 ]]; then
    echo -e "${GREEN}✓ Server tests passed - ready for deployment testing${NC}"
    if [[ $WARN_COUNT -gt 0 ]]; then
        echo -e "${YELLOW}⚠ Address warnings for best results${NC}"
    fi
else
    echo -e "${RED}✗ Server tests failed${NC}"
    echo ""
    echo "Failed tests:"
    printf '%s\n' "${TEST_RESULTS[@]}" | grep "^FAIL:" | sed 's/^FAIL: /  - /'
fi

echo ""
echo "Logs saved to:"
echo "  - /tmp/fastmcp-test-stdio.log (if tested)"
echo "  - /tmp/fastmcp-test-http.log (if tested)"
echo ""

exit $EXIT_CODE
