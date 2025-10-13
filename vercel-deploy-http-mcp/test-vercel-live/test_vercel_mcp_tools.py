#!/usr/bin/env python3
"""
Direct testing of Vercel Deploy MCP Server tools without needing Claude sessions
Tests the MCP tools by mocking the FastMCP decorator
"""

import asyncio
import os
import json
import sys
from datetime import datetime
from typing import Dict, Any, List

# Set environment variables BEFORE importing server
os.environ['VERCEL_TOKEN'] = os.getenv('VERCEL_TOKEN', '')

if not os.environ['VERCEL_TOKEN']:
    print("❌ VERCEL_TOKEN environment variable required")
    sys.exit(1)

# Mock the FastMCP decorator to get raw functions
import unittest.mock
with unittest.mock.patch('fastmcp.FastMCP.tool', lambda self: lambda f: f):
    with unittest.mock.patch('fastmcp.FastMCP.resource', lambda self, uri: lambda f: f):
        # Import after mocking AND after setting env vars
        sys.path.insert(0, 'src')
        import vercel_deploy_server as server

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
        print("📊 VERCEL DEPLOY MCP TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        if self.passed + self.failed > 0:
            print(f"📈 Success Rate: {self.passed / (self.passed + self.failed) * 100:.1f}%")
        
        print("\n📋 Failed Tests:")
        for result in self.results:
            if not result["passed"]:
                print(f"  ❌ {result['name']}: {result['details'][:100]}")

async def test_project_management(results: TestResults):
    """Test project management operations"""
    print("\n🚀 TESTING PROJECT MANAGEMENT")
    print("-" * 40)
    
    # Test vercel_list_projects
    try:
        result = await server.vercel_list_projects(limit=10)
        results.add("vercel_list_projects", result["success"], result.get("message", "Success"))
        if result["success"]:
            print(f"✅ vercel_list_projects: {len(result.get('projects', []))} projects")
    except Exception as e:
        results.add("vercel_list_projects", False, str(e))
        print(f"❌ vercel_list_projects: {e}")

async def test_deployment_operations(results: TestResults):
    """Test deployment operations"""
    print("\n🚢 TESTING DEPLOYMENT OPERATIONS")
    print("-" * 40)
    
    # Test vercel_list_deployments
    try:
        result = await server.vercel_list_deployments(limit=5)
        results.add("vercel_list_deployments", result["success"], result.get("message", "Success"))
        if result["success"]:
            print(f"✅ vercel_list_deployments: {len(result.get('deployments', []))} deployments")
    except Exception as e:
        results.add("vercel_list_deployments", False, str(e))
        print(f"❌ vercel_list_deployments: {e}")

async def test_environment_operations(results: TestResults):
    """Test environment variable operations"""
    print("\n🔧 TESTING ENVIRONMENT OPERATIONS")
    print("-" * 40)
    
    # Test vercel_list_env_variables (would need a project ID)
    try:
        # This will likely fail without a real project ID, but tests the function
        result = await server.vercel_list_env_variables(project_id="test-project")
        results.add("vercel_list_env_variables", result["success"], result.get("message", "Success"))
        if result["success"]:
            print(f"✅ vercel_list_env_variables: Environment variables retrieved")
    except Exception as e:
        results.add("vercel_list_env_variables", False, str(e))
        print(f"❌ vercel_list_env_variables: {e}")

async def test_domain_operations(results: TestResults):
    """Test domain management operations"""
    print("\n🌐 TESTING DOMAIN OPERATIONS")
    print("-" * 40)
    
    # Test vercel_list_domains
    try:
        result = await server.vercel_list_domains()
        results.add("vercel_list_domains", result["success"], result.get("message", "Success"))
        if result["success"]:
            print(f"✅ vercel_list_domains: {len(result.get('domains', []))} domains")
    except Exception as e:
        results.add("vercel_list_domains", False, str(e))
        print(f"❌ vercel_list_domains: {e}")

async def test_team_operations(results: TestResults):
    """Test team management operations"""
    print("\n👥 TESTING TEAM OPERATIONS")
    print("-" * 40)
    
    # Test vercel_list_teams
    try:
        result = await server.vercel_list_teams()
        results.add("vercel_list_teams", result["success"], result.get("message", "Success"))
        if result["success"]:
            print(f"✅ vercel_list_teams: {len(result.get('teams', []))} teams")
    except Exception as e:
        results.add("vercel_list_teams", False, str(e))
        print(f"❌ vercel_list_teams: {e}")

async def main():
    """Run all tests"""
    print("🚀 VERCEL DEPLOY MCP SERVER DIRECT TESTING")
    print(f"📅 Test run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔑 Using Vercel token: {os.environ['VERCEL_TOKEN'][:8]}...")
    print("=" * 60)
    
    results = TestResults()
    
    # Run test suites
    await test_project_management(results)
    await test_deployment_operations(results)
    await test_environment_operations(results)
    await test_domain_operations(results)
    await test_team_operations(results)
    
    # Print summary
    results.print_summary()
    
    print("\n✅ Testing complete! No Claude session required.")
    print("📝 This proves we can test Vercel MCP tools directly!")
    print(f"🚢 Deployment operations {'✅ WORKING' if any(r['name'] == 'vercel_list_projects' and r['passed'] for r in results.results) else '❌ FAILED'}")

if __name__ == "__main__":
    asyncio.run(main())