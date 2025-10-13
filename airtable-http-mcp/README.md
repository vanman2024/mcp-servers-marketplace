# Airtable HTTP MCP Server

Comprehensive Airtable API integration for ANY base with dynamic discovery and full CRUD operations.

## Features

- **Dynamic Base Discovery**: Automatically discover and work with any accessible Airtable base
- **Complete CRUD Operations**: Create, read, update, and delete records with batch support
- **Schema Management**: Create and modify tables, fields, and views
- **Advanced Features**: Webhooks, comments, CSV sync, and attachment uploads
- **Rate Limiting**: Automatic handling of Airtable's 5 requests/second limit
- **Comprehensive Resources**: API guides, field type references, and best practices

## Server Organization

### 🛠️ Tools (20+ tools)

#### Base & Table Discovery
- **list_bases**: Discover all accessible Airtable bases
- **get_base_schema**: Get complete schema with tables and fields
- **create_table**: Create new tables with field definitions
- **create_field**: Add fields to existing tables

#### Record Operations
- **list_records**: Query records with filtering, sorting, and pagination
- **get_record**: Retrieve single record by ID
- **create_records**: Create up to 10 records per request
- **update_records_batch**: Update multiple records efficiently
- **delete_records_batch**: Delete multiple records
- **sync_csv_data**: Sync CSV data with upsert operations

#### Comments & Collaboration
- **create_comment**: Add comments to records with threading
- **list_comments**: Get all comments for a record
- **update_comment**: Modify existing comments
- **delete_comment**: Remove comments

#### Webhooks
- **create_webhook**: Set up webhooks for real-time updates
- **list_webhooks**: View all webhooks for a base
- **list_webhook_payloads**: Get webhook event history
- **refresh_webhook**: Extend webhook expiration

### 📚 Resources (5 comprehensive guides)

- **airtable_usage_guide**: Complete guide for using the MCP server
- **field_type_reference**: All Airtable field types with configurations
- **filter_formula_guide**: Creating complex filter formulas
- **webhook_patterns**: Webhook implementation best practices
- **api_examples**: Real-world usage examples

### 💡 Prompts (5 specialized assistants)

- **airtable_query_builder**: Build complex queries based on requirements
- **schema_design_assistant**: Design optimal table schemas
- **troubleshooting_guide**: Resolve common API issues
- **migration_planner**: Plan data migration to Airtable
- **automation_designer**: Design webhook-based automations

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your Airtable Personal Access Token:
   ```bash
   export AIRTABLE_PERSONAL_ACCESS_TOKEN=your_token_here
   # or
   export AIRTABLE_API_KEY=your_token_here
   ```

3. Optional: Set custom port:
   ```bash
   export AIRTABLE_MCP_PORT=8040  # Default: 8040
   ```

4. Run the server:
   ```bash
   python src/airtable_server.py
   ```

## Usage with Claude

1. Add to Claude:
   ```bash
   claude mcp add --transport http airtable-http http://localhost:8040
   ```

2. Discover bases:
   ```python
   # List all accessible bases
   /mcp__airtable__list_bases
   
   # Get schema for a specific base
   /mcp__airtable__get_base_schema "appXXXXXXXXXXXX"
   ```

3. Work with records:
   ```python
   # List records with filtering
   /mcp__airtable__list_records \
     base_id="appXXXXXXXXXXXX" \
     table="Table Name" \
     filter_formula="AND({Status} = 'Active', {Priority} > 3)"
   
   # Create records
   /mcp__airtable__create_records \
     base_id="appXXXXXXXXXXXX" \
     table="Table Name" \
     records=[{"fields": {"Name": "New Item", "Status": "Active"}}]
   ```

4. Access resources:
   ```bash
   # Get usage guide
   /mcp_resource airtable://usage_guide
   
   # Get field type reference
   /mcp_resource airtable://field_type_reference
   ```

## API Authentication

This server requires a valid Airtable Personal Access Token (PAT) or OAuth token.

