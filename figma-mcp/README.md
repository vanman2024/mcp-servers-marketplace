# Figma MCP Server

A comprehensive HTTP MCP server for design-to-code workflow using Figma API, ShadCN components, and Supabase storage.

## Features

- **Figma Integration**: Connect to Figma files and extract component data
- **Component Normalization**: Convert Figma designs to standardized JSON format
- **ShadCN Mapping**: Automatically map Figma components to ShadCN UI library
- **Supabase Storage**: Persistent storage for design components and metadata
- **Design Tokens**: Extract and manage design tokens (colors, spacing, typography)
- **Real-time Sync**: Keep components synchronized with Figma source
- **Search & Filter**: Find components by name, type, tags, and theme
- **Variant Support**: Handle component variants and states

## Quick Start

### Prerequisites

- Python 3.8+
- Figma Personal Access Token
- Supabase project with database

### Installation

1. Clone the repository and navigate to the Figma MCP server directory:
```bash
cd servers/http/figma-mcp
```

2. Set up environment variables:
```bash
export FIGMA_ACCESS_TOKEN="your_figma_token"
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_SERVICE_KEY="your_supabase_service_key"
```

3. Run the database migration:
```bash
# Execute the SQL in migrations/001_initial_schema.sql in your Supabase dashboard
```

4. Start the server:
```bash
./start.sh
```

The server will be available at `http://localhost:8030`

## MCP Tools

### `register_design_file`
Register a Figma design file for component extraction.

```python
await register_design_file(
    file_url="https://www.figma.com/file/ABC123/My-Design-File",
    name="My Design System",
    description="Components for our app"
)
```

### `import_components`
Import components from a registered Figma file.

```python
await import_components(
    file_key="ABC123",
    component_filter="Button",  # Optional: filter by component name
    include_variants=True
)
```

### `get_component_layout`
Get normalized layout data for a specific component.

```python
await get_component_layout(
    component_name="Primary Button",
    file_key="ABC123",  # Optional: scope to specific file
    format="shadcn"     # Options: "shadcn", "raw", "figma"
)
```

### `search_components`
Search for components with filters.

```python
await search_components(
    query="button",
    tags=["primary", "interactive"],
    component_type="button",
    theme="light",
    limit=20
)
```

### `sync_design_changes`
Sync design changes from Figma source.

```python
await sync_design_changes(
    file_key="ABC123",
    force=False  # Set to True to force sync
)
```

### `health_check`
Check server health and connectivity.

```python
await health_check()
```

## Database Schema

The server uses Supabase with the following main tables:

- **`design_files`**: Registered Figma files with metadata
- **`design_components`**: Individual components with normalized JSON layouts
- **`component_variants`**: Different states and variations of components
- **`design_tokens`**: Global design tokens (colors, spacing, typography)
- **`component_usage`**: Analytics tracking for component usage

## ShadCN Component Mapping

The server automatically maps Figma components to ShadCN UI components based on:

- Component naming patterns
- Visual structure analysis
- Layout properties
- Design patterns

### Supported ShadCN Components

- Button (with variants: default, secondary, destructive, outline, ghost, link)
- Card (with subcomponents: CardHeader, CardContent, CardFooter)
- Input (with placeholder detection)
- Select (with dropdown detection)
- Checkbox, Radio, Switch
- Badge, Avatar, Dialog, Alert
- Tabs, Accordion, Separator, Tooltip
- Form components

## Configuration

Configuration is handled through environment variables and `config.json`:

```json
{
    "server_name": "figma-design",
    "port": 8030,
    "environment_variables": {
        "FIGMA_ACCESS_TOKEN": "Required",
        "SUPABASE_URL": "Required",
        "SUPABASE_SERVICE_KEY": "Required"
    }
}
```

## Development

### Running Tests

```bash
cd servers/http/figma-mcp
python -m pytest tests/ -v --cov=src --cov-report=html
```

### Test Coverage

The test suite includes:
- Unit tests for all modules
- Integration tests with mocked APIs
- Component mapping tests
- Design normalization tests
- Error handling tests

Target coverage: 90%+

### Project Structure

```
servers/http/figma-mcp/
├── src/
│   ├── figma_server.py        # Main FastMCP server
│   ├── figma_client.py        # Figma API client
│   ├── supabase_storage.py    # Database operations
│   ├── design_normalizer.py   # Component normalization
│   └── component_mapper.py    # ShadCN mapping
├── tests/
│   ├── test_figma_client.py
│   ├── test_component_mapper.py
│   ├── test_design_normalizer.py
│   └── conftest.py
├── migrations/
│   └── 001_initial_schema.sql
├── requirements.txt
├── config.json
├── start.sh
└── README.md
```

