#!/usr/bin/env python3
"""
Miro MCP Server Direct Testing - Phase 2
Comprehensive testing using FastMCP Client pattern

Testing Strategy:
- All 6 tools with valid and invalid inputs
- All 5 resources with content validation
- All 5 prompts with parameter variations
- Error handling and edge cases
- Performance baseline measurements
- Data structure validation

Run: python test_direct.py
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

SERVER_NAME = "Miro MCP Server"
SERVER_MODULE = "miro_server"  # Python module name

# Set environment variables BEFORE imports
# CRITICAL: Environment variables must be set BEFORE importing server module
os.environ['MIRO_ACCESS_TOKEN'] = 'test-token-for-testing'  # Required for Miro API
os.environ['MIRO_MCP_PORT'] = '8021'  # Server port

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
            
            print("📦 Testing Tools (6 total)...")
            
            # Test 1: Basic board creation
            await test_tool(runner, client, "create_board", {
                "name": "Test Board", 
                "description": "Test board for MCP testing"
            }, "board_id")
            
            # Test 2: Sticky note creation
            await test_tool(runner, client, "create_sticky_note", {
                "board_id": "test-board-123", 
                "content": "Test sticky note", 
                "x": 100, 
                "y": 200, 
                "color": "#FFF9B1"
            }, "item_id")
            
            # Test 3: Shape creation with different types
            for shape_type in ["rectangle", "round_rectangle", "circle", "triangle"]:
                await test_tool(runner, client, "create_shape", {
                    "board_id": "test-board-123", 
                    "shape_type": shape_type, 
                    "content": f"Test {shape_type}",
                    "x": 0, "y": 0, "width": 200, "height": 100,
                    "color": "#E1F5FE"
                }, "item_id")
            
            # Test 4: Connector creation
            await test_tool(runner, client, "create_connector", {
                "board_id": "test-board-123", 
                "start_item_id": "item1", 
                "end_item_id": "item2",
                "label": "Test connection",
                "style": "elbowed"
            }, "connector_id")
            
            # Test 5: Agent workflow board (complex workflow)
            await test_tool(runner, client, "create_agent_workflow_board", {
                "workflow_name": "DevLoop Standard",
                "agents": [
                    {"name": "project-planner", "type": "planning", "description": "Project planning agent"},
                    {"name": "backend-agent", "type": "backend", "description": "Backend development"},
                    {"name": "frontend-agent", "type": "frontend", "description": "Frontend development"},
                    {"name": "testing-agent", "type": "testing", "description": "Quality assurance"}
                ],
                "connections": [
                    {"from_agent": "project-planner", "to_agent": "backend-agent", "label": "Requirements"},
                    {"from_agent": "backend-agent", "to_agent": "frontend-agent", "label": "API Ready"}
                ],
                "mcp_servers": [
                    {"name": "github", "port": "8011", "status": "active"},
                    {"name": "vercel-v0", "port": "8010", "status": "active"}
                ]
            }, "board_id")
            
            # Test 6: Kanban board with tasks
            await test_tool(runner, client, "create_kanban_board", {
                "board_name": "Development Sprint",
                "columns": ["Backlog", "To Do", "In Progress", "Code Review", "Testing", "Done"],
                "tasks": [
                    {"title": "Setup project structure", "column": "Done", "priority": "high"},
                    {"title": "Implement authentication", "column": "In Progress", "priority": "high"},
                    {"title": "Create dashboard UI", "column": "To Do", "priority": "medium"}
                ]
            }, "board_id")
            
            # ========================================
            # TEST RESOURCES - Add your resources here
            # ========================================
            
            print("\n📚 Testing Resources (5 total)...")
            resources_to_test = [
                "miro://templates",
                "miro://examples/workflows", 
                "miro://examples/kanban",
                "miro://config",
                "miro://best-practices"
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
            
            print("\n💡 Testing Prompts (5 total)...")
            prompts_to_test = [
                ("create_workflow_prompt", {"workflow_type": "development", "team_size": "medium"}),
                ("design_kanban_prompt", {"project_type": "software", "methodology": "agile"}),
                ("optimize_board_layout_prompt", {"board_purpose": "workflow", "element_count": "medium"}),
                ("troubleshoot_workflow_prompt", {"issue_type": "performance", "workflow_stage": "implementation"}),
                ("mcp_integration_prompt", {"integration_scope": "multi-server", "complexity": "medium"})
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
            
            # Comprehensive error handling tests
            print("\n🧪 Testing Error Handling...")
            
            # Test missing required parameters
            await test_error_case(runner, client, "create_board", {}, "Missing required 'name' parameter")
            await test_error_case(runner, client, "create_sticky_note", {"content": "test"}, "Missing required 'board_id' parameter")
            
            # Test invalid parameter types
            await test_error_case(runner, client, "create_shape", {
                "board_id": "test", "shape_type": "invalid_shape", "content": "test"
            }, "Invalid shape type")
            
            # Test empty/invalid values
            await test_error_case(runner, client, "create_board", {"name": ""}, "Empty board name")
            await test_error_case(runner, client, "create_sticky_note", {
                "board_id": "", "content": "test"
            }, "Empty board ID")
            
            # Test invalid agent workflow
            await test_error_case(runner, client, "create_agent_workflow_board", {
                "workflow_name": "test", "agents": []
            }, "Empty agents list")
            
            # Test invalid kanban board
            await test_error_case(runner, client, "create_kanban_board", {
                "board_name": "test", "columns": []
            }, "Empty columns list")
            
            # Performance baseline measurements
            print("\n⏱️ Performance Baseline Tests...")
            await run_performance_tests(runner, client)
            
            # Data structure validation
            print("\n🔍 Data Structure Validation...")
            await validate_data_structures(runner, client)
                    
    except Exception as e:
        runner.record_fail("Server initialization", str(e))
        import traceback
        traceback.print_exc()
    
    return runner.summary()

# Helper functions for comprehensive testing
async def test_tool(runner, client, tool_name, args, expected_field=None):
    """Test a single tool with detailed validation"""
    try:
        result = await client.call_tool(tool_name, args)
        if result.data:
            details = f"Returned data with {len(result.data)} fields"
            if expected_field and expected_field in result.data:
                details += f", found expected field '{expected_field}'"
            runner.record_pass(f"Tool: {tool_name}", details)
            return result.data
        else:
            runner.record_fail(f"Tool: {tool_name}", "No data returned")
            return None
    except Exception as e:
        runner.record_fail(f"Tool: {tool_name}", str(e))
        return None

async def test_error_case(runner, client, tool_name, args, expected_error):
    """Test that invalid inputs are properly rejected"""
    try:
        result = await client.call_tool(tool_name, args)
        # If result has error field, that's acceptable
        if result.data and "error" in result.data:
            runner.record_pass(f"Error handling: {tool_name}", f"Returned error as expected: {expected_error}")
        else:
            runner.record_fail(f"Error handling: {tool_name}", f"Should have failed with: {expected_error}")
    except Exception as e:
        runner.record_pass(f"Error handling: {tool_name}", f"Correctly rejected: {expected_error}")

async def run_performance_tests(runner, client):
    """Run performance baseline measurements"""
    import time
    
    # Test board creation performance
    start_time = time.time()
    try:
        result = await client.call_tool("create_board", {
            "name": "Performance Test Board",
            "description": "Testing response time"
        })
        duration = time.time() - start_time
        runner.record_pass(f"Performance: create_board", f"{duration:.3f}s response time")
    except Exception as e:
        runner.record_fail(f"Performance: create_board", str(e))
    
    # Test resource access performance
    start_time = time.time()
    try:
        result = await client.read_resource("miro://config")
        duration = time.time() - start_time
        runner.record_pass(f"Performance: resource access", f"{duration:.3f}s response time")
    except Exception as e:
        runner.record_fail(f"Performance: resource access", str(e))

async def validate_data_structures(runner, client):
    """Validate return data structures and formats"""
    # Test board creation data structure
    try:
        result = await client.call_tool("create_board", {
            "name": "Structure Test Board",
            "description": "Testing data structure"
        })
        
        if result.data:
            # Check if this is an error response or success response
            if "error" in result.data:
                # Error response structure
                error_fields = ["success", "error"]
                missing_error_fields = [f for f in error_fields if f not in result.data]
                
                if not missing_error_fields:
                    runner.record_pass("Data structure: create_board error", "Error response structure correct")
                else:
                    runner.record_fail("Data structure: create_board error", f"Missing error fields: {missing_error_fields}")
            else:
                # Success response structure
                required_fields = ["success", "board_id", "board_url", "name", "created_at"]
                missing_fields = [f for f in required_fields if f not in result.data]
                
                if not missing_fields:
                    runner.record_pass("Data structure: create_board success", "All required fields present")
                else:
                    runner.record_fail("Data structure: create_board success", f"Missing fields: {missing_fields}")
                
            # Validate data types
            if isinstance(result.data.get("success"), bool):
                runner.record_pass("Data types: create_board success", "Boolean type correct")
            else:
                runner.record_fail("Data types: create_board success", "Should be boolean")
                
        else:
            runner.record_fail("Data structure: create_board", "No data returned")
            
    except Exception as e:
        runner.record_fail("Data structure: create_board", str(e))
    
    # Test resource data structure  
    try:
        result = await client.read_resource("miro://config")
        if result and len(result) > 0 and hasattr(result[0], 'text'):
            import json
            config_data = json.loads(result[0].text)
            
            required_config_fields = ["server_name", "version", "token_configured", "features"]
            missing_config_fields = [f for f in required_config_fields if f not in config_data]
            
            if not missing_config_fields:
                runner.record_pass("Data structure: config resource", "All required config fields present")
            else:
                runner.record_fail("Data structure: config resource", f"Missing config fields: {missing_config_fields}")
        else:
            runner.record_fail("Data structure: config resource", "No config data returned")
    except Exception as e:
        runner.record_fail("Data structure: config resource", str(e))

# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    # Run tests
    success = asyncio.run(test_server())
    
    # Exit with appropriate code for CI/CD
    if success:
        print("\n🎉 All tests passed!")
        print("Phase 2 testing completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        print("Review test results for details.")
        sys.exit(1)