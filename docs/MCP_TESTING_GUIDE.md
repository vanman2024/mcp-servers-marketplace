# MCP Server Testing Guide

This guide provides standardized testing patterns for all MCP servers in this repository.

## 🚀 Quick Start

For any MCP server, testing follows this pattern:

```bash
cd servers/http/your-server-name
python test_direct.py      # Interactive test with detailed output
python test_ci.py          # CI/CD test with JSON results
```

## 📋 Testing Patterns

### 1. In-Memory Testing (Recommended)

The most efficient way to test MCP servers is using FastMCP's Client with in-memory connection:

```python
#!/usr/bin/env python3
"""Direct testing using FastMCP Client - NO HTTP/SSE complexity!"""

import asyncio
import os
import sys
from fastmcp import Client

# Set environment variables BEFORE imports
os.environ['MOCK_MODE'] = 'true'
os.environ['API_TOKEN'] = 'test-token'

# Add server path
sys.path.insert(0, 'src')

async def test_server():
    # Import AFTER setting env vars
    from your_server import mcp
    
    async with Client(mcp) as client:
        # Test tools
        result = await client.call_tool("tool_name", {"arg": "value"})
        print(f"Result: {result.data}")
        
        # Test resources
        resource = await client.read_resource("resource://name")
        print(f"Resource: {resource[0].text}")
        
        # Test prompts
        prompt = await client.get_prompt("prompt_name", {"param": "value"})
        print(f"Prompt: {prompt.messages[0].content.text}")

if __name__ == "__main__":
    asyncio.run(test_server())
```

### 2. Why This Works

- **No HTTP/SSE complexity** - Direct function calls
- **No session management** - Client handles it
- **Fast execution** - No network overhead
- **Easy debugging** - Standard Python exceptions

### 3. Common Pitfalls to Avoid

❌ **DON'T test with curl/HTTP directly**
- SSE requires special headers
- Session management is complex
- Error messages are obscured

❌ **DON'T use browser-based testing**
- Browsers can't handle SSE properly
- CORS issues
- No proper error handling

❌ **DON'T import server before setting env vars**
```python
# WRONG - env vars not set yet
from server import mcp
os.environ['MOCK_MODE'] = 'true'  # Too late!

# CORRECT - set env vars first
os.environ['MOCK_MODE'] = 'true'
from server import mcp
```

## 📝 Test Template

Copy this template for new MCP servers:

```python
#!/usr/bin/env python3
"""
Direct testing of [Server Name] MCP Server
Tests all tools, resources, and prompts
"""

import asyncio
import os
import sys
import json
from datetime import datetime
from fastmcp import Client

# Configure test environment
os.environ['MOCK_MODE'] = 'true'
os.environ['YOUR_API_TOKEN'] = 'test-token'

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
        self.errors.append({"test": test_name, "error": str(error)})
        print(f"❌ {test_name}: {error}")
        
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"Test Results: {self.passed}/{total} passed")
        return self.failed == 0

async def test_server():
    runner = TestRunner()
    
    print("🧪 [Server Name] MCP Server Test")
    print("=" * 50)
    
    try:
        from your_server import mcp
        
        async with Client(mcp) as client:
            # Test Tools
            tools = [
                ("tool_name", {"arg": "value"}),
                # Add more tools...
            ]
            
            for tool_name, args in tools:
                try:
                    result = await client.call_tool(tool_name, args)
                    if result.data:
                        runner.record_pass(f"Tool: {tool_name}")
                except Exception as e:
                    runner.record_fail(f"Tool: {tool_name}", str(e))
            
            # Test Resources
            resources = [
                "resource://name",
                # Add more resources...
            ]
            
            for resource_uri in resources:
                try:
                    result = await client.read_resource(resource_uri)
                    if result and len(result) > 0:
                        runner.record_pass(f"Resource: {resource_uri}")
                except Exception as e:
                    runner.record_fail(f"Resource: {resource_uri}", str(e))
            
            # Test Prompts
            prompts = [
                ("prompt_name", {"param": "value"}),
                # Add more prompts...
            ]
            
            for prompt_name, args in prompts:
                try:
                    result = await client.get_prompt(prompt_name, args)
                    if result.messages:
                        runner.record_pass(f"Prompt: {prompt_name}")
                except Exception as e:
                    runner.record_fail(f"Prompt: {prompt_name}", str(e))
                    
    except Exception as e:
        runner.record_fail("Server initialization", str(e))
    
    return runner.summary()

if __name__ == "__main__":
    success = asyncio.run(test_server())
    sys.exit(0 if success else 1)
```

## 🔧 Real-World Example: Digital Ocean Server

Here's how the Digital Ocean server implements testing:

### File Structure
```
digitalocean-http-mcp/
├── src/
│   └── digitalocean_server.py
├── test_direct.py          # Interactive testing
├── test_ci.py              # CI/CD testing
└── README.md
```

### Running Tests
```bash
# Interactive test with detailed output
$ python test_direct.py
🌊 Digital Ocean MCP Server In-Memory Test
==================================================
✅ Client connected successfully!
📊 Testing get_account_info...
Account email: test@example.com
...

# CI test with JSON results
$ python test_ci.py
🌊 Digital Ocean MCP Server CI/CD Test
==================================================
✅ Tool: get_account_info
✅ Tool: list_ssh_keys
...
Test Results: 20/20 passed
```

### CI/CD Integration

Add to `.github/workflows/test-your-server.yml`:

```yaml
- name: Run server tests
  env:
    MOCK_MODE: 'true'
    YOUR_API_TOKEN: 'github-actions-test'
  run: |
    cd servers/http/your-server-name
    python test_ci.py
```

## 🎯 Best Practices

1. **Always use mock mode for testing**
   - Faster execution
   - No API rate limits
   - Predictable results

2. **Test everything**
   - All tools with various arguments
   - All resources
   - All prompts with different parameters

3. **Handle errors gracefully**
   - Catch exceptions
   - Record failures
   - Continue testing other components

4. **Use meaningful test data**
   - Real-world scenarios
   - Edge cases
   - Invalid inputs

## 🐛 Debugging Tips

### Server won't start?
```python
# Add logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Tool not found?
```python
# List available tools
async with Client(mcp) as client:
    # Client will show available tools on connection
```

### Environment variables not working?
```python
# Verify they're set before import
print(f"MOCK_MODE: {os.getenv('MOCK_MODE')}")
from your_server import mcp  # Import AFTER
```

## 📊 Test Result Format

CI tests should output JSON results:

```json
{
  "timestamp": "2024-01-20T10:30:00",
  "passed": 20,
  "failed": 0,
  "errors": []
}
```

This enables:
- GitHub Actions integration
- Automated reporting
- Trend analysis

## 🚀 Conclusion

Testing MCP servers is straightforward when you:
1. Use FastMCP Client for in-memory testing
2. Set environment variables before imports
3. Test all components systematically
4. Handle errors gracefully

No need for complex HTTP/SSE testing - FastMCP handles it all!