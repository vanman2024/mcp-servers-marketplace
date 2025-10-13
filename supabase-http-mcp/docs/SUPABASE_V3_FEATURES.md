# Supabase MCP Server v3.0.0 Features

## Overview
The v3.0.0 release is a major enhancement that fixes critical issues and adds AI/Vector and GraphQL support.

## Fixed Issues (from v2)
1. ✅ **Data Operations** - Fixed insert_data, select_data, update_data, delete_data using SQL via Management API
2. ✅ **Pagination** - Added pagination to extract_complete_schema (was returning 310k tokens)
3. ✅ **Edge Functions** - Full implementation of all 8 Edge Function tools
4. ✅ **Prompts** - Added 5 workflow prompts for common Supabase tasks

## New Features in v3

### Vector/AI Operations (7 new tools)
1. `enable_pgvector` - Enable pgvector extension
2. `create_vector_table` - Create tables with vector columns
3. `create_vector_index` - Create HNSW or IVFFlat indexes
4. `vector_search` - Perform similarity searches
5. `hybrid_search` - Combine keyword and vector search
6. `setup_automatic_embeddings` - Auto-generate embeddings with OpenAI
7. `analyze_vector_distribution` - Analyze vector data distribution

### GraphQL Operations (6 new tools)
1. `enable_graphql` - Enable pg_graphql extension
2. `create_graphql_schema` - Configure table exposure
3. `graphql_introspection` - Get schema introspection
4. `execute_graphql_query` - Execute GraphQL queries
5. `create_graphql_function` - Create custom GraphQL functions
6. `setup_graphql_subscriptions` - Enable real-time subscriptions

### Prompts (1 new)
- `setup_vector_search` - Guide for implementing vector search

## Total Tool Count
- **v2.0.0**: 22 tools
- **v3.0.0**: 35 tools (58% increase)

## Key Improvements

### Data Operations Fix
```python
# Now uses Management API SQL execution
async def insert_data(
    table: str,
    data: Union[Dict, List[Dict], str],
    project_id: str,
    returning: List[str] = ["*"],
    on_conflict: Optional[str] = None
) -> Dict[str, Any]:
    # Builds SQL INSERT query dynamically
    # Handles single or batch inserts
    # Supports UPSERT with on_conflict
```

### Vector Search Implementation
```python
# Supports all major distance metrics
async def vector_search(
    project_id: str,
    table_name: str,
    query_embedding: List[float],
    limit: int = 10,
    distance_method: str = "cosine",  # cosine, l2, ip
    metadata_filter: Optional[Dict] = None
) -> Dict[str, Any]:
    # Uses proper PostgreSQL vector operators
    # Supports metadata filtering
    # Returns distance scores
```

### GraphQL Integration
```python
# Execute GraphQL directly via SQL
async def execute_graphql_query(
    project_id: str,
    query: str,
    variables: Optional[Dict] = None
) -> Dict[str, Any]:
    # Uses pg_graphql's resolve function
    # Supports variables
    # Returns GraphQL response
```

## Testing Status
- Core functionality implemented
- Ready for deployment and testing
- All tools follow Supabase best practices

## Migration Notes
To upgrade from v2 to v3:
1. Replace `supabase_server.py` with `supabase_server_v3.py`
2. Restart the MCP server
3. All existing tools remain compatible
4. New tools are immediately available