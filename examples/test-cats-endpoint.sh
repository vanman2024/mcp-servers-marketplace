#!/bin/bash
# Quick test of CATS MCP Server endpoint

ENDPOINT="https://cats-mcp-server.fastmcp.app/mcp"

echo "🔍 Testing CATS MCP Server"
echo "   Endpoint: $ENDPOINT"
echo ""

# Test 1: List tools
echo "📋 Listing tools..."
curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }' | jq -r '.result.tools | length'
echo ""

# Test 2: List prompts
echo "📝 Listing prompts..."
curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "prompts/list",
    "params": {}
  }' | jq -r '.result.prompts | length'
echo ""

# Test 3: List resources
echo "📦 Listing resources..."
curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "resources/list",
    "params": {}
  }' | jq -r '.result.resources | length'
echo ""

# Test 4: Call a tool
echo "🔧 Calling get_site tool..."
curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/call",
    "params": {
      "name": "get_site",
      "arguments": {}
    }
  }' | jq '.result'

echo ""
echo "✅ All tests complete!"
