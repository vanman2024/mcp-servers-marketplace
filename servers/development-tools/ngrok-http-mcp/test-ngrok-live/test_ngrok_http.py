#!/usr/bin/env python3
"""
HTTP Test client for ngrok MCP server
"""

import requests
import json
import uuid
from datetime import datetime

class NgrokHTTPTestClient:
    def __init__(self, base_url="http://localhost:8050"):
        self.base_url = base_url
        self.session_id = str(uuid.uuid4())
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "X-Session-ID": self.session_id
        }
        
    def call_tool(self, tool_name, **kwargs):
        """Call an ngrok MCP tool"""
        url = f"{self.base_url}/tool/{tool_name}"
        
        print(f"\n📤 Calling: {tool_name}")
        print(f"   URL: {url}")
        print(f"   Params: {json.dumps(kwargs, indent=2)}")
        
        try:
            response = requests.post(
                url,
                json=kwargs,
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
        print("🚀 Testing ngrok MCP Server")
        print(f"📋 Session ID: {self.session_id}")
        print("=" * 60)
        
        # Test 1: Create tunnels for all MCP servers
        print("\n=== Creating Tunnels for MCP Servers ===")
        
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
            result = self.call_tool(
                "create_tunnel",
                name=name,
                protocol="http",
                addr=f"localhost:{port}"
            )
            if result:
                created_tunnels.append(name)
        
        # Test 2: List all tunnels
        print("\n=== Listing All Tunnels ===")
        self.call_tool("list_tunnels")
        
        # Test 3: Get tunnel details
        if created_tunnels:
            print(f"\n=== Inspecting Tunnel: {created_tunnels[0]} ===")
            self.call_tool(
                "tunnel_inspect",
                tunnel_id=created_tunnels[0],
                include_traffic=True
            )
        
        # Test 4: Health dashboard
        print("\n=== Generating Health Dashboard ===")
        self.call_tool(
            "health_dashboard_generate",
            include_all_resources=True
        )
        
        # Test 5: Try to reserve a domain (if using paid ngrok)
        print("\n=== Testing Domain Reservation (Paid Feature) ===")
        self.call_tool(
            "reserve_domain",
            name="mcp-servers.ngrok.app"
        )
        
        print("\n✅ Testing completed!")
        print("\n📝 Summary:")
        print(f"   - Created {len(created_tunnels)} tunnels")
        print("   - Tunnels are now publicly accessible via ngrok URLs")
        print("\n💡 Next steps:")
        print("   1. Check the tunnel URLs from the list_tunnels output")
        print("   2. Test accessing your MCP servers via those URLs")
        print("   3. Configure custom domains if you have ngrok paid plan")

def main():
    # First check if ngrok MCP server is running
    print("🔍 Checking if ngrok MCP server is running...")
    
    try:
        response = requests.get("http://localhost:8050/health", timeout=2)
        if response.status_code != 200:
            print("⚠️  ngrok MCP server might not be fully operational")
    except:
        print("❌ Cannot connect to ngrok MCP server on port 8050")
        print("\nPlease ensure it's running:")
        print("  ./scripts/mcp-manager.sh start ngrok-http")
        return
    
    # Run tests
    client = NgrokHTTPTestClient()
    client.test_all_features()

if __name__ == "__main__":
    main()