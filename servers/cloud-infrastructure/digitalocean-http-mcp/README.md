# Digital Ocean HTTP MCP Server

A comprehensive MCP server for managing Digital Ocean cloud infrastructure including droplets, databases, Kubernetes clusters, App Platform apps, and more.

## Features

### Current Tools (11 implemented)
- **Account Management**
  - `get_account_info` - Get account details and limits
  - `list_ssh_keys` - List SSH keys in account

- **Droplet Management**
  - `list_droplets` - List all droplets with filtering
  - `create_droplet` - Create new droplets
  - `manage_droplet` - Power operations (on/off/reboot)
  - `delete_droplet` - Delete droplets

- **Database Management**
  - `list_databases` - List managed database clusters
  - `create_database` - Create PostgreSQL, MySQL, Redis, MongoDB clusters

- **App Platform**
  - `list_apps` - List App Platform applications
  - `create_app` - Deploy new apps from spec

### Resources
- `usage_guide` - Critical usage documentation
- `regions` - Available DO regions
- `sizes` - Droplet sizes and pricing
- `images` - OS images and applications
- `examples/droplet_creation` - Example configurations

### Prompts
- `droplet_creation_guide` - Recommendations by use case
- `troubleshooting_guide` - Common issue solutions
- `migration_guide` - Migrate from other providers
- `cost_optimization` - Cost saving strategies
- `security_best_practices` - Security hardening

## Setup

### Environment Variables
```bash
# Required for real API access
export DIGITALOCEAN_API_TOKEN=your_token_here

# Optional - enable mock mode for testing
export DO_MOCK_MODE=true

# Optional - custom port (default: 8040)
export DIGITALOCEAN_MCP_PORT=8040
```

### Installation
```bash
cd servers/http/digitalocean-http-mcp
pip install -r requirements.txt
```

### Running the Server
```bash
# Production mode (requires API token)
python src/digitalocean_server.py

# Mock mode for testing
DO_MOCK_MODE=true python src/digitalocean_server.py
```

## Testing

### Run comprehensive tests
```bash
# In-memory testing with FastMCP Client
python test_digitalocean_direct.py

# CI/CD test suite
python test_ci.py
```

### Manual testing with curl
```bash
# Initialize connection
curl -X POST http://localhost:8040/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {
      "protocolVersion": "0.1.0",
      "capabilities": {},
      "clientInfo": {
        "name": "Test Client",
        "version": "1.0.0"
      }
    },
    "id": 1
  }'
```

## Usage Examples

### Create a Droplet
```python
result = await client.call_tool("create_droplet", {
    "name": "web-server-01",
    "region": "nyc3",
    "size": "s-2vcpu-2gb",
    "image": "ubuntu-22-04-x64",
    "ssh_keys": ["your-ssh-fingerprint"],
    "tags": ["production", "web"],
    "monitoring": True,
    "backups": True
})
```

### Create a Database
```python
result = await client.call_tool("create_database", {
    "name": "prod-db",
    "engine": "pg",
    "version": "15",
    "region": "nyc3",
    "size": "db-s-2vcpu-4gb",
    "num_nodes": 2
})
```

## TODO - Additional Tools Needed

### High Priority
- Kubernetes cluster management
- Load Balancer management  
- Firewall and networking tools
- Volumes/Block Storage tools

### Medium Priority
- Snapshots and Backups tools
- Domain/DNS management
- Monitoring/Alerts tools
- VPC management tools

### Low Priority
- Container Registry tools
- Spaces (S3-compatible storage) tools

## Architecture

Built with FastMCP for streamable-http transport, supporting:
- Server-Sent Events (SSE) for real-time updates
- Mock mode for testing without API access
- Comprehensive error handling
- Rate limit awareness

## Contributing

1. Add new tools to appropriate classes (DropletTools, DatabaseTools, etc.)
2. Include mock responses for testing
3. Update test_ci.py with new tools
4. Document in README