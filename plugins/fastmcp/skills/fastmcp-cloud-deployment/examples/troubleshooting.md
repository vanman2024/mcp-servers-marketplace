# FastMCP Deployment Troubleshooting Guide

This guide covers common deployment issues and their solutions.

## Pre-Deployment Issues

### Validation Script Failures

#### Issue: "Python syntax errors detected"

**Symptoms**:
```bash
$ ./scripts/validate-server.sh .
✗ Python syntax errors detected
  File "server.py", line 42
    return {"result" result}
                          ^
SyntaxError: invalid syntax
```

**Solution**:
1. Fix the syntax error in your code
2. Use a Python linter: `python3 -m pylint server.py`
3. Run validation again
4. Consider using pre-commit hooks to catch syntax errors before committing

#### Issue: "FastMCP not found in requirements.txt"

**Symptoms**:
```bash
✗ FastMCP not found in requirements.txt
```

**Solution**:
```bash
# Add FastMCP to requirements.txt
echo "fastmcp==0.5.0" >> requirements.txt

# Or if using uv
uv add fastmcp
```

#### Issue: "Unpinned dependencies"

**Symptoms**:
```bash
⚠ Found 5 unpinned dependencies (recommend using == for production)
```

**Solution**:
```bash
# Pin all dependencies
pip freeze > requirements.txt

# Or manually specify versions
# Bad:  requests
# Good: requests==2.31.0
```

### Environment Variable Issues

#### Issue: "Missing required variable"

**Symptoms**:
```bash
$ ./scripts/check-env-vars.sh .
✗ Missing 1 required variable(s):
  - API_KEY
```

**Solution**:
```bash
# Add to .env file
echo "API_KEY=your-api-key-here" >> .env

# Verify it's set
./scripts/check-env-vars.sh .
```

#### Issue: ".env not in .gitignore"

**Symptoms**:
```bash
✗ .env is NOT in .gitignore - risk of committing secrets!
```

**Solution**:
```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore
echo "!.env.example" >> .gitignore

# If already committed, remove from git
git rm --cached .env
git commit -m "Remove .env from git"
```

### Local Testing Failures

#### Issue: "Server failed to start"

**Symptoms**:
```bash
$ ./scripts/test-local.sh .
✗ Server failed to start
ModuleNotFoundError: No module named 'fastmcp'
```

**Solution**:
```bash
# Install dependencies
pip install -r requirements.txt

# Or create virtual environment first
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue: "Port already in use"

**Symptoms**:
```bash
$ ./scripts/test-local.sh .
✗ Port 8000 already in use
```

**Solution**:
```bash
# Find process using port
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
PORT=8001 ./scripts/test-local.sh .
```

#### Issue: "No MCP messages detected"

**Symptoms**:
```bash
⚠ No MCP messages detected yet (may need more time)
```

**Solution**:
1. Check server is using MCP protocol correctly
2. Verify FastMCP initialization in code
3. Check logs for errors: `cat /tmp/fastmcp-test-stdio.log`
4. Increase test duration: `TEST_DURATION=30 ./scripts/test-local.sh .`

## Deployment Issues

### FastMCP Cloud Deployment

#### Issue: "Build failed - dependency installation"

**Symptoms**:
```
[Error] Failed to install dependencies
Could not find a version that satisfies the requirement fastmcp==999.0.0
```

**Solution**:
1. Check version exists: `pip index versions fastmcp`
2. Update to valid version in requirements.txt
3. Push changes and redeploy

#### Issue: "Environment variable not set"

**Symptoms**:
```
[Error] Server crashed during startup
KeyError: 'API_KEY'
```

**Solution**:
1. Go to FastMCP Cloud dashboard
2. Settings > Environment Variables
3. Add missing variable
4. Redeploy or restart server

#### Issue: "Entry point not found"

**Symptoms**:
```
[Error] Cannot find entry point: server.py
```

**Solution**:
1. Check fastmcp.json has correct entryPoint
2. Ensure file exists in repository root
3. Verify file name matches exactly (case-sensitive)

```json
{
  "name": "my-server",
  "version": "1.0.0",
  "entryPoint": "server.py"  // Must match actual filename
}
```

### HTTP Deployment Issues

#### Issue: "Connection refused"

**Symptoms**:
```bash
$ ./scripts/verify-deployment.sh http://my-server.com/mcp
✗ Cannot reach server at http://my-server.com
curl: (7) Failed to connect to my-server.com port 80: Connection refused
```

**Solution**:
1. Check server is running: `systemctl status my-server`
2. Check firewall: `sudo ufw status`
3. Open port: `sudo ufw allow 80/tcp`
4. Check server logs for errors

#### Issue: "502 Bad Gateway"

**Symptoms**:
```
HTTP/1.1 502 Bad Gateway
```

**Solution**:
1. Check upstream server is running
2. Review nginx/reverse proxy config
3. Check proxy_pass URL is correct
4. Verify backend server is listening on correct port

```nginx
# Good nginx config
location /mcp {
    proxy_pass http://localhost:8000/mcp;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

#### Issue: "CORS errors"

**Symptoms**:
```
Access to fetch at 'https://my-server.com/mcp' from origin 'https://app.example.com'
has been blocked by CORS policy
```

**Solution**:
```python
# In your FastMCP server
from fastmcp import FastMCP

mcp = FastMCP("my-server")

# Add CORS middleware
mcp.add_cors(
    origins=["https://app.example.com"],
    allow_credentials=True
)
```

### SSL/TLS Issues

#### Issue: "Certificate has expired"

**Symptoms**:
```bash
✗ Certificate has expired!
```

**Solution**:
```bash
# For Let's Encrypt
sudo certbot renew

# For other providers, get new certificate
# Then update web server config
sudo systemctl reload nginx
```

#### Issue: "Self-signed certificate"

**Symptoms**:
```
curl: (60) SSL certificate problem: self signed certificate
```

**Solution**:
1. For production: Get proper certificate from Let's Encrypt or commercial CA
2. For testing only: `curl -k` to skip verification (NOT for production!)

```bash
# Get Let's Encrypt certificate
sudo certbot --nginx -d my-server.com
```

## Post-Deployment Issues

### Verification Failures

#### Issue: "Health endpoint not responding"

**Symptoms**:
```bash
$ ./scripts/verify-deployment.sh https://my-server.com/mcp
⚠ No standard health endpoint found
```

**Solution**:
1. Add health endpoint to your server:

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.health_check()
async def health():
    return {"status": "healthy"}
```

2. Redeploy server
3. Verify: `curl https://my-server.com/health`

#### Issue: "MCP endpoint not ready"

**Symptoms**:
```bash
⚠ MCP endpoint not ready (HTTP 503)
Retrying in 10s...
```

**Solution**:
1. Server may be starting up - wait for retries to complete
2. If continues failing, check server logs
3. Verify dependencies loaded correctly
4. Check for startup errors in logs

#### Issue: "Server returned no tools"

**Symptoms**:
```bash
⚠ Server returned no tools
```

**Solution**:
1. Verify tools are registered in code:

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
async def my_tool(param: str) -> str:
    """Tool description"""
    return f"Result: {param}"
```

2. Check server logs for registration errors
3. Test locally first: `TEST_TRANSPORT=stdio ./scripts/test-local.sh .`

### Performance Issues

#### Issue: "Response time slow (>5s)"

**Symptoms**:
```bash
⚠ Response time slow (>5s) - consider optimization
Sample 1: 6.234s
Sample 2: 5.891s
Sample 3: 6.012s
```

**Solution**:
1. **Check network latency**: Run from closer location
2. **Enable caching**: Cache frequently accessed data
3. **Optimize database queries**: Add indexes, reduce N+1 queries
4. **Increase server resources**: More CPU/RAM
5. **Add CDN**: For static assets
6. **Profile code**: Identify bottlenecks

```python
# Add simple caching
from functools import lru_cache

@mcp.tool()
@lru_cache(maxsize=100)
async def expensive_operation(param: str) -> str:
    # Expensive computation here
    pass
```

#### Issue: "Memory leak"

**Symptoms**:
- Memory usage increases over time
- Server becomes slow
- Eventually crashes

**Solution**:
1. **Profile memory usage**: Use memory profiler
2. **Check for unclosed connections**: Close database/HTTP connections
3. **Clear caches periodically**: Don't cache unlimited data
4. **Fix resource leaks**: Use context managers

```python
# Good: Using context manager
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        return await response.json()

# Bad: Not closing session
session = aiohttp.ClientSession()
response = await session.get(url)  # Never closes!
```

## Runtime Issues

### Server Crashes

#### Issue: "Server keeps crashing"

**Symptoms**:
```
Server status: inactive (crashed)
Last exit code: 1
```

**Solution**:
1. Check logs: `journalctl -u my-server -n 100`
2. Look for error messages before crash
3. Common causes:
   - Unhandled exceptions
   - Missing dependencies
   - Invalid environment variables
   - Out of memory

```python
# Add error handling
@mcp.tool()
async def my_tool(param: str) -> str:
    try:
        # Your code here
        return result
    except Exception as e:
        # Log error
        logger.error(f"Tool failed: {e}")
        # Return error to user
        raise MCPError(f"Operation failed: {str(e)}")
```

#### Issue: "ImportError at runtime"

**Symptoms**:
```
ImportError: cannot import name 'FastMCP' from 'fastmcp'
```

**Solution**:
1. Check FastMCP version matches code requirements
2. Verify all dependencies installed
3. Check Python version compatibility
4. Reinstall dependencies: `pip install --force-reinstall -r requirements.txt`

### Authentication Issues

#### Issue: "401 Unauthorized"

**Symptoms**:
```bash
✓ MCP endpoint responding (HTTP 401)
⚠ Authentication required
```

**Solution**:
1. If authentication is expected, provide credentials
2. If not expected, check server configuration
3. Verify authentication middleware is correct

```python
# Add authentication
from fastmcp import FastMCP
from fastmcp.auth import BearerAuth

mcp = FastMCP("my-server")
mcp.add_auth(BearerAuth(token="your-secret-token"))
```

## Debugging Tools

### Enable Verbose Logging

```bash
# For validation
VERBOSE=1 ./scripts/validate-server.sh .

# For verification
VERBOSE=1 ./scripts/verify-deployment.sh https://my-server.com/mcp

# In server code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Server Logs

```bash
# FastMCP Cloud
# View via dashboard > Logs

# SystemD service
journalctl -u my-server -f

# Docker
docker logs -f my-server

# Direct logs
tail -f /var/log/my-server.log
```

### Test MCP Endpoint Manually

```bash
# Test tools/list
curl -X POST https://my-server.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Expected response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {"name": "my_tool", "description": "...", "inputSchema": {...}}
    ]
  }
}
```

### Network Debugging

```bash
# Check DNS
dig my-server.com

# Check connectivity
ping my-server.com

# Check port
nc -zv my-server.com 443

# Trace route
traceroute my-server.com

# Check SSL certificate
openssl s_client -connect my-server.com:443 -servername my-server.com
```

## Getting Help

### Information to Include

When asking for help, include:

1. **Error message** (full output)
2. **Script output** (validation/test/verification)
3. **Server logs** (last 50 lines before crash)
4. **Configuration files** (fastmcp.json, .env.example)
5. **Deployment target** (FastMCP Cloud, HTTP, STDIO)
6. **Steps to reproduce**

### Where to Get Help

- **FastMCP Documentation**: https://gofastmcp.com/docs
- **GitHub Issues**: https://github.com/jlowin/fastmcp/issues
- **Discord Community**: https://discord.gg/fastmcp
- **Stack Overflow**: Tag `fastmcp` or `mcp-protocol`

## Preventive Measures

### Before Every Deployment

1. ✅ Run all validation scripts
2. ✅ Test locally in both STDIO and HTTP modes
3. ✅ Verify environment variables
4. ✅ Check dependencies are pinned
5. ✅ Review deployment checklist
6. ✅ Have rollback plan ready

### Monitoring

Set up monitoring to catch issues early:

```python
# Add health check with details
@mcp.health_check()
async def health():
    return {
        "status": "healthy",
        "uptime": get_uptime(),
        "memory_usage": get_memory_usage(),
        "version": "1.0.0"
    }
```

### Regular Maintenance

- Update dependencies monthly
- Review logs weekly
- Test deployment process quarterly
- Renew SSL certificates before expiration
- Rotate secrets regularly

---

**Remember**: Most issues are caught by running the validation scripts before deployment!
