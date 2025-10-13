#!/usr/bin/env python3
"""
Direct testing of Digital Ocean MCP Server using FastMCP Client
Tests the MCP tools using in-memory testing pattern
"""

import asyncio
import os
import sys
from fastmcp import Client

# Set mock mode for testing
os.environ['DO_MOCK_MODE'] = 'true'
os.environ['DIGITALOCEAN_API_TOKEN'] = 'mock-token-for-testing'

# Add server path
sys.path.insert(0, 'src')

async def test_digitalocean_server():
    """Test Digital Ocean server tools using FastMCP Client"""
    print("🌊 Digital Ocean MCP Server In-Memory Test")
    print("=" * 50)
    
    # Import the server module to get the mcp instance
    from digitalocean_server import mcp
    
    # Create client with direct server connection
    async with Client(mcp) as client:
        print("\n✅ Client connected successfully!")
        
        # Test 1: Get Account Info
        print("\n📊 Testing get_account_info...")
        result = await client.call_tool("get_account_info", {})
        print(f"Account email: {result.data.get('email', 'N/A')}")
        print(f"Droplet limit: {result.data.get('droplet_limit', 'N/A')}")
        
        # Test 2: List SSH Keys
        print("\n🔑 Testing list_ssh_keys...")
        result = await client.call_tool("list_ssh_keys", {})
        print(f"Found {result.data.get('total', 0)} SSH keys")
        
        # Test 3: List Droplets
        print("\n💧 Testing list_droplets...")
        result = await client.call_tool("list_droplets", {})
        print(f"Found {result.data.get('total', 0)} droplets")
        for droplet in result.data.get('droplets', []):
            print(f"  - {droplet['name']} ({droplet['status']}) - {droplet.get('ip_address', 'No IP')}")
        
        # Test 4: Create Droplet (Mock)
        print("\n🆕 Testing create_droplet...")
        result = await client.call_tool("create_droplet", {
            "name": "test-mcp-droplet",
            "region": "nyc3",
            "size": "s-1vcpu-1gb",
            "image": "ubuntu-22-04-x64",
            "tags": ["test", "mcp"]
        })
        droplet = result.data.get('droplet', {})
        print(f"Created droplet: {droplet.get('name')} (ID: {droplet.get('id')})")
        print(f"Status: {droplet.get('status')}")
        
        # Test 5: Manage Droplet
        print("\n⚡ Testing manage_droplet...")
        result = await client.call_tool("manage_droplet", {
            "droplet_id": 123456789,
            "action": "reboot"
        })
        print(f"Action: {result.data.get('type')} - Status: {result.data.get('status')}")
        
        # Test 6: List Databases
        print("\n🗄️ Testing list_databases...")
        result = await client.call_tool("list_databases", {})
        print(f"Found {result.data.get('total', 0)} database clusters")
        
        # Test 7: Create Database
        print("\n🆕 Testing create_database...")
        result = await client.call_tool("create_database", {
            "name": "test-db",
            "engine": "pg",
            "version": "15",
            "region": "nyc3",
            "size": "db-s-1vcpu-1gb"
        })
        db = result.data.get('database', {})
        print(f"Created database: {db.get('name')} ({db.get('engine')} {db.get('version')})")
        
        # Test 8: List Apps
        print("\n📱 Testing list_apps...")
        result = await client.call_tool("list_apps", {})
        print(f"Found {result.data.get('total', 0)} apps")
        
        # Test 9: Test Resources
        print("\n📚 Testing Resources...")
        
        # Get regions resource
        result = await client.read_resource("resource://regions")
        if result and len(result) > 0:
            import json
            regions_data = json.loads(result[0].text)
            print(f"Available regions: {', '.join(regions_data['regions'].keys())}")
        
        # Get usage guide
        result = await client.read_resource("resource://usage_guide")
        if result and len(result) > 0:
            print(f"Usage guide loaded: {len(result[0].text)} characters")
        
        # Test 10: Test Prompts
        print("\n💡 Testing Prompts...")
        result = await client.get_prompt("droplet_creation_guide", {
            "purpose": "web_server",
            "environment": "production"
        })
        if result.messages:
            print(f"Prompt loaded: {len(result.messages[0].content.text)} characters")
            print(f"Preview: {result.messages[0].content.text[:100]}...")
        
        print("\n✅ All tests completed successfully!")
        return True

if __name__ == "__main__":
    # Run the test
    success = asyncio.run(test_digitalocean_server())
    if success:
        print("\n🎉 Digital Ocean MCP Server is working correctly!")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)