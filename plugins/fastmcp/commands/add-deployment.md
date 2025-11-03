---
description: Configure deployment for FastMCP server (HTTP, STDIO, FastMCP Cloud, production config)
argument-hint: [deployment-type] [--server-path=path]
allowed-tools: Task
---

**Arguments**: $ARGUMENTS

Goal: Configure deployment and transport for an existing FastMCP server. Supports HTTP, STDIO (Claude Desktop/Cursor/Claude Code), FastMCP Cloud, and production configuration.

## Overview

This command delegates to the specialized FastMCP deployment agent which handles:
- Transport configuration (STDIO, HTTP, FastMCP Cloud)
- IDE integration (Claude Desktop, Cursor, Claude Code)
- Production features (monitoring, logging, error handling, rate limiting)
- Security setup (CORS, SSL/TLS, authentication)
- Deployment scripts and documentation

## Reference Documentation

The deployment agent references:
- Deployment strategy: @plugins/fastmcp/docs/DEPLOYMENT.md
- FastMCP documentation: @plugins/fastmcp/docs/fastmcp-documentation.md
- Official FastMCP docs via WebFetch:
  - https://gofastmcp.com/deployment/running-server
  - https://gofastmcp.com/deployment/http
  - https://gofastmcp.com/deployment/fastmcp-cloud
  - https://gofastmcp.com/deployment/server-configuration

## Implementation

Use Task tool to launch the fastmcp-deployment agent:

```
Task(
  subagent_type: "fastmcp:fastmcp-deployment",
  description: "Configure FastMCP server deployment",
  prompt: "Use the @plugins/fastmcp/agents/fastmcp-deployment.md agent to configure deployment for the FastMCP server.

  Arguments provided: $ARGUMENTS

  The agent should:
  1. Discover current server configuration
  2. Gather deployment requirements from the user
  3. Configure requested transport protocols (STDIO, HTTP, FastMCP Cloud)
  4. Generate IDE configuration files as needed
  5. Add production features (logging, monitoring, error handling)
  6. Create deployment scripts and documentation
  7. Verify the deployment configuration works

  Follow all phases in the fastmcp-deployment agent systematically."
)
```

## Expected Outputs

After the agent completes, the server should have:
- ✅ Configured transport protocols based on requirements
- ✅ IDE configuration files for selected targets
- ✅ Production middleware (logging, monitoring, error handling)
- ✅ Environment-specific configs (.env.development, .env.production)
- ✅ Security features (CORS, SSL/TLS, rate limiting)
- ✅ Health check endpoint
- ✅ Deployment scripts (start.sh, deploy.sh)
- ✅ Updated README with deployment instructions
- ✅ Documented environment variables
