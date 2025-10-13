#!/usr/bin/env python3
"""
Test client for ngrok MCP server
Tests all ngrok functionality in a proper client-server setup
"""

import asyncio
import json
import uuid
import websockets
from datetime import datetime

class NgrokMCPTestClient:
    def __init__(self, server_url="ws://localhost:8050"):
        self.server_url = server_url
        self.session_id = str(uuid.uuid4())
        self.message_id = 0
        
    def get_next_id(self):
        self.message_id += 1
        return self.message_id
        
    async def send_request(self, websocket, method, params=None):
        """Send a JSON-RPC request and wait for response"""
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self.get_next_id(),
            "params": params or {}
        }
        
        print(f"\n📤 Sending: {method}")
        print(json.dumps(request, indent=2))
        
        await websocket.send(json.dumps(request))
        
        # Wait for response
        response = await websocket.recv()
        response_data = json.loads(response)
        
        print(f"\n📥 Response:")
        print(json.dumps(response_data, indent=2))
        
        return response_data
        
    async def test_ngrok_operations(self):
        """Test all ngrok MCP operations"""
        headers = {
            "X-Session-ID": self.session_id
        }
        
        async with websockets.connect(
            self.server_url,
            extra_headers=headers,
            subprotocols=["mcp"]
        ) as websocket:
            print(f"✅ Connected to ngrok MCP server at {self.server_url}")
            print(f"📋 Session ID: {self.session_id}")
            
            # Test 1: List available tools
            print("\n=== Test 1: List Available Tools ===")
            await self.send_request(websocket, "tools/list")
            
            # Test 2: Create tunnel for GitHub MCP
            print("\n=== Test 2: Create Tunnel for GitHub MCP ===")
            result = await self.send_request(websocket, "tools/call", {
                "name": "create_tunnel",
                "arguments": {
                    "name": "github-mcp-test",
                    "protocol": "http",
                    "addr": "localhost:8011"
                }
            })
            
            # Test 3: Create tunnel for Figma MCP
            print("\n=== Test 3: Create Tunnel for Figma MCP ===")
            await self.send_request(websocket, "tools/call", {
                "name": "create_tunnel",
                "arguments": {
                    "name": "figma-mcp-test",
                    "protocol": "http", 
                    "addr": "localhost:8042"
                }
            })
            
            # Test 4: List all tunnels
            print("\n=== Test 4: List All Tunnels ===")
            tunnels = await self.send_request(websocket, "tools/call", {
                "name": "list_tunnels",
                "arguments": {}
            })
            
            # Test 5: Get tunnel traffic/status
            print("\n=== Test 5: Get Tunnel Status ===")
            if tunnels.get("result") and tunnels["result"].get("content"):
                content = json.loads(tunnels["result"]["content"][0]["text"])
                if content.get("tunnels") and len(content["tunnels"]) > 0:
                    tunnel_id = content["tunnels"][0].get("name", "github-mcp-test")
                    await self.send_request(websocket, "tools/call", {
                        "name": "tunnel_inspect",
                        "arguments": {
                            "tunnel_id": tunnel_id,
                            "include_traffic": True
                        }
                    })
            
            # Test 6: Health dashboard
            print("\n=== Test 6: Generate Health Dashboard ===")
            await self.send_request(websocket, "tools/call", {
                "name": "health_dashboard_generate",
                "arguments": {
                    "include_all_resources": True
                }
            })
            
            print("\n✅ All tests completed!")

async def main():
    print("🚀 Starting ngrok MCP Test Client")
    print("=" * 50)
    
    client = NgrokMCPTestClient()
    
    try:
        await client.test_ngrok_operations()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure the ngrok MCP server is running on port 8050")
        print("Run: ./scripts/mcp-manager.sh status | grep ngrok")

if __name__ == "__main__":
    asyncio.run(main())