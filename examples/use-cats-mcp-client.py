#!/usr/bin/env python3
"""
Example: Using CATS MCP Server via HTTP Client

This shows how to connect to the deployed FastMCP Cloud server
and call tools programmatically without Claude Desktop.
"""
import asyncio
import httpx
from typing import Any


class CATSMCPClient:
    """Simple MCP client for CATS server"""

    def __init__(self, url: str = "https://cats-mcp-server.fastmcp.app/mcp"):
        self.url = url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.request_id = 0

    async def _call(self, method: str, params: dict = None) -> Any:
        """Make MCP JSON-RPC call"""
        self.request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }

        response = await self.client.post(self.url, json=payload)
        response.raise_for_status()
        result = response.json()

        if "error" in result:
            raise Exception(f"MCP Error: {result['error']}")

        return result.get("result")

    async def list_tools(self) -> list[dict]:
        """List all available tools"""
        result = await self._call("tools/list")
        return result.get("tools", [])

    async def list_prompts(self) -> list[dict]:
        """List all available prompts"""
        result = await self._call("prompts/list")
        return result.get("prompts", [])

    async def list_resources(self) -> list[dict]:
        """List all available resources"""
        result = await self._call("resources/list")
        return result.get("resources", [])

    async def call_tool(self, name: str, arguments: dict = None) -> Any:
        """Call a specific tool"""
        result = await self._call("tools/call", {
            "name": name,
            "arguments": arguments or {}
        })
        return result

    async def get_prompt(self, name: str, arguments: dict = None) -> str:
        """Get a prompt"""
        result = await self._call("prompts/get", {
            "name": name,
            "arguments": arguments or {}
        })
        return result.get("messages", [])

    async def read_resource(self, uri: str) -> str:
        """Read a resource"""
        result = await self._call("resources/read", {
            "uri": uri
        })
        contents = result.get("contents", [])
        if contents:
            return contents[0].get("text", "")
        return ""

    async def close(self):
        """Close the client"""
        await self.client.aclose()


# Example usage
async def main():
    client = CATSMCPClient()

    try:
        print("🔍 Connecting to CATS MCP Server...")
        print(f"   URL: {client.url}\n")

        # List available capabilities
        print("📋 Available Tools:")
        tools = await client.list_tools()
        print(f"   Found {len(tools)} tools")
        for tool in tools[:5]:  # Show first 5
            print(f"   - {tool.get('name')}: {tool.get('description', '')[:60]}")
        print(f"   ... and {len(tools) - 5} more\n")

        print("📝 Available Prompts:")
        prompts = await client.list_prompts()
        print(f"   Found {len(prompts)} prompts")
        for prompt in prompts:
            print(f"   - {prompt.get('name')}: {prompt.get('description', '')}")
        print()

        print("📦 Available Resources:")
        resources = await client.list_resources()
        print(f"   Found {len(resources)} resources")
        for resource in resources:
            print(f"   - {resource.get('uri')}: {resource.get('description', '')}")
        print()

        # Example: Get site info
        print("🔧 Calling tool: get_site")
        result = await client.call_tool("get_site")
        print(f"   Result: {result}")
        print()

        # Example: Search candidates
        print("🔧 Calling tool: search_candidates")
        result = await client.call_tool("search_candidates", {
            "query": "Python developer",
            "limit": 5
        })
        print(f"   Found {len(result.get('candidates', []))} candidates")
        print()

        # Example: Get a prompt
        print("📝 Getting prompt: draft_rejection_email")
        messages = await client.get_prompt("draft_rejection_email", {
            "candidate_id": 12345
        })
        print(f"   Prompt messages: {len(messages)}")
        if messages:
            print(f"   First message: {messages[0].get('content', {}).get('text', '')[:100]}...")
        print()

        # Example: Read a resource
        print("📦 Reading resource: candidate://12345")
        content = await client.read_resource("candidate://12345")
        print(f"   Content: {content[:200]}...")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
