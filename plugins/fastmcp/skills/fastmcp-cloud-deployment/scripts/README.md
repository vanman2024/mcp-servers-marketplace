# FastMCP Cloud Deployment Scripts

This directory contains functional scripts for managing the FastMCP server deployment lifecycle.

## Scripts Overview

### validate-server.sh

**Purpose**: Pre-deployment validation of server code and configuration

**Usage**:
```bash
./validate-server.sh <server-path>

# Examples
./validate-server.sh .
./validate-server.sh /path/to/server
VERBOSE=1 ./validate-server.sh .
```

**What it checks**:
- Server file exists (server.py, server.ts, index.ts)
- Syntax is valid (Python/TypeScript compilation)
- Dependencies declared and FastMCP included
- fastmcp.json configuration is valid
- No hardcoded secrets in code
- Environment files present (.env.example)
- .gitignore properly configured

**Exit codes**:
- `0`: Validation passed
- `1`: Validation failed (fix errors before deployment)

---

### test-local.sh

**Purpose**: Local testing of server before deployment

**Usage**:
```bash
./test-local.sh <server-path>

# Examples
./test-local.sh .
TRANSPORT=both ./test-local.sh .
TRANSPORT=http PORT=3000 ./test-local.sh .
TEST_DURATION=30 ./test-local.sh .
```

**Environment variables**:
- `TRANSPORT`: `stdio`, `http`, or `both` (default: `stdio`)
- `PORT`: HTTP port to use (default: `8000`)
- `TEST_DURATION`: Test duration in seconds (default: `10`)

**What it tests**:
- Module imports work
- Server starts successfully (STDIO mode)
- Server produces MCP protocol messages
- HTTP server starts and responds (if testing HTTP)
- Health endpoints accessible
- Server runs stable for test duration
- Environment variables configured

**Exit codes**:
- `0`: Tests passed
- `1`: Tests failed

---

### check-env-vars.sh

**Purpose**: Validate environment variable configuration

**Usage**:
```bash
./check-env-vars.sh <server-path>

# Examples
./check-env-vars.sh .
ENV_FILE=.env.production ./check-env-vars.sh .
CHECK_MODE=required ./check-env-vars.sh .
```

**Environment variables**:
- `ENV_FILE`: Environment file to check (default: `.env`)
- `CHECK_MODE`: `all`, `required`, or `optional` (default: `all`)

**What it checks**:
- .env.example exists and documents variables
- Required vs optional variables identified
- Local .env has all required variables
- fastmcp.json env declarations match .env.example
- .env is in .gitignore (security check)
- No placeholder values (your-api-key, TODO, etc.)

**Exit codes**:
- `0`: Environment configuration valid
- `1`: Missing required variables or security issues

---

### verify-deployment.sh

**Purpose**: Post-deployment verification of deployed server

**Usage**:
```bash
./verify-deployment.sh <deployment-url>

# Examples
./verify-deployment.sh https://my-server.fastmcp.app/mcp
./verify-deployment.sh http://localhost:8000/mcp
MAX_RETRIES=10 TIMEOUT=60 ./verify-deployment.sh https://my-server.com/mcp
VERBOSE=1 ./verify-deployment.sh https://my-server.com/mcp
```

**Environment variables**:
- `MAX_RETRIES`: Maximum retry attempts (default: `5`)
- `RETRY_DELAY`: Seconds between retries (default: `10`)
- `TIMEOUT`: Request timeout in seconds (default: `30`)
- `VERBOSE`: Show detailed output (default: `0`)

**What it verifies**:
- DNS resolution working
- Server is reachable
- Health endpoint responding
- MCP endpoint accepts JSON-RPC requests
- Valid JSON-RPC responses returned
- Server provides tools
- SSL/TLS certificate valid (for HTTPS)
- Response time acceptable

**Exit codes**:
- `0`: Deployment verified successfully
- `1`: Verification failed

---

## Typical Workflow

1. **Before Deployment**:
   ```bash
   # Validate code is ready
   ./validate-server.sh .

   # Check environment variables
   ./check-env-vars.sh .

   # Test locally
   TRANSPORT=both ./test-local.sh .
   ```

2. **After Deployment**:
   ```bash
   # Verify deployment is working
   ./verify-deployment.sh https://your-deployment-url/mcp
   ```

## Dependencies

All scripts require:
- `bash` (standard on Linux/macOS)
- `curl` (for HTTP testing and verification)

Script-specific requirements:
- **validate-server.sh**:
  - `python3` (for Python servers)
  - `tsc` (for TypeScript servers)
  - `jq` (for JSON validation)
- **test-local.sh**:
  - `python3` or `tsx` (depending on server language)
  - `lsof` (for port checking)
- **check-env-vars.sh**:
  - `jq` (for fastmcp.json parsing)
- **verify-deployment.sh**:
  - `host` or `dig` (for DNS checking)
  - `openssl` (for SSL verification)
  - `bc` (for calculations)
  - `jq` (for JSON parsing)

Install missing dependencies:
```bash
# Ubuntu/Debian
sudo apt install curl jq bc dnsutils openssl

# macOS
brew install jq bc curl openssl
```

## Troubleshooting

**Permission denied**:
```bash
chmod +x scripts/*.sh
```

**Command not found**:
```bash
# Check which commands are missing
which python3 curl jq bc host openssl

# Install missing packages (see Dependencies above)
```

**Script hangs**:
```bash
# Reduce test duration
TEST_DURATION=5 ./test-local.sh .

# Increase timeout for slow networks
TIMEOUT=60 ./verify-deployment.sh <url>
```

## Integration

These scripts are designed to work together and can be integrated into:
- CI/CD pipelines
- Pre-commit hooks
- Deployment automation
- Monitoring systems

Example CI/CD integration:
```yaml
# .github/workflows/deploy.yml
- name: Validate server
  run: ./scripts/validate-server.sh .

- name: Check environment
  run: ENV_FILE=.env.production ./scripts/check-env-vars.sh .

- name: Test locally
  run: TRANSPORT=both ./scripts/test-local.sh .

- name: Deploy
  run: # Your deployment command

- name: Verify deployment
  run: ./scripts/verify-deployment.sh $DEPLOYMENT_URL
```

## Contributing

When adding new checks:
1. Keep scripts focused on single responsibility
2. Use clear success/failure indicators (✓/✗)
3. Provide helpful error messages
4. Include examples in usage comments
5. Handle edge cases gracefully
6. Test on both Linux and macOS

---

**Script Collection Version**: 1.0.0
**Last Updated**: 2025-01-15
