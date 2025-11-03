#!/bin/bash
# FastMCP Server Post-Deployment Verification Script
# Verifies deployed server is accessible and functioning correctly

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
DEPLOYMENT_URL="${1:-}"
MAX_RETRIES="${MAX_RETRIES:-5}"
RETRY_DELAY="${RETRY_DELAY:-10}"
TIMEOUT="${TIMEOUT:-30}"

# Verification results tracking
VERIFICATION_RESULTS=()
EXIT_CODE=0

echo -e "${BLUE}=== FastMCP Server Deployment Verification ===${NC}"

# Helper functions
log_pass() {
    echo -e "${GREEN}✓${NC} $1"
    VERIFICATION_RESULTS+=("PASS: $1")
}

log_fail() {
    echo -e "${RED}✗${NC} $1"
    VERIFICATION_RESULTS+=("FAIL: $1")
    EXIT_CODE=1
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    VERIFICATION_RESULTS+=("WARN: $1")
}

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Validate deployment URL
if [[ -z "$DEPLOYMENT_URL" ]]; then
    echo -e "${RED}Error: Deployment URL required${NC}"
    echo "Usage: $0 <deployment-url>"
    echo ""
    echo "Examples:"
    echo "  $0 https://my-server.fastmcp.app/mcp"
    echo "  $0 http://localhost:8000/mcp"
    echo "  $0 https://my-server.example.com/mcp"
    exit 1
fi

# Normalize URL (remove trailing slash)
DEPLOYMENT_URL="${DEPLOYMENT_URL%/}"

echo "Deployment URL: $DEPLOYMENT_URL"
echo "Max retries: $MAX_RETRIES"
echo "Timeout: ${TIMEOUT}s"
echo ""

# Detect base URL and MCP endpoint
if [[ "$DEPLOYMENT_URL" == */mcp ]]; then
    BASE_URL="${DEPLOYMENT_URL%/mcp}"
    MCP_ENDPOINT="$DEPLOYMENT_URL"
else
    BASE_URL="$DEPLOYMENT_URL"
    MCP_ENDPOINT="${DEPLOYMENT_URL}/mcp"
fi

# Test 1: DNS Resolution
echo -e "${BLUE}[1/6] Testing DNS resolution...${NC}"
DOMAIN=$(echo "$DEPLOYMENT_URL" | sed -E 's|https?://([^:/]+).*|\1|')
if host "$DOMAIN" > /dev/null 2>&1; then
    IP=$(host "$DOMAIN" | grep "has address" | head -1 | awk '{print $NF}')
    log_pass "DNS resolved: $DOMAIN -> $IP"
else
    log_fail "DNS resolution failed for $DOMAIN"
fi
echo ""

# Test 2: Network Connectivity
echo -e "${BLUE}[2/6] Testing network connectivity...${NC}"
if curl -s --max-time $TIMEOUT --head "$BASE_URL" > /dev/null 2>&1; then
    log_pass "Server is reachable"
else
    log_fail "Cannot reach server at $BASE_URL"
fi
echo ""

# Test 3: Health Check Endpoint
echo -e "${BLUE}[3/6] Testing health endpoint...${NC}"

# Try common health check paths
HEALTH_PATHS=("/health" "/healthz" "/.well-known/health-check" "/api/health")
HEALTH_FOUND=false

for path in "${HEALTH_PATHS[@]}"; do
    HEALTH_URL="${BASE_URL}${path}"
    log_info "Trying $HEALTH_URL..."

    RESPONSE=$(curl -s --max-time $TIMEOUT -w "\n%{http_code}" "$HEALTH_URL" 2>/dev/null || echo "000")
    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    BODY=$(echo "$RESPONSE" | head -n -1)

    if [[ "$HTTP_CODE" == "200" ]]; then
        log_pass "Health endpoint available at $path (HTTP $HTTP_CODE)"
        log_info "Response: $BODY"
        HEALTH_FOUND=true
        break
    fi
done

if [[ "$HEALTH_FOUND" == false ]]; then
    log_warn "No standard health endpoint found (checked: ${HEALTH_PATHS[*]})"
fi
echo ""

# Test 4: MCP Endpoint Accessibility
echo -e "${BLUE}[4/6] Testing MCP endpoint...${NC}"

ATTEMPT=1
MCP_SUCCESS=false

