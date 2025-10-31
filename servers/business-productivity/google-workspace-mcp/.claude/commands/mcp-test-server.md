---
allowed-tools: Bash, TodoWrite, mcp__supabase-http-v3__list_projects, mcp__github-http__list_issues, mcp__vercel-v0-http__analyze_project_dependencies
description: Test a specific MCP server with comprehensive validation
---

# 🧪 Test Specific MCP Server

## Usage
```
/project:mcp-test-server server=github test-type=health
/project:mcp-test-server server=supabase-v3 test-type=all verbose=true
/project:mcp-test-server server=vercel-v0 test-type=integration
```

Testing server: $ARGUMENTS

## Parse Arguments
!`echo "$ARGUMENTS" | grep -oP 'server=\K[^ ]+' > /tmp/test-server.txt && echo "Server: $(cat /tmp/test-server.txt)" || echo "❌ Error: server argument required"`
!`echo "$ARGUMENTS" | grep -oP 'test-type=\K[^ ]+' > /tmp/test-type.txt || echo "health" > /tmp/test-type.txt && echo "Test type: $(cat /tmp/test-type.txt)"`
!`echo "$ARGUMENTS" | grep -oP 'verbose=\K[^ ]+' > /tmp/test-verbose.txt || echo "false" > /tmp/test-verbose.txt`

## Server Port Mapping
!`SERVER=$(cat /tmp/test-server.txt 2>/dev/null || echo ""); PORT=""; DIR=""; 
if [ -n "$SERVER" ]; then
  case "$SERVER" in
    "supabase-v3"|"supabase") PORT="8013"; DIR="supabase-http-mcp" ;;
    "github") PORT="8011"; DIR="github-http-mcp" ;;
    "vercel-v0") PORT="8010"; DIR="vercel-v0-mcp" ;;
    "docker") PORT="8020"; DIR="docker-http-mcp" ;;
    "slack") PORT="8017"; DIR="slack-http-mcp" ;;
    "redis") PORT="8018"; DIR="redis-http-mcp" ;;
    "anthropic") PORT="8015"; DIR="anthropic-comprehensive-http-mcp" ;;
    "openai") PORT="8012"; DIR="openai-tools-http-mcp" ;;
    "gemini") PORT="8014"; DIR="gemini-http-mcp" ;;
    "memory") PORT="8007"; DIR="memory-http-mcp" ;;
    "filesystem") PORT="8006"; DIR="filesystem-http-mcp" ;;
    "routing") PORT="8026"; DIR="routing-http-mcp" ;;
    "everything") PORT="8021"; DIR="everything-http-mcp" ;;
    "fetch") PORT="8022"; DIR="fetch-http-mcp" ;;
    "browserbase") PORT="8023"; DIR="browserbase-http-mcp" ;;
    "hostinger") PORT="8024"; DIR="hostinger-http-mcp" ;;
    "vercel-deploy") PORT="8025"; DIR="vercel-deploy-http-mcp" ;;
    "context7") PORT="8019"; DIR="context7-http-mcp" ;;
    "sequential-thinking") PORT="8016"; DIR="sequential-thinking-http-mcp" ;;
    "brave-search") PORT="8003"; DIR="brave-search-http-mcp" ;;
    "mui") PORT="8040"; DIR="mui-http-mcp" ;;
    *) echo "❌ Unknown server: $SERVER"; exit 1 ;;
  esac
  echo "$PORT" > /tmp/test-port.txt
  echo "$DIR" > /tmp/test-dir.txt
  echo "✅ Port: $PORT, Directory: $DIR"
else
  echo "❌ No server specified"
fi`

## Validate Server Directory
!`DIR=$(cat /tmp/test-dir.txt 2>/dev/null); if [ -z "$DIR" ]; then echo "❌ Usage: /mcp-test-server server=<name> [test-type=unit|integration|health|all]"; exit 1; elif [ ! -d "/home/gotime2022/mcp-kernel-new/servers/http/$DIR" ]; then echo "❌ Server directory $DIR not found"; ls -la /home/gotime2022/mcp-kernel-new/servers/http/ | grep -i $(cat /tmp/test-server.txt); else echo "✅ Testing $DIR server"; fi`

## Pre-Test: Check Server Status
!`PORT=$(cat /tmp/test-port.txt 2>/dev/null); SERVER=$(cat /tmp/test-server.txt 2>/dev/null); 
if [ -n "$PORT" ] && [ -n "$SERVER" ]; then
  echo "📡 Checking if $SERVER is running on port $PORT..."; 
  if lsof -i :$PORT >/dev/null 2>&1; then 
    echo "✅ Server is running on port $PORT"; 
  else 
    echo "⚠️ Server not detected on port $PORT"; 
  fi; 
else
  echo "⚠️ No server/port info available"
fi`

## Start Server If Needed
!`PORT=$(cat /tmp/test-port.txt 2>/dev/null); DIR=$(cat /tmp/test-dir.txt 2>/dev/null); 
if [ -n "$PORT" ] && [ -n "$DIR" ]; then
  if ! lsof -i :$PORT >/dev/null 2>&1; then 
    echo "🚀 Starting server..."; 
    cd /home/gotime2022/mcp-kernel-new && ./manage_mcp_servers.sh start $(echo $DIR | sed 's/-http-mcp//') 2>&1 | tail -5; 
    sleep 3; 
    if lsof -i :$PORT >/dev/null 2>&1; then 
      echo "✅ Server started successfully"; 
    else 
      echo "❌ Failed to start server"; 
    fi; 
  else
    echo "✅ Server already running on port $PORT"
  fi; 
else
  echo "⚠️ No port/directory info available"
fi`

