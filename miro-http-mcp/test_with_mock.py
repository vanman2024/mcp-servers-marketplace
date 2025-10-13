#!/usr/bin/env python3
"""
Miro MCP Server Testing with Mock Responses
Tests all tools with simulated Miro API responses
"""

import asyncio
import os
import sys
import json
from datetime import datetime
from unittest.mock import patch, AsyncMock
from fastmcp import Client

# Configure test environment
SERVER_NAME = "Miro MCP Server"

# Set environment variables BEFORE imports
os.environ['MIRO_ACCESS_TOKEN'] = 'test-token-for-testing'

# Add server source path
sys.path.insert(0, 'src')

class MockMiroClient:
    """Mock Miro client that returns test data"""
    
    async def make_request(self, method: str, endpoint: str, data=None):
        """Simulate Miro API responses"""
        if method == "POST" and "/boards" in endpoint and "items" not in endpoint:
            # Create board
            return {
                "id": "test-board-123",
                "name": data.get("name", "Test Board"),
                "description": data.get("description", ""),
                "viewLink": "https://miro.com/app/board/test-board-123",
                "createdAt": datetime.now().isoformat()
            }
        elif method == "POST" and "/sticky_notes" in endpoint:
            # Create sticky note
            return {
                "id": "sticky-123",
                "type": "sticky_note",
                "content": data.get("data", {}).get("content", "Test"),
                "position": data.get("position", {"x": 0, "y": 0})
            }
        elif method == "POST" and "/shapes" in endpoint:
            # Create shape
            return {
                "id": "shape-123",
                "type": data.get("data", {}).get("shape", "rectangle"),
                "content": data.get("data", {}).get("content", ""),
                "position": data.get("position", {"x": 0, "y": 0})
            }
        elif method == "POST" and "/connectors" in endpoint:
            # Create connector
            return {
                "id": "connector-123",
                "startItem": {"id": data.get("startItem", {}).get("id", "item1")},
                "endItem": {"id": data.get("endItem", {}).get("id", "item2")}
            }
        elif method == "GET" and "/boards/" in endpoint:
            # Get board (for validation)
            board_id = endpoint.split("/")[-1]
            if board_id:
                return {
                    "id": board_id,
                    "name": "Test Board",
                    "viewLink": f"https://miro.com/app/board/{board_id}"
                }
            else:
                return {"error": "Board ID required"}
        else:
            return {"error": f"Mock not implemented for {method} {endpoint}"}

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
        
        # Write JSON results
        results = {
            "server": SERVER_NAME,
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

async def test_server():
    runner = TestRunner()
    
    print(f"🧪 {SERVER_NAME} Test with Mock Responses")
    print("=" * 50)
    
    try:
        # Import and patch the miro_client
        import miro_server
        
        # Patch the client before creating FastMCP client
        mock_client = MockMiroClient()
        with patch.object(miro_server, 'miro_client', mock_client):
            # Also patch the client in the tool classes
            with patch.object(miro_server.board_tools, 'client', mock_client):
                with patch.object(miro_server.workflow_tools.board_tools, 'client', mock_client):
                    
                    async with Client(miro_server.mcp) as client:
                        print("✅ Client connected successfully!\n")
                        
                        # Test Tools
                        print("📦 Testing Tools...")
                        
                        # Test create_board
                        try:
                            result = await client.call_tool("create_board", {
                                "name": "Test Board",
                                "description": "Test description"
                            })
                            if result.data.get("success") and result.data.get("board_id"):
                                runner.record_pass("Tool: create_board", f"Created board {result.data['board_id']}")
                            else:
                                runner.record_fail("Tool: create_board", "No board_id returned")
                        except Exception as e:
                            runner.record_fail("Tool: create_board", str(e))
                        
                        # Test create_sticky_note
                        try:
                            result = await client.call_tool("create_sticky_note", {
                                "board_id": "test-board-123",
                                "content": "Test Note",
                                "x": 100,
                                "y": 200
                            })
                            if result.data.get("success") and result.data.get("item_id"):
                                runner.record_pass("Tool: create_sticky_note", f"Created sticky {result.data['item_id']}")
                            else:
                                runner.record_fail("Tool: create_sticky_note", "No item_id returned")
                        except Exception as e:
                            runner.record_fail("Tool: create_sticky_note", str(e))
                        
                        # Test create_shape
                        try:
                            result = await client.call_tool("create_shape", {
                                "board_id": "test-board-123",
                                "shape_type": "rectangle",
                                "content": "Test Shape",
                                "x": 300,
                                "y": 400
                            })
                            if result.data.get("success") and result.data.get("item_id"):
                                runner.record_pass("Tool: create_shape", f"Created shape {result.data['item_id']}")
                            else:
                                runner.record_fail("Tool: create_shape", "No item_id returned")
                        except Exception as e:
                            runner.record_fail("Tool: create_shape", str(e))
                        
                        # Test create_connector
                        try:
                            result = await client.call_tool("create_connector", {
                                "board_id": "test-board-123",
                                "start_item_id": "item1",
                                "end_item_id": "item2",
                                "label": "Test Connection"
                            })
                            if result.data.get("success") and result.data.get("connector_id"):
                                runner.record_pass("Tool: create_connector", f"Created connector {result.data['connector_id']}")
                            else:
                                runner.record_fail("Tool: create_connector", "No connector_id returned")
                        except Exception as e:
                            runner.record_fail("Tool: create_connector", str(e))
                        
                        # Test create_agent_workflow_board
                        try:
                            result = await client.call_tool("create_agent_workflow_board", {
                                "workflow_name": "Test Workflow",
                                "agents": [
                                    {"name": "Frontend Agent", "type": "frontend", "description": "Handles UI"},
                                    {"name": "Backend Agent", "type": "backend", "description": "Handles API"}
                                ],
                                "connections": [
                                    {"from": "Frontend Agent", "to": "Backend Agent", "label": "API calls"}
                                ]
                            })
                            if result.data.get("success") and result.data.get("board_id"):
                                runner.record_pass("Tool: create_agent_workflow_board", 
                                                 f"Created workflow board {result.data['board_id']}")
                            else:
                                runner.record_fail("Tool: create_agent_workflow_board", "No board_id returned")
                        except Exception as e:
                            runner.record_fail("Tool: create_agent_workflow_board", str(e))
                        
                        # Test create_kanban_board
                        try:
                            result = await client.call_tool("create_kanban_board", {
                                "board_name": "Test Kanban",
                                "columns": ["To Do", "In Progress", "Done"],
                                "tasks": [
                                    {"title": "Task 1", "column": "To Do", "priority": "high"},
                                    {"title": "Task 2", "column": "In Progress", "priority": "medium"}
                                ]
                            })
                            if result.data.get("success") and result.data.get("board_id"):
                                runner.record_pass("Tool: create_kanban_board", 
                                                 f"Created kanban board {result.data['board_id']}")
                            else:
                                runner.record_fail("Tool: create_kanban_board", "No board_id returned")
                        except Exception as e:
                            runner.record_fail("Tool: create_kanban_board", str(e))
                        
                        # Test error handling
                        print("\n🧪 Testing Error Handling...")
                        
                        # Test missing required parameters
                        try:
                            result = await client.call_tool("create_board", {})  # Missing 'name'
                            runner.record_fail("Error handling - missing params", "Should have failed")
                        except Exception as e:
                            if "name" in str(e).lower():
                                runner.record_pass("Error handling - missing params", 
                                                 "Correctly rejected missing 'name'")
                            else:
                                runner.record_fail("Error handling - missing params", 
                                                 f"Wrong error: {str(e)}")
                        
                        # Test invalid shape type
                        try:
                            result = await client.call_tool("create_shape", {
                                "board_id": "test-board-123",
                                "shape_type": "invalid_shape",
                                "content": "Test"
                            })
                            # Miro server should validate shape types
                            if result.data.get("success"):
                                runner.record_fail("Error handling - invalid shape", 
                                                 "Should have rejected invalid shape type")
                            else:
                                runner.record_pass("Error handling - invalid shape", 
                                                 "Correctly handled invalid shape type")
                        except Exception as e:
                            runner.record_pass("Error handling - invalid shape", 
                                             f"Rejected invalid shape: {str(e)}")
                            
    except Exception as e:
        runner.record_fail("Server initialization", str(e))
        import traceback
        traceback.print_exc()
    
    return runner.summary()

if __name__ == "__main__":
    success = asyncio.run(test_server())
    sys.exit(0 if success else 1)