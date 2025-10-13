#!/usr/bin/env python3
"""
Enhanced Airtable MCP Server with Multi-Token Support
Allows switching between different Airtable workspaces/accounts
"""

import os
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import asyncio
import aiohttp
from fastmcp import FastMCP, Context
from datetime import datetime

# Token configuration
@dataclass
class AirtableWorkspace:
    """Represents an Airtable workspace with its own token"""
    name: str
    token: str
    description: str = ""
    default_base_id: Optional[str] = None

class MultiTokenAirtableClient:
    """Enhanced Airtable client supporting multiple tokens"""
    
    def __init__(self):
        self.workspaces: Dict[str, AirtableWorkspace] = {}
        self.current_workspace: Optional[str] = None
        self.sessions: Dict[str, aiohttp.ClientSession] = {}
        self.base_url = "https://api.airtable.com/v0"
        self.load_workspaces()
    
    def load_workspaces(self):
        """Load workspace configurations from environment or config file"""
        
        # Method 1: Load from environment variables with pattern
        # AIRTABLE_TOKEN_WORKSPACE1=token1
        # AIRTABLE_TOKEN_WORKSPACE2=token2
        for key, value in os.environ.items():
            if key.startswith('AIRTABLE_TOKEN_'):
                workspace_name = key.replace('AIRTABLE_TOKEN_', '').lower()
                self.workspaces[workspace_name] = AirtableWorkspace(
                    name=workspace_name,
                    token=value,
                    description=os.getenv(f'AIRTABLE_DESC_{workspace_name.upper()}', '')
                )
        
        # Method 2: Load from JSON config file
        config_file = os.path.join(os.path.dirname(__file__), '..', 'workspaces.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                for ws in config.get('workspaces', []):
                    self.workspaces[ws['name']] = AirtableWorkspace(**ws)
                self.current_workspace = config.get('default_workspace')
        
        # Method 3: Single token fallback (backward compatibility)
        if not self.workspaces:
            single_token = os.getenv('AIRTABLE_PERSONAL_ACCESS_TOKEN')
            if single_token:
                self.workspaces['default'] = AirtableWorkspace(
                    name='default',
                    token=single_token,
                    description='Default workspace'
                )
                self.current_workspace = 'default'
    
    def get_current_token(self) -> Optional[str]:
        """Get the current workspace token"""
        if self.current_workspace and self.current_workspace in self.workspaces:
            return self.workspaces[self.current_workspace].token
        return None
    
    def switch_workspace(self, workspace_name: str) -> bool:
        """Switch to a different workspace"""
        if workspace_name in self.workspaces:
            self.current_workspace = workspace_name
            return True
        return False
    
    def add_workspace(self, name: str, token: str, description: str = "", 
                     default_base_id: Optional[str] = None):
        """Add a new workspace dynamically"""
        self.workspaces[name] = AirtableWorkspace(
            name=name,
            token=token,
            description=description,
            default_base_id=default_base_id
        )
    
    async def get_session(self, workspace_name: Optional[str] = None) -> aiohttp.ClientSession:
        """Get or create session for a workspace"""
        ws_name = workspace_name or self.current_workspace
        if not ws_name or ws_name not in self.workspaces:
            raise ValueError(f"Invalid workspace: {ws_name}")
        
        if ws_name not in self.sessions:
            token = self.workspaces[ws_name].token
            self.sessions[ws_name] = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
        return self.sessions[ws_name]
    
    async def make_request(self, method: str, endpoint: str, 
                          workspace: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Make API request with workspace-specific token"""
        ws_name = workspace or self.current_workspace
        if not ws_name:
            return {"success": False, "error": "No workspace selected"}
        
        try:
            session = await self.get_session(ws_name)
            url = f"{self.base_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
            
            async with session.request(method, url, **kwargs) as response:
                data = await response.json()
                
                if response.status == 200:
                    return {"success": True, "data": data, "workspace": ws_name}
                else:
                    return {
                        "success": False, 
                        "error": f"API error: {response.status}",
                        "details": data,
                        "workspace": ws_name
                    }
        except Exception as e:
            return {"success": False, "error": str(e), "workspace": ws_name}
    
    async def cleanup(self):
        """Clean up all sessions"""
        for session in self.sessions.values():
            await session.close()

# Initialize FastMCP server with multi-token support
mcp = FastMCP("Airtable Multi-Token Server")
client = MultiTokenAirtableClient()

# Token/Workspace Management Tools
@mcp.tool()
async def list_workspaces(ctx: Optional[Context] = None) -> Dict[str, Any]:
    """List all configured Airtable workspaces.
    
    Returns:
        List of available workspaces with their details
    """
    workspaces = []
    for name, ws in client.workspaces.items():
        workspaces.append({
            "name": name,
            "description": ws.description,
            "is_current": name == client.current_workspace,
            "has_default_base": ws.default_base_id is not None,
            "default_base_id": ws.default_base_id
        })
    
    return {
        "success": True,
        "workspaces": workspaces,
        "current_workspace": client.current_workspace,
        "total": len(workspaces)
    }

@mcp.tool()
async def switch_workspace(workspace_name: str, ctx: Optional[Context] = None) -> Dict[str, Any]:
    """Switch to a different Airtable workspace.
    
    Args:
        workspace_name: Name of the workspace to switch to
    
    Returns:
        Switch result with workspace details
    """
    if client.switch_workspace(workspace_name):
        ws = client.workspaces[workspace_name]
        return {
            "success": True,
            "message": f"Switched to workspace: {workspace_name}",
            "workspace": {
                "name": ws.name,
                "description": ws.description,
                "default_base_id": ws.default_base_id
            }
        }
    else:
        return {
            "success": False,
            "error": f"Workspace '{workspace_name}' not found",
            "available_workspaces": list(client.workspaces.keys())
        }

@mcp.tool()
async def add_workspace(
    name: str,
    token: str,
    description: str = "",
    default_base_id: Optional[str] = None,
    switch_to: bool = True,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Add a new Airtable workspace dynamically.
    
    Args:
        name: Workspace name (alphanumeric and underscores)
        token: Airtable Personal Access Token
        description: Optional workspace description
        default_base_id: Optional default base ID for this workspace
        switch_to: Whether to switch to this workspace after adding
    
    Returns:
        Result of adding the workspace
    """
    # Validate name
    if not name.replace('_', '').isalnum():
        return {
            "success": False,
            "error": "Workspace name must be alphanumeric with underscores only"
        }
    
    # Add the workspace
    client.add_workspace(name, token, description, default_base_id)
    
    result = {
        "success": True,
        "message": f"Added workspace: {name}",
        "workspace": {
            "name": name,
            "description": description,
            "default_base_id": default_base_id
        }
    }
    
    # Switch if requested
    if switch_to:
        client.current_workspace = name
        result["switched"] = True
        result["message"] += f" and switched to it"
    
    return result

@mcp.tool()
async def remove_workspace(
    workspace_name: str,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Remove a workspace from memory (does not affect config files).
    
    Args:
        workspace_name: Name of workspace to remove
    
    Returns:
        Removal result
    """
    if workspace_name not in client.workspaces:
        return {
            "success": False,
            "error": f"Workspace '{workspace_name}' not found"
        }
    
    # Don't remove current workspace
    if workspace_name == client.current_workspace:
        return {
            "success": False,
            "error": "Cannot remove current workspace. Switch to another first."
        }
    
    # Close session if exists
    if workspace_name in client.sessions:
        await client.sessions[workspace_name].close()
        del client.sessions[workspace_name]
    
    # Remove workspace
    del client.workspaces[workspace_name]
    
    return {
        "success": True,
        "message": f"Removed workspace: {workspace_name}",
        "remaining_workspaces": list(client.workspaces.keys())
    }

@mcp.tool()
async def save_workspace_config(
    file_path: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Save current workspace configuration to a JSON file.
    
    Args:
        file_path: Optional path to save config (defaults to workspaces.json)
    
    Returns:
        Save result
    """
    if not file_path:
        file_path = os.path.join(os.path.dirname(__file__), '..', 'workspaces.json')
    
    config = {
        "default_workspace": client.current_workspace,
        "workspaces": []
    }
    
    for name, ws in client.workspaces.items():
        # Don't save tokens directly - use placeholders
        config["workspaces"].append({
            "name": ws.name,
            "token": f"${{{name.upper()}_TOKEN}}",  # Environment variable placeholder
            "description": ws.description,
            "default_base_id": ws.default_base_id
        })
    
    try:
        with open(file_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return {
            "success": True,
            "message": f"Saved configuration to {file_path}",
            "workspaces_saved": len(config["workspaces"])
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to save config: {str(e)}"
        }

# Enhanced base operations with workspace support
@mcp.tool()
async def list_bases_multi(
    workspace: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """List bases from a specific workspace or current workspace.
    
    Args:
        workspace: Optional workspace name (uses current if not specified)
    
    Returns:
        List of bases accessible in the workspace
    """
    ws_name = workspace or client.current_workspace
    if not ws_name:
        return {"success": False, "error": "No workspace selected"}
    
    result = await client.make_request('GET', 'meta/bases', workspace=ws_name)
    
    if result.get('success'):
        bases = result['data'].get('bases', [])
        return {
            "success": True,
            "workspace": ws_name,
            "bases": bases,
            "count": len(bases)
        }
    return result

@mcp.tool()
async def cross_workspace_query(
    workspaces: List[str],
    operation: str,
    params: Dict[str, Any],
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Execute the same operation across multiple workspaces.
    
    Args:
        workspaces: List of workspace names to query
        operation: Operation to perform (e.g., 'list_bases', 'list_records')
        params: Parameters for the operation
    
    Returns:
        Results from all workspaces
    """
    results = {}
    
    for ws_name in workspaces:
        if ws_name not in client.workspaces:
            results[ws_name] = {"error": f"Workspace '{ws_name}' not found"}
            continue
        
        # Execute operation based on type
        if operation == 'list_bases':
            result = await list_bases_multi(workspace=ws_name)
        elif operation == 'list_records':
            # You'd implement workspace-aware list_records here
            result = {"error": "Not implemented yet"}
        else:
            result = {"error": f"Unknown operation: {operation}"}
        
        results[ws_name] = result
    
    return {
        "success": True,
        "operation": operation,
        "workspaces_queried": len(workspaces),
        "results": results
    }

# Resources for multi-token usage
@mcp.resource("resource://multi_token_guide/{section}")
async def get_multi_token_guide(section: str = "overview") -> str:
    """Guide for using multiple Airtable tokens"""
    return """
# Multi-Token Airtable MCP Server Guide

## Setup Methods

### 1. Environment Variables
Set multiple tokens with pattern:
```bash
export AIRTABLE_TOKEN_SALES=pat_sales_token_here
export AIRTABLE_TOKEN_MARKETING=pat_marketing_token_here
export AIRTABLE_TOKEN_OPERATIONS=pat_ops_token_here
```

### 2. Configuration File (workspaces.json)
```json
{
  "default_workspace": "sales",
  "workspaces": [
    {
      "name": "sales",
      "token": "${SALES_TOKEN}",
      "description": "Sales team workspace",
      "default_base_id": "appXXXXXXXXXXXX"
    },
    {
      "name": "marketing",
      "token": "${MARKETING_TOKEN}",
      "description": "Marketing campaigns",
      "default_base_id": "appYYYYYYYYYYYY"
    }
  ]
}
```

### 3. Dynamic Addition
Use the `add_workspace` tool to add workspaces at runtime.

## Usage Examples

1. **List available workspaces:**
   ```
   list_workspaces()
   ```

2. **Switch workspace:**
   ```
   switch_workspace("marketing")
   ```

3. **Add new workspace:**
   ```
   add_workspace(
     name="hr",
     token="pat_hr_token",
     description="HR database"
   )
   ```

4. **Query across workspaces:**
   ```
   cross_workspace_query(
     workspaces=["sales", "marketing"],
     operation="list_bases",
     params={}
   )
   ```

## Best Practices

1. **Security:** Never hardcode tokens. Use environment variables or secure vaults.
2. **Naming:** Use descriptive workspace names (team, department, project).
3. **Defaults:** Set default_base_id for frequently accessed bases.
4. **Sessions:** The server maintains separate sessions per workspace for efficiency.
"""

if __name__ == "__main__":
    # Startup message
    print("🚀 Airtable Multi-Token MCP Server")
    print(f"📊 Loaded {len(client.workspaces)} workspace(s)")
    for name, ws in client.workspaces.items():
        current = "✓" if name == client.current_workspace else " "
        print(f"  [{current}] {name}: {ws.description or 'No description'}")
    
    # Run server with streamable-http transport
    port = int(os.getenv("MCP_SERVER_PORT", 8041))
    print(f"\n🌐 Starting server on port {port}")
    print(f"📍 Test interface: http://localhost:{port}/")
    
    mcp.run(
        transport="streamable-http",
        port=port
    )