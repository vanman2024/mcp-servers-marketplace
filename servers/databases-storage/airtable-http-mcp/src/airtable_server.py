#!/usr/bin/env python3
"""
Airtable HTTP MCP Server - Comprehensive API integration for ANY Airtable base
Provides dynamic base/table discovery and all CRUD operations
"""

import os
import logging
import json
import asyncio
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from urllib.parse import urlencode
import aiohttp
from fastmcp import FastMCP
from fastmcp.server.context import Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Airtable API Server")

# ===================================================================
# CONFIGURATION & INITIALIZATION
# ===================================================================

class AirtableClient:
    """Airtable API client with rate limiting and error handling"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('AIRTABLE_API_KEY') or os.getenv('AIRTABLE_PERSONAL_ACCESS_TOKEN')
        self.base_url = "https://api.airtable.com/v0"
        self.meta_url = "https://api.airtable.com/v0/meta"
        self.session = None
        self.rate_limit_remaining = 5  # 5 requests per second
        self.last_request_time = datetime.now()
        
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
            )
    
    async def _rate_limit(self):
        """Implement rate limiting (5 requests per second)"""
        now = datetime.now()
        elapsed = (now - self.last_request_time).total_seconds()
        
        if elapsed < 0.2:  # 200ms between requests (5 per second)
            await asyncio.sleep(0.2 - elapsed)
        
        self.last_request_time = datetime.now()
    
    async def request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Make an API request with rate limiting and error handling"""
        await self._ensure_session()
        await self._rate_limit()
        
        try:
            async with self.session.request(method, url, **kwargs) as response:
                data = await response.json()
                
                if response.status >= 400:
                    error_message = data.get('error', {}).get('message', 'Unknown error')
                    return {
                        "success": False,
                        "error": f"API Error {response.status}: {error_message}",
                        "status_code": response.status
                    }
                
                return {
                    "success": True,
                    "data": data,
                    "status_code": response.status
                }
                
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()

# Global client instance
airtable_client = None

def get_client() -> AirtableClient:
    """Get or create Airtable client"""
    global airtable_client
    if not airtable_client:
        airtable_client = AirtableClient()
    return airtable_client

# ===================================================================
# HELPER FUNCTIONS
# ===================================================================

