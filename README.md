# MCP Servers

This directory contains FastMCP servers built for this project. All servers are developed in this monorepo for convenience.

## Important: Deployment Architecture

**Development**: All servers live here in `mcp-servers/` monorepo
**Production**: Choose deployment based on needs (see [plugins/fastmcp/docs/DEPLOYMENT.md](./plugins/fastmcp/docs/DEPLOYMENT.md))

### Quick Decision Guide

- **STDIO** (local IDEs): Keep in monorepo ✅
- **HTTP** (your infrastructure): Keep in monorepo ✅
- **FastMCP Cloud**: Extract to separate repo when ready for production

**TL;DR**: FastMCP Cloud requires one server per GitHub repo, but you develop all servers here and extract only when needed for cloud deployment.

## Structure

```
mcp-servers/
├── .claude-plugin/
│   └── marketplace.json           # Marketplace registry with categorized servers
├── plugins/
│   └── fastmcp/                   # FastMCP plugin for building MCP servers
│       ├── commands/              # /fastmcp:* slash commands
│       ├── agents/                # Specialized agents (setup, verifier, etc.)
│       ├── skills/                # Reusable templates and scripts
│       └── docs/                  # FastMCP documentation
├── docs/                          # Project-level documentation
├── servers/                       # All MCP servers organized by category
│   ├── ai-llm/                   # AI & LLM Services
│   │   ├── anthropic-comprehensive-http-mcp
│   │   ├── context7-http-mcp
│   │   ├── gemini-http-mcp
│   │   ├── openai-tools-http-mcp
│   │   └── sequential-thinking-http-mcp
│   ├── cloud-infrastructure/      # Cloud & Infrastructure
│   │   ├── digitalocean-http-mcp
│   │   ├── docker-http-mcp
│   │   ├── hostinger-http-mcp
│   │   └── vercel-deploy-http-mcp
│   ├── design-tools/              # Design & UI/UX
│   │   ├── figma-mcp
│   │   ├── figma-mcp-application
│   │   ├── figma-mcp-ecommerce
│   │   ├── figma-mcp-marketing
│   │   ├── miro-http-mcp
│   │   ├── mui-http-mcp
│   │   ├── tailwind-ui-mcp
│   │   ├── uiux-design-http-mcp
│   │   ├── vercel-v0-mcp
│   │   └── vercel-v0-enhanced-mcp
│   ├── development-tools/         # Development & Coding
│   │   ├── claude-code-http-mcp
│   │   ├── documentation-analyzer-http-mcp
│   │   ├── git-advanced-http-mcp
│   │   ├── github-http-mcp
│   │   └── ngrok-http-mcp
│   ├── databases-storage/         # Databases & Storage
│   │   ├── airtable-http-mcp
│   │   ├── filesystem-http-mcp
│   │   ├── memory-http-mcp
│   │   ├── redis-http-mcp
│   │   └── supabase-http-mcp
│   ├── content-media/             # Content & Media
│   │   ├── brave-search-http-mcp
│   │   └── content-image-generation-mcp
│   ├── business-productivity/     # Business & Productivity
│   │   ├── ayrshare-mcp
│   │   ├── cats-mcp-server
│   │   ├── google-workspace-mcp
│   │   ├── signalhire
│   │   └── slack-http-mcp
│   ├── workflow-orchestration/    # Workflow & Orchestration
│   │   ├── everything-http-mcp
│   │   ├── routing-http-mcp
│   │   └── synapseai-workflow-mcp
│   └── web-automation/            # Web & Browser Automation
│       ├── browserbase-http-mcp
│       └── fetch-http-mcp
├── scripts/                       # Build and deployment scripts
├── templates/                     # Server templates
└── config/                        # Configuration files
```

**Note**: `.mcp.json` files are CLIENT-SIDE (go in projects that USE the server, not here)

## Creating a New MCP Server

Use the FastMCP plugin to create servers:

```bash
# From the project root
/fastmcp:new-server my-server
```

## Available Commands

The fastmcp plugin provides commands for building and configuring MCP servers:

- `/fastmcp:new-server <name>` - Create new FastMCP server (Python or TypeScript)
- `/fastmcp:new-client <name>` - Create new FastMCP client
- `/fastmcp:add-components [type]` - Add tools, resources, prompts, middleware
- `/fastmcp:add-auth [type]` - Add OAuth 2.1, JWT, or Bearer token authentication
- `/fastmcp:add-deployment [type]` - Configure STDIO, HTTP, or FastMCP Cloud deployment
- `/fastmcp:add-integration [type]` - Add FastAPI, OpenAPI, LLM platform integrations
- `/fastmcp:add-api-wrapper <collection>` - Generate MCP tools from Postman collections
- `/fastmcp:build-full-server <name>` - Build complete production-ready server
- `/fastmcp:test` - Generate and run comprehensive test suite

## Deployment Options

### 1. Local Development (STDIO)
For use with Claude Desktop, Cursor, or Claude Code:

```bash
# Test the server
python my-server/server.py

# Add to your IDE's .mcp.json
```

### 2. HTTP Server (Local/Remote)
For web-based access or remote clients:

```bash
# Run locally
python my-server/server.py  # Configure for HTTP in code

# Deploy to your infrastructure
```

### 3. FastMCP Cloud
For managed hosting:

```bash
# Deploy to FastMCP Cloud
# Use fastmcp.json configuration
```

See [plugins/fastmcp/docs/DEPLOYMENT.md](./plugins/fastmcp/docs/DEPLOYMENT.md) for detailed deployment strategies.

## Documentation

All FastMCP documentation is now consolidated in the plugin:

- **FastMCP Plugin**: `plugins/fastmcp/` (commands, agents, skills)
- **FastMCP SDK Docs**: `plugins/fastmcp/docs/fastmcp-documentation.md`
- **Deployment Guide**: `plugins/fastmcp/docs/DEPLOYMENT.md`
- **FastMCP Links**: `plugins/fastmcp/docs/fastmcp-links-organized.md`
- **FastMCP Website**: https://gofastmcp.com/
- **Templates**: `plugins/fastmcp/skills/mcp-server-config/templates/`

## Marketplace

This project is registered as the `mcp-servers` marketplace, providing the fastmcp plugin for building MCP servers. The plugin is automatically available when working in this directory.