while [[ $ATTEMPT -le $MAX_RETRIES ]]; do
    log_info "Attempt $ATTEMPT/$MAX_RETRIES..."

    # Test MCP endpoint (should support POST with JSON-RPC)
    MCP_RESPONSE=$(curl -s --max-time $TIMEOUT \
        -w "\n%{http_code}" \
        -X POST \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' \
        "$MCP_ENDPOINT" 2>/dev/null || echo -e "\n000")

    HTTP_CODE=$(echo "$MCP_RESPONSE" | tail -1)
    BODY=$(echo "$MCP_RESPONSE" | head -n -1)

    if [[ "$HTTP_CODE" == "200" ]]; then
        log_pass "MCP endpoint responding (HTTP $HTTP_CODE)"

        # Validate JSON-RPC response
        if echo "$BODY" | jq -e '.jsonrpc' > /dev/null 2>&1; then
            log_pass "Valid JSON-RPC response received"

            # Check for tools in response
            TOOL_COUNT=$(echo "$BODY" | jq -r '.result.tools // [] | length' 2>/dev/null || echo "0")
            if [[ "$TOOL_COUNT" -gt 0 ]]; then
                log_pass "Server provides $TOOL_COUNT tool(s)"
            else
                log_warn "Server returned no tools"
            fi

            MCP_SUCCESS=true
            break
        else
            log_warn "Response is not valid JSON-RPC"
            if [[ $VERBOSE -eq 1 ]]; then
                echo "Response body: $BODY"
            fi
        fi
    elif [[ "$HTTP_CODE" == "401" ]] || [[ "$HTTP_CODE" == "403" ]]; then
        log_warn "Authentication required (HTTP $HTTP_CODE)"
        MCP_SUCCESS=true  # Server is up, just needs auth
        break
    else
        log_warn "MCP endpoint not ready (HTTP $HTTP_CODE)"
    fi

    if [[ $ATTEMPT -lt $MAX_RETRIES ]]; then
        log_info "Retrying in ${RETRY_DELAY}s..."
        sleep $RETRY_DELAY
    fi

    ATTEMPT=$((ATTEMPT + 1))
done

if [[ "$MCP_SUCCESS" == false ]]; then
    log_fail "MCP endpoint verification failed after $MAX_RETRIES attempts"
fi
echo ""

# Test 5: SSL/TLS Certificate (for HTTPS)
if [[ "$DEPLOYMENT_URL" == https://* ]]; then
    echo -e "${BLUE}[5/6] Verifying SSL/TLS certificate...${NC}"

    # Check certificate validity
    CERT_INFO=$(echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN:443" 2>/dev/null | openssl x509 -noout -dates 2>/dev/null || echo "")

    if [[ -n "$CERT_INFO" ]]; then
        log_pass "Valid SSL/TLS certificate"

        # Extract expiration date
        EXPIRY=$(echo "$CERT_INFO" | grep "notAfter" | cut -d= -f2)
        log_info "Certificate expires: $EXPIRY"

        # Check if expiring soon (within 30 days)
        EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s 2>/dev/null || echo "0")
        NOW_EPOCH=$(date +%s)
        DAYS_LEFT=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))

        if [[ $DAYS_LEFT -lt 30 ]] && [[ $DAYS_LEFT -gt 0 ]]; then
            log_warn "Certificate expires in $DAYS_LEFT days - renewal recommended"
        elif [[ $DAYS_LEFT -le 0 ]]; then
            log_fail "Certificate has expired!"
        fi
    else
        log_fail "Could not verify SSL/TLS certificate"
    fi
    echo ""
else
    echo -e "${BLUE}[5/6] Skipping SSL check (HTTP deployment)${NC}"
    log_warn "Deployment uses HTTP - HTTPS recommended for production"
    echo ""
fi

# Test 6: Response Time and Performance
echo -e "${BLUE}[6/6] Testing performance...${NC}"

TOTAL_TIME=0
SAMPLES=3

for i in $(seq 1 $SAMPLES); do
    RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" --max-time $TIMEOUT "$BASE_URL" 2>/dev/null || echo "0")
    TOTAL_TIME=$(echo "$TOTAL_TIME + $RESPONSE_TIME" | bc)
    log_info "Sample $i: ${RESPONSE_TIME}s"
done

AVG_TIME=$(echo "scale=3; $TOTAL_TIME / $SAMPLES" | bc)
log_info "Average response time: ${AVG_TIME}s"

# Performance thresholds
if (( $(echo "$AVG_TIME < 1.0" | bc -l) )); then
    log_pass "Response time excellent (<1s)"
elif (( $(echo "$AVG_TIME < 3.0" | bc -l) )); then
    log_pass "Response time good (<3s)"
elif (( $(echo "$AVG_TIME < 5.0" | bc -l) )); then
    log_warn "Response time acceptable (3-5s)"
else
    log_warn "Response time slow (>5s) - consider optimization"
fi
echo ""

# Summary
echo -e "${BLUE}=== Verification Summary ===${NC}"
echo ""

PASS_COUNT=$(printf '%s\n' "${VERIFICATION_RESULTS[@]}" | grep -c "^PASS:" || true)
FAIL_COUNT=$(printf '%s\n' "${VERIFICATION_RESULTS[@]}" | grep -c "^FAIL:" || true)
WARN_COUNT=$(printf '%s\n' "${VERIFICATION_RESULTS[@]}" | grep -c "^WARN:" || true)

echo "Results: $PASS_COUNT passed, $FAIL_COUNT failed, $WARN_COUNT warnings"
echo ""

if [[ $EXIT_CODE -eq 0 ]]; then
    echo -e "${GREEN}✓ Deployment verified successfully${NC}"
    echo -e "${GREEN}Server is accessible and responding correctly${NC}"

    if [[ $WARN_COUNT -gt 0 ]]; then
        echo ""
        echo -e "${YELLOW}Warnings:${NC}"
        printf '%s\n' "${VERIFICATION_RESULTS[@]}" | grep "^WARN:" | sed 's/^WARN: /  - /'
    fi
else
    echo -e "${RED}✗ Deployment verification failed${NC}"
    echo ""
    echo "Failures:"
    printf '%s\n' "${VERIFICATION_RESULTS[@]}" | grep "^FAIL:" | sed 's/^FAIL: /  - /'
fi

echo ""
exit $EXIT_CODE
