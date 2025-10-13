# Supabase MCP Server v3

A comprehensive Model Context Protocol (MCP) server for Supabase that provides 55 tools for managing all aspects of Supabase projects.

## Features

### ✅ Complete Coverage (55 Tools - 100% Working)

- **Organization Management** (2 tools)
- **Project Management** (4 tools)
- **Database Operations** (8 tools)
- **Edge Functions** (8 tools)
- **Storage Operations** (5 tools)
- **Authentication** (4 tools)
- **Postgres Configuration** (2 tools)
- **Vector Operations** (7 tools)
- **GraphQL Support** (6 tools)
- **SynapseAI Integration** (5 tools)
- **Database Branching** (4 tools)

## Installation

1. Install dependencies:
```bash
pip install fastmcp supabase httpx
```

2. Set environment variables:
```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_SERVICE_KEY="your-service-key"
export SUPABASE_ACCESS_TOKEN="your-access-token"  # For Management API
```

## Usage

### Running the Server

```bash
cd servers/http/supabase-http-mcp/src
python supabase_server_v3.py
```

The server will start on `http://localhost:8000`.

### Testing

Run the comprehensive test suite:
```bash
python test_all_55_tools.py
```

This will test all 55 tools and generate a detailed JSON report.

## Tools Overview

### Database Operations
- `execute_sql` - Run SQL queries
- `apply_migration` - Apply database migrations
- `insert_data`, `select_data`, `update_data`, `delete_data` - CRUD operations
- `extract_complete_schema` - Get full database schema
- `create_function` - Create SQL functions

### Edge Functions
- `deploy_function` - Deploy serverless functions
- `list_functions`, `get_function`, `delete_function` - Manage functions
- `update_function` - Update function configuration
- `get_deployment_status` - Check deployment status

### Storage
- `create_bucket`, `list_buckets` - Manage storage buckets
- `upload_file`, `download_file` - File operations

### Vector Operations (pgvector)
- `enable_pgvector` - Enable vector extension
- `create_vector_table` - Create tables with embeddings
- `create_vector_index` - Create HNSW/IVFFlat indexes
- `vector_search`, `hybrid_search` - Similarity search

### GraphQL
- `enable_graphql` - Enable GraphQL extension
- `create_graphql_schema` - Set up GraphQL schemas
- `execute_graphql_query` - Run GraphQL queries
- `setup_graphql_subscriptions` - Configure real-time subscriptions

### Database Branching
- `create_branch`, `list_branches`, `delete_branch` - Manage preview branches
- `create_database_branch` - Create isolated database environments

## API Endpoints

The server uses:
- Supabase Management API: `https://api.supabase.com/v1`
- Project-specific APIs for data operations
- Direct database connections for SQL operations

## Environment Requirements

- Python 3.8+
- Valid Supabase project
- Service role key (for admin operations)
- Management API access token (for project management)

## Error Handling

The server includes comprehensive error handling with:
- Automatic retries for transient failures
- SQL fallbacks for unavailable APIs
- Detailed error messages for debugging
- Timeout handling for long-running operations (60s for branch creation)

## Test Results

Latest test run: **100% success rate** (55/55 tools passing)
- Test results saved in: `test_all_55_tools_v3_all_*.json`

## License

MIT License