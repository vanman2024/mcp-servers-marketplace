# Supabase HTTP MCP Server

Complete FastMCP server for Supabase database operations, storage, auth, and edge functions via HTTP API.

## Server Organization

### 🛠️ Tools (8 main tools)
- **Organization Management**: `list_organizations`, `get_organization` - Manage Supabase organizations
- **Project Management**: `list_projects`, `get_project` - Handle project operations  
- **Database Operations**: `execute_sql` - Execute raw SQL queries with fallback support
- **Schema Analysis**: `extract_complete_schema` - Complete database schema extraction with pagination
- **Data Operations**: `insert_data`, `select_data` - CRUD operations with Supabase client
- **Configuration**: Project and auth configuration management

### 📚 Resources (3 resource endpoints)
- **Configuration**: `supabase://config` - Server capabilities and environment status
- **Examples**: `supabase://examples/{operation}` - Usage examples for SQL, vector, storage operations
- **Best Practices**: `supabase://best-practices` - Development guidelines and recommendations

### 💡 Prompts (5 specialized prompts)
- **Schema Analysis**: `analyze_database_schema` - Database optimization and analysis
- **Vector Database**: `design_vector_database` - Vector search implementation with pgvector
- **Performance**: `optimize_supabase_performance` - Performance tuning and optimization
- **Edge Functions**: `setup_edge_function_workflow` - Edge Function development and deployment
- **Migration**: `migrate_to_supabase` - Database migration planning and execution

## Features

- **Class-based architecture** to prevent 'FunctionTool' object is not callable errors
- **Comprehensive error handling** with context-aware logging
- **SQL execution fallbacks** for maximum compatibility
- **Schema extraction** with pagination and filtering
- **Project validation** and access control
- **Environment configuration** with optional access tokens

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export SUPABASE_URL=https://your-project.supabase.co
   export SUPABASE_SERVICE_KEY=your_service_key
   export SUPABASE_ACCESS_TOKEN=your_access_token  # Optional
   export SUPABASE_MCP_PORT=8034                   # Optional
   ```

3. Run the server:
   ```bash
   python src/supabase_server_v3_fixed_clean.py
   ```

## Usage with Claude

1. Add to Claude:
   ```bash
   claude mcp add --transport http supabase-http http://localhost:8034
   ```

2. Use tools:
   - List: `/mcp`
   - Execute: `/mcp__supabase__execute_sql "project_id" "SELECT 1;"`
   - Schema: `/mcp__supabase__extract_complete_schema "project_id"`

3. Access resources:
   ```bash
   /mcp_resource supabase://config
   /mcp_resource supabase://examples/sql
   /mcp_resource supabase://best-practices
   ```

## Testing Status

Based on comprehensive testing (see SUPABASE_MCP_TEST_RESULTS.md):
- ✅ **23 tools fully working** (Organization, Project, Database, Storage basic, Edge Functions)
- ❌ **34 tools with issues** (Vector, GraphQL, SynapseAI, Advanced storage)
- **Workaround**: Most functionality achievable through `execute_sql` and direct API calls

## Architecture

The server uses a hybrid pattern:
- **Standalone tools** with `@mcp.tool()` for simple operations
- **Class-based tools** with `mcp.tool(instance.method)` for complex operations that call other functions
- **Helper functions** (not decorated) for shared logic between tools

This prevents the common FastMCP error where decorated tools try to call other decorated tools.

## Development

To add new tools:
1. Simple tools: Use `@mcp.tool()` decorator directly
2. Complex tools: Add to `SupabaseComplexOperations` class and register with `mcp.tool(instance.method)`
3. Shared logic: Create helper functions (not decorated) that can be called by both patterns

## Environment Variables

- `SUPABASE_URL` - Required: Your Supabase project URL
- `SUPABASE_SERVICE_KEY` - Required: Service role key for admin operations  
- `SUPABASE_ACCESS_TOKEN` - Optional: User access token for organization/project operations
- `SUPABASE_MCP_PORT` - Optional: Server port (default: 8034)