## Error Handling

The server includes comprehensive error handling:

- **Rate Limiting**: Automatic retry logic for Figma API rate limits
- **Validation**: Input validation for all MCP tools
- **Graceful Degradation**: Partial data return when possible
- **Logging**: Detailed logging for debugging and monitoring
- **Health Checks**: Endpoint to verify system health

## Performance Optimization

- **Caching**: Redis integration for hot data caching
- **Pagination**: Cursor-based pagination for large datasets
- **Async Operations**: Full async/await support for high performance
- **Connection Pooling**: Efficient database connection management

## License

MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Troubleshooting

### Authentication Issues

#### "Figma authentication token not found"
This error means the server can't find your Figma API token. 

**Solution:**
1. Set the environment variable:
   ```bash
   export FIGMA_PAT="your-figma-personal-access-token"
   # OR
   export FIGMA_ACCESS_TOKEN="your-figma-token"
   ```

2. Or create a `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env and add your tokens
   ```

#### "Figma API connection failed: 401 Unauthorized"
Your token is invalid or expired.

**Solution:**
1. Generate a new token at https://www.figma.com/developers/access-tokens
2. Ensure the token has "File content" read permission
3. Tokens expire after 90 days of inactivity

#### "Figma token may have incorrect format"
The token doesn't match expected Figma token patterns.

**Solution:**
- Figma PATs should start with `figd_` or `figp_`
- Make sure you copied the entire token
- Don't include quotes in the environment variable value

### Supabase Connection Issues

#### "SUPABASE_SERVICE_KEY not found"
The server needs your Supabase service key to access the database.

**Solution:**
1. Go to https://app.supabase.com
2. Select your project → Settings → API
3. Copy the `service_role` key (NOT the `anon` key!)
4. Set it: `export SUPABASE_SERVICE_KEY="your-key"`

#### "Database tables not found"
The required tables haven't been created in Supabase.

**Solution:**
1. Open your Supabase project dashboard
2. Go to SQL Editor → New Query
3. Copy and run the contents of `migrations/001_initial_schema.sql`
4. Click "Run" to create the tables

#### "Invalid API key"
You're using the wrong Supabase key.

**Solution:**
- Make sure you're using the `service_role` key, not the `anon`/public key
- The service_role key has full database access
- It's much longer than the anon key (200+ characters)

### Debugging Tools

#### Configuration Validator
Test your configuration before starting the server:
```bash
cd servers/http/figma-mcp
python validate_config.py
```

This will:
- Check all environment variables
- Validate token formats
- Test API connections
- Provide specific error messages

#### Health Check Endpoint
Once the server is running, check its health:
```bash
curl http://localhost:8031/health
```

This returns detailed status including:
- Token validation status
- API connectivity
- Error hints for common issues

#### Debug Mode
Enable verbose logging:
```bash
export FIGMA_DEBUG=true
./start.sh
```

### Common Issues

#### Port Already in Use
If port 8031 is busy:
```bash
export FIGMA_MCP_PORT=8032
./start.sh
```

#### Virtual Environment Issues
If you see Python import errors:
```bash
rm -rf venv
./start.sh  # Will recreate venv
```

#### Network/Proxy Issues
If behind a corporate proxy:
```bash
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
```

### Quick Start Checklist

1. **Copy example config:**
   ```bash
   cp .env.example .env
   ```

2. **Add your tokens to .env:**
   - FIGMA_PAT from https://www.figma.com/developers/access-tokens
   - SUPABASE_URL from your Supabase project
   - SUPABASE_SERVICE_KEY (service_role key)

3. **Validate configuration:**
   ```bash
   python validate_config.py
   ```

4. **Run database migrations** in Supabase SQL editor

5. **Start the server:**
   ```bash
   ./start.sh
   ```

6. **Check health:**
   ```bash
   curl http://localhost:8031/health
   ```

## Support

For issues and questions:
- Run the configuration validator first: `python validate_config.py`
- Check the detailed troubleshooting guide above
- Enable debug mode for verbose logging
- Create an issue in the GitHub repository with:
  - Error messages from the validator
  - Health check output
  - Debug logs (with tokens masked)