### Creating a Personal Access Token:
1. Go to https://airtable.com/create/tokens
2. Click "Create token"
3. Set scopes:
   - `data.records:read` - Read records
   - `data.records:write` - Create/update/delete records
   - `data.recordComments:read` - Read comments
   - `data.recordComments:write` - Create/update/delete comments
   - `schema.bases:read` - Read base schema
   - `schema.bases:write` - Create/modify tables and fields
   - `webhook:manage` - Create and manage webhooks
4. Select bases to access (or all bases)
5. Copy the token and set as environment variable

## Rate Limiting

Airtable API limits:
- **5 requests per second** per base
- **100 records** per page (list operations)
- **10 records** per batch (create/update/delete)

The server automatically handles rate limiting with built-in delays.

## Field Types Support

### Primary Field Types (can be first field):
- `singleLineText`
- `number`
- `autoNumber`

### All Supported Types:
- Text: `singleLineText`, `multilineText`, `email`, `url`, `phoneNumber`
- Numbers: `number`, `percent`, `currency`, `rating`, `duration`
- Dates: `date`, `dateTime`, `createdTime`, `lastModifiedTime`
- Selection: `singleSelect`, `multipleSelects`
- Users: `singleCollaborator`, `multipleCollaborators`, `createdBy`, `lastModifiedBy`
- Links: `multipleRecordLinks`, `lookup`, `rollup`, `count`
- Media: `multipleAttachments`, `barcode`
- Computed: `formula`, `button`
- Other: `checkbox`, `autoNumber`

## Common Use Cases

### 1. Database Discovery
```python
# Find all bases and their tables
bases = await list_bases()
for base in bases['bases']:
    schema = await get_base_schema(base['id'])
    print(f"Base: {base['name']}")
    for table in schema['tables']:
        print(f"  Table: {table['name']} ({len(table['fields'])} fields)")
```

### 2. Data Migration
```python
# Migrate data from CSV
csv_data = read_csv_file("data.csv")
result = await sync_csv_data(
    base_id="appXXXXXXXXXXXX",
    table="Imported Data",
    csv_data=csv_data,
    unique_field="Email"  # Upsert based on email
)
```

### 3. Bulk Operations
```python
# Update multiple records
updates = [
    {"id": "recXXX", "fields": {"Status": "Complete"}},
    {"id": "recYYY", "fields": {"Status": "In Progress"}}
]
await update_records_batch(base_id, table, updates)
```

### 4. Real-time Sync
```python
# Set up webhook for changes
webhook = await create_webhook(
    base_id="appXXXXXXXXXXXX",
    notification_url="https://your-server.com/webhook",
    filters={"changeTypes": ["add", "update"]}
)
# Store webhook['macSecretBase64'] securely!
```

## Error Handling

The server returns structured error responses:
```json
{
  "success": false,
  "error": "Error message",
  "status_code": 404
}
```

Common error codes:
- `401`: Invalid or missing API token
- `403`: Insufficient permissions
- `404`: Base/table/record not found
- `422`: Invalid request data
- `429`: Rate limit exceeded
- `500`: Server error

## Best Practices

1. **Use IDs over names**: Table and field IDs don't change
2. **Batch operations**: Process up to 10 records per request
3. **Filter server-side**: Use `filter_formula` instead of client filtering
4. **Cache schemas**: Base structures don't change frequently
5. **Handle pagination**: Results come in pages of 100
6. **Implement retries**: For rate limits and transient errors
7. **Verify webhooks**: Always validate webhook signatures
8. **Store secrets securely**: Never log or commit API keys

## Support

- [Airtable API Documentation](https://airtable.com/developers/web/api/introduction)
- [Field Type Reference](https://airtable.com/developers/web/api/field-model)
- [Filter Formula Reference](https://support.airtable.com/docs/formula-field-reference)
- [Webhook Documentation](https://airtable.com/developers/web/api/webhooks-overview)