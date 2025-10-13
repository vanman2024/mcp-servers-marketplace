#!/usr/bin/env python3
"""Test Digital Ocean MCP server using FastMCP client"""

import asyncio
from fastmcp import FastMCP

# Create a test client that uses our server as a tool
test_app = FastMCP("DO Test Client")

@test_app.tool()
async def test_all_do_tools():
    """Test all Digital Ocean tools"""
    # Import the server directly
    import sys
    sys.path.append('/home/gotime2022/mcp-kernel-new/servers/http/digitalocean-http-mcp/src')
    from digitalocean_server import (
        get_account_info, list_ssh_keys, 
        droplet_tools, database_tools, app_tools
    )
    
    results = {}
    
    # Test 1: Account Info
    print("🔍 Testing get_account_info...")
    account = await get_account_info()
    results['account'] = account
    print(f"✅ Account: {account.get('email', 'N/A')}")
    
    # Test 2: SSH Keys
    print("\n🔑 Testing list_ssh_keys...")
    keys = await list_ssh_keys()
    results['ssh_keys'] = keys
    print(f"✅ Found {keys.get('total', 0)} SSH keys")
    
    # Test 3: List Droplets
    print("\n💧 Testing list_droplets...")
    droplets = await droplet_tools.list_droplets()
    results['droplets'] = droplets
    print(f"✅ Found {droplets.get('total', 0)} droplets")
    
    # Test 4: Create Droplet
    print("\n🆕 Testing create_droplet...")
    new_droplet = await droplet_tools.create_droplet(
        name="test-mcp-droplet",
        region="nyc3",
        size="s-1vcpu-1gb",
        image="ubuntu-22-04-x64",
        tags=["test", "mcp"]
    )
    results['new_droplet'] = new_droplet
    print(f"✅ Created droplet: {new_droplet.get('droplet', {}).get('name', 'N/A')}")
    
    # Test 5: Manage Droplet
    print("\n⚡ Testing manage_droplet...")
    action = await droplet_tools.manage_droplet(
        droplet_id=123456789,
        action="reboot"
    )
    results['droplet_action'] = action
    print(f"✅ Action: {action.get('type', 'N/A')} - {action.get('status', 'N/A')}")
    
    # Test 6: List Databases
    print("\n🗄️ Testing list_databases...")
    databases = await database_tools.list_databases()
    results['databases'] = databases
    print(f"✅ Found {databases.get('total', 0)} databases")
    
    # Test 7: Create Database
    print("\n🆕 Testing create_database...")
    new_db = await database_tools.create_database(
        name="test-db",
        engine="pg",
        version="15",
        region="nyc3",
        size="db-s-1vcpu-1gb"
    )
    results['new_database'] = new_db
    print(f"✅ Created database: {new_db.get('database', {}).get('name', 'N/A')}")
    
    # Test 8: List Apps
    print("\n📱 Testing list_apps...")
    apps = await app_tools.list_apps()
    results['apps'] = apps
    print(f"✅ Found {apps.get('total', 0)} apps")
    
    # Test 9: Create App
    print("\n🆕 Testing create_app...")
    new_app = await app_tools.create_app(
        spec={
            "name": "test-app",
            "region": "nyc",
            "services": [{
                "name": "web",
                "environment_slug": "node-js"
            }]
        }
    )
    results['new_app'] = new_app
    print(f"✅ Created app: {new_app.get('spec', {}).get('name', 'N/A')}")
    
    return results

# Test resources
@test_app.tool()
async def test_resources():
    """Test resource access"""
    import sys
    sys.path.append('/home/gotime2022/mcp-kernel-new/servers/http/digitalocean-http-mcp/src')
    from digitalocean_server import usage_guide, regions_list, droplet_sizes
    
    print("\n📚 Testing Resources...")
    
    # Test usage guide
    guide = usage_guide()
    print(f"✅ Usage guide: {len(guide)} characters")
    
    # Test regions
    regions = regions_list()
    print(f"✅ Regions: {len(regions['regions'])} available")
    
    # Test sizes
    sizes = droplet_sizes()
    print(f"✅ Droplet sizes: {len(sizes)} categories")
    
    return True

# Test prompts
@test_app.tool()
async def test_prompts():
    """Test prompt generation"""
    import sys
    sys.path.append('/home/gotime2022/mcp-kernel-new/servers/http/digitalocean-http-mcp/src')
    from digitalocean_server import droplet_creation_guide, troubleshooting_guide
    
    print("\n💡 Testing Prompts...")
    
    # Test droplet guide
    guide = droplet_creation_guide("web_server", "production")
    print(f"✅ Droplet guide: {len(guide)} characters")
    
    # Test troubleshooting
    trouble = troubleshooting_guide("ssh_connection")
    print(f"✅ Troubleshooting guide: {len(trouble)} characters")
    
    return True

async def main():
    print("🌊 Digital Ocean MCP Server Direct Test")
    print("=" * 50)
    
    # Test all tools
    results = await test_all_do_tools()
    
    # Test resources
    await test_resources()
    
    # Test prompts
    await test_prompts()
    
    print("\n✅ All tests completed successfully!")
    print(f"\nSummary:")
    print(f"- Account verified: {results['account'].get('email', 'N/A')}")
    print(f"- Droplets: {results['droplets']['total']}")
    print(f"- Databases: {results['databases']['total']}")
    print(f"- Apps: {results['apps']['total']}")
    print(f"- SSH Keys: {results['ssh_keys']['total']}")

if __name__ == "__main__":
    # Set mock mode
    import os
    os.environ['DO_MOCK_MODE'] = 'true'
    os.environ['DIGITALOCEAN_API_TOKEN'] = 'mock-token'
    
    asyncio.run(main())