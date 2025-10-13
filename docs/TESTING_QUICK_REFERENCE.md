# MCP Server Testing Quick Reference

## 🚀 Test Any MCP Server in 30 Seconds

```bash
cd servers/http/your-server
cp ../test_template.py test_direct.py
# Edit: SERVER_NAME, SERVER_MODULE, tools, resources, prompts
python test_direct.py
```

## ✅ The Golden Rule

**Set environment variables BEFORE importing the server!**

```python
# ✅ CORRECT
os.environ['MOCK_MODE'] = 'true'
from your_server import mcp

# ❌ WRONG  
from your_server import mcp
os.environ['MOCK_MODE'] = 'true'  # Too late!
```

## 📝 Minimal Test Example

```python
#!/usr/bin/env python3
import asyncio
import os
import sys
from fastmcp import Client

# 1. Set env vars
os.environ['MOCK_MODE'] = 'true'
sys.path.insert(0, 'src')

# 2. Test function
async def test():
    from your_server import mcp
    async with Client(mcp) as client:
        # Test a tool
        result = await client.call_tool("tool_name", {})
        print(f"Result: {result.data}")

# 3. Run it
asyncio.run(test())
```

## 🔍 What to Test

### Tools
```python
result = await client.call_tool("tool_name", {"arg": "value"})
assert result.data is not None
```

### Resources
```python
result = await client.read_resource("resource://name")
assert len(result) > 0
assert result[0].text is not None
```

### Prompts
```python
result = await client.get_prompt("prompt_name", {"param": "value"})
assert len(result.messages) > 0
```

## 🐛 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "Module not found" | Add `sys.path.insert(0, 'src')` |
| "API key required" | Set env var: `os.environ['API_KEY'] = 'test'` |
| "Connection refused" | You're testing HTTP - use Client(mcp) instead |
| "No such tool" | Check exact tool name in server file |
| "SSE errors" | Don't use curl/HTTP - use Client(mcp) |

## 📊 CI/CD Integration

```yaml
# .github/workflows/test-server.yml
- name: Test MCP Server
  run: |
    cd servers/http/your-server
    python -m pip install fastmcp
    python test_ci.py
```

## 🎯 Test Output Examples

**Good Test Output:**
```
🧪 Digital Ocean MCP Server Test
==================================================
✅ Tool: list_droplets - Found 3 droplets
✅ Tool: create_droplet - Created ID: 12345
✅ Resource: resource://regions - 1500 chars
✅ Prompt: help_text - 2000 chars

Test Results: 4/4 passed in 0.5s
```

**With Errors:**
```
🧪 My Server Test
==================================================
✅ Tool: working_tool
❌ Tool: broken_tool: list index out of range
✅ Resource: resource://config

Test Results: 2/3 passed
Failed tests:
  - Tool: broken_tool: list index out of range
```

## 💡 Pro Tips

1. **Use Mock Mode** - Faster, no rate limits, predictable
2. **Test Everything** - All tools, resources, prompts
3. **Check Edge Cases** - Empty results, invalid args, missing data
4. **JSON Output** - CI/CD can parse test_results.json
5. **Verbose Errors** - Print full exceptions during development

## 🚨 Remember

**FastMCP Client + In-Memory Testing = Simple & Fast**

No HTTP, no SSE, no sessions, no complexity!