async def paginate_results(
    client: AirtableClient,
    url: str,
    params: Dict[str, Any] = None,
    max_records: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Handle pagination for list endpoints"""
    all_records = []
    offset = None
    params = params or {}
    
    while True:
        if offset:
            params['offset'] = offset
        
        result = await client.request('GET', url, params=params)
        
        if not result['success']:
            return all_records
        
        data = result['data']
        records = data.get('records', data.get('bases', data.get('tables', [])))
        all_records.extend(records)
        
        if max_records and len(all_records) >= max_records:
            return all_records[:max_records]
        
        offset = data.get('offset')
        if not offset:
            break
    
    return all_records

def build_filter_formula(filters: Dict[str, Any]) -> str:
    """Build Airtable filter formula from dictionary"""
    if not filters:
        return ""
    
    conditions = []
    for field, value in filters.items():
        if isinstance(value, str):
            conditions.append(f"{{{{field}}}} = '{value}'")
        elif isinstance(value, (int, float)):
            conditions.append(f"{{{{field}}}} = {value}")
        elif isinstance(value, bool):
            conditions.append(f"{{{{field}}}} = {str(value).upper()}")
    
    if len(conditions) == 1:
        return conditions[0]
    else:
        return f"AND({', '.join(conditions)})"

# ===================================================================
# STANDALONE TOOLS - Base & Table Discovery
# ===================================================================

@mcp.tool()
async def list_bases(
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    List all accessible Airtable bases.
    
    Returns:
        List of bases with IDs, names, and permission levels
    """
    try:
        client = get_client()
        
        if ctx:
            await ctx.info("Fetching accessible bases")
        
        url = f"{client.meta_url}/bases"
        bases = await paginate_results(client, url)
        
        if ctx:
            await ctx.info(f"Found {len(bases)} accessible bases")
        
        return {
            "success": True,
            "bases": bases,
            "count": len(bases)
        }
        
    except Exception as e:
        logger.error(f"Failed to list bases: {e}")
        if ctx:
            await ctx.error(f"Failed to list bases: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_base_schema(
    base_id: str,
    include_views: bool = False,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Get complete schema for a base including all tables and fields.
    
    Args:
        base_id: The Airtable base ID
        include_views: Whether to include view details
        ctx: Context for logging
    
    Returns:
        Complete base schema with tables, fields, and views
    """
    try:
        client = get_client()
        
        if ctx:
            await ctx.info(f"Fetching schema for base {base_id}")
        
        url = f"{client.meta_url}/bases/{base_id}/tables"
        params = {}
        if include_views:
            params['include'] = ['visibleFieldIds']
        
        result = await client.request('GET', url, params=params)
        
        if not result['success']:
            return result
        
        tables = result['data'].get('tables', [])
        
        if ctx:
            await ctx.info(f"Found {len(tables)} tables in base")
        
        return {
            "success": True,
            "base_id": base_id,
            "tables": tables,
            "table_count": len(tables),
            "total_fields": sum(len(t.get('fields', [])) for t in tables)
        }
        
    except Exception as e:
        logger.error(f"Failed to get base schema: {e}")
        if ctx:
            await ctx.error(f"Failed to get base schema: {str(e)}")
        return {"success": False, "error": str(e)}

# ===================================================================
# STANDALONE TOOLS - Record Operations
# ===================================================================

@mcp.tool()
async def list_records(
    base_id: str,
    table: str,
    view: Optional[str] = None,
    fields: Optional[List[str]] = None,
    filter_formula: Optional[str] = None,
    max_records: Optional[int] = None,
    page_size: int = 100,
    sort: Optional[List[Dict[str, str]]] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    List records from an Airtable table with filtering and pagination.
    
    Args:
        base_id: The Airtable base ID
        table: Table name or ID
        view: Optional view name or ID
        fields: List of field names to return
        filter_formula: Airtable filter formula
        max_records: Maximum records to return
        page_size: Records per page (max 100)
        sort: List of sort objects [{"field": "Name", "direction": "asc"}]
        ctx: Context for logging
    
    Returns:
        List of records with specified fields
    """
    try:
        client = get_client()
        
        if ctx:
            await ctx.info(f"Listing records from {table} in base {base_id}")
        
        url = f"{client.base_url}/{base_id}/{table}"
        params = {}
        
        if view:
            params['view'] = view
        if fields:
            params['fields'] = fields
        if filter_formula:
            params['filterByFormula'] = filter_formula
        if max_records:
            params['maxRecords'] = max_records
        if page_size and page_size <= 100:
            params['pageSize'] = page_size
        if sort:
            for i, s in enumerate(sort):
                params[f'sort[{i}][field]'] = s['field']
                params[f'sort[{i}][direction]'] = s.get('direction', 'asc')
        
        records = await paginate_results(client, url, params, max_records)
        
        if ctx:
            await ctx.info(f"Retrieved {len(records)} records")
        
        return {
            "success": True,
            "records": records,
            "count": len(records)
        }
        
    except Exception as e:
        logger.error(f"Failed to list records: {e}")
        if ctx:
            await ctx.error(f"Failed to list records: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_record(
    base_id: str,
    table: str,
    record_id: str,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Get a single record by ID.
    
    Args:
        base_id: The Airtable base ID
        table: Table name or ID
        record_id: Record ID to retrieve
        ctx: Context for logging
    
    Returns:
        Record data with all fields
    """
    try:
        client = get_client()
        
        if ctx:
            await ctx.info(f"Getting record {record_id} from {table}")
        
        url = f"{client.base_url}/{base_id}/{table}/{record_id}"
        result = await client.request('GET', url)
        
        if ctx and result['success']:
            await ctx.info("Record retrieved successfully")
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to get record: {e}")
        if ctx:
            await ctx.error(f"Failed to get record: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_records(
    base_id: str,
    table: str,
    records: List[Dict[str, Any]],
    typecast: bool = False,
    return_fields: bool = True,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Create one or more records in a table (max 10 per request).
    
    Args:
        base_id: The Airtable base ID
        table: Table name or ID
        records: List of record objects with 'fields' key
        typecast: Automatically typecast values
        return_fields: Return field values in response
        ctx: Context for logging
    
    Returns:
        Created records with IDs
    """
    try:
        client = get_client()
        
        if ctx:
            await ctx.info(f"Creating {len(records)} records in {table}")
        
        # Batch records (max 10 per request)
        all_created = []
        for i in range(0, len(records), 10):
            batch = records[i:i+10]
            
            url = f"{client.base_url}/{base_id}/{table}"
            body = {
                "records": batch,
                "typecast": typecast
            }
            
            if not return_fields:
                body["returnFieldsByFieldId"] = False
            
            result = await client.request('POST', url, json=body)
            
            if result['success']:
                all_created.extend(result['data'].get('records', []))
            else:
                if ctx:
                    await ctx.error(f"Batch {i//10 + 1} failed: {result['error']}")
        
        if ctx:
            await ctx.info(f"Created {len(all_created)} records successfully")
        
        return {
            "success": True,
            "records": all_created,
            "count": len(all_created)
        }
        
    except Exception as e:
        logger.error(f"Failed to create records: {e}")
        if ctx:
            await ctx.error(f"Failed to create records: {str(e)}")
        return {"success": False, "error": str(e)}

# ===================================================================
# CLASS-BASED TOOLS - Complex Operations
# ===================================================================

class ComplexAirtableTools:
    """Complex tools that orchestrate multiple operations"""
    
    async def update_records_batch(
        self,
        base_id: str,
        table: str,
        updates: List[Dict[str, Any]],
        typecast: bool = False,
        replace: bool = False,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Update multiple records in batches (max 10 per request).
        
        Args:
            base_id: The Airtable base ID
            table: Table name or ID
            updates: List of objects with 'id' and 'fields'
            typecast: Automatically typecast values
            replace: Replace entire record (True) or merge (False)
            ctx: Context for logging
        
        Returns:
            Updated records
        """
        try:
            client = get_client()
            
            if ctx:
                await ctx.info(f"Updating {len(updates)} records in {table}")
            
            all_updated = []
            method = 'PUT' if replace else 'PATCH'
            
            for i in range(0, len(updates), 10):
                batch = updates[i:i+10]
                
                url = f"{client.base_url}/{base_id}/{table}"
                body = {
                    "records": batch,
                    "typecast": typecast
                }
                
                result = await client.request(method, url, json=body)
                
                if result['success']:
                    all_updated.extend(result['data'].get('records', []))
                else:
                    if ctx:
                        await ctx.error(f"Batch {i//10 + 1} failed: {result['error']}")
            
            if ctx:
                await ctx.info(f"Updated {len(all_updated)} records")
            
            return {
                "success": True,
                "records": all_updated,
                "count": len(all_updated)
            }
            
        except Exception as e:
            logger.error(f"Failed to update records: {e}")
            if ctx:
                await ctx.error(f"Failed to update records: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def delete_records_batch(
        self,
        base_id: str,
        table: str,
        record_ids: List[str],
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Delete multiple records in batches (max 10 per request).
        
        Args:
            base_id: The Airtable base ID
            table: Table name or ID
            record_ids: List of record IDs to delete
            ctx: Context for logging
        
        Returns:
            Deletion results
        """
        try:
            client = get_client()
            
            if ctx:
                await ctx.info(f"Deleting {len(record_ids)} records from {table}")
            
            all_deleted = []
            
            for i in range(0, len(record_ids), 10):
                batch = record_ids[i:i+10]
                
                url = f"{client.base_url}/{base_id}/{table}"
                params = {'records[]': batch}
                
                result = await client.request('DELETE', url, params=params)
                
                if result['success']:
                    all_deleted.extend(result['data'].get('records', []))
                else:
                    if ctx:
                        await ctx.error(f"Batch {i//10 + 1} failed: {result['error']}")
            
            if ctx:
                await ctx.info(f"Deleted {len(all_deleted)} records")
            
            return {
                "success": True,
                "deleted": all_deleted,
                "count": len(all_deleted)
            }
            
        except Exception as e:
            logger.error(f"Failed to delete records: {e}")
            if ctx:
                await ctx.error(f"Failed to delete records: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def sync_csv_data(
        self,
        base_id: str,
        table: str,
        csv_data: str,
        unique_field: str,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Sync CSV data with a table (upsert operation).
        
        Args:
            base_id: The Airtable base ID
            table: Table name or ID
            csv_data: CSV content as string
            unique_field: Field to use for matching records
            ctx: Context for logging
        
        Returns:
            Sync results
        """
        try:
            client = get_client()
            
            if ctx:
                await ctx.info(f"Syncing CSV data to {table}")
            
            url = f"{client.base_url}/{base_id}/{table}/sync"
            
            # Parse CSV and prepare for sync
            import csv
            import io
            
            reader = csv.DictReader(io.StringIO(csv_data))
            records = list(reader)
            
            body = {
                "performUpsert": {
                    "fieldsToMergeOn": [unique_field]
                },
                "records": [{"fields": record} for record in records]
            }
            
            result = await client.request('POST', url, json=body)
            
            if ctx and result['success']:
                await ctx.info(f"Synced {len(records)} records")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to sync CSV data: {e}")
            if ctx:
                await ctx.error(f"Failed to sync CSV: {str(e)}")
            return {"success": False, "error": str(e)}

# Register class-based tools
complex_tools = ComplexAirtableTools()
mcp.tool(complex_tools.update_records_batch)
mcp.tool(complex_tools.delete_records_batch)
mcp.tool(complex_tools.sync_csv_data)

# ===================================================================
# STANDALONE TOOLS - Table & Field Management
# ===================================================================

@mcp.tool()
async def create_table(
    base_id: str,
    name: str,
    fields: List[Dict[str, Any]],
    description: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Create a new table in a base.
    
    Args:
        base_id: The Airtable base ID
        name: Table name
        fields: List of field configurations
        description: Optional table description
        ctx: Context for logging
    
    Returns:
        Created table schema
    """
    try:
        client = get_client()
        
        if ctx:
            await ctx.info(f"Creating table '{name}' in base {base_id}")
        
        url = f"{client.meta_url}/bases/{base_id}/tables"
        body = {
            "name": name,
            "fields": fields
        }
        
        if description:
            body["description"] = description
        
        result = await client.request('POST', url, json=body)
        
        if ctx and result['success']:
            await ctx.info(f"Table '{name}' created successfully")
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to create table: {e}")
        if ctx:
            await ctx.error(f"Failed to create table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_field(
    base_id: str,
    table_id: str,
    name: str,
    field_type: str,
    options: Optional[Dict[str, Any]] = None,
    description: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Create a new field in a table.
    
    Args:
        base_id: The Airtable base ID
        table_id: Table ID
        name: Field name
        field_type: Field type (e.g., 'singleLineText', 'number', 'checkbox')
        options: Field-specific options
        description: Optional field description
        ctx: Context for logging
    
    Returns:
        Created field schema
    """
    try:
        client = get_client()
        
        if ctx:
            await ctx.info(f"Creating field '{name}' in table {table_id}")
        
        url = f"{client.meta_url}/bases/{base_id}/tables/{table_id}/fields"
        body = {
            "name": name,
            "type": field_type
        }
        
        if options:
            body["options"] = options
        if description:
            body["description"] = description
        
        result = await client.request('POST', url, json=body)
        
        if ctx and result['success']:
            await ctx.info(f"Field '{name}' created successfully")
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to create field: {e}")
        if ctx:
            await ctx.error(f"Failed to create field: {str(e)}")
        return {"success": False, "error": str(e)}

# ===================================================================
# STANDALONE TOOLS - Comments
# ===================================================================

@mcp.tool()
async def create_comment(
    base_id: str,
    table: str,
    record_id: str,
    text: str,
    parent_comment_id: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Create a comment on a record.
    
    Args:
        base_id: The Airtable base ID
        table: Table name or ID
        record_id: Record ID
        text: Comment text (supports @mentions)
        parent_comment_id: Optional parent comment for threading
        ctx: Context for logging
    
    Returns:
        Created comment details
    """
    try:
        client = get_client()
        
        if ctx:
            await ctx.info(f"Creating comment on record {record_id}")
        
        url = f"{client.base_url}/{base_id}/{table}/{record_id}/comments"
        body = {"text": text}
        
        if parent_comment_id:
            body["parentCommentId"] = parent_comment_id
        
        result = await client.request('POST', url, json=body)
        
        if ctx and result['success']:
            await ctx.info("Comment created successfully")
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to create comment: {e}")
        if ctx:
            await ctx.error(f"Failed to create comment: {str(e)}")
        return {"success": False, "error": str(e)}

# ===================================================================
# STANDALONE TOOLS - Webhooks
# ===================================================================

@mcp.tool()
async def create_webhook(
    base_id: str,
    notification_url: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None,
    includes: Optional[List[str]] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Create a webhook for base changes.
    
    Args:
        base_id: The Airtable base ID
        notification_url: URL to receive notifications
        filters: Specification filters for changes
        includes: Data to include in payloads
        ctx: Context for logging
    
    Returns:
        Webhook details including ID and secret
    """
    try:
        client = get_client()
        
        if ctx:
            await ctx.info(f"Creating webhook for base {base_id}")
        
        url = f"{client.base_url}/bases/{base_id}/webhooks"
        body = {
            "specification": {
                "options": {}
            }
        }
        
        if notification_url:
            body["notificationUrl"] = notification_url
        if filters:
            body["specification"]["options"]["filters"] = filters
        if includes:
            body["specification"]["options"]["includes"] = includes
        
        result = await client.request('POST', url, json=body)
        
        if ctx and result['success']:
            await ctx.info("Webhook created successfully")
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to create webhook: {e}")
        if ctx:
            await ctx.error(f"Failed to create webhook: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_webhooks(
    base_id: str,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    List all webhooks for a base.
    
    Args:
        base_id: The Airtable base ID
        ctx: Context for logging
    
    Returns:
        List of webhooks with their configurations
    """
    try:
        client = get_client()
        
        if ctx:
            await ctx.info(f"Listing webhooks for base {base_id}")
        
        url = f"{client.base_url}/bases/{base_id}/webhooks"
        result = await client.request('GET', url)
        
        if ctx and result['success']:
            webhooks = result['data'].get('webhooks', [])
            await ctx.info(f"Found {len(webhooks)} webhooks")
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to list webhooks: {e}")
        if ctx:
            await ctx.error(f"Failed to list webhooks: {str(e)}")
        return {"success": False, "error": str(e)}

# ===================================================================
# RESOURCES - API Documentation and Best Practices
# ===================================================================

@mcp.resource("resource://airtable_usage_guide")
def usage_guide() -> str:
    """Critical guide for using the Airtable MCP server"""
    return """
# Airtable MCP Server Usage Guide

## 🚨 CRITICAL: Authentication Required

This server requires a valid Airtable Personal Access Token or OAuth token.
Set the environment variable: AIRTABLE_PERSONAL_ACCESS_TOKEN

## Key Concepts

### Base Discovery Pattern
Always start by discovering available bases:
1. list_bases() - Get all accessible bases
2. get_base_schema(base_id) - Get tables and fields
3. Then operate on specific tables

### Rate Limiting
- **5 requests per second** per base
- Server automatically handles rate limiting
- Batch operations process 10 records at a time

## Common Operations

### 1. List All Bases
```python
bases = await list_bases()
# Returns: {"bases": [...], "count": N}
```

### 2. Get Base Schema
```python
schema = await get_base_schema(base_id="appXXXXXXXXXXXX")
# Returns complete table and field definitions
```

### 3. List Records with Filtering
```python
records = await list_records(
    base_id="appXXXXXXXXXXXX",
    table="Table Name",
    filter_formula="AND({Status} = 'Active', {Priority} > 3)",
    sort=[{"field": "Created", "direction": "desc"}],
    max_records=100
)
```

### 4. Create Multiple Records
```python
new_records = await create_records(
    base_id="appXXXXXXXXXXXX",
    table="Table Name",
    records=[
        {"fields": {"Name": "Item 1", "Status": "New"}},
        {"fields": {"Name": "Item 2", "Status": "New"}}
    ]
)
```

### 5. Update Records (Batch)
```python
updates = await update_records_batch(
    base_id="appXXXXXXXXXXXX",
    table="Table Name",
    updates=[
        {"id": "recXXXXXX", "fields": {"Status": "Complete"}},
        {"id": "recYYYYYY", "fields": {"Status": "In Progress"}}
    ]
)
```

## Field Types

### Supported Primary Field Types:
- singleLineText
- number
- autoNumber

### All Field Types:
- singleLineText
- email
- url
- multilineText
- number
- percent
- currency
- singleSelect
- multipleSelects
- singleCollaborator
- multipleCollaborators
- multipleRecordLinks
- date
- dateTime
- checkbox
- formula
- rollup
- count
- lookup
- multipleAttachments
- barcode
- rating
- duration
- phoneNumber
- createdTime
- createdBy
- lastModifiedTime
- lastModifiedBy
- button

## Best Practices

1. **Always use base_id and table IDs when possible** - Names can change
2. **Batch operations** - Process up to 10 records per request
3. **Use filter formulas** - More efficient than client-side filtering
4. **Handle pagination** - Results come in pages of 100 records
5. **Implement retry logic** - For rate limit errors (429)
6. **Cache base schemas** - They don't change frequently

## Error Handling

Common errors:
- 401: Invalid authentication token
- 403: Insufficient permissions
- 404: Base/table/record not found
- 422: Invalid request (check field types)
- 429: Rate limit exceeded (retry after delay)
- 500: Server error (retry with exponential backoff)
"""

@mcp.resource("resource://field_type_reference")
def field_type_reference() -> str:
    """Complete field type reference with options"""
    return """
# Airtable Field Type Reference

## Text Fields

### singleLineText
```json
{
  "type": "singleLineText",
  "name": "Title"
}
```

### multilineText
```json
{
  "type": "multilineText",
  "name": "Description"
}
```

### email
```json
{
  "type": "email",
  "name": "Email Address"
}
```

### url
```json
{
  "type": "url",
  "name": "Website"
}
```

### phoneNumber
```json
{
  "type": "phoneNumber",
  "name": "Contact"
}
```

## Number Fields

### number
```json
{
  "type": "number",
  "name": "Quantity",
  "options": {
    "precision": 2
  }
}
```

### percent
```json
{
  "type": "percent",
  "name": "Progress",
  "options": {
    "precision": 0
  }
}
```

### currency
```json
{
  "type": "currency",
  "name": "Price",
  "options": {
    "precision": 2,
    "symbol": "$"
  }
}
```

### rating
```json
{
  "type": "rating",
  "name": "Priority",
  "options": {
    "icon": "star",
    "max": 5,
    "color": "yellowBright"
  }
}
```

## Date/Time Fields

### date
```json
{
  "type": "date",
  "name": "Due Date",
  "options": {
    "dateFormat": {
      "name": "iso",
      "format": "YYYY-MM-DD"
    }
  }
}
```

### dateTime
```json
{
  "type": "dateTime",
  "name": "Meeting Time",
  "options": {
    "dateFormat": {
      "name": "iso",
      "format": "YYYY-MM-DD"
    },
    "timeFormat": {
      "name": "24hour",
      "format": "HH:mm"
    },
    "timeZone": "America/New_York"
  }
}
```

### duration
```json
{
  "type": "duration",
  "name": "Time Spent",
  "options": {
    "durationFormat": "h:mm"
  }
}
```

## Selection Fields

### singleSelect
```json
{
  "type": "singleSelect",
  "name": "Status",
  "options": {
    "choices": [
      {"name": "To Do", "color": "redLight"},
      {"name": "In Progress", "color": "yellowLight"},
      {"name": "Done", "color": "greenLight"}
    ]
  }
}
```

### multipleSelects
```json
{
  "type": "multipleSelects",
  "name": "Tags",
  "options": {
    "choices": [
      {"name": "Urgent", "color": "redBright"},
      {"name": "Important", "color": "blueBright"},
      {"name": "Review", "color": "purpleBright"}
    ]
  }
}
```

## Linked Records

### multipleRecordLinks
```json
{
  "type": "multipleRecordLinks",
  "name": "Related Items",
  "options": {
    "linkedTableId": "tblXXXXXXXXXXXX",
    "prefersSingleRecordLink": false,
    "inverseLinkFieldId": "fldYYYYYYYYYYYY"
  }
}
```

## Computed Fields

### formula
```json
{
  "type": "formula",
  "name": "Total",
  "options": {
    "formula": "{Quantity} * {Price}"
  }
}
```

### rollup
```json
{
  "type": "rollup",
  "name": "Total Sales",
  "options": {
    "fieldIdInLinkedTable": "fldXXXXXXXXXXXX",
    "recordLinkFieldId": "fldYYYYYYYYYYYY",
    "formula": "SUM(values)"
  }
}
```

### count
```json
{
  "type": "count",
  "name": "Item Count",
  "options": {
    "recordLinkFieldId": "fldXXXXXXXXXXXX"
  }
}
```

### lookup
```json
{
  "type": "lookup",
  "name": "Customer Name",
  "options": {
    "fieldIdInLinkedTable": "fldXXXXXXXXXXXX",
    "recordLinkFieldId": "fldYYYYYYYYYYYY"
  }
}
```

## Special Fields

### checkbox
```json
{
  "type": "checkbox",
  "name": "Completed",
  "options": {
    "icon": "check",
    "color": "greenBright"
  }
}
```

### multipleAttachments
```json
{
  "type": "multipleAttachments",
  "name": "Files"
}
```

### barcode
```json
{
  "type": "barcode",
  "name": "Product Code"
}
```

### button
```json
{
  "type": "button",
  "name": "Open URL",
  "options": {
    "label": "View Details",
    "url": "https://example.com/{Record ID}"
  }
}
```

## System Fields (Read-only)

### autoNumber
```json
{
  "type": "autoNumber",
  "name": "ID"
}
```

### createdTime
```json
{
  "type": "createdTime",
  "name": "Created"
}
```

### createdBy
```json
{
  "type": "createdBy",
  "name": "Creator"
}
```

### lastModifiedTime
```json
{
  "type": "lastModifiedTime",
  "name": "Updated"
}
```

### lastModifiedBy
```json
{
  "type": "lastModifiedBy",
  "name": "Last Editor"
}
```
"""

@mcp.resource("resource://filter_formula_guide")
def filter_formula_guide() -> str:
    """Guide for creating Airtable filter formulas"""
    return """
# Airtable Filter Formula Guide

## Basic Comparison Operators

### Equality
```
{Field Name} = 'Value'
{Status} = 'Complete'
{Priority} = 5
```

### Inequality
```
{Field Name} != 'Value'
{Status} != 'Archived'
```

### Greater/Less Than
```
{Priority} > 3
{Amount} <= 1000
{Date} >= '2024-01-01'
```

## Logical Operators

### AND
```
AND({Status} = 'Active', {Priority} > 3)
AND({Category} = 'Sales', {Amount} > 1000, {Region} = 'West')
```

### OR
```
OR({Status} = 'New', {Status} = 'In Progress')
OR({Priority} = 5, {Urgent} = TRUE())
```

### NOT
```
NOT({Status} = 'Complete')
NOT(OR({Category} = 'A', {Category} = 'B'))
```

## Text Functions

### SEARCH
```
SEARCH('keyword', {Description})
SEARCH('urgent', LOWER({Title}))
```

### FIND
```
FIND('substring', {Field})
FIND('@', {Email}) > 0
```

### Text Comparison
```
LOWER({Name}) = 'john doe'
UPPER({Code}) = 'ABC123'
LEN({Description}) > 100
```

## Date Functions

### Date Comparisons
```
{Due Date} = TODAY()
{Created} >= DATEADD(TODAY(), -7, 'days')
{Expiry} <= DATEADD(TODAY(), 30, 'days')
```

### Date Checks
```
IS_BEFORE({Date1}, {Date2})
IS_AFTER({Start Date}, '2024-01-01')
IS_SAME({Date}, TODAY(), 'month')
```

### Date Extraction
```
YEAR({Date}) = 2024
MONTH({Date}) = 1
WEEKDAY({Date}) = 1  // Monday
```

## Checkbox Fields

### Check Status
```
{Completed} = TRUE()
{Completed} = 1
NOT({Archived})
{Active} = FALSE()
```

## Empty/Null Checks

### BLANK
```
{Field} = BLANK()
{Email} != BLANK()
NOT({Description} = BLANK())
```

### Combined with OR
```
OR({Field} = BLANK(), {Field} = '')
```

## Number Functions

### Mathematical
```
{Quantity} * {Price} > 100
MOD({Number}, 2) = 0  // Even numbers
ABS({Difference}) < 10
ROUND({Value}, 2) = 99.99
```

### Aggregations in Rollup Fields
```
{Total} = SUM({Line Items})
{Average} > AVG({Scores})
{Count} = COUNT({Items})
```

## Select Fields

### Single Select
```
{Status} = 'Active'
{Category} != 'Archived'
```

### Multiple Select
```
FIND('Tag1', {Tags}) > 0
AND(FIND('Important', {Tags}), FIND('Urgent', {Tags}))
```

## Linked Records

### Has Links
```
{Linked Table} != BLANK()
COUNT({Related Items}) > 0
```

### Count Links
```
COUNT({Assignments}) = 3
COUNT({Tags}) >= 2
```

## Complex Examples

### Project Management
```
AND(
  {Status} != 'Complete',
  {Due Date} <= DATEADD(TODAY(), 7, 'days'),
  OR({Priority} >= 4, {Urgent} = TRUE())
)
```

### Sales Pipeline
```
AND(
  {Stage} = 'Qualified',
  {Amount} > 10000,
  {Close Date} >= TODAY(),
  {Close Date} <= DATEADD(TODAY(), 30, 'days')
)
```

### Content Calendar
```
AND(
  OR({Status} = 'Draft', {Status} = 'Review'),
  {Publish Date} >= TODAY(),
  {Publish Date} <= DATEADD(TODAY(), 14, 'days'),
  {Assigned To} != BLANK()
)
```

### Customer Support
```
AND(
  {Type} = 'Bug',
  {Priority} >= 4,
  OR(
    {Status} = 'New',
    AND({Status} = 'In Progress', {Days Open} > 3)
  )
)
```

## Performance Tips

1. **Use indexed fields** in filters when possible
2. **Avoid complex SEARCH** operations on large text fields
3. **Limit OR conditions** - they can slow down queries
4. **Test formulas** in Airtable UI first
5. **Use specific conditions** before broad ones
"""

@mcp.resource("resource://webhook_patterns")
def webhook_patterns() -> str:
    """Webhook implementation patterns"""
    return """
# Airtable Webhook Patterns

## Creating Webhooks

### Basic Webhook
```python
webhook = await create_webhook(
    base_id="appXXXXXXXXXXXX",
    notification_url="https://your-server.com/webhook"
)
# Store webhook.macSecretBase64 securely!
```

### Filtered Webhook
```python
webhook = await create_webhook(
    base_id="appXXXXXXXXXXXX",
    notification_url="https://your-server.com/webhook",
    filters={
        "dataTypes": ["tableData"],
        "recordChangeScope": "tblXXXXXXXXXXXX",  # Specific table
        "changeTypes": ["add", "update", "remove"]
    }
)
```

### Webhook with Includes
```python
webhook = await create_webhook(
    base_id="appXXXXXXXXXXXX",
    notification_url="https://your-server.com/webhook",
    includes={
        "includePreviousCellValues": True,
        "includePreviousFieldDefinitions": True
    }
)
```

## Webhook Payload Structure

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "baseTransactionNumber": 1234,
  "payloadFormat": "v0",
  "actionMetadata": {
    "source": "publicApi",
    "sourceMetadata": {
      "user": {
        "id": "usrXXXXXXXXXXXX",
        "email": "user@example.com",
        "name": "User Name"
      }
    }
  },
  "changedTablesById": {
    "tblXXXXXXXXXXXX": {
      "changedRecordsById": {
        "recXXXXXXXXXXXX": {
          "current": {
            "cellValuesByFieldId": {
              "fldXXXXXXXXXXXX": "New Value"
            }
          },
          "previous": {
            "cellValuesByFieldId": {
              "fldXXXXXXXXXXXX": "Old Value"
            }
          },
          "unchanged": {
            "cellValuesByFieldId": {
              "fldYYYYYYYYYYYY": "Unchanged Value"
            }
          }
        }
      },
      "createdRecordsById": {
        "recYYYYYYYYYYYY": {
          "cellValuesByFieldId": {
            "fldXXXXXXXXXXXX": "Initial Value"
          }
        }
      },
      "destroyedRecordIds": ["recZZZZZZZZZZZZ"]
    }
  }
}
```

## Webhook Verification

### Python Example
```python
import hmac
import hashlib
import base64

def verify_webhook(request_body: bytes, signature: str, secret: str) -> bool:
    '''
    Verify webhook signature
    
    Args:
        request_body: Raw request body bytes
        signature: Value from X-Airtable-Content-MAC header
        secret: macSecretBase64 from webhook creation
    '''
    secret_bytes = base64.b64decode(secret)
    expected = hmac.new(
        secret_bytes,
        request_body,
        hashlib.sha256
    ).digest()
    expected_b64 = base64.b64encode(expected).decode()
    
    return hmac.compare_digest(signature, f"sha256={expected_b64}")
```

## Webhook Lifecycle

### Creation and Expiration
- Webhooks expire after 7 days (OAuth/PAT)
- No expiration for API key webhooks
- Maximum 10 webhooks per base
- OAuth integrations limited to 2 per base

### Refreshing Webhooks
```python
# Refresh before expiration
await refresh_webhook(
    base_id="appXXXXXXXXXXXX",
    webhook_id="webhookXXXXXXXXXXXX"
)
```

### Listing Webhook Payloads
```python
payloads = await list_webhook_payloads(
    base_id="appXXXXXXXXXXXX",
    webhook_id="webhookXXXXXXXXXXXX",
    cursor=None,  # For pagination
    limit=20
)
```

## Processing Patterns

### Idempotent Processing
```python
async def process_webhook(payload):
    # Use baseTransactionNumber for idempotency
    transaction_id = payload['baseTransactionNumber']
    
    if await is_processed(transaction_id):
        return {"status": "already_processed"}
    
    # Process changes
    for table_id, changes in payload['changedTablesById'].items():
        # Handle created records
        for record_id, record in changes.get('createdRecordsById', {}).items():
            await handle_created_record(record_id, record)
        
        # Handle updated records
        for record_id, record in changes.get('changedRecordsById', {}).items():
            await handle_updated_record(
                record_id,
                record['current'],
                record['previous']
            )
        
        # Handle deleted records
        for record_id in changes.get('destroyedRecordIds', []):
            await handle_deleted_record(record_id)
    
    await mark_processed(transaction_id)
    return {"status": "processed"}
```

### Error Handling
```python
async def webhook_handler(request):
    try:
        # Verify signature
        if not verify_webhook(request.body, request.headers['X-Airtable-Content-MAC'], secret):
            return {"status": 401, "error": "Invalid signature"}
        
        # Parse payload
        payload = json.loads(request.body)
        
        # Process with retry
        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = await process_webhook(payload)
                return {"status": 200, "result": result}
            except Exception as e:
                if attempt == max_retries - 1:
                    # Log to dead letter queue
                    await log_failed_webhook(payload, str(e))
                    return {"status": 500, "error": "Processing failed"}
                await asyncio.sleep(2 ** attempt)
        
    except Exception as e:
        logger.error(f"Webhook handler error: {e}")
        return {"status": 500, "error": str(e)}
```

## Best Practices

1. **Store secrets securely** - Never log or expose macSecretBase64
2. **Verify signatures** - Always validate webhook authenticity
3. **Handle duplicates** - Use baseTransactionNumber for idempotency
4. **Process asynchronously** - Return 200 quickly, process in background
5. **Implement retry logic** - Handle transient failures gracefully
6. **Monitor webhook health** - Track processing success/failure rates
7. **Refresh before expiration** - Set up scheduled refresh for long-lived webhooks
8. **Use filtering** - Only subscribe to relevant changes
9. **Batch processing** - Group related changes for efficiency
10. **Maintain audit log** - Track all webhook events for debugging
"""

@mcp.resource("resource://api_examples")
def api_examples() -> str:
    """Comprehensive API usage examples"""
    return """
# Airtable API Examples

## Complete CRUD Workflow

### 1. Discover and Setup
```python
# Find available bases
bases = await list_bases()
base_id = bases['bases'][0]['id']

# Get base schema
schema = await get_base_schema(base_id)
table = schema['tables'][0]['name']
```

### 2. Create Records
```python
# Single record
new_record = await create_records(
    base_id=base_id,
    table=table,
    records=[{
        "fields": {
            "Name": "New Item",
            "Status": "Active",
            "Priority": 5,
            "Due Date": "2024-12-31"
        }
    }]
)

# Batch create
batch_records = await create_records(
    base_id=base_id,
    table=table,
    records=[
        {"fields": {"Name": f"Item {i}", "Priority": i}}
        for i in range(1, 11)
    ]
)
```

### 3. Query Records
```python
# With filtering and sorting
active_high_priority = await list_records(
    base_id=base_id,
    table=table,
    filter_formula="AND({Status} = 'Active', {Priority} >= 4)",
    sort=[{"field": "Priority", "direction": "desc"}],
    fields=["Name", "Status", "Priority", "Due Date"],
    max_records=50
)

# Paginated retrieval
all_records = []
offset = None
while True:
    page = await list_records(
        base_id=base_id,
        table=table,
        page_size=100,
        offset=offset
    )
    all_records.extend(page['records'])
    offset = page.get('offset')
    if not offset:
        break
```

### 4. Update Records
```python
# Update single field
await update_records_batch(
    base_id=base_id,
    table=table,
    updates=[{
        "id": "recXXXXXXXXXXXX",
        "fields": {"Status": "Complete"}
    }]
)

# Bulk updates with different values
updates = [
    {"id": rec['id'], "fields": {"Processed": True}}
    for rec in records_to_process
]
await update_records_batch(
    base_id=base_id,
    table=table,
    updates=updates
)
```

### 5. Delete Records
```python
# Delete specific records
await delete_records_batch(
    base_id=base_id,
    table=table,
    record_ids=["recXXXXXX", "recYYYYYY", "recZZZZZZ"]
)

# Delete based on condition
old_records = await list_records(
    base_id=base_id,
    table=table,
    filter_formula=f"IS_BEFORE({{Created}}, '{cutoff_date}')"
)
if old_records['records']:
    ids_to_delete = [r['id'] for r in old_records['records']]
    await delete_records_batch(
        base_id=base_id,
        table=table,
        record_ids=ids_to_delete
    )
```

## Advanced Patterns

### Dynamic Table Creation
```python
# Create project tracking table
project_table = await create_table(
    base_id=base_id,
    name="Projects",
    description="Project tracking and management",
    fields=[
        {"type": "singleLineText", "name": "Project Name"},
        {"type": "singleSelect", "name": "Status", "options": {
            "choices": [
                {"name": "Planning", "color": "grayLight"},
                {"name": "In Progress", "color": "yellowLight"},
                {"name": "Complete", "color": "greenLight"}
            ]
        }},
        {"type": "number", "name": "Budget", "options": {"precision": 2}},
        {"type": "date", "name": "Start Date"},
        {"type": "date", "name": "End Date"},
        {"type": "multipleCollaborators", "name": "Team"},
        {"type": "multipleAttachments", "name": "Documents"},
        {"type": "formula", "name": "Duration", "options": {
            "formula": "DATETIME_DIFF({End Date}, {Start Date}, 'days')"
        }}
    ]
)
```

### CSV Data Sync
```python
# Prepare CSV data
csv_content = '''Name,Email,Department,Salary
John Doe,john@example.com,Engineering,75000
Jane Smith,jane@example.com,Marketing,65000
Bob Johnson,bob@example.com,Sales,70000'''

# Sync with upsert on Email field
sync_result = await sync_csv_data(
    base_id=base_id,
    table="Employees",
    csv_data=csv_content,
    unique_field="Email"
)
```

### Linked Records Management
```python
# Create records with links
customer = await create_records(
    base_id=base_id,
    table="Customers",
    records=[{
        "fields": {
            "Name": "Acme Corp",
            "Industry": "Technology"
        }
    }]
)

order = await create_records(
    base_id=base_id,
    table="Orders",
    records=[{
        "fields": {
            "Order Number": "ORD-001",
            "Customer": [customer['records'][0]['id']],  # Link to customer
            "Total": 5000
        }
    }]
)
```

### Comment Threading
```python
# Create parent comment
parent = await create_comment(
    base_id=base_id,
    table=table,
    record_id="recXXXXXXXXXXXX",
    text="Initial review complete. @[usrYYYYYYYYYYYY] please check."
)

# Add reply
reply = await create_comment(
    base_id=base_id,
    table=table,
    record_id="recXXXXXXXXXXXX",
    text="Reviewed and approved!",
    parent_comment_id=parent['data']['id']
)
```

### Webhook Integration
```python
# Set up webhook for specific table
webhook = await create_webhook(
    base_id=base_id,
    notification_url="https://api.yourapp.com/airtable-webhook",
    filters={
        "dataTypes": ["tableData"],
        "recordChangeScope": table_id,
        "changeTypes": ["add", "update"]
    },
    includes={
        "includePreviousCellValues": True
    }
)

# Store the secret securely
webhook_secret = webhook['data']['macSecretBase64']
# Save to secure storage, not in code!
```

### Error Recovery Pattern
```python
async def robust_create(base_id, table, records, max_retries=3):
    '''Create records with retry logic'''
    for attempt in range(max_retries):
        try:
            result = await create_records(
                base_id=base_id,
                table=table,
                records=records,
                typecast=True
            )
            if result['success']:
                return result
            
            # Handle specific errors
            if 'rate limit' in result.get('error', '').lower():
                await asyncio.sleep(2 ** attempt)
                continue
            else:
                return result
                
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
    
    return {"success": False, "error": "Max retries exceeded"}
```

### Batch Processing Pattern
```python
async def process_large_dataset(base_id, table, items, batch_size=10):
    '''Process large dataset in batches'''
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        
        # Transform to Airtable format
        records = [{"fields": item} for item in batch]
        
        # Create with progress tracking
        result = await create_records(
            base_id=base_id,
            table=table,
            records=records
        )
        
        results.extend(result.get('records', []))
        
        # Progress update
        progress = min(i + batch_size, len(items))
        print(f"Processed {progress}/{len(items)} items")
        
        # Rate limit compliance
        await asyncio.sleep(0.2)
    
    return results
```
"""

# ===================================================================
# PROMPTS - Guide LLM interactions
# ===================================================================

@mcp.prompt
def airtable_query_builder(
    operation: str,
    requirements: str
) -> str:
    """Build Airtable API query based on requirements"""
    return f"""
# Airtable Query Builder for {operation}

## Requirements:
{requirements}

## Steps to build the query:

1. **Identify the base and table**
   - Use list_bases() to find available bases
   - Use get_base_schema(base_id) to find tables and fields

2. **Construct the filter formula** (if needed)
   - Use field names in curly braces: {{Field Name}}
   - Combine conditions with AND/OR
   - Use appropriate functions for the field type

3. **Set up sorting** (if needed)
   - Specify field and direction
   - Multiple sort levels supported

4. **Configure pagination**
   - Default page size is 100
   - Use offset for subsequent pages

5. **Select specific fields** (optional)
   - List only needed fields for efficiency

## Example query structure:
```python
result = await list_records(
    base_id="appXXXXXXXXXXXX",
    table="Table Name",
    filter_formula="your_formula_here",
    sort=[{{"field": "Field", "direction": "asc"}}],
    fields=["Field1", "Field2"],
    max_records=100
)
```

Based on the requirements, construct the appropriate Airtable API call.
"""

@mcp.prompt
def schema_design_assistant(
    use_case: str,
    data_types: str
) -> str:
    """Design Airtable schema for specific use case"""
    return f"""
# Airtable Schema Design for {use_case}

## Data Types to Include:
{data_types}

## Schema Design Recommendations:

### 1. Table Structure
Consider creating separate tables for:
- Main entities (e.g., Customers, Orders, Products)
- Junction tables for many-to-many relationships
- Lookup tables for consistent values

### 2. Field Selection
Choose appropriate field types:
- **Primary field**: Must be singleLineText, number, or autoNumber
- **Identifiers**: Use autoNumber for unique IDs
- **Relationships**: Use multipleRecordLinks for connections
- **Calculations**: Use formula, rollup, count, lookup fields
- **Metadata**: Use createdTime, createdBy, lastModifiedTime

### 3. Naming Conventions
- Use clear, descriptive names
- Avoid spaces in field names if using in formulas
- Be consistent with capitalization

### 4. Performance Considerations
- Index frequently filtered fields
- Limit formula complexity
- Use views for common filters
- Implement archiving for old records

### 5. Integration Planning
- Design with API access in mind
- Consider webhook needs
- Plan for data import/export

## Recommended Schema:

Based on your use case, here's a suggested structure:

[Provide specific table and field recommendations based on the use_case and data_types]
"""

@mcp.prompt
def troubleshooting_guide(
    error_type: str,
    context: str
) -> str:
    """Troubleshooting guide for common Airtable API issues"""
    return f"""
# Airtable API Troubleshooting: {error_type}

## Context:
{context}

## Common Issues and Solutions:

### Authentication Errors (401)
- Verify Personal Access Token is valid
- Check token has required scopes
- Ensure Bearer prefix in Authorization header

### Permission Errors (403)
- Verify user has required base permissions
- Check if operation requires creator-level access
- Confirm base/table IDs are correct

### Not Found Errors (404)
- Validate base ID format (starts with 'app')
- Check table name/ID exists
- Verify record ID format (starts with 'rec')

### Validation Errors (422)
- Check field types match data
- Verify required fields are included
- Validate formula syntax
- Ensure unique field values where required

### Rate Limit Errors (429)
- Implement exponential backoff
- Batch operations (max 10 records)
- Cache frequently accessed data
- Use webhooks for real-time updates

### Server Errors (500)
- Retry with exponential backoff
- Check Airtable status page
- Reduce request complexity
- Contact support for persistent issues

## Debugging Steps:

1. **Log the full error response**
2. **Verify request format**
3. **Test in Airtable UI first**
4. **Use minimal request to isolate issue**
5. **Check API changelog for changes**

## Resolution for {error_type}:
[Provide specific resolution based on error_type and context]
"""

@mcp.prompt
def migration_planner(
    source_system: str,
    data_volume: str
) -> str:
    """Plan migration from another system to Airtable"""
    return f"""
# Migration Plan: {source_system} to Airtable

## Data Volume: {data_volume}

## Migration Strategy:

### Phase 1: Schema Design
1. Analyze source data structure
2. Map to Airtable field types
3. Design table relationships
4. Create base and tables via API

### Phase 2: Data Preparation
1. Export source data
2. Clean and normalize data
3. Handle data type conversions
4. Prepare for Airtable constraints

### Phase 3: Migration Execution
1. Use batch operations (10 records/request)
2. Implement progress tracking
3. Handle errors and retries
4. Validate migrated data

### Phase 4: Post-Migration
1. Set up webhooks
2. Configure integrations
3. Train users
4. Document processes

## Code Template:

```python
async def migrate_data(source_data, base_id, table):
    migrated = []
    failed = []
    
    # Process in batches
    for batch in chunks(source_data, 10):
        try:
            # Transform data
            records = transform_for_airtable(batch)
            
            # Create records
            result = await create_records(
                base_id=base_id,
                table=table,
                records=records,
                typecast=True
            )
            
            migrated.extend(result['records'])
            
        except Exception as e:
            failed.extend(batch)
            log_error(e, batch)
        
        # Rate limit compliance
        await asyncio.sleep(0.2)
    
    return {{
        "migrated": len(migrated),
        "failed": len(failed),
        "success_rate": len(migrated) / len(source_data)
    }}
```

## Specific Considerations for {source_system}:
[Provide system-specific migration considerations]
"""

@mcp.prompt
def automation_designer(
    workflow: str,
    triggers: str
) -> str:
    """Design Airtable automation workflow"""
    return f"""
# Airtable Automation Design: {workflow}

## Triggers: {triggers}

## Automation Architecture:

### 1. Webhook Setup
```python
webhook = await create_webhook(
    base_id=base_id,
    notification_url=webhook_endpoint,
    filters={{
        "dataTypes": ["tableData"],
        "changeTypes": {triggers}
    }}
)
```

### 2. Event Processing
- Verify webhook signatures
- Parse change payloads
- Identify affected records
- Determine required actions

### 3. Action Implementation
Based on {workflow}, implement:
- Record updates
- Cross-table operations
- External integrations
- Notification sending

### 4. Error Handling
- Retry failed operations
- Log errors for review
- Send alerts for critical failures
- Implement circuit breakers

### 5. Monitoring
- Track automation performance
- Measure processing time
- Monitor success rates
- Generate reports

## Implementation Template:

```python
async def process_automation(webhook_payload):
    # Extract changes
    for table_id, changes in webhook_payload['changedTablesById'].items():
        
        # Process based on trigger type
        if '{triggers}' in changes:
            await handle_{workflow}(changes)
    
    return {{"processed": True}}

async def handle_{workflow}(changes):
    # Implement workflow logic
    pass
```

## Best Practices:
1. Make operations idempotent
2. Process asynchronously
3. Batch where possible
4. Monitor and alert
5. Document workflows
"""

# ===================================================================
# SERVER EXECUTION
# ===================================================================

if __name__ == "__main__":
    # Get configuration from environment
    port = int(os.getenv('AIRTABLE_MCP_PORT', '8040'))
    
    # Check for API key
    api_key = os.getenv('AIRTABLE_PERSONAL_ACCESS_TOKEN') or os.getenv('AIRTABLE_API_KEY')
    if not api_key:
        logger.warning("No Airtable API key found - set AIRTABLE_PERSONAL_ACCESS_TOKEN environment variable")
    
    logger.info(f"Starting Airtable MCP Server on port {port}")
    logger.info("Server provides comprehensive Airtable API access for ANY base")
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")