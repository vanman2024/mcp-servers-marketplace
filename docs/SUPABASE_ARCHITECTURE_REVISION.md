# Supabase MCP Server Architecture Revision

## Current Issue
We've been implementing raw SQL queries and Management API calls instead of using Supabase's auto-generated APIs and official Python SDK.

## Supabase's Actual Architecture

### 1. Data API (PostgREST)
- **Auto-generated REST endpoints** from database schema
- No need to manually implement CRUD operations
- Handles filtering, sorting, pagination automatically
- Examples:
  ```
  GET /rest/v1/users?select=*
  POST /rest/v1/users
  PATCH /rest/v1/users?id=eq.1
  DELETE /rest/v1/users?id=eq.1
  ```

### 2. Python SDK (supabase-py)
- **Official client** that wraps all APIs
- Clean, Pythonic interface:
  ```python
  # Instead of our complex SQL building:
  supabase.table('users').insert({"name": "John"}).execute()
  supabase.table('users').select("*").eq('id', 1).execute()
  supabase.table('users').update({"name": "Jane"}).eq('id', 1).execute()
  supabase.table('users').delete().eq('id', 1).execute()
  ```

### 3. GraphQL API
- Auto-generated from database schema
- Single endpoint with introspection
- No manual schema definition needed

### 4. Vector/AI Operations
- Built-in pgvector support
- Dedicated vector operations through SDK

### 5. Management API
- For project/organization management
- Separate from data operations

## Proposed New Architecture

### Server Split Strategy

1. **supabase-data-http-mcp** (Data Operations)
   - Use Python SDK for ALL data operations
   - No manual SQL building
   - Tools: insert, select, update, delete, upsert, rpc
   - Leverage SDK's built-in filtering, joins, etc.

2. **supabase-management-http-mcp** (Project Management)
   - Organizations, projects, auth config
   - Use Management API directly
   - Tools: list_projects, create_project, etc.

3. **supabase-storage-http-mcp** (File Storage)
   - Use SDK's storage client
   - Tools: upload, download, list_buckets, create_bucket

4. **supabase-vector-http-mcp** (AI/Vector Operations)
   - Use SDK's vector operations
   - Tools: vector_search, create_embedding, etc.

5. **supabase-edge-http-mcp** (Edge Functions)
   - Deploy and manage edge functions
   - Tools: deploy_function, invoke_function, etc.

6. **supabase-realtime-http-mcp** (Realtime Operations)
   - Manage realtime subscriptions
   - Tools: enable_realtime, configure_realtime, etc.

## Benefits of This Approach

1. **Massively reduced code** - No SQL building, no manual API handling
2. **Better performance** - SDK handles connection pooling, retries
3. **Automatic features** - Filtering, pagination, joins work out of the box
4. **Type safety** - SDK provides proper typing
5. **Error handling** - SDK handles common errors
6. **Future-proof** - Updates to Supabase automatically available

## Migration Plan

1. Create new simplified servers using SDK
2. Test thoroughly with existing test suite
3. Deprecate v3 monolithic server
4. Update documentation

## Example: New Data Server Implementation

```python
from supabase import create_client, Client
from fastmcp import FastMCP

mcp = FastMCP("supabase-data")
supabase: Client = create_client(url, key)

@mcp.tool()
async def select_data(
    table: str,
    columns: str = "*",
    filters: Optional[Dict[str, Any]] = None,
    order_by: Optional[str] = None,
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """Select data using Supabase SDK"""
    query = supabase.table(table).select(columns)
    
    # Apply filters
    if filters:
        for key, value in filters.items():
            if isinstance(value, dict):
                # Handle operators like {'gt': 5}
                for op, val in value.items():
                    query = getattr(query, op)(key, val)
            else:
                query = query.eq(key, value)
    
    if order_by:
        query = query.order(order_by)
    
    if limit:
        query = query.limit(limit)
    
    return query.execute().dict()
```

This is MUCH simpler than our current 100+ line implementations!