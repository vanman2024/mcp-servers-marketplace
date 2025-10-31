# Test MCP Server

Tests any MCP server using the proven in-memory FastMCP Client pattern.

## Usage
```bash
/test-mcp [server_path] [token_env_var]
```

## Examples
```bash
# Test Airtable MCP server
/test-mcp servers/http/airtable-http-mcp AIRTABLE_PERSONAL_ACCESS_TOKEN

# Test GitHub MCP server  
/test-mcp servers/http/github-http-mcp GITHUB_TOKEN

# Test any MCP server
/test-mcp path/to/server TOKEN_NAME
```

## What it does
1. Uses the **mcp-tester** specialist agent
2. Imports the MCP server directly (no network issues)
3. Tests with FastMCP Client in-memory pattern
4. Validates all tools, resources, and prompts
5. Runs actual tool calls with real data
6. Reports comprehensive results

This is the **gold standard** for MCP testing - bypasses all HTTP/protocol issues and tests the actual MCP logic directly.