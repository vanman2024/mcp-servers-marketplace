#!/usr/bin/env python3
"""
MCP Server Test Template
Copy this file to test your MCP server

Usage:
1. Copy to your server directory
2. Update SERVER_NAME and imports
3. Set appropriate environment variables
4. Add your tools, resources, and prompts to test
5. Run: python test_template.py
"""

import asyncio
import os
import sys
import json
from datetime import datetime
from fastmcp import Client

# ============================================
# CUSTOMIZE THESE FOR YOUR SERVER
# ============================================

SERVER_NAME = "Your Server Name"
SERVER_MODULE = "your_server"  # Python module name

# Set environment variables BEFORE imports
os.environ['MOCK_MODE'] = 'true'  # Remove if testing real API
# os.environ['YOUR_API_KEY'] = 'test-key'  # Add your env vars

# Add server source path
sys.path.insert(0, 'src')

# ============================================
# TEST RUNNER (Usually no changes needed)
# ============================================

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.start_time = datetime.now()
        
    def record_pass(self, test_name, details=None):
        self.passed += 1
        msg = f"✅ {test_name}"
        if details:
            msg += f" - {details}"
        print(msg)
        
    def record_fail(self, test_name, error):
        self.failed += 1
        self.errors.append({
            "test": test_name,
            "error": str(error),
            "time": datetime.now().isoformat()
        })
        print(f"❌ {test_name}: {error}")
        
    def summary(self):
        total = self.passed + self.failed
        duration = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\n{'='*50}")
        print(f"Test Results: {self.passed}/{total} passed in {duration:.2f}s")
        
        if self.failed > 0:
            print(f"\nFailed tests:")
            for err in self.errors:
                print(f"  - {err['test']}: {err['error']}")
        
        # Write JSON results for CI/CD
        results = {
            "timestamp": self.start_time.isoformat(),
            "duration_seconds": duration,
            "passed": self.passed,
            "failed": self.failed,
            "total": total,
            "errors": self.errors
        }
        
        with open('test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        return self.failed == 0

# ============================================
# MAIN TEST FUNCTION
# ============================================

async def test_server():
    runner = TestRunner()
    
    print(f"🧪 {SERVER_NAME} MCP Server Test")
    print("=" * 50)
    
    try:
        # Import server module
        server = __import__(SERVER_MODULE)
        mcp = server.mcp
        
        async with Client(mcp) as client:
            print("✅ Client connected successfully!\n")
            
            # ========================================
            # TEST TOOLS - Add your tools here
            # ========================================
            
            print("📦 Testing Tools...")
            tools_to_test = [
                # ("tool_name", {"arg1": "value1", "arg2": "value2"}, "expected_field"),
                # Example:
                # ("list_items", {}, "items"),
                # ("create_item", {"name": "test"}, "id"),
            ]
            
            for test_case in tools_to_test:
                tool_name = test_case[0]
                args = test_case[1]
                expected_field = test_case[2] if len(test_case) > 2 else None
                
                try:
                    result = await client.call_tool(tool_name, args)
                    if result.data:
                        details = None
                        if expected_field and expected_field in result.data:
                            details = f"Found {expected_field}"
                        runner.record_pass(f"Tool: {tool_name}", details)
                    else:
                        runner.record_fail(f"Tool: {tool_name}", "No data returned")
                except Exception as e:
                    runner.record_fail(f"Tool: {tool_name}", str(e))
            
            # ========================================
            # TEST RESOURCES - Add your resources here
            # ========================================
            
            print("\n📚 Testing Resources...")
            resources_to_test = [
                # "resource://resource_name",
                # Example:
                # "resource://config",
                # "resource://help",
            ]
            
            for resource_uri in resources_to_test:
                try:
                    result = await client.read_resource(resource_uri)
                    if result and len(result) > 0:
                        size = len(result[0].text) if hasattr(result[0], 'text') else 'unknown'
                        runner.record_pass(f"Resource: {resource_uri}", f"{size} chars")
                    else:
                        runner.record_fail(f"Resource: {resource_uri}", "No content")
                except Exception as e:
                    runner.record_fail(f"Resource: {resource_uri}", str(e))
            
            # ========================================
            # TEST PROMPTS - Add your prompts here
            # ========================================
            
            print("\n💡 Testing Prompts...")
            prompts_to_test = [
                # ("prompt_name", {"param1": "value1"}),
                # Example:
                # ("generate_code", {"language": "python"}),
                # ("help_text", {}),
            ]
            
            for prompt_name, args in prompts_to_test:
                try:
                    result = await client.get_prompt(prompt_name, args)
                    if result.messages and len(result.messages) > 0:
                        chars = len(result.messages[0].content.text)
                        runner.record_pass(f"Prompt: {prompt_name}", f"{chars} chars")
                    else:
                        runner.record_fail(f"Prompt: {prompt_name}", "No messages")
                except Exception as e:
                    runner.record_fail(f"Prompt: {prompt_name}", str(e))
            
            # ========================================
            # CUSTOM TESTS - Add specific tests here
            # ========================================
            
            # Example: Test error handling
            # try:
            #     result = await client.call_tool("tool_name", {"invalid": "args"})
            #     runner.record_fail("Error handling", "Should have failed")
            # except Exception as e:
            #     runner.record_pass("Error handling", "Correctly rejected invalid args")
                    
    except Exception as e:
        runner.record_fail("Server initialization", str(e))
        import traceback
        traceback.print_exc()
    
    return runner.summary()

# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    # Run tests
    success = asyncio.run(test_server())
    
    # Exit with appropriate code for CI/CD
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)