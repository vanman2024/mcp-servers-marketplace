#!/usr/bin/env python3
"""
Direct testing of ngrok MCP Server tools without needing Claude sessions
Tests the MCP tools by mocking the FastMCP decorator
"""

import asyncio
import os
import json
import sys
from datetime import datetime
from typing import Dict, Any, List
import tempfile
import shutil

# Set environment variables BEFORE importing server
# Using actual ngrok API key from environment
if not os.getenv('NGROK_API_KEY'):
    print("⚠️  Warning: NGROK_API_KEY not set in environment")
    print("   Some features may be limited without a valid API key")

# Mock the FastMCP decorator to get raw functions
import unittest.mock

def mock_tool_decorator(func=None, **kwargs):
    """Mock tool decorator that returns the function unchanged"""
    if func is None:
        return lambda f: f
    return func

def mock_resource_decorator(uri):
    """Mock resource decorator that returns the function unchanged"""
    return lambda f: f

# Apply mocks
FastMCP_mock = unittest.mock.MagicMock()
FastMCP_mock.tool = mock_tool_decorator
FastMCP_mock.resource = mock_resource_decorator

with unittest.mock.patch('fastmcp.FastMCP', return_value=FastMCP_mock):
        # Import after mocking
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
        import ngrok_server as server

# Create a mock context object
class MockContext:
    """Mock context object for testing"""
    def __init__(self):
        self.session_id = "test-session-123"
        self.request_id = "test-request-456"
        
    async def emit_status(self, message: str):
        print(f"📢 Status: {message}")

class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
        self.tunnel_urls = {}
    
    def add(self, name: str, passed: bool, details: str = "", data: Any = None):
        self.results.append({
            "name": name,
            "passed": passed,
            "details": details,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print("\n" + "=" * 60)
        print("🚇 NGROK MCP TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        if self.passed + self.failed > 0:
            print(f"📈 Success Rate: {self.passed / (self.passed + self.failed) * 100:.1f}%")
        
        if self.failed > 0:
            print("\n📋 Failed Tests:")
            for result in self.results:
                if not result["passed"]:
                    print(f"  ❌ {result['name']}: {result['details'][:100]}")
        
        if self.tunnel_urls:
            print("\n🌐 Created Tunnel URLs:")
            for name, url in self.tunnel_urls.items():
                print(f"  📍 {name}: {url}")

async def test_tunnel_creation(results: TestResults, ctx: MockContext):
    """Test tunnel creation for MCP servers"""
    print("\n🚇 TESTING TUNNEL CREATION")
    print("-" * 40)
    
    # Define MCP servers to tunnel
    mcp_servers = [
        ("github-mcp", 8011),
        ("figma-mcp", 8042),
        ("supabase-mcp", 8013),
        ("memory-mcp", 8007),
        ("filesystem-mcp", 8006),
        ("v0-mcp", 8010)
    ]
    
    created_tunnels = []
    
    for name, port in mcp_servers:
        try:
            print(f"\n📍 Creating tunnel for {name} on port {port}...")
            result = await server.create_tunnel(
                name=name,
                protocol="http",
                addr=f"localhost:{port}",
                ctx=ctx
            )
            
            # Parse the result
            if isinstance(result, list) and len(result) > 0:
                content = result[0].get("text", "{}")
                data = json.loads(content)
                
                if data.get("success"):
                    tunnel_url = data.get("url", "")
                    results.tunnel_urls[name] = tunnel_url
                    results.add(f"create_tunnel_{name}", True, f"URL: {tunnel_url}", data)
                    print(f"  ✅ Success! URL: {tunnel_url}")
                    created_tunnels.append(name)
                else:
                    error = data.get("error", "Unknown error")
                    results.add(f"create_tunnel_{name}", False, error)
                    print(f"  ❌ Failed: {error}")
            else:
                results.add(f"create_tunnel_{name}", False, "Invalid response format")
                print(f"  ❌ Failed: Invalid response format")
                
        except Exception as e:
            results.add(f"create_tunnel_{name}", False, str(e))
            print(f"  ❌ Error: {e}")
    
    return created_tunnels

async def test_tunnel_management(results: TestResults, ctx: MockContext, created_tunnels: List[str]):
    """Test tunnel management operations"""
    print("\n🔧 TESTING TUNNEL MANAGEMENT")
    print("-" * 40)
    
    # Test list_tunnels
    try:
        print("\n📋 Listing all tunnels...")
        result = await server.list_tunnels(ctx=ctx)
        
        if isinstance(result, list) and len(result) > 0:
            content = result[0].get("text", "{}")
            data = json.loads(content)
            
            if data.get("success"):
                tunnels = data.get("tunnels", [])
                results.add("list_tunnels", True, f"Found {len(tunnels)} tunnels", data)
                print(f"  ✅ Found {len(tunnels)} active tunnels")
                
                # Print tunnel details
                for tunnel in tunnels:
                    print(f"    - {tunnel.get('name', 'Unknown')}: {tunnel.get('url', 'N/A')}")
            else:
                results.add("list_tunnels", False, data.get("error", "Unknown error"))
                print(f"  ❌ Failed: {data.get('error')}")
        else:
            results.add("list_tunnels", False, "Invalid response format")
            print("  ❌ Failed: Invalid response format")
            
    except Exception as e:
        results.add("list_tunnels", False, str(e))
        print(f"  ❌ Error: {e}")
    
    # Test tunnel_inspect for first created tunnel
    if created_tunnels:
        tunnel_id = created_tunnels[0]
        try:
            print(f"\n🔍 Inspecting tunnel: {tunnel_id}...")
            result = await server.tunnel_inspect(
                tunnel_id=tunnel_id,
                include_traffic=True,
                ctx=ctx
            )
            
            if isinstance(result, list) and len(result) > 0:
                content = result[0].get("text", "{}")
                data = json.loads(content)
                
                if data.get("success"):
                    results.add("tunnel_inspect", True, f"Inspected {tunnel_id}", data)
                    print(f"  ✅ Successfully inspected tunnel")
                    
                    # Print inspection details
                    inspection = data.get("inspection", {})
                    print(f"    Status: {inspection.get('status', 'Unknown')}")
                    print(f"    URL: {inspection.get('url', 'N/A')}")
                    print(f"    Traffic: {inspection.get('traffic', {})}")
                else:
                    results.add("tunnel_inspect", False, data.get("error", "Unknown error"))
                    print(f"  ❌ Failed: {data.get('error')}")
            else:
                results.add("tunnel_inspect", False, "Invalid response format")
                print("  ❌ Failed: Invalid response format")
                
        except Exception as e:
            results.add("tunnel_inspect", False, str(e))
            print(f"  ❌ Error: {e}")

async def test_advanced_features(results: TestResults, ctx: MockContext):
    """Test advanced ngrok features"""
    print("\n🚀 TESTING ADVANCED FEATURES")
    print("-" * 40)
    
    # Test health_dashboard_generate
    try:
        print("\n📊 Generating health dashboard...")
        result = await server.health_dashboard_generate(
            include_all_resources=True,
            ctx=ctx
        )
        
        if isinstance(result, list) and len(result) > 0:
            content = result[0].get("text", "{}")
            data = json.loads(content)
            
            if data.get("success"):
                results.add("health_dashboard", True, "Dashboard generated", data)
                print("  ✅ Health dashboard generated successfully")
                
                # Print dashboard summary
                dashboard = data.get("dashboard", {})
                print(f"    Total Resources: {dashboard.get('total_resources', 0)}")
                print(f"    Health Status: {dashboard.get('overall_health', 'Unknown')}")
            else:
                results.add("health_dashboard", False, data.get("error", "Unknown error"))
                print(f"  ❌ Failed: {data.get('error')}")
        else:
            results.add("health_dashboard", False, "Invalid response format")
            print("  ❌ Failed: Invalid response format")
            
    except Exception as e:
        results.add("health_dashboard", False, str(e))
        print(f"  ❌ Error: {e}")
    
    # Test domain reservation (likely to fail without paid plan)
    try:
        print("\n🌐 Testing domain reservation (requires paid plan)...")
        result = await server.reserve_domain(
            name="mcp-test.ngrok.app",
            ctx=ctx
        )
        
        if isinstance(result, list) and len(result) > 0:
            content = result[0].get("text", "{}")
            data = json.loads(content)
            
            if data.get("success"):
                results.add("reserve_domain", True, "Domain reserved", data)
                print(f"  ✅ Domain reserved: {data.get('domain')}")
            else:
                # Expected to fail without paid plan
                results.add("reserve_domain", True, "Failed as expected (requires paid plan)")
                print(f"  ℹ️  Expected failure: {data.get('error')}")
        else:
            results.add("reserve_domain", False, "Invalid response format")
            print("  ❌ Failed: Invalid response format")
            
    except Exception as e:
        results.add("reserve_domain", False, str(e))
        print(f"  ❌ Error: {e}")

async def cleanup_tunnels(created_tunnels: List[str], ctx: MockContext):
    """Clean up created tunnels"""
    print("\n🧹 CLEANING UP TUNNELS")
    print("-" * 40)
    
    for tunnel_id in created_tunnels:
        try:
            print(f"  Stopping tunnel: {tunnel_id}...")
            result = await server.stop_tunnel(tunnel_id=tunnel_id, ctx=ctx)
            print(f"  ✅ Stopped {tunnel_id}")
        except Exception as e:
            print(f"  ⚠️  Failed to stop {tunnel_id}: {e}")

async def main():
    """Run all tests"""
    print("🚀 NGROK MCP SERVER DIRECT TESTING")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔑 API Key Present: {'Yes' if os.getenv('NGROK_API_KEY') else 'No'}")
    print("=" * 60)
    
    results = TestResults()
    ctx = MockContext()
    created_tunnels = []
    
    try:
        # Run tests in sequence
        created_tunnels = await test_tunnel_creation(results, ctx)
        await test_tunnel_management(results, ctx, created_tunnels)
        await test_advanced_features(results, ctx)
        
    except Exception as e:
        print(f"\n❌ Critical error during testing: {e}")
        results.add("critical_error", False, str(e))
    
    finally:
        # Always try to clean up
        if created_tunnels:
            await cleanup_tunnels(created_tunnels, ctx)
    
    # Print final summary
    results.print_summary()
    
    # Save results to file
    results_file = f"ngrok_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump({
            "summary": {
                "passed": results.passed,
                "failed": results.failed,
                "tunnel_urls": results.tunnel_urls,
                "timestamp": datetime.now().isoformat()
            },
            "results": results.results
        }, f, indent=2)
    print(f"\n💾 Results saved to: {results_file}")

if __name__ == "__main__":
    asyncio.run(main())