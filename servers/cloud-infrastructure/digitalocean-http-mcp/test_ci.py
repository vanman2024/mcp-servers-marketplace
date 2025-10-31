#!/usr/bin/env python3
"""
CI/CD test for Digital Ocean MCP Server
Runs all tests and exits with appropriate code for GitHub Actions
"""

import asyncio
import os
import sys
import json
from datetime import datetime
from fastmcp import Client

# Force mock mode for CI/CD
os.environ['DO_MOCK_MODE'] = 'true'
os.environ['DIGITALOCEAN_API_TOKEN'] = 'ci-test-token'

# Add server path
sys.path.insert(0, 'src')

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        
    def record_pass(self, test_name):
        self.passed += 1
        print(f"✅ {test_name}")
        
    def record_fail(self, test_name, error):
        self.failed += 1
        self.errors.append({
            "test": test_name,
            "error": str(error)
        })
        print(f"❌ {test_name}: {error}")
        
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"Test Results: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"\nFailed tests:")
            for err in self.errors:
                print(f"  - {err['test']}: {err['error']}")
        return self.failed == 0

async def test_digital_ocean_server():
    """Run comprehensive tests for CI/CD"""
    runner = TestRunner()
    
    print("🌊 Digital Ocean MCP Server CI/CD Test")
    print("=" * 50)
    
    try:
        from digitalocean_server import mcp
        
        async with Client(mcp) as client:
            # Test all tools
            tools_to_test = [
                ("get_account_info", {}),
                ("list_ssh_keys", {}),
                ("list_droplets", {}),
                ("create_droplet", {
                    "name": "ci-test-droplet",
                    "region": "nyc3",
                    "size": "s-1vcpu-1gb",
                    "image": "ubuntu-22-04-x64"
                }),
                ("manage_droplet", {
                    "droplet_id": 123456789,
                    "action": "reboot"
                }),
                ("delete_droplet", {
                    "droplet_id": 123456789
                }),
                ("list_databases", {}),
                ("create_database", {
                    "name": "ci-test-db",
                    "engine": "pg",
                    "version": "15",
                    "region": "nyc3",
                    "size": "db-s-1vcpu-1gb"
                }),
                ("list_apps", {}),
                ("create_app", {
                    "spec": {
                        "name": "ci-test-app",
                        "region": "nyc"
                    }
                })
            ]
            
            for tool_name, args in tools_to_test:
                try:
                    result = await client.call_tool(tool_name, args)
                    if result.data:
                        runner.record_pass(f"Tool: {tool_name}")
                    else:
                        runner.record_fail(f"Tool: {tool_name}", "No data returned")
                except Exception as e:
                    runner.record_fail(f"Tool: {tool_name}", str(e))
            
            # Test resources
            resources_to_test = [
                "resource://usage_guide",
                "resource://regions",
                "resource://sizes",
                "resource://images",
                "resource://examples/droplet_creation"
            ]
            
            for resource_uri in resources_to_test:
                try:
                    result = await client.read_resource(resource_uri)
                    if result and len(result) > 0:
                        runner.record_pass(f"Resource: {resource_uri}")
                    else:
                        runner.record_fail(f"Resource: {resource_uri}", "No content")
                except Exception as e:
                    runner.record_fail(f"Resource: {resource_uri}", str(e))
            
            # Test prompts
            prompts_to_test = [
                ("droplet_creation_guide", {"purpose": "web_server", "environment": "production"}),
                ("troubleshooting_guide", {"issue_type": "ssh_connection"}),
                ("migration_guide", {"from_provider": "AWS"}),
                ("cost_optimization", {}),
                ("security_best_practices", {})
            ]
            
            for prompt_name, args in prompts_to_test:
                try:
                    result = await client.get_prompt(prompt_name, args)
                    if result.messages:
                        runner.record_pass(f"Prompt: {prompt_name}")
                    else:
                        runner.record_fail(f"Prompt: {prompt_name}", "No messages")
                except Exception as e:
                    runner.record_fail(f"Prompt: {prompt_name}", str(e))
            
    except Exception as e:
        runner.record_fail("Server initialization", str(e))
    
    # Write results for CI/CD
    results = {
        "timestamp": datetime.now().isoformat(),
        "passed": runner.passed,
        "failed": runner.failed,
        "errors": runner.errors
    }
    
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return runner.summary()

if __name__ == "__main__":
    success = asyncio.run(test_digital_ocean_server())
    sys.exit(0 if success else 1)