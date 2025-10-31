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
│   └── marketplace.json        # Marketplace registry
├── plugins/
│   └── fastmcp/                # FastMCP plugin for building MCP servers
│       ├── commands/           # /fastmcp:* slash commands
│       ├── agents/             # Specialized agents (setup, verifier, etc.)
│       ├── skills/             # Reusable templates and scripts
│       └── docs/               # FastMCP documentation
│           ├── DEPLOYMENT.md   # Deployment strategy guide
│           ├── fastmcp-documentation.md
│           └── fastmcp-links-organized.md
├── docs/                       # Project-level documentation
├── my-server/
│   ├── server.py               # Main server file
│   ├── fastmcp.json            # (Optional) FastMCP Cloud deployment config
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variables template
│   └── README.md               # Server documentation
└── another-server/
    └── ...
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