## Health Check Test
!`SERVER=$(cat /tmp/test-server.txt 2>/dev/null); PORT=$(cat /tmp/test-port.txt 2>/dev/null); TYPE=$(cat /tmp/test-type.txt 2>/dev/null); 
if [ -n "$PORT" ] && ([ "$TYPE" == "health" ] || [ "$TYPE" == "all" ]); then 
  echo "🏥 Running health check..."; 
  curl -s http://localhost:$PORT/health 2>/dev/null && echo "✅ Health endpoint OK" || echo "⚠️ No health endpoint"; 
else
  echo "⏭️ Skipping health check"
fi`

## Protocol Test - List Tools
!`PORT=$(cat /tmp/test-port.txt 2>/dev/null); TYPE=$(cat /tmp/test-type.txt 2>/dev/null); 
if [ -n "$PORT" ] && ([ "$TYPE" == "protocol" ] || [ "$TYPE" == "all" ]); then 
  echo "🔧 Testing MCP protocol - List Tools..."; 
  curl -s -X POST http://localhost:$PORT/v1 -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}' 2>/dev/null | jq -r '.result.tools[]?.name' 2>/dev/null | head -10 && echo "✅ Tools listed successfully" || echo "❌ Failed to list tools"; 
else
  echo "⏭️ Skipping protocol test"
fi`

## Specific Server Tests
!`SERVER=$(cat /tmp/test-server.txt); TYPE=$(cat /tmp/test-type.txt); if [ "$TYPE" == "integration" ] || [ "$TYPE" == "all" ]; then echo "🔗 Running server-specific tests..."; fi`

### Supabase V3 Test
!`SERVER=$(cat /tmp/test-server.txt); TYPE=$(cat /tmp/test-type.txt); if ([ "$TYPE" == "integration" ] || [ "$TYPE" == "all" ]) && [ "$SERVER" == "supabase-v3" -o "$SERVER" == "supabase" ]; then echo "📊 Testing Supabase V3 integration..."; fi`

When server is supabase-v3, test list_projects:
!mcp__supabase-http-v3__list_projects()

### GitHub Test  
!`SERVER=$(cat /tmp/test-server.txt); TYPE=$(cat /tmp/test-type.txt); if ([ "$TYPE" == "integration" ] || [ "$TYPE" == "all" ]) && [ "$SERVER" == "github" ]; then echo "🐙 Testing GitHub integration..."; fi`

When server is github, test list_issues:
!mcp__github-http__list_issues(owner="mcp-kernel-clean", repo="mcp-kernel-clean", limit=1)

### Vercel V0 Test
!`SERVER=$(cat /tmp/test-server.txt); TYPE=$(cat /tmp/test-type.txt); if ([ "$TYPE" == "integration" ] || [ "$TYPE" == "all" ]) && [ "$SERVER" == "vercel-v0" ]; then echo "▲ Testing Vercel V0 integration..."; fi`

When server is vercel-v0, test analyze dependencies:
!mcp__vercel-v0-http__analyze_project_dependencies(project_path="/home/gotime2022/mcp-kernel-new")

## Performance Test
!`PORT=$(cat /tmp/test-port.txt); TYPE=$(cat /tmp/test-type.txt); if [ "$TYPE" == "performance" ] || [ "$TYPE" == "all" ]; then echo "⚡ Running performance test..."; START=$(date +%s%N); for i in {1..10}; do curl -s -X POST http://localhost:$PORT/v1 -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":'$i'}' >/dev/null 2>&1; done; END=$(date +%s%N); DIFF=$((($END - $START) / 10000000)); echo "Average response time: ${DIFF}ms for 10 requests"; fi`

## Test Summary
!`SERVER=$(cat /tmp/test-server.txt); TYPE=$(cat /tmp/test-type.txt); PORT=$(cat /tmp/test-port.txt); echo -e "\n📊 Test Summary\n==============\nServer: $SERVER\nPort: $PORT\nTest Type: $TYPE\nTime: $(date)"`

## Save Results
!`SERVER=$(cat /tmp/test-server.txt); TIMESTAMP=$(date +%Y%m%d_%H%M%S); mkdir -p /home/gotime2022/mcp-kernel-new/test_suite/test_reports && echo "Test completed for $SERVER at $TIMESTAMP" > /home/gotime2022/mcp-kernel-new/test_suite/test_reports/mcp_test_${SERVER}_${TIMESTAMP}.txt`

## Stop Server (Optional)
!`SERVER=$(cat /tmp/test-server.txt 2>/dev/null); echo "Server remains running. To stop: ./manage_mcp_servers.sh stop $SERVER"`

## Cleanup
!`rm -f /tmp/test-*.txt`

## Quick Test Examples
- Health check: `/mcp-test-server server=github test-type=health`
- Full test: `/mcp-test-server server=supabase-v3 test-type=all`
- Integration: `/mcp-test-server server=vercel-v0 test-type=integration`
- Performance: `/mcp-test-server server=memory test-type=performance`

## Available Servers
- `supabase-v3` - Supabase v3 with enhanced features
- `github` - GitHub API operations  
- `vercel-v0` - Vercel v0 component generation
- `mui` - Material-UI component generation
- `docker` - Docker container management
- `slack` - Slack messaging
- `redis` - Redis key-value store
- `anthropic` - Anthropic Claude API
- `openai` - OpenAI tools
- `gemini` - Google Gemini AI
- `memory` - Knowledge graph memory
- `filesystem` - File system operations
- `routing` - Multi-agent orchestration
- `brave-search` - Web search
- And more...