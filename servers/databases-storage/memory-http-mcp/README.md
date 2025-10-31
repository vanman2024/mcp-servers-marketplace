# Memory MCP Server (HTTP)

Knowledge graph system for persistent information storage using FastMCP with HTTP transport.

Converted from the official MCP TypeScript stdio server to Python HTTP implementation.

## Features

- **Knowledge graph storage** with entities and relations
- **Persistent memory** across sessions (JSON file storage)
- **HTTP transport** using FastMCP with streamable-http
- **Rich search** capabilities across names, types, and observations
- **Thread-safe operations** for concurrent access
- **Atomic saves** to prevent data corruption

## Tools

### Entity Management
- `create_entities(entities)` - Create new entities with observations
- `add_observations(observations)` - Add observations to existing entities
- `delete_entities(entity_names)` - Delete entities and their relations
- `delete_observations(deletions)` - Remove specific observations

### Relation Management
- `create_relations(relations)` - Create relations between entities
- `delete_relations(relations)` - Remove specific relations

### Query Operations
- `read_graph()` - Read the entire knowledge graph
- `search_nodes(query)` - Search entities by name, type, or observations
- `open_nodes(names)` - Get specific entities with their relations

## Data Model

### Entities
```python
{
    "name": "Claude",
    "entityType": "AI Assistant",
    "observations": [
        "Helps with coding",
        "Understands context",
        "Maintains memory"
    ]
}
```

### Relations
```python
{
    "from": "Claude",
    "to": "MCP Protocol",
    "relationType": "implements"
}
```

## Configuration

### Environment Variables

```bash
# Path to persistent graph storage
MEMORY_GRAPH_PATH="/home/user/.mcp-memory-graph.json"

# Server port
MEMORY_MCP_PORT=8002
```

### Default Settings
- **Default graph path**: `~/.mcp-memory-graph.json`
- **Default port**: 8002
- **Transport**: streamable-http

## Installation

```bash
# Install dependencies
pip install fastmcp python-dotenv uvicorn

# Run server
python src/memory_server.py
```

## Usage Examples

### Create a knowledge graph
```python
# Create entities
{
    "name": "create_entities",
    "arguments": {
        "entities": [
            {
                "name": "DevLoop Project",
                "entityType": "Project",
                "observations": ["Uses MCP servers", "Automates development"]
            },
            {
                "name": "FastMCP",
                "entityType": "Framework",
                "observations": ["HTTP transport", "Python-based"]
            }
        ]
    }
}

# Create relations
{
    "name": "create_relations",
    "arguments": {
        "relations": [
            {
                "from": "DevLoop Project",
                "to": "FastMCP",
                "relationType": "uses"
            }
        ]
    }
}
```

### Search the graph
```python
# Search for nodes
{
    "name": "search_nodes",
    "arguments": {
        "query": "MCP"
    }
}

# Open specific nodes with relations
{
    "name": "open_nodes",
    "arguments": {
        "names": ["DevLoop Project", "FastMCP"]
    }
}
```

## HTTP Endpoints

The server runs on `http://localhost:8002` with MCP tools available at:
- `POST /tools/call` - Execute MCP tools
- `GET /tools/list` - List available tools
- `GET /health` - Health check

## Persistence

The knowledge graph is automatically saved to disk after each modification:
- **Atomic writes** using temporary files
- **JSON format** for easy inspection and backup
- **Thread-safe** operations prevent corruption
- **Automatic loading** on server restart

## Conversion Notes

This server maintains 100% API compatibility with the original TypeScript stdio version while adding:

- **HTTP transport** for web integration
- **Thread safety** for concurrent operations
- **Better error handling** with detailed messages
- **Relevance scoring** in search results
- **Metadata** in graph responses

## Testing

```bash
# Create an entity
curl -X POST http://localhost:8002/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "create_entities",
    "arguments": {
        "entities": [{
            "name": "Test Entity",
            "entityType": "Test",
            "observations": ["This is a test"]
        }]
    }
  }'

# Read the graph
curl -X POST http://localhost:8002/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "read_graph",
    "arguments": {}
  }'
```