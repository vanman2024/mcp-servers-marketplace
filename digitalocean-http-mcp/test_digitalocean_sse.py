#!/usr/bin/env python3
"""Test Digital Ocean MCP server with SSE support"""

import asyncio
import httpx
import json

async def parse_sse_response(response_text):
    """Parse Server-Sent Events response"""
    for line in response_text.strip().split('\n'):
        if line.startswith('data: '):
            return json.loads(line[6:])
    return None

async def test_digitalocean_mcp():
    """Test Digital Ocean MCP server tools"""
    base_url = "http://localhost:8040/"
    headers = {"Accept": "text/event-stream"}
    
    async with httpx.AsyncClient() as client:
        # Initialize connection
        print("🔌 Initializing connection...")
        response = await client.post(base_url, json={
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "0.1.0",
                "capabilities": {},
                "clientInfo": {
                    "name": "DO MCP Test",
                    "version": "1.0.0"
                }
            },
            "id": 1
        }, headers=headers)
        
        result = await parse_sse_response(response.text)
        if result and 'result' in result:
            print(f"✅ Connected: {result['result']['serverInfo']['name']}")
        
        # Test 1: Get Account Info
        print("\n📊 Testing get_account_info...")
        response = await client.post(base_url, json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "get_account_info",
                "arguments": {}
            },
            "id": 2
        }, headers=headers)
        
        result = await parse_sse_response(response.text)
        if result and 'result' in result:
            print(f"Account Email: {result['result'].get('email', 'N/A')}")
            print(f"Droplet Limit: {result['result'].get('droplet_limit', 'N/A')}")
            print(f"Status: {result['result'].get('status', 'N/A')}")
        
        # Test 2: List Droplets
        print("\n💧 Testing list_droplets...")
        response = await client.post(base_url, json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "list_droplets",
                "arguments": {}
            },
            "id": 3
        }, headers=headers)
        
        result = await parse_sse_response(response.text)
        if result and 'result' in result:
            droplets = result['result'].get('droplets', [])
            print(f"Found {len(droplets)} droplets")
            for droplet in droplets:
                print(f"  - {droplet['name']} ({droplet['status']}) - {droplet['ip_address']}")
        
        # Test 3: Create Droplet (Mock)
        print("\n🆕 Testing create_droplet...")
        response = await client.post(base_url, json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "create_droplet",
                "arguments": {
                    "name": "test-mcp-droplet",
                    "region": "nyc3",
                    "size": "s-1vcpu-1gb",
                    "image": "ubuntu-22-04-x64",
                    "tags": ["mcp-test", "demo"]
                }
            },
            "id": 4
        }, headers=headers)
        
        result = await parse_sse_response(response.text)
        if result and 'result' in result:
            droplet = result['result'].get('droplet', {})
            print(f"Created droplet: {droplet.get('name')} (ID: {droplet.get('id')})")
            print(f"Status: {droplet.get('status')}")
        
        # Test 4: List SSH Keys
        print("\n🔑 Testing list_ssh_keys...")
        response = await client.post(base_url, json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "list_ssh_keys",
                "arguments": {}
            },
            "id": 5
        }, headers=headers)
        
        result = await parse_sse_response(response.text)
        if result and 'result' in result:
            keys = result['result'].get('ssh_keys', [])
            print(f"Found {len(keys)} SSH keys")
            for key in keys:
                print(f"  - {key['name']} ({key['fingerprint']})")
        
        # Test 5: Get Resource - Regions
        print("\n📚 Testing resource: regions...")
        response = await client.post(base_url, json={
            "jsonrpc": "2.0",
            "method": "resources/read",
            "params": {
                "uri": "resource://regions"
            },
            "id": 6
        }, headers=headers)
        
        result = await parse_sse_response(response.text)
        if result and 'result' in result:
            content = result['result']['contents'][0]
            if content['mimeType'] == 'application/json':
                regions = json.loads(content['text'])['regions']
                print(f"Available regions: {', '.join(regions.keys())}")
        
        # Test 6: Get Prompt - Droplet Creation Guide
        print("\n💡 Testing prompt: droplet_creation_guide...")
        response = await client.post(base_url, json={
            "jsonrpc": "2.0",
            "method": "prompts/get",
            "params": {
                "name": "droplet_creation_guide",
                "arguments": {
                    "purpose": "web_server",
                    "environment": "production"
                }
            },
            "id": 7
        }, headers=headers)
        
        result = await parse_sse_response(response.text)
        if result and 'result' in result:
            prompt_text = result['result']['messages'][0]['content']['text']
            print("Prompt preview:")
            print(prompt_text[:200] + "...")
        
        # Test 7: Manage Droplet Action
        print("\n⚡ Testing manage_droplet (reboot)...")
        response = await client.post(base_url, json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "manage_droplet",
                "arguments": {
                    "droplet_id": 123456789,
                    "action": "reboot"
                }
            },
            "id": 8
        }, headers=headers)
        
        result = await parse_sse_response(response.text)
        if result and 'result' in result:
            action = result['result']
            print(f"Action initiated: {action.get('type')} (ID: {action.get('action_id')})")
            print(f"Status: {action.get('status')}")

if __name__ == "__main__":
    print("🌊 Digital Ocean MCP Server Test (with SSE)")
    print("=" * 50)
    asyncio.run(test_digitalocean_mcp())