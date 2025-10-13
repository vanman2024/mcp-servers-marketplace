# Reuse Guide: What to Copy from Supabase v3 Server

## For Instance 1 (Data & Storage) - US

### Copy These Storage Functions Directly:
```python
# From line ~700-850 in v3
- create_bucket()
- list_buckets()  
- upload_file()
- download_file()
```

### Replace These with SDK:
- ❌ insert_data() - Use SDK instead
- ❌ update_data() - Use SDK instead
- ❌ delete_data() - Use SDK instead
- ❌ select_data() - Use SDK instead

## For Instance 2 (Management & Schema)

### Copy These Management Functions Directly:
```python
# The entire management_api_request() helper (line ~82)
# All these tools (lines ~1000-1400):
- list_organizations()
- get_organization()
- create_organization()
- list_projects()
- get_project()
- create_project() 
- pause_project()
- restore_project()
- get_auth_config()
- update_auth_config()
```

### Copy These Schema Functions:
```python
# Lines ~200-280
- execute_sql() - Still needed for schema ops
- apply_migration()
- create_database_branch()
- extract_complete_schema()
```

## For Instance 3 (Realtime, Vector, Edge)

### Copy These Edge Functions:
```python
# Lines ~1600-1800
- create_function()
- update_function()
- delete_function()
- list_functions()
- invoke_function()
```

### Copy These Vector Functions:
```python
# Lines ~1900-2000
- create_vector_table()
- Basic vector operation patterns
```

### Build New for Realtime:
- Realtime needs SDK-based implementation
- Don't copy any SQL-based realtime code

## Shared Utilities to Extract

### Copy to supabase-common:
```python
# Response formatting patterns
# Timeout configurations
# Error response structures
# The array_params_fix import pattern
```

## Testing Approach

Since Instance 1 (us) will run all tests:

1. Create `/servers/http/supabase-tests/` directory
2. Test each server individually first
3. Run comprehensive integration tests
4. Use the existing test patterns from v3

## Quick Copy Commands

For Instance 2:
```bash
# Extract management functions
sed -n '1000,1400p' supabase_server_v3.py > /tmp/management_tools.py
```

For Instance 3:
```bash
# Extract edge functions
sed -n '1600,1800p' supabase_server_v3.py > /tmp/edge_tools.py
```

## Important Notes

1. **Keep the good parts**: Error handling, response formatting, timeout handling
2. **Replace the bad parts**: Manual SQL building, complex string concatenation
3. **Test everything**: Even copied code needs testing in the new context
4. **Update imports**: Change to use supabase-common utilities