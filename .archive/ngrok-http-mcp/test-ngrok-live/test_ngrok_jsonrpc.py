#!/usr/bin/env python3
"""
JSON-RPC Test client for ngrok MCP server
"""

import requests
import json
import uuid
from datetime import datetime

class NgrokJSONRPCTestClient:
    def __init__(self, base_url="http://localhost:8050"):
        self.base_url = base_url
        self.session_id = str(uuid.uuid4())
        self.message_id = 0
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "X-Session-ID": self.session_id
        }
        
    def get_next_id(self):
        self.message_id += 1
        return self.message_id
        
    def call_method(self, method, params=None):
        """Call a JSON-RPC method"""
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": self.get_next_id()
        }
        
        print(f"\n📤 Calling: {method}")
        print(json.dumps(request, indent=2))
        
        try:
            response = requests.post(
                self.base_url,
                json=request,
                headers=self.headers,
                timeout=30
            )
            
            print(f"\n📥 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(json.dumps(data, indent=2))
                return data
            else:
                print(f"❌ Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Request failed: {str(e)}")
            return None
    
    def test_all_features(self):
        """Test all ngrok features"""
        print("🚀 Testing ngrok MCP Server with JSON-RPC")
        print(f"📋 Session ID: {self.session_id}")
        print("=" * 60)
        
        # Test 1: List available tools
        print("\n=== Test 1: List Available Tools ===")
        self.call_method("tools/list")
        
        # Test 2: Create tunnels for MCP servers
        print("\n=== Test 2: Creating Tunnels for MCP Servers ===")
        
        servers = [
            ("github-mcp", 8011),
            ("figma-mcp", 8042),
            ("supabase-mcp", 8013),
            ("memory-mcp", 8007),
            ("filesystem-mcp", 8006),
            ("v0-mcp", 8010)
        ]
        
        created_tunnels = []
        
        for name, port in servers:
            print(f"\n--- Creating tunnel for {name} on port {port} ---")
            result = self.call_method("tools/call", {
                "name": "create_tunnel",
                "arguments": {
                    "name": name,
                    "protocol": "http",
                    "addr": f"localhost:{port}"
                }
            })
            
            if result and "result" in result:
                created_tunnels.append(name)
                print(f"✅ Tunnel created for {name}")
        
        # Test 3: List all tunnels
        print("\n=== Test 3: List All Tunnels ===")
        self.call_method("tools/call", {
            "name": "list_tunnels",
            "arguments": {}
        })
        
        # Test 4: Get tunnel details
        if created_tunnels:
            print(f"\n=== Test 4: Inspect Tunnel: {created_tunnels[0]} ===")
            self.call_method("tools/call", {
                "name": "tunnel_inspect",
                "arguments": {
                    "tunnel_id": created_tunnels[0],
                    "include_traffic": True
                }
            })
        
        # Test 5: Health dashboard
        print("\n=== Test 5: Generate Health Dashboard ===")
        self.call_method("tools/call", {
            "name": "health_dashboard_generate",
            "arguments": {
                "include_all_resources": True
            }
        })
        
        print("\n✅ Testing completed!")
        print(f"\n📝 Summary: Created {len(created_tunnels)} tunnels")
        
        # Print tunnel URLs if available
        print("\n🌐 Your MCP servers should now be accessible via ngrok URLs")
        print("   Check the list_tunnels output above for the public URLs")

def main():
    # Run tests
    client = NgrokJSONRPCTestClient()
    client.test_all_features()

if __name__ == "__main__":
    main()