# MCP Server Deployment Strategy

## The Problem: FastMCP Cloud vs Monorepo

**FastMCP Cloud Requirement**: One server per GitHub repository
**Our Setup**: Multiple servers in `mcp-servers/` directory (monorepo)

## Solution: Choose Your Deployment Strategy

### Option 1: STDIO/HTTP Only (Recommended for Development)
**When to use**: Development, internal tools, testing

**Setup**: Keep all servers in `mcp-servers/` monorepo
```
mcp-servers/
├── server-1/
│   ├── server.py
│   └── requirements.txt
├── server-2/
└── ...
```

**Deployment**:
- **STDIO**: Run locally for Claude Desktop/Cursor/Claude Code
- **HTTP**: Run on your own infrastructure (localhost, VPS, AWS, etc.)

**Client Configuration** (in your `.mcp.json`):
```json
{
  "mcpServers": {
    "server-1": {
      "command": "python",
      "args": ["mcp-servers/server-1/server.py"]
    },
    "server-2": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### Option 2: Split for FastMCP Cloud (Production Hosting)
**When to use**: Production servers, public APIs, managed hosting

**Process**:
1. Develop servers in `mcp-servers/` monorepo
2. When ready for production, extract to separate repos
3. Deploy each repo to FastMCP Cloud

**Extraction Script** (create when needed):
```bash
# Extract server-1 to its own repo
./scripts/extract-server-to-repo.sh server-1
# Creates ../mcp-server-1/ with git initialized
```

**Result**:
```
mcp-servers/server-1/          # Development (stays here)
../mcp-server-1/               # Production (separate repo for FastMCP Cloud)
  ├── server.py
  ├── fastmcp.json
  ├── requirements.txt
  └── README.md
```

**Client Configuration** (after deployment):
```json
{
  "mcpServers": {
    "server-1": {
      "url": "https://server-1.fastmcp.app/mcp"
    }
  }
}
```

### Option 3: Hybrid Approach (Best of Both Worlds)
**Recommended for most projects**

**Development**:
- Build and test all servers in `mcp-servers/` monorepo
- Use STDIO for local development
- Use HTTP for local testing between services

**Production**:
- Only extract servers that need public/managed hosting
- Keep internal-only servers in monorepo, deploy to your infrastructure
- Use FastMCP Cloud only for servers that benefit from it

**Example**:
```
mcp-servers/
├── internal-server/           # Stays here, deploy via HTTP to your VPS
├── public-api/               # Extract to separate repo → FastMCP Cloud
└── dev-tools/                # Stays here, STDIO only
```

## Deployment Target Decision Matrix

| Server Type | Development | Production | Deployment |
|-------------|-------------|------------|------------|
| Internal tools | STDIO | HTTP (your infra) | Keep in monorepo |
| Public APIs | STDIO | FastMCP Cloud | Extract to separate repo |
| Team services | STDIO | HTTP (your infra) | Keep in monorepo |
| Customer-facing | STDIO | FastMCP Cloud | Extract to separate repo |

## Configuration Files by Deployment

### STDIO (Local Development)
**Server**: Just `server.py` in monorepo
**Client**: `.mcp.json` with `command` and `args`
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["mcp-servers/my-server/server.py"]
    }
  }
}
```

### HTTP (Your Infrastructure)
**Server**: `server.py` configured for HTTP transport in monorepo
**Client**: `.mcp.json` with `url`
```json
{
  "mcpServers": {
    "my-server": {
      "url": "http://your-server.com:8000/mcp"
    }
  }
}
```

### FastMCP Cloud (Managed Hosting)
**Server**: Separate GitHub repo with `fastmcp.json`
**Client**: `.mcp.json` with FastMCP Cloud URL
```json
{
  "mcpServers": {
    "my-server": {
      "url": "https://my-server.fastmcp.app/mcp"
    }
  }
}
```

## Recommended Workflow

1. **Develop in monorepo** (`mcp-servers/`)
   - Use `/fastmcp:new-server`
   - Add features with `/fastmcp:add-components`, etc.
   - Test locally with STDIO

2. **Configure deployment** with `/fastmcp:add-deployment`
   - Select STDIO + HTTP for development
   - Select FastMCP Cloud only when ready for production

3. **Deploy based on needs**:
   - **Keep internal**: Deploy HTTP to your infrastructure
   - **Go public**: Extract to separate repo, push to FastMCP Cloud

4. **Update client configs** in your projects
   - Development: Point to STDIO (local files)
   - Staging: Point to HTTP (your test server)
   - Production: Point to FastMCP Cloud URL

## Why This Approach?

**Advantages**:
- ✅ Develop all servers together in one repo (easy to share code/utils)
- ✅ No overhead for servers that don't need FastMCP Cloud
- ✅ Extract only when needed for production
- ✅ Keep development workflow simple

**FastMCP Cloud is optional** - it's for:
- Public-facing APIs
- High-availability requirements
- Automatic scaling/monitoring
- Free hosting for personal projects

Most internal servers can stay in monorepo and deploy to your own infrastructure via HTTP.
