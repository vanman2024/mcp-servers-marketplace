#!/usr/bin/env python3
"""
Everything HTTP MCP Server
Test server that exercises all MCP protocol features for client testing.
Based on the official Everything MCP server pattern with FastMCP HTTP transport.
"""

import os
import json
import base64
from datetime import datetime
from typing import Any, Dict, List, Optional
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Everything HTTP Server")

# Sample data storage
memory_store = {}
counter = 0

@mcp.tool()
async def everything_echo(message: str, includeTimestamp: bool = False) -> Dict[str, Any]:
    """Echo a message back with optional timestamp"""
    try:
        result = {
            "success": True,
            "message": message,
            "action": "echo"
        }
        
        if includeTimestamp:
            result["timestamp"] = datetime.now().isoformat()
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def everything_add_numbers(a: float, b: float) -> Dict[str, Any]:
    """Add two numbers together"""
    try:
        result = a + b
        return {
            "success": True,
            "result": result,
            "operation": "add",
            "a": a,
            "b": b,
            "formula": f"{a} + {b} = {result}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def everything_count_items() -> Dict[str, Any]:
    """Get the current counter value"""
    global counter
    try:
        counter += 1
        return {
            "success": True,
            "count": counter,
            "message": f"Counter incremented to {counter}",
            "action": "count"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def everything_store_value(key: str, value: Any) -> Dict[str, Any]:
    """Store a value in memory"""
    global memory_store
    try:
        memory_store[key] = value
        return {
            "success": True,
            "message": f"Stored value for key: {key}",
            "key": key,
            "value": value,
            "action": "store"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def everything_retrieve_value(key: str) -> Dict[str, Any]:
    """Retrieve a value from memory"""
    global memory_store
    try:
        if key in memory_store:
            return {
                "success": True,
                "key": key,
                "value": memory_store[key],
                "found": True,
                "action": "retrieve"
            }
        else:
            return {
                "success": True,
                "key": key,
                "value": None,
                "found": False,
                "message": f"Key '{key}' not found",
                "action": "retrieve"
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def everything_list_keys() -> Dict[str, Any]:
    """List all stored keys"""
    global memory_store
    try:
        keys = list(memory_store.keys())
        return {
            "success": True,
            "keys": keys,
            "count": len(keys),
            "action": "list_keys"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def everything_clear_memory() -> Dict[str, Any]:
    """Clear all stored values"""
    global memory_store, counter
    try:
        old_count = len(memory_store)
        memory_store.clear()
        counter = 0
        return {
            "success": True,
            "message": "Memory cleared",
            "items_cleared": old_count,
            "action": "clear"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def everything_generate_data(
    dataType: str = "json",
    count: int = 5,
    includeNested: bool = False
) -> Dict[str, Any]:
    """Generate sample data of various types"""
    try:
        if dataType == "json":
            data = []
            for i in range(count):
                item = {
                    "id": i + 1,
                    "name": f"Item {i + 1}",
                    "value": (i + 1) * 10,
                    "active": i % 2 == 0
                }
                if includeNested:
                    item["nested"] = {
                        "level": 1,
                        "data": f"Nested data for item {i + 1}"
                    }
                data.append(item)
        elif dataType == "text":
            data = "\n".join([f"Line {i + 1}: Sample text data" for i in range(count)])
        elif dataType == "numbers":
            data = [i * 3.14 for i in range(1, count + 1)]
        else:
            data = f"Unknown data type: {dataType}"
            
        return {
            "success": True,
            "dataType": dataType,
            "count": count,
            "includeNested": includeNested,
            "data": data,
            "action": "generate"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def everything_simulate_error(errorType: str = "generic") -> Dict[str, Any]:
    """Simulate various error conditions for testing"""
    try:
        if errorType == "generic":
            raise Exception("This is a simulated generic error")
        elif errorType == "timeout":
            import asyncio
            await asyncio.sleep(60)  # Simulate timeout
        elif errorType == "validation":
            raise ValueError("This is a simulated validation error")
        elif errorType == "permission":
            raise PermissionError("This is a simulated permission error")
        else:
            return {
                "success": False,
                "error": f"Unknown error type: {errorType}",
                "availableTypes": ["generic", "timeout", "validation", "permission"]
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "errorType": errorType,
            "simulated": True
        }

@mcp.tool()
async def everything_process_image(
    operation: str = "info",
    imageData: Optional[str] = None
) -> Dict[str, Any]:
    """Process image data (base64 encoded)"""
    try:
        if operation == "info":
            if imageData:
                # Decode to check validity
                try:
                    decoded = base64.b64decode(imageData)
                    return {
                        "success": True,
                        "operation": operation,
                        "size": len(decoded),
                        "valid": True,
                        "message": "Image data is valid base64"
                    }
                except:
                    return {
                        "success": False,
                        "operation": operation,
                        "valid": False,
                        "message": "Invalid base64 image data"
                    }
            else:
                return {
                    "success": True,
                    "operation": operation,
                    "message": "No image data provided"
                }
        elif operation == "generate":
            # Generate a 1x1 pixel PNG
            dummy_png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
            return {
                "success": True,
                "operation": operation,
                "imageData": dummy_png,
                "format": "PNG",
                "size": "1x1",
                "message": "Generated dummy image"
            }
        else:
            return {
                "success": False,
                "error": f"Unknown operation: {operation}",
                "availableOperations": ["info", "generate"]
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def everything_batch_operation(
    operations: List[Dict[str, Any]],
    stopOnError: bool = False
) -> Dict[str, Any]:
    """Execute multiple operations in batch"""
    try:
        results = []
        errors = 0
        
        for i, op in enumerate(operations):
            try:
                op_type = op.get("type", "unknown")
                op_data = op.get("data", {})
                
                if op_type == "echo":
                    result = await everything_echo(**op_data)
                elif op_type == "add":
                    result = await everything_add_numbers(**op_data)
                elif op_type == "store":
                    result = await everything_store_value(**op_data)
                else:
                    result = {"success": False, "error": f"Unknown operation type: {op_type}"}
                
                results.append({
                    "index": i,
                    "operation": op_type,
                    "result": result
                })
                
                if not result.get("success", False):
                    errors += 1
                    if stopOnError:
                        break
                        
            except Exception as e:
                error_result = {
                    "index": i,
                    "operation": op.get("type", "unknown"),
                    "result": {"success": False, "error": str(e)}
                }
                results.append(error_result)
                errors += 1
                if stopOnError:
                    break
                    
        return {
            "success": errors == 0,
            "totalOperations": len(operations),
            "executedOperations": len(results),
            "errors": errors,
            "stopOnError": stopOnError,
            "results": results,
            "action": "batch"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def everything_get_system_info() -> Dict[str, Any]:
    """Get system and server information"""
    try:
        import platform
        import sys
        
        return {
            "success": True,
            "server": {
                "name": "Everything HTTP MCP Server",
                "version": "1.0.0",
                "protocol": "MCP",
                "transport": "HTTP"
            },
            "system": {
                "platform": platform.system(),
                "release": platform.release(),
                "python_version": sys.version,
                "processor": platform.processor()
            },
            "memory": {
                "stored_items": len(memory_store),
                "counter": counter
            },
            "timestamp": datetime.now().isoformat(),
            "action": "system_info"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Get port from environment variable
    port = int(os.getenv('EVERYTHING_MCP_PORT', '8021'))
    
    print(f"Everything MCP test server initializing...")
    print(f"Starting Everything HTTP MCP Server on port {port}")
    print("This server implements various test operations for MCP client testing")
    
    # Run the server
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")