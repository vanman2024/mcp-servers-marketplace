#!/bin/bash

echo "🌊 Testing Digital Ocean MCP Server"
echo "==================================="

# Initialize and get session ID
echo -e "\n1️⃣ Initializing connection..."
INIT_RESPONSE=$(curl -s -X POST http://localhost:8040/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {
      "protocolVersion": "0.1.0",
      "capabilities": {},
      "clientInfo": {
        "name": "Test Client",
        "version": "1.0.0"
      }
    },
    "id": 1
  }')

# Extract session ID from headers (need to capture headers)
SESSION_RESPONSE=$(curl -s -i -X POST http://localhost:8040/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {
      "protocolVersion": "0.1.0",
      "capabilities": {},
      "clientInfo": {
        "name": "Test Client",
        "version": "1.0.0"
      }
    },
    "id": 1
  }')

SESSION_ID=$(echo "$SESSION_RESPONSE" | grep -i "mcp-session-id:" | cut -d' ' -f2 | tr -d '\r')
echo "Session ID: $SESSION_ID"

# Test get_account_info
echo -e "\n2️⃣ Testing get_account_info..."
curl -s -X POST http://localhost:8040/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Cookie: mcp-session-id=$SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_account_info",
      "arguments": {}
    },
    "id": 2
  }' | sed 's/^data: //' | jq '.result'

# Test list_droplets
echo -e "\n3️⃣ Testing list_droplets..."
curl -s -X POST http://localhost:8040/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Cookie: mcp-session-id=$SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "list_droplets",
      "arguments": {}
    },
    "id": 3
  }' | sed 's/^data: //' | jq '.result'

# Test create_droplet (mock)
echo -e "\n4️⃣ Testing create_droplet..."
curl -s -X POST http://localhost:8040/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Cookie: mcp-session-id=$SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "create_droplet",
      "arguments": {
        "name": "test-droplet-bash",
        "region": "nyc3",
        "size": "s-1vcpu-1gb",
        "image": "ubuntu-22-04-x64",
        "tags": ["test", "mcp"]
      }
    },
    "id": 4
  }' | sed 's/^data: //' | jq '.result'

# Test resources
echo -e "\n5️⃣ Testing resource: regions..."
curl -s -X POST http://localhost:8040/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Cookie: mcp-session-id=$SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "method": "resources/read",
    "params": {
      "uri": "resource://regions"
    },
    "id": 5
  }' | sed 's/^data: //' | jq '.result.contents[0].text | fromjson'

echo -e "\n✅ All tests completed!"