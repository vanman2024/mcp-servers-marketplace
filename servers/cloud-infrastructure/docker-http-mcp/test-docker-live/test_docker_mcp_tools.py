#!/usr/bin/env python3
"""
Direct testing of Docker MCP Server tools without needing Claude sessions
Tests the MCP tools by mocking the FastMCP decorator
"""

import asyncio
import os
import json
import sys
from datetime import datetime
from typing import Dict, Any, List

# Mock the FastMCP decorator to get raw functions
import unittest.mock
with unittest.mock.patch('fastmcp.FastMCP.tool', lambda self: lambda f: f):
    with unittest.mock.patch('fastmcp.FastMCP.resource', lambda self, uri: lambda f: f):
        # Import after mocking
        sys.path.insert(0, '.')
        import docker_server as server

class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def add(self, name: str, passed: bool, details: str = ""):
        self.results.append({
            "name": name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print("\n" + "=" * 60)
        print("📊 DOCKER MCP TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        if self.passed + self.failed > 0:
            print(f"📈 Success Rate: {self.passed / (self.passed + self.failed) * 100:.1f}%")
        
        print("\n📋 Failed Tests:")
        for result in self.results:
            if not result["passed"]:
                print(f"  ❌ {result['name']}: {result['details'][:100]}")

async def test_docker_system(results: TestResults):
    """Test Docker system operations"""
    print("\n🐳 TESTING DOCKER SYSTEM")
    print("-" * 40)
    
    # Test docker_system_info
    try:
        result = await server.docker_system_info()
        results.add("docker_system_info", result["success"], result.get("message", "Success"))
        if result["success"]:
            print(f"✅ docker_system_info: Docker system info retrieved")
    except Exception as e:
        results.add("docker_system_info", False, str(e))
        print(f"❌ docker_system_info: {e}")

async def test_container_operations(results: TestResults):
    """Test container management operations"""
    print("\n📦 TESTING CONTAINER OPERATIONS")
    print("-" * 40)
    
    # Test docker_list_containers
    try:
        result = await server.docker_list_containers(all=True)
        results.add("docker_list_containers", result["success"], result.get("message", "Success"))
        if result["success"]:
            print(f"✅ docker_list_containers: {len(result.get('containers', []))} containers found")
    except Exception as e:
        results.add("docker_list_containers", False, str(e))
        print(f"❌ docker_list_containers: {e}")

async def test_image_operations(results: TestResults):
    """Test image management operations"""
    print("\n🏗️ TESTING IMAGE OPERATIONS")
    print("-" * 40)
    
    # Test docker_list_images
    try:
        result = await server.docker_list_images(all=True)
        results.add("docker_list_images", result["success"], result.get("message", "Success"))
        if result["success"]:
            print(f"✅ docker_list_images: {len(result.get('images', []))} images found")
    except Exception as e:
        results.add("docker_list_images", False, str(e))
        print(f"❌ docker_list_images: {e}")

async def test_network_operations(results: TestResults):
    """Test network operations"""
    print("\n🌐 TESTING NETWORK OPERATIONS")
    print("-" * 40)
    
    # Test docker_network_list
    try:
        result = await server.docker_network_list()
        results.add("docker_network_list", result["success"], result.get("message", "Success"))
        if result["success"]:
            print(f"✅ docker_network_list: {len(result.get('networks', []))} networks found")
    except Exception as e:
        results.add("docker_network_list", False, str(e))
        print(f"❌ docker_network_list: {e}")

async def test_volume_operations(results: TestResults):
    """Test volume operations"""
    print("\n💾 TESTING VOLUME OPERATIONS")
    print("-" * 40)
    
    # Test docker_volume_list
    try:
        result = await server.docker_volume_list()
        results.add("docker_volume_list", result["success"], result.get("message", "Success"))
        if result["success"]:
            print(f"✅ docker_volume_list: {len(result.get('volumes', []))} volumes found")
    except Exception as e:
        results.add("docker_volume_list", False, str(e))
        print(f"❌ docker_volume_list: {e}")

async def main():
    """Run all tests"""
    print("🚀 DOCKER MCP SERVER DIRECT TESTING")
    print(f"📅 Test run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = TestResults()
    
    # Run test suites
    await test_docker_system(results)
    await test_container_operations(results)
    await test_image_operations(results)
    await test_network_operations(results)
    await test_volume_operations(results)
    
    # Print summary
    results.print_summary()
    
    print("\n✅ Testing complete! No Claude session required.")
    print("📝 This proves we can test Docker MCP tools directly!")
    print(f"🐳 Docker operations {'✅ WORKING' if any(r['name'] == 'docker_system_info' and r['passed'] for r in results.results) else '❌ FAILED'}")

if __name__ == "__main__":
    asyncio.run(main())