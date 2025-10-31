# Airtable MCP Server - Multi-Token/Workspace Support

## Overview
You now have **THREE different ways** to handle multiple Airtable Personal Access Tokens for accessing different databases/workspaces:

## Option 1: Single-Token Server (Original)
**File:** `src/airtable_server.py`  
**Port:** 8040  
**Use Case:** When you only need one token at a time

```bash
# Set token
export AIRTABLE_PERSONAL_ACCESS_TOKEN="your_token_here"

# Start server
python src/airtable_server.py
```

**Switching Tokens:** Stop server, change environment variable, restart

---

## Option 2: Multi-Token Server with Dynamic Switching
**File:** `src/airtable_multi_token.py`  
**Port:** 8041  
**Use Case:** When you need to switch between multiple workspaces dynamically

### Setup Methods:

#### Method 1: Environment Variables
```bash
# Set multiple tokens with naming pattern
export AIRTABLE_TOKEN_CATS="pata5j3UkmpQbqDiA.xxx"
export AIRTABLE_TOKEN_SALES="pat_sales_token"
export AIRTABLE_TOKEN_MARKETING="pat_marketing_token"
export AIRTABLE_TOKEN_HR="pat_hr_token"

# Optional descriptions
export AIRTABLE_DESC_CATS="CATS Organization recruitment"
export AIRTABLE_DESC_SALES="Sales CRM database"

# Start server
python src/airtable_multi_token.py
```

#### Method 2: Configuration File
Create `workspaces.json`:
```json
{
  "default_workspace": "cats_org",
  "workspaces": [
    {
      "name": "cats_org",
      "token": "${AIRTABLE_TOKEN_CATS}",
      "description": "CATS Organization Database",
      "default_base_id": "app73n4PobC7M8mmZ"
    },
    {
      "name": "sales",
      "token": "${AIRTABLE_TOKEN_SALES}",
      "description": "Sales CRM",
      "default_base_id": null
    }
  ]
}
```

#### Method 3: Dynamic Addition at Runtime
Using the MCP tools:
```python
# Add workspace
add_workspace(
    name="new_workspace",
    token="pat_new_token",
    description="New workspace",
    switch_to=True
)

# Switch workspace
switch_workspace("sales")

# List all workspaces
list_workspaces()
```

### Available Tools:
- `list_workspaces` - Show all configured workspaces
- `switch_workspace` - Change active workspace
- `add_workspace` - Add new workspace dynamically
- `remove_workspace` - Remove workspace from memory
- `save_workspace_config` - Save configuration to file
- `list_bases_multi` - List bases from specific workspace
- `cross_workspace_query` - Query multiple workspaces simultaneously

---

## Option 3: Multiple Server Instances
**Use Case:** When you need parallel access to multiple workspaces

Run multiple servers on different ports:
```bash
# Terminal 1 - CATS Organization
AIRTABLE_PERSONAL_ACCESS_TOKEN="token1" \
MCP_SERVER_PORT=8040 \
python src/airtable_server.py

# Terminal 2 - Sales Database
AIRTABLE_PERSONAL_ACCESS_TOKEN="token2" \
MCP_SERVER_PORT=8042 \
python src/airtable_server.py

# Terminal 3 - Marketing
AIRTABLE_PERSONAL_ACCESS_TOKEN="token3" \
MCP_SERVER_PORT=8043 \
python src/airtable_server.py
```

---

## Testing Interfaces

### Single-Token Test
- **HTML:** `test-airtable-mcp.html`
- **Python:** `test_airtable_direct.py`
- **Port:** 8040

### Multi-Token Test
- **HTML:** `test-multi-workspace.html`
- **Port:** 8041
- **Endpoint:** `http://localhost:8041/mcp/`

---

## Real-World Usage Examples

### Example 1: Department-Based Access
Different departments have their own Airtable workspaces:
```bash
export AIRTABLE_TOKEN_HR="pat_hr_xxx"
export AIRTABLE_TOKEN_SALES="pat_sales_xxx"
export AIRTABLE_TOKEN_OPS="pat_ops_xxx"
```

### Example 2: Client-Based Access
Managing multiple client databases:
```bash
export AIRTABLE_TOKEN_CLIENT_A="pat_clienta_xxx"
export AIRTABLE_TOKEN_CLIENT_B="pat_clientb_xxx"
export AIRTABLE_TOKEN_CLIENT_C="pat_clientc_xxx"
```

### Example 3: Environment-Based Access
Different tokens for dev/staging/production:
```bash
export AIRTABLE_TOKEN_DEV="pat_dev_xxx"
export AIRTABLE_TOKEN_STAGING="pat_staging_xxx"
export AIRTABLE_TOKEN_PROD="pat_prod_xxx"
```

---

## Security Best Practices

1. **Never hardcode tokens** - Always use environment variables
2. **Use .env files** - Keep tokens in `.env` (gitignored)
3. **Rotate tokens regularly** - Airtable supports token rotation
4. **Limit token scope** - Create tokens with minimal required permissions
5. **Use secure storage** - Consider using secret management tools in production

---

## Current Setup

Your current token is configured for:
- **Workspace:** CATS Organization
- **Base ID:** app73n4PobC7M8mmZ
- **Tables:** Candidates, Tags, Status, etc.
- **Token:** Stored in `.env` file

To add more workspaces, simply set additional environment variables following the pattern above and restart the multi-token server.

---

## Deployment

When deploying to DigitalOcean or other cloud providers:

1. Use environment variables for tokens (not files)
2. Consider using a secrets manager
3. Run multi-token server for flexibility
4. Use reverse proxy (nginx) to route to correct port
5. Enable HTTPS for production use