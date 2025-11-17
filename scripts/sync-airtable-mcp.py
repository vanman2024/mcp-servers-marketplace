#!/usr/bin/env python3
"""
Sync Airtable MCP Servers data to GitHub repository
Generates markdown files and JSON exports for all MCP servers
Maps deployment configurations, tools, and server metadata
"""

import os
import json
from datetime import datetime
from pathlib import Path
from pyairtable import Api

# Configuration
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "appHbSB7WhT1TxEQb")

# Output directories
SYNC_DIR = Path("airtable-mcp-sync")
SERVERS_DIR = SYNC_DIR / "servers"
PLUGINS_DIR = SYNC_DIR / "plugins"
CONFIGS_DIR = SYNC_DIR / "configs"

def setup_directories():
    """Create output directories"""
    for directory in [SYNC_DIR, SERVERS_DIR, PLUGINS_DIR, CONFIGS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

def clean_field_value(value):
    """Clean field values for safe serialization"""
    if isinstance(value, list):
        return [clean_field_value(v) for v in value]
    elif isinstance(value, dict):
        return {k: clean_field_value(v) for k, v in value.items()}
    else:
        return value

def sync_table_to_json(api, table_name, output_file):
    """Sync entire table to JSON file"""
    table = api.table(AIRTABLE_BASE_ID, table_name)
    records = table.all()

    # Extract just the fields with cleaned values
    data = [
        {
            "id": record["id"],
            "fields": {k: clean_field_value(v) for k, v in record["fields"].items()}
        }
        for record in records
    ]

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Synced {len(data)} records from {table_name} to {output_file}")
    return data

def sync_mcp_servers_to_markdown(servers_data):
    """Generate markdown files for each MCP server"""
    for server in servers_data:
        fields = server["fields"]
        server_name = fields.get("MCP Server Name", "unknown")

        # Determine server type and deployment
        server_type = fields.get("Server Type", "Unknown")
        deployment = fields.get("Deployment Method", "Unknown")
        cloud_status = fields.get("FastMCP Cloud Status", "Not Deployed")

        # Create markdown content
        md_content = f"""# {server_name}

## Overview

**Description**: {fields.get("Description", "No description provided")}

**Purpose**: {fields.get("Purpose", "No purpose specified")}

## Configuration

| Property | Value |
|----------|-------|
| **Server Type** | {server_type} |
| **Deployment Method** | {deployment} |
| **FastMCP Cloud Status** | {cloud_status} |
| **Source Plugin** | {', '.join(fields.get("Source Plugin", [])) if fields.get("Source Plugin") else "N/A"} |
| **Agent Count** | {fields.get("Agent Count", 0)} |

## Connection Details

"""

        # Add connection details based on server type
        if server_type in ["HTTP (Local)", "HTTP (Remote)", "HTTP (FastMCP Cloud)"]:
            port = fields.get("Local Server Port", "N/A")
            md_content += f"**Local Port**: {port}\n"
            md_content += f"**Connection URL**: `{fields.get('Connection URL/Command', 'N/A')}`\n\n"
        else:
            md_content += f"**Command**: `{fields.get('Connection URL/Command', 'N/A')}`\n\n"

        # FastMCP Cloud deployment
        if cloud_status == "Deployed":
            md_content += f"""## FastMCP Cloud Deployment

**Cloud URL**: {fields.get("FastMCP Cloud URL", "N/A")}

"""

        # Environment variables
        env_vars = fields.get("Environment Variables", "")
        if env_vars:
            md_content += f"""## Environment Variables

```bash
{env_vars}
```

"""

        # Available tools
        tools = fields.get("Available Tools", "")
        if tools:
            md_content += f"""## Available Tools

{tools}

"""

        # Package/Source information
        package = fields.get("Package/Source", "")
        if package:
            md_content += f"""## Installation

**Package/Source**: `{package}`

"""

        # Configuration path
        config_path = fields.get("Configuration Path", "")
        if config_path:
            md_content += f"""## Configuration File

**Path**: `{config_path}`

"""

        # Security notes
        security = fields.get("Security Notes", "")
        if security:
            md_content += f"""## Security

{security}

"""

        # Related agents
        agents = fields.get("Agents", [])
        if agents:
            md_content += f"""## Used By Agents

{chr(10).join(f"- {agent}" for agent in agents)}

"""

        md_content += f"""---
*Last synced: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}*
*Airtable Record ID: {server["id"]}*
"""

        # Write to file
        filename = SERVERS_DIR / f"{server_name.lower().replace(' ', '-')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)

    print(f"✅ Generated {len(servers_data)} MCP server markdown files")

def generate_mcp_config_files(servers_data):
    """Generate .mcp.json compatible configuration for each deployment type"""

    # Group by deployment method
    stdio_servers = []
    http_servers = []
    cloud_servers = []

    for server in servers_data:
        fields = server["fields"]
        server_type = fields.get("Server Type", "")
        deployment = fields.get("Deployment Method", "")

        if deployment in ["npx", "Python Script"]:
            stdio_servers.append(fields)
        elif deployment in ["Local HTTP Server", "External Service"]:
            http_servers.append(fields)
        elif deployment == "FastMCP Cloud":
            cloud_servers.append(fields)

    # Generate STDIO servers config
    if stdio_servers:
        stdio_config = {
            "mcpServers": {}
        }

        for server in stdio_servers:
            name = server.get("MCP Server Name", "").lower().replace(" ", "-")
            command_str = server.get("Connection URL/Command", "")

            # Parse command (simple split for now)
            parts = command_str.split()
            command = parts[0] if parts else "npx"
            args = parts[1:] if len(parts) > 1 else []

            # Parse environment variables
            env_vars = {}
            env_str = server.get("Environment Variables", "")
            if env_str:
                for line in env_str.strip().split('\n'):
                    if '=' in line:
                        key, val = line.split('=', 1)
                        env_vars[key.strip()] = val.strip()

            stdio_config["mcpServers"][name] = {
                "command": command,
                "args": args
            }

            if env_vars:
                stdio_config["mcpServers"][name]["env"] = env_vars

        with open(CONFIGS_DIR / "stdio-servers.mcp.json", 'w') as f:
            json.dump(stdio_config, f, indent=2)

        print(f"✅ Generated STDIO servers config ({len(stdio_servers)} servers)")

    # Generate HTTP servers config
    if http_servers:
        http_config = {
            "mcpServers": {}
        }

        for server in http_servers:
            name = server.get("MCP Server Name", "").lower().replace(" ", "-")
            url = server.get("Connection URL/Command", "http://localhost:8000")

            # Parse environment variables
            env_vars = {}
            env_str = server.get("Environment Variables", "")
            if env_str:
                for line in env_str.strip().split('\n'):
                    if '=' in line:
                        key, val = line.split('=', 1)
                        env_vars[key.strip()] = val.strip()

            http_config["mcpServers"][name] = {
                "type": "http",
                "url": url
            }

            if env_vars:
                http_config["mcpServers"][name]["env"] = env_vars

        with open(CONFIGS_DIR / "http-servers.mcp.json", 'w') as f:
            json.dump(http_config, f, indent=2)

        print(f"✅ Generated HTTP servers config ({len(http_servers)} servers)")

    # Generate FastMCP Cloud servers list
    if cloud_servers:
        cloud_list = []
        for server in cloud_servers:
            cloud_list.append({
                "name": server.get("MCP Server Name"),
                "url": server.get("FastMCP Cloud URL"),
                "status": server.get("FastMCP Cloud Status"),
                "description": server.get("Description")
            })

        with open(CONFIGS_DIR / "fastmcp-cloud-servers.json", 'w') as f:
            json.dump(cloud_list, f, indent=2)

        print(f"✅ Generated FastMCP Cloud servers list ({len(cloud_servers)} servers)")

def sync_fastmcp_plugins(api):
    """Sync FastMCP plugin data from Plugins table"""
    table = api.table(AIRTABLE_BASE_ID, "Plugins")
    records = table.all()

    # Filter for FastMCP plugin
    fastmcp_plugins = [
        {
            "id": record["id"],
            "fields": {k: clean_field_value(v) for k, v in record["fields"].items()}
        }
        for record in records
        if "fastmcp" in record["fields"].get("Name", "").lower() or
           "mcp" in record["fields"].get("Name", "").lower()
    ]

    with open(PLUGINS_DIR / "fastmcp-plugins.json", 'w') as f:
        json.dump(fastmcp_plugins, f, indent=2)

    print(f"✅ Synced {len(fastmcp_plugins)} FastMCP-related plugins")
    return fastmcp_plugins

def generate_summary_report(servers_data, plugins_data):
    """Generate comprehensive summary report"""

    # Count by deployment type
    deployment_counts = {}
    for server in servers_data:
        deployment = server["fields"].get("Deployment Method", "Unknown")
        deployment_counts[deployment] = deployment_counts.get(deployment, 0) + 1

    # Count by server type
    type_counts = {}
    for server in servers_data:
        server_type = server["fields"].get("Server Type", "Unknown")
        type_counts[server_type] = type_counts.get(server_type, 0) + 1

    # Count FastMCP Cloud deployments
    cloud_deployed = sum(1 for s in servers_data if s["fields"].get("FastMCP Cloud Status") == "Deployed")

    report = f"""# Airtable MCP Sync Report

**Last Updated**: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}

## Overview

- **Total MCP Servers**: {len(servers_data)}
- **FastMCP Plugins**: {len(plugins_data)}
- **FastMCP Cloud Deployed**: {cloud_deployed}

## Deployment Methods

{chr(10).join(f"- **{method}**: {count}" for method, count in sorted(deployment_counts.items()))}

## Server Types

{chr(10).join(f"- **{stype}**: {count}" for stype, count in sorted(type_counts.items()))}

## Files Generated

- Server markdown files: {len(servers_data)}
- Configuration files: {len([f for f in CONFIGS_DIR.glob('*.json')])}
- Plugin data: {len(plugins_data)} plugins

## Configuration Files

"""

    # List all generated config files
    for config_file in sorted(CONFIGS_DIR.glob('*.json')):
        report += f"- `{config_file.relative_to(SYNC_DIR)}`\n"

    report += f"""
---
*Generated automatically by Airtable MCP sync workflow*
"""

    with open(SYNC_DIR / "MCP-SYNC-REPORT.md", 'w', encoding='utf-8') as f:
        f.write(report)

    print("✅ Generated MCP sync summary report")

def main():
    """Main sync function"""
    print("🚀 Starting Airtable MCP to GitHub sync...")

    if not AIRTABLE_TOKEN:
        print("❌ Error: AIRTABLE_TOKEN environment variable not set")
        return 1

    # Initialize Airtable API
    api = Api(AIRTABLE_TOKEN)

    # Setup directories
    setup_directories()

    # Sync MCP Servers table
    print("\n📥 Syncing MCP Servers table...")
    servers_data = sync_table_to_json(api, "MCP Servers", SYNC_DIR / "mcp-servers.json")

    # Sync FastMCP plugins
    print("\n📥 Syncing FastMCP plugins...")
    plugins_data = sync_fastmcp_plugins(api)

    # Generate markdown files
    print("\n📝 Generating server markdown files...")
    sync_mcp_servers_to_markdown(servers_data)

    # Generate MCP config files
    print("\n⚙️  Generating MCP configuration files...")
    generate_mcp_config_files(servers_data)

    # Generate summary report
    print("\n📊 Generating summary report...")
    generate_summary_report(servers_data, plugins_data)

    print("\n✅ MCP sync completed successfully!")
    return 0

if __name__ == "__main__":
    exit(main())
