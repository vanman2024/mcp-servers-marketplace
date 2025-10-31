# Filesystem MCP Server (HTTP)

Secure filesystem operations server using FastMCP with HTTP transport.

Converted from the official MCP TypeScript stdio server to Python HTTP implementation.

## Features

- **Secure file operations** with path validation
- **HTTP transport** using FastMCP with streamable-http
- **Multiple file operations** in parallel
- **Advanced editing** with pattern matching
- **Recursive search** with exclude patterns
- **Detailed metadata** retrieval

## Tools

### File Operations
- `read_file(path)` - Read complete file contents
- `read_multiple_files(paths)` - Read multiple files simultaneously
- `write_file(path, content)` - Create or overwrite files
- `edit_file(path, edits, dry_run?)` - Advanced pattern-based editing

### Directory Operations
- `create_directory(path)` - Create directories (with parents)
- `list_directory(path)` - List directory contents with metadata
- `move_file(source, destination)` - Move/rename files and directories

### Search Operations
- `search_files(path, pattern, exclude_patterns?)` - Recursive search
- `get_file_info(path)` - Detailed file/directory metadata

## Security

- **Path validation**: All operations restricted to allowed directories
- **Symlink safety**: Prevents directory traversal attacks
- **Text file detection**: Binary file protection
- **Error handling**: Comprehensive error messages

## Configuration

### Environment Variables

```bash
# Allowed directories (colon-separated)
FILESYSTEM_ALLOWED_DIRS="/home/user/project:/tmp/safe"

# Server port
FILESYSTEM_MCP_PORT=8001
```

### Default Settings
- **Default directories**: Current directory (`.`)
- **Default port**: 8001
- **Transport**: streamable-http

## Installation

```bash
# Install dependencies
pip install fastmcp python-dotenv uvicorn

# Run server
python src/filesystem_server.py
```

## Usage Examples

### Read a file
```python
# Tool call
{
    "name": "read_file",
    "arguments": {
        "path": "src/example.py"
    }
}
```

### Edit multiple sections
```python
# Tool call
{
    "name": "edit_file",
    "arguments": {
        "path": "config.yaml",
        "edits": [
            {
                "oldText": "debug: false",
                "newText": "debug: true"
            },
            {
                "oldText": "port: 3000",
                "newText": "port: 8080"
            }
        ]
    }
}
```

### Search with exclusions
```python
# Tool call
{
    "name": "search_files",
    "arguments": {
        "path": "src/",
        "pattern": "*.py",
        "exclude_patterns": ["__pycache__", "*.pyc"]
    }
}
```

## HTTP Endpoints

The server runs on `http://localhost:8001` with MCP tools available at:
- `POST /tools/call` - Execute MCP tools
- `GET /tools/list` - List available tools
- `GET /health` - Health check

## Conversion Notes

This server maintains 100% API compatibility with the original TypeScript stdio version while adding:

- **HTTP transport** for better integration
- **Async/await** throughout for performance
- **Enhanced error messages** with context
- **Environment-based configuration**
- **Docker-ready** deployment

## Testing

```bash
# Test basic functionality
curl -X POST http://localhost:8001/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "read_file",
    "arguments": {"path": "README.md"}
  }'
```