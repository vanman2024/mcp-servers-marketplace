#!/usr/bin/env python3
"""
Digital Ocean HTTP MCP Server - Cloud Infrastructure Management

A comprehensive MCP server for managing Digital Ocean resources including droplets,
databases, Kubernetes clusters, App Platform apps, and more.

All tools use class-based methods for better testability and maintainability.
"""

import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import httpx
import json
from fastmcp import FastMCP
from fastmcp.server.context import Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================================================================
# CONFIGURATION & INITIALIZATION  
# ===================================================================

# Initialize FastMCP server
mcp = FastMCP("Digital Ocean Manager")

# Digital Ocean API configuration
DO_API_BASE = "https://api.digitalocean.com/v2"
DO_API_TOKEN = os.getenv("DIGITALOCEAN_API_TOKEN")
MOCK_MODE = os.getenv("DO_MOCK_MODE", "false").lower() == "true"

class DigitalOceanClient:
    """Async client for Digital Ocean API interactions with error handling"""
    
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {DO_API_TOKEN}",
            "Content-Type": "application/json"
        }
    
    async def make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Digital Ocean API with error handling"""
        
        # Mock mode for testing
        if MOCK_MODE:
            return await self._mock_response(method, endpoint, data, params)
        
        url = f"{DO_API_BASE}{endpoint}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, headers=self.headers, params=params)
                elif method.upper() == "POST":
                    response = await client.post(url, headers=self.headers, json=data)
                elif method.upper() == "PUT":
                    response = await client.put(url, headers=self.headers, json=data)
                elif method.upper() == "DELETE":
                    response = await client.delete(url, headers=self.headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json() if response.text else {"success": True}
                
            except httpx.HTTPStatusError as e:
                logger.error(f"DO API HTTP error: {e.response.status_code} - {e.response.text}")
                return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
            except Exception as e:
                logger.error(f"DO API request failed: {str(e)}")
                return {"error": str(e)}
    
    async def _mock_response(self, method: str, endpoint: str, data: Optional[Dict], params: Optional[Dict]) -> Dict[str, Any]:
        """Generate mock responses for testing"""
        if endpoint == "/account":
            return {
                "account": {
                    "email": "test@example.com",
                    "uuid": "test-uuid-123",
                    "status": "active",
                    "droplet_limit": 25,
                    "floating_ip_limit": 5,
                    "email_verified": True,
                    "team": {"uuid": "team-123", "name": "Test Team"}
                }
            }
        elif endpoint == "/account/keys":
            return {
                "ssh_keys": [
                    {
                        "id": 12345,
                        "name": "test-key",
                        "fingerprint": "aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99",
                        "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQtest..."
                    }
                ]
            }
        elif endpoint == "/droplets":
            if method == "GET":
                return {
                    "droplets": [
                        {
                            "id": 123456789,
                            "name": "test-droplet-01",
                            "status": "active",
                            "size_slug": "s-2vcpu-2gb",
                            "region": {"slug": "nyc3"},
                            "image": {"slug": "ubuntu-22-04-x64"},
                            "networks": {"v4": [{"ip_address": "192.168.1.1"}]},
                            "created_at": "2024-01-01T00:00:00Z",
                            "tags": ["test", "mcp"],
                            "features": ["monitoring", "ipv6"]
                        }
                    ]
                }
            elif method == "POST":
                return {
                    "droplet": {
                        "id": 987654321,
                        "name": data.get("name", "new-droplet"),
                        "status": "new",
                        "size_slug": data.get("size"),
                        "region": {"slug": data.get("region")},
                        "image": {"slug": data.get("image")},
                        "networks": {"v4": []},
                        "created_at": datetime.now().isoformat(),
                        "tags": data.get("tags", []),
                        "features": []
                    },
                    "links": {"actions": [{"id": 111222333}]}
                }
        elif endpoint.startswith("/droplets/") and "/actions" in endpoint:
            return {
                "action": {
                    "id": 444555666,
                    "status": "in-progress",
                    "type": data.get("type"),
                    "started_at": datetime.now().isoformat(),
                    "resource_type": "droplet",
                    "resource_id": int(endpoint.split("/")[2])
                }
            }
        elif endpoint.startswith("/droplets/") and method == "DELETE":
            return {"success": True}
        elif endpoint == "/databases":
            if method == "GET":
                return {
                    "databases": [
                        {
                            "id": "db-123",
                            "name": "test-db-cluster",
                            "engine": "pg",
                            "version": "15",
                            "size": "db-s-2vcpu-4gb",
                            "region": "nyc3",
                            "status": "online",
                            "num_nodes": 2,
                            "connection": {
                                "host": "test-db-cluster-do-user-123.db.ondigitalocean.com",
                                "port": 25060,
                                "database": "defaultdb",
                                "user": "doadmin"
                            }
                        }
                    ]
                }
            elif method == "POST":
                return {
                    "database": {
                        "id": "db-456",
                        "name": data.get("name"),
                        "engine": data.get("engine"),
                        "version": data.get("version"),
                        "size": data.get("size"),
                        "region": data.get("region"),
                        "status": "creating",
                        "num_nodes": data.get("num_nodes", 1),
                        "connection": {}
                    }
                }
        elif endpoint == "/apps":
            if method == "GET":
                return {
                    "apps": [
                        {
                            "id": "app-123",
                            "spec": {"name": "test-app", "region": "nyc"},
                            "default_ingress": "https://test-app.ondigitalocean.app",
                            "created_at": "2024-01-01T00:00:00Z",
                            "updated_at": "2024-01-01T00:00:00Z",
                            "active_deployment": {"id": "deploy-123"},
                            "in_progress_deployment": None
                        }
                    ]
                }
            elif method == "POST":
                spec = data.get("spec", {})
                return {
                    "app": {
                        "id": "app-456",
                        "spec": spec,
                        "default_ingress": f"https://{spec.get('name', 'app')}.ondigitalocean.app",
                        "created_at": datetime.now().isoformat()
                    }
                }
        
        return {"error": f"Mock response not implemented for {method} {endpoint}"}

# Initialize Digital Ocean client
do_client = DigitalOceanClient()

# Helper functions
def format_droplet_info(droplet: Dict) -> Dict[str, Any]:
    """Format droplet information for display"""
    # Safely get IP address from networks
    v4_networks = droplet.get("networks", {}).get("v4", [])
    ip_address = v4_networks[0].get("ip_address") if v4_networks else None
    
    return {
        "id": droplet.get("id"),
        "name": droplet.get("name"),
        "status": droplet.get("status"),
        "size": droplet.get("size_slug"),
        "region": droplet.get("region", {}).get("slug"),
        "image": droplet.get("image", {}).get("slug"),
        "ip_address": ip_address,
        "created_at": droplet.get("created_at"),
        "tags": droplet.get("tags", []),
        "features": droplet.get("features", [])
    }

def format_database_info(db: Dict) -> Dict[str, Any]:
    """Format database cluster information"""
    return {
        "id": db.get("id"),
        "name": db.get("name"),
        "engine": db.get("engine"),
        "version": db.get("version"),
        "size": db.get("size"),
        "region": db.get("region"),
        "status": db.get("status"),
        "nodes": db.get("num_nodes"),
        "connection": {
            "host": db.get("connection", {}).get("host"),
            "port": db.get("connection", {}).get("port"),
            "database": db.get("connection", {}).get("database"),
            "user": db.get("connection", {}).get("user")
        }
    }

# ===================================================================
# STANDALONE TOOLS (simple tools that don't call other tools)
# ===================================================================

@mcp.tool()
async def get_account_info(ctx: Optional[Context] = None) -> Dict[str, Any]:
    """
    Get Digital Ocean account information including limits and status.
    
    Returns:
        Account details including email, droplet limit, and status
    """
    if not DO_API_TOKEN:
        return {"error": "Digital Ocean API token not configured"}
    
    if ctx:
        await ctx.info("Fetching Digital Ocean account information")
    
    result = await do_client.make_request("GET", "/account")
    
    if "error" in result:
        return result
    
    account = result.get("account", {})
    return {
        "email": account.get("email"),
        "uuid": account.get("uuid"),
        "status": account.get("status"),
        "droplet_limit": account.get("droplet_limit"),
        "floating_ip_limit": account.get("floating_ip_limit"),
        "email_verified": account.get("email_verified"),
        "team": {
            "uuid": account.get("team", {}).get("uuid"),
            "name": account.get("team", {}).get("name")
        }
    }

@mcp.tool()
async def list_ssh_keys(ctx: Optional[Context] = None) -> Dict[str, Any]:
    """
    List all SSH keys in the account.
    
    Returns:
        List of SSH keys with fingerprints and names
    """
    if ctx:
        await ctx.info("Listing SSH keys")
    
    result = await do_client.make_request("GET", "/account/keys")
    
    if "error" in result:
        return result
    
    keys = result.get("ssh_keys", [])
    return {
        "ssh_keys": [
            {
                "id": key.get("id"),
                "name": key.get("name"),
                "fingerprint": key.get("fingerprint"),
                "public_key": key.get("public_key")[:50] + "..." if key.get("public_key") else None
            }
            for key in keys
        ],
        "total": len(keys)
    }

# ===================================================================
# CLASS-BASED TOOLS (complex tools that call other tools)
# ===================================================================

class DropletTools:
    """Tools for managing Digital Ocean droplets"""
    
    async def list_droplets(
        self,
        tag_name: Optional[str] = None,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        List all droplets or filter by tag.
        
        Args:
            tag_name: Optional tag to filter droplets
            ctx: Context for logging
            
        Returns:
            List of droplets with details
        """
        if ctx:
            await ctx.info(f"Listing droplets{' with tag: ' + tag_name if tag_name else ''}")
        
        params = {"tag_name": tag_name} if tag_name else None
        result = await do_client.make_request("GET", "/droplets", params=params)
        
        if "error" in result:
            return result
        
        droplets = result.get("droplets", [])
        return {
            "droplets": [format_droplet_info(d) for d in droplets],
            "total": len(droplets),
            "filtered_by_tag": tag_name
        }
    
    async def create_droplet(
        self,
        name: str,
        region: str,
        size: str,
        image: str,
        ssh_keys: Optional[List[str]] = None,
        backups: bool = False,
        ipv6: bool = True,
        monitoring: bool = True,
        tags: Optional[List[str]] = None,
        user_data: Optional[str] = None,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Create a new droplet.
        
        Args:
            name: Droplet hostname
            region: Region slug (e.g., "nyc3", "sfo3")
            size: Size slug (e.g., "s-1vcpu-1gb", "s-2vcpu-2gb")
            image: Image slug (e.g., "ubuntu-22-04-x64") or ID
            ssh_keys: List of SSH key IDs or fingerprints
            backups: Enable automated backups
            ipv6: Enable IPv6
            monitoring: Enable monitoring
            tags: List of tags
            user_data: Cloud-init user data script
            ctx: Context for logging
            
        Returns:
            Created droplet details
        """
        if ctx:
            await ctx.info(f"Creating droplet '{name}' in {region}")
        
        data = {
            "name": name,
            "region": region,
            "size": size,
            "image": image,
            "ssh_keys": ssh_keys or [],
            "backups": backups,
            "ipv6": ipv6,
            "monitoring": monitoring,
            "tags": tags or [],
            "user_data": user_data
        }
        
        result = await do_client.make_request("POST", "/droplets", data=data)
        
        if "error" in result:
            return result
        
        droplet = result.get("droplet", {})
        return {
            "droplet": format_droplet_info(droplet),
            "action_id": result.get("links", {}).get("actions", [{}])[0].get("id")
        }
    
    async def manage_droplet(
        self,
        droplet_id: int,
        action: str,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Perform an action on a droplet (power on/off, reboot, etc).
        
        Args:
            droplet_id: Droplet ID
            action: Action type (power_on, power_off, reboot, shutdown, enable_backups)
            ctx: Context for logging
            
        Returns:
            Action status
        """
        valid_actions = [
            "power_on", "power_off", "reboot", "shutdown", 
            "enable_backups", "disable_backups", "enable_ipv6",
            "snapshot", "rebuild", "resize"
        ]
        
        if action not in valid_actions:
            return {"error": f"Invalid action. Must be one of: {', '.join(valid_actions)}"}
        
        if ctx:
            await ctx.info(f"Performing '{action}' on droplet {droplet_id}")
        
        data = {"type": action}
        result = await do_client.make_request("POST", f"/droplets/{droplet_id}/actions", data=data)
        
        if "error" in result:
            return result
        
        action_info = result.get("action", {})
        return {
            "action_id": action_info.get("id"),
            "status": action_info.get("status"),
            "type": action_info.get("type"),
            "started_at": action_info.get("started_at"),
            "resource_type": action_info.get("resource_type"),
            "resource_id": action_info.get("resource_id")
        }
    
    async def delete_droplet(
        self,
        droplet_id: int,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Delete a droplet permanently.
        
        Args:
            droplet_id: Droplet ID to delete
            ctx: Context for logging
            
        Returns:
            Deletion status
        """
        if ctx:
            await ctx.warning(f"Deleting droplet {droplet_id}")
        
        result = await do_client.make_request("DELETE", f"/droplets/{droplet_id}")
        
        if "error" in result:
            return result
        
        return {
            "success": True,
            "message": f"Droplet {droplet_id} deletion initiated"
        }

class DatabaseTools:
    """Tools for managing Digital Ocean managed databases"""
    
    async def list_databases(
        self,
        tag_name: Optional[str] = None,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        List all database clusters.
        
        Args:
            tag_name: Optional tag to filter databases
            ctx: Context for logging
            
        Returns:
            List of database clusters
        """
        if ctx:
            await ctx.info("Listing database clusters")
        
        params = {"tag_name": tag_name} if tag_name else None
        result = await do_client.make_request("GET", "/databases", params=params)
        
        if "error" in result:
            return result
        
        databases = result.get("databases", [])
        return {
            "databases": [format_database_info(db) for db in databases],
            "total": len(databases)
        }
    
    async def create_database(
        self,
        name: str,
        engine: str,
        version: str,
        region: str,
        size: str,
        num_nodes: int = 1,
        tags: Optional[List[str]] = None,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Create a managed database cluster.
        
        Args:
            name: Database cluster name
            engine: Database engine (pg, mysql, redis, mongodb)
            version: Engine version
            region: Region slug
            size: Size slug (e.g., "db-s-1vcpu-1gb")
            num_nodes: Number of nodes (1-3)
            tags: Optional tags
            ctx: Context for logging
            
        Returns:
            Created database details
        """
        if ctx:
            await ctx.info(f"Creating {engine} database '{name}'")
        
        data = {
            "name": name,
            "engine": engine,
            "version": version,
            "region": region,
            "size": size,
            "num_nodes": num_nodes,
            "tags": tags or []
        }
        
        result = await do_client.make_request("POST", "/databases", data=data)
        
        if "error" in result:
            return result
        
        database = result.get("database", {})
        return {
            "database": format_database_info(database),
            "message": "Database cluster creation initiated"
        }

class AppPlatformTools:
    """Tools for managing App Platform applications"""
    
    async def list_apps(
        self,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        List all App Platform apps.
        
        Returns:
            List of apps with details
        """
        if ctx:
            await ctx.info("Listing App Platform apps")
        
        result = await do_client.make_request("GET", "/apps")
        
        if "error" in result:
            return result
        
        apps = result.get("apps", [])
        return {
            "apps": [
                {
                    "id": app.get("id"),
                    "spec": {
                        "name": app.get("spec", {}).get("name"),
                        "region": app.get("spec", {}).get("region")
                    },
                    "default_ingress": app.get("default_ingress"),
                    "created_at": app.get("created_at"),
                    "updated_at": app.get("updated_at"),
                    "active_deployment_id": app.get("active_deployment", {}).get("id") if app.get("active_deployment") else None,
                    "in_progress_deployment_id": app.get("in_progress_deployment", {}).get("id") if app.get("in_progress_deployment") else None
                }
                for app in apps
            ],
            "total": len(apps)
        }
    
    async def create_app(
        self,
        spec: Dict[str, Any],
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Create a new App Platform app from spec.
        
        Args:
            spec: App specification (see Digital Ocean docs)
            ctx: Context for logging
            
        Returns:
            Created app details
        """
        if ctx:
            await ctx.info(f"Creating app '{spec.get('name', 'unnamed')}'")
        
        data = {"spec": spec}
        result = await do_client.make_request("POST", "/apps", data=data)
        
        if "error" in result:
            return result
        
        app = result.get("app", {})
        return {
            "app_id": app.get("id"),
            "spec": app.get("spec"),
            "default_ingress": app.get("default_ingress"),
            "created_at": app.get("created_at")
        }

# Register class methods with mcp.tool()
droplet_tools = DropletTools()
mcp.tool(droplet_tools.list_droplets)
mcp.tool(droplet_tools.create_droplet)
mcp.tool(droplet_tools.manage_droplet)
mcp.tool(droplet_tools.delete_droplet)

database_tools = DatabaseTools()
mcp.tool(database_tools.list_databases)
mcp.tool(database_tools.create_database)

app_tools = AppPlatformTools()
mcp.tool(app_tools.list_apps)
mcp.tool(app_tools.create_app)

# ===================================================================
# RESOURCES
# ===================================================================

@mcp.resource("resource://usage_guide")
def usage_guide() -> str:
    """Critical usage guide - READ THIS FIRST"""
    return """
# Digital Ocean MCP Server Usage Guide

## 🚨 CRITICAL: Authentication Required!

This server requires a Digital Ocean API token. Set it as:
```bash
export DIGITALOCEAN_API_TOKEN=your_token_here
```

Get your token from: https://cloud.digitalocean.com/account/api/tokens

## Server Capabilities

### Droplet Management
- List, create, manage, and delete droplets
- Power operations (on/off/reboot)
- Enable backups, IPv6, monitoring
- Snapshot and resize operations

### Database Management
- Create managed PostgreSQL, MySQL, Redis, MongoDB clusters
- List and manage existing clusters
- Automatic backups and failover

### App Platform
- Deploy containerized apps
- Manage deployments
- Scale applications

## Common Operations

### Creating a Droplet:
```python
await create_droplet(
    name="web-server-01",
    region="nyc3",
    size="s-2vcpu-2gb",
    image="ubuntu-22-04-x64",
    ssh_keys=["fingerprint_here"],
    tags=["production", "web"]
)
```

### Managing Droplets:
```python
# Power operations
await manage_droplet(droplet_id=123456, action="reboot")

# Enable backups
await manage_droplet(droplet_id=123456, action="enable_backups")
```

## Rate Limits
- Standard: 5,000 requests/hour
- Burst: 250 requests/minute
- Use pagination for large lists

## Best Practices
1. Always tag resources for organization
2. Enable backups for production droplets
3. Use monitoring for observability
4. Implement proper error handling
5. Store sensitive data in environment variables
"""

@mcp.resource("resource://regions")
def regions_list() -> Dict[str, Any]:
    """Available Digital Ocean regions"""
    return {
        "regions": {
            "nyc1": {"name": "New York 1", "available": True},
            "nyc3": {"name": "New York 3", "available": True},
            "sfo3": {"name": "San Francisco 3", "available": True},
            "ams3": {"name": "Amsterdam 3", "available": True},
            "sgp1": {"name": "Singapore 1", "available": True},
            "lon1": {"name": "London 1", "available": True},
            "fra1": {"name": "Frankfurt 1", "available": True},
            "tor1": {"name": "Toronto 1", "available": True},
            "blr1": {"name": "Bangalore 1", "available": True}
        }
    }

@mcp.resource("resource://sizes")
def droplet_sizes() -> Dict[str, Any]:
    """Available droplet sizes and pricing"""
    return {
        "basic": {
            "s-1vcpu-1gb": {"vcpus": 1, "memory": "1GB", "disk": "25GB", "price": "$6/mo"},
            "s-1vcpu-2gb": {"vcpus": 1, "memory": "2GB", "disk": "50GB", "price": "$12/mo"},
            "s-2vcpu-2gb": {"vcpus": 2, "memory": "2GB", "disk": "60GB", "price": "$18/mo"},
            "s-2vcpu-4gb": {"vcpus": 2, "memory": "4GB", "disk": "80GB", "price": "$24/mo"}
        },
        "general": {
            "g-2vcpu-8gb": {"vcpus": 2, "memory": "8GB", "disk": "25GB", "price": "$60/mo"},
            "g-4vcpu-16gb": {"vcpus": 4, "memory": "16GB", "disk": "50GB", "price": "$120/mo"}
        },
        "cpu_optimized": {
            "c-2": {"vcpus": 2, "memory": "4GB", "disk": "25GB", "price": "$40/mo"},
            "c-4": {"vcpus": 4, "memory": "8GB", "disk": "50GB", "price": "$80/mo"}
        }
    }

@mcp.resource("resource://images")
def available_images() -> Dict[str, Any]:
    """Common droplet images"""
    return {
        "distributions": {
            "ubuntu-22-04-x64": "Ubuntu 22.04 LTS",
            "ubuntu-20-04-x64": "Ubuntu 20.04 LTS",
            "debian-11-x64": "Debian 11",
            "centos-stream-9-x64": "CentOS Stream 9",
            "fedora-38-x64": "Fedora 38",
            "rocky-9-x64": "Rocky Linux 9"
        },
        "applications": {
            "docker-20-04": "Docker on Ubuntu 20.04",
            "wordpress-20-04": "WordPress on Ubuntu 20.04",
            "nodejs-20-04": "NodeJS on Ubuntu 20.04",
            "lamp-20-04": "LAMP on Ubuntu 20.04"
        }
    }

@mcp.resource("resource://examples/droplet_creation")
def droplet_examples() -> str:
    """Examples of droplet creation"""
    return """
# Droplet Creation Examples

## Basic Web Server
```python
await create_droplet(
    name="web-prod-01",
    region="nyc3",
    size="s-2vcpu-4gb",
    image="ubuntu-22-04-x64",
    ssh_keys=["your-ssh-fingerprint"],
    monitoring=True,
    tags=["production", "web"]
)
```

## Development Environment
```python
await create_droplet(
    name="dev-env-01",
    region="sfo3",
    size="s-1vcpu-2gb",
    image="docker-20-04",
    backups=False,
    tags=["development"],
    user_data=\"\"\"#!/bin/bash
    apt-get update
    apt-get install -y git vim
    \"\"\"
)
```

## Database Server
```python
await create_droplet(
    name="db-prod-01",
    region="nyc3",
    size="g-4vcpu-16gb",
    image="ubuntu-22-04-x64",
    backups=True,
    monitoring=True,
    tags=["production", "database"],
    ssh_keys=["your-ssh-fingerprint"]
)
```
"""

# ===================================================================
# PROMPTS
# ===================================================================

@mcp.prompt
def droplet_creation_guide(purpose: str, environment: str = "production") -> str:
    """Guide for creating droplets based on purpose"""
    configs = {
        "web_server": {
            "production": {
                "size": "s-2vcpu-4gb or higher",
                "features": ["monitoring", "backups", "ipv6"],
                "recommended_image": "ubuntu-22-04-x64"
            },
            "development": {
                "size": "s-1vcpu-1gb",
                "features": ["ipv6"],
                "recommended_image": "docker-20-04"
            }
        },
        "database": {
            "production": {
                "size": "g-4vcpu-16gb or higher",
                "features": ["monitoring", "backups"],
                "recommended_image": "ubuntu-22-04-x64",
                "note": "Consider managed databases for production"
            }
        },
        "api_server": {
            "production": {
                "size": "s-2vcpu-2gb or higher",
                "features": ["monitoring", "ipv6"],
                "recommended_image": "ubuntu-22-04-x64"
            }
        }
    }
    
    config = configs.get(purpose, {}).get(environment, {})
    
    return f"""
# Droplet Creation Guide for {purpose} ({environment})

## Recommended Configuration:
- Size: {config.get('size', 's-1vcpu-1gb')}
- Image: {config.get('recommended_image', 'ubuntu-22-04-x64')}
- Features: {', '.join(config.get('features', []))}

## Considerations:
1. Choose region closest to your users
2. Enable monitoring for production workloads
3. Always enable backups for critical data
4. Use tags for organization
5. Configure firewall rules after creation

{config.get('note', '')}

## Example Command:
Create a {purpose} droplet with appropriate settings based on the recommendations above.
"""

@mcp.prompt
def troubleshooting_guide(issue_type: str) -> str:
    """Troubleshooting guide for common issues"""
    guides = {
        "ssh_connection": """
# SSH Connection Troubleshooting

1. **Check droplet status**: Ensure droplet is powered on
2. **Verify SSH key**: Confirm key was added during creation
3. **Check firewall**: Port 22 must be open
4. **Use console**: Access via DO web console if SSH fails
5. **Reset root password**: Use DO panel if needed
""",
        "slow_performance": """
# Performance Troubleshooting

1. **Check metrics**: Use monitoring to identify bottlenecks
2. **Review size**: Upgrade if CPU/memory constrained
3. **Check disk I/O**: Look for high disk usage
4. **Network issues**: Test bandwidth and latency
5. **Application tuning**: Optimize application configuration
""",
        "api_errors": """
# API Error Troubleshooting

1. **Check authentication**: Verify API token is valid
2. **Rate limits**: Ensure not exceeding limits
3. **Validate parameters**: Check all required fields
4. **Region availability**: Confirm resources available in region
5. **Account limits**: Verify not at droplet limit
"""
    }
    
    return guides.get(issue_type, "Please specify: ssh_connection, slow_performance, or api_errors")

@mcp.prompt
def migration_guide(from_provider: str) -> str:
    """Guide for migrating from other providers"""
    return f"""
# Migration Guide from {from_provider} to Digital Ocean

## Pre-Migration Checklist:
1. Inventory current resources
2. Document configurations
3. Export data and databases
4. Note networking setup
5. List dependencies

## Migration Steps:
1. **Create DO resources**: Match current setup
2. **Transfer data**: Use rsync or backup/restore
3. **Update DNS**: Point to new IP addresses
4. **Test thoroughly**: Verify all functionality
5. **Cut over**: Switch traffic to DO
6. **Monitor**: Watch for issues

## Post-Migration:
- Keep old resources for rollback
- Update documentation
- Train team on DO tools
- Set up monitoring/alerts
"""

@mcp.prompt
def cost_optimization() -> str:
    """Cost optimization strategies"""
    return """
# Digital Ocean Cost Optimization Guide

## Strategies:
1. **Right-size droplets**: Monitor usage and adjust
2. **Use snapshots**: Instead of keeping unused droplets
3. **Reserved capacity**: For long-term workloads
4. **Automated backups**: Only for critical systems
5. **Clean up**: Remove unused resources

## Tools:
- Monitoring: Track resource utilization
- Alerts: Notify of unusual usage
- Tags: Organize for cost tracking
- Billing alerts: Set spending limits

## Best Practices:
- Review monthly usage
- Automate resource cleanup
- Use object storage for static assets
- Consider managed services vs self-hosted
"""

@mcp.prompt
def security_best_practices() -> str:
    """Security configuration guide"""
    return """
# Digital Ocean Security Best Practices

## Essential Security Measures:

### 1. SSH Security
- Disable root login
- Use SSH keys only
- Change default SSH port
- Implement fail2ban

### 2. Firewall Configuration
- Enable cloud firewalls
- Restrict ports to necessary only
- Implement IP whitelisting
- Use VPC for internal communication

### 3. System Updates
- Enable automatic security updates
- Regular patching schedule
- Monitor CVE alerts

### 4. Monitoring
- Enable DO monitoring
- Set up alerts
- Log aggregation
- Intrusion detection

### 5. Backups
- Automated backups
- Test restore procedures
- Off-site backup copies
- Encryption at rest
"""

# ===================================================================
# SERVER EXECUTION
# ===================================================================

if __name__ == "__main__":
    # Check for API token
    if not DO_API_TOKEN:
        logger.warning("DIGITALOCEAN_API_TOKEN not found - server will run with limited functionality")
        logger.info("Set DIGITALOCEAN_API_TOKEN environment variable to enable full Digital Ocean API access")
    
    # Get port from environment or use default
    port = int(os.getenv('DIGITALOCEAN_MCP_PORT', '8040'))
    
    logger.info(f"Starting Digital Ocean Manager MCP Server on port {port}")
    logger.info("Available tools: list_droplets, create_droplet, manage_droplet, list_databases, create_database, list_apps, create_app")
    logger.info("Available resources: usage_guide, regions, sizes, images, examples/droplet_creation")
    logger.info("Available prompts: droplet_creation_guide, troubleshooting_guide, migration_guide, cost_optimization, security_best_practices")
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")