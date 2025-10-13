#!/usr/bin/env python3
"""
Miro MCP Server CI/CD Test
Minimal output, JSON results for automation
"""

import asyncio
import os
import sys
import json
from datetime import datetime
from unittest.mock import patch
from fastmcp import Client

# Set environment
os.environ['MIRO_ACCESS_TOKEN'] = 'test-token'
sys.path.insert(0, 'src')

class MockMiroClient:
    async def make_request(self, method, endpoint, data=None):
        if "boards" in endpoint and method == "POST":
            return {"id": "test-123", "viewLink": "https://miro.com/test"}
        elif method == "GET":
            return {"id": endpoint.split("/")[-1], "name": "Test"}
        return {"id": "mock-id", "type": "mock"}

async def test_server():
    results = {
        "server": "miro-http-mcp",
        "timestamp": datetime.now().isoformat(),
        "passed": 0,
        "failed": 0,
        "errors": []
    }
    
    try:
        import miro_server
        mock_client = MockMiroClient()
        
        with patch.object(miro_server, 'miro_client', mock_client):
            with patch.object(miro_server.board_tools, 'client', mock_client):
                with patch.object(miro_server.workflow_tools.board_tools, 'client', mock_client):
                    
                    async with Client(miro_server.mcp) as client:
                        # Test all tools
                        tools = [
                            ("create_board", {"name": "Test"}),
                            ("create_sticky_note", {"board_id": "test", "content": "Note"}),
                            ("create_shape", {"board_id": "test", "shape_type": "rectangle"}),
                            ("create_connector", {"board_id": "test", "start_item_id": "a", "end_item_id": "b"}),
                            ("create_agent_workflow_board", {"workflow_name": "Test", "agents": [{"name": "A", "type": "frontend"}]}),
                            ("create_kanban_board", {"board_name": "Test", "columns": ["A", "B"]})
                        ]
                        
                        for tool_name, args in tools:
                            try:
                                result = await client.call_tool(tool_name, args)
                                if result.data:
                                    results["passed"] += 1
                                    print(f"✅ Tool: {tool_name}")
                                else:
                                    results["failed"] += 1
                                    results["errors"].append({
                                        "tool": tool_name,
                                        "error": "No data returned"
                                    })
                                    print(f"❌ Tool: {tool_name}")
                            except Exception as e:
                                results["failed"] += 1
                                results["errors"].append({
                                    "tool": tool_name,
                                    "error": str(e)
                                })
                                print(f"❌ Tool: {tool_name}")
                                
    except Exception as e:
        results["failed"] += 1
        results["errors"].append({
            "test": "initialization",
            "error": str(e)
        })
    
    results["total"] = results["passed"] + results["failed"]
    
    # Write results
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nTest Results: {results['passed']}/{results['total']} passed")
    return results["failed"] == 0

if __name__ == "__main__":
    success = asyncio.run(test_server())
    sys.exit(0 if success else 1)