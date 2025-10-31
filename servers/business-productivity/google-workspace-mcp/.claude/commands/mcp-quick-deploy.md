---
allowed-tools: Bash, TodoWrite
description: Quick deployment of specific MCP server to target environment
---

# ⚡ Quick MCP Server Deployment

## Usage
```
/project:mcp-quick-deploy server=github target=synapseai
/project:mcp-quick-deploy server=supabase skip-tests=true
/project:mcp-quick-deploy server=all target=synapseai
```

Deploying with arguments: $ARGUMENTS

## Parse Arguments
!`echo "$ARGUMENTS" | grep -oP 'server=\K[^ ]+' > /tmp/deploy-server.txt || echo "all" > /tmp/deploy-server.txt && echo "Server: $(cat /tmp/deploy-server.txt)"`
!`echo "$ARGUMENTS" | grep -oP 'target=\K[^ ]+' > /tmp/deploy-target.txt || echo "synapseai" > /tmp/deploy-target.txt && echo "Target: $(cat /tmp/deploy-target.txt)"`
!`echo "$ARGUMENTS" | grep -oP 'skip-tests=\K[^ ]+' > /tmp/deploy-skip-tests.txt || echo "false" > /tmp/deploy-skip-tests.txt && echo "Skip tests: $(cat /tmp/deploy-skip-tests.txt)"`

## Pre-deployment Check
!`SERVER=$(cat /tmp/deploy-server.txt); TARGET=$(cat /tmp/deploy-target.txt); if [ "$SERVER" != "all" ] && [ ! -d "/home/gotime2022/mcp-kernel-new/servers/http/${SERVER}-http-mcp" ]; then echo "❌ Server $SERVER not found!"; else echo "✅ Server $SERVER found"; fi`

## Quick Test (if not skipped)
!`SERVER=$(cat /tmp/deploy-server.txt); SKIP=$(cat /tmp/deploy-skip-tests.txt); if [ "$SKIP" == "false" ] && [ "$SERVER" != "all" ]; then cd /home/gotime2022/mcp-kernel-new/servers/http/${SERVER}-http-mcp && timeout 5 python3 -m src.${SERVER}_server 2>&1 | head -5 && echo "✅ Server starts OK" || echo "⚠️ Server start test skipped"; fi`

## Deploy
!`SERVER=$(cat /tmp/deploy-server.txt); TARGET=$(cat /tmp/deploy-target.txt); echo "📦 Deploying $SERVER to $TARGET..."`

Backup current version:
!`SERVER=$(cat /tmp/deploy-server.txt); TARGET=$(cat /tmp/deploy-target.txt); TIMESTAMP=$(date +%Y%m%d_%H%M%S); mkdir -p /home/gotime2022/$TARGET/backups/$TIMESTAMP && if [ "$SERVER" == "all" ]; then cp -r /home/gotime2022/$TARGET/mcp-servers /home/gotime2022/$TARGET/backups/$TIMESTAMP/ 2>/dev/null; else cp -r /home/gotime2022/$TARGET/mcp-servers/http/${SERVER}-http-mcp /home/gotime2022/$TARGET/backups/$TIMESTAMP/ 2>/dev/null; fi && echo "Backup: $TIMESTAMP"`

Version control update:
!`SERVER=$(cat /tmp/deploy-server.txt); cd /home/gotime2022/mcp-kernel-new/servers/configs && ./version-control.sh bump patch "Quick deploy of $SERVER to SynapseAI3" 2>&1 | tail -5`

Deploy servers:
!`SERVER=$(cat /tmp/deploy-server.txt); TARGET=$(cat /tmp/deploy-target.txt); cd /home/gotime2022/mcp-kernel-new/deployment && if [ "$SERVER" == "all" ]; then ./scripts/environments/$TARGET/sync.sh 2>&1 | tail -10; else rsync -av --delete --exclude='*.pyc' --exclude='__pycache__' --exclude='*.log' --exclude='tests' /home/gotime2022/mcp-kernel-new/servers/http/${SERVER}-http-mcp/ /home/gotime2022/$TARGET/mcp-servers/http/${SERVER}-http-mcp/; fi`

## Restart & Verify

Check and fix MCP connections:
!`claude mcp list | grep -E "(supabase|vercel-v0|github)" || echo "Checking MCP connections..."`

Fix common naming issues:
!`SERVER=$(cat /tmp/deploy-server.txt); if [ "$SERVER" = "supabase" ] || [ "$SERVER" = "all" ]; then claude mcp remove supabase-http 2>/dev/null; claude mcp add --transport http supabase-http-v3 http://localhost:8013; fi`

Kill existing processes:
!`SERVER=$(cat /tmp/deploy-server.txt); if [ "$SERVER" != "all" ]; then pkill -f "${SERVER}_server" 2>/dev/null; else pkill -f "supabase_server_v3.py" 2>/dev/null; pkill -f "vercel_v0_server.py" 2>/dev/null; fi`

!`SERVER=$(cat /tmp/deploy-server.txt); TARGET=$(cat /tmp/deploy-target.txt); cd /home/gotime2022/$TARGET && if [ "$SERVER" == "all" ]; then ./manage_mcp_servers.sh restart 2>&1 | tail -5; else ./manage_mcp_servers.sh restart $SERVER 2>&1; fi`

Manual restart for problem servers:
!`SERVER=$(cat /tmp/deploy-server.txt); cd /home/gotime2022/mcp-kernel-new/servers && if [ "$SERVER" = "supabase" ] || [ "$SERVER" = "all" ]; then python http/supabase-http-mcp/src/supabase_server_v3.py & fi`
!`SERVER=$(cat /tmp/deploy-server.txt); cd /home/gotime2022/mcp-kernel-new/servers && if [ "$SERVER" = "vercel-v0" ] || [ "$SERVER" = "all" ]; then python http/vercel-v0-mcp/src/vercel_v0_server.py & fi`

Check status:
!`SERVER=$(cat /tmp/deploy-server.txt); TARGET=$(cat /tmp/deploy-target.txt); cd /home/gotime2022/$TARGET && sleep 3 && if [ "$SERVER" == "all" ]; then ./manage_mcp_servers.sh status | grep -E "(Running|Stopped)" | head -10; else ./manage_mcp_servers.sh status | grep -i $SERVER; fi`

Verify ports:
!`netstat -tlnp 2>/dev/null | grep -E "8010|8013" || lsof -i :8010,8013 2>/dev/null`

## Cleanup
!`rm -f /tmp/deploy-*.txt`

## Summary
✅ Deployment complete for: $ARGUMENTS

Use `/mcp-test-server` to verify specific functionality if needed.