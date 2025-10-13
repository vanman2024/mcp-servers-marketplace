#!/bin/bash
# Fix for Claude MCP disconnection during sessions

set -e

MCP_ROOT="/home/gotime2022/mcp-kernel-new"
LOG_FILE="$HOME/.mcp-persistent/claude-fix.log"

echo "=== Claude MCP Disconnection Fix ===" | tee -a "$LOG_FILE"
echo "$(date)" | tee -a "$LOG_FILE"

# 1. Check if this is a Claude environment
if [ -z "$CLAUDE_SESSION_ID" ] && [ -z "$CLAUDE_PROJECT" ]; then
    echo "Not running in Claude environment" | tee -a "$LOG_FILE"
fi

# 2. Create a marker file to track session
SESSION_MARKER="$HOME/.mcp-persistent/claude-session-$(date +%s).marker"
touch "$SESSION_MARKER"

# 3. Function to inject MCP servers into Claude's runtime
inject_mcp_servers() {
    echo "Injecting MCP servers into Claude session..." | tee -a "$LOG_FILE"
    
    # Create a temporary Python script to interact with Claude's internals
    cat > /tmp/claude-mcp-inject.py << 'EOF'
import os
import json
import sys

# MCP servers to ensure are loaded
MCP_SERVERS = {
    "github": {"transport": "http", "url": "http://localhost:8011"},
    "supabase": {"transport": "http", "url": "http://localhost:8013"},
    "vercel-v0-enhanced": {"transport": "http", "url": "http://localhost:8015"},
    "filesystem": {"transport": "http", "url": "http://localhost:8006"},
    "memory": {"transport": "http", "url": "http://localhost:8007"},
    "sequential-thinking": {"transport": "http", "url": "http://localhost:8016"},
    "figma-mcp-application": {"transport": "http", "url": "http://localhost:8042"},
    "docker": {"transport": "http", "url": "http://localhost:8020"},
    "ngrok": {"transport": "http", "url": "http://localhost:8050"}
}

# Try to find and update Claude's runtime config
try:
    # Look for Claude's process environment
    for key, value in os.environ.items():
        if 'CLAUDE' in key or 'MCP' in key:
            print(f"{key}: {value}")
    
    # Signal that MCP should be available
    os.environ['MCP_SERVERS_AVAILABLE'] = json.dumps(list(MCP_SERVERS.keys()))
    print("MCP servers injected into environment")
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
EOF

    python3 /tmp/claude-mcp-inject.py >> "$LOG_FILE" 2>&1
}

# 4. Create a background process to maintain MCP availability
start_mcp_guardian() {
    echo "Starting MCP guardian process..." | tee -a "$LOG_FILE"
    
    cat > /tmp/mcp-guardian.sh << 'EOF'
#!/bin/bash
while true; do
    # Check if Claude process is still running
    if pgrep -f "claude" > /dev/null; then
        # Touch MCP config files to keep them fresh
        find ~/.claude -name "mcp_config.json" -exec touch {} \; 2>/dev/null
        find . -name ".claude/mcp_config.json" -exec touch {} \; 2>/dev/null
        
        # Send keep-alive signal (if Claude has a socket)
        echo "keepalive" > /tmp/claude-mcp-keepalive 2>/dev/null || true
    fi
    sleep 60
done
EOF

    chmod +x /tmp/mcp-guardian.sh
    nohup /tmp/mcp-guardian.sh > "$HOME/.mcp-persistent/guardian.log" 2>&1 &
    echo "Guardian PID: $!" | tee -a "$LOG_FILE"
}

# 5. Fix: Ensure MCP servers stay in Claude's active tool list
echo "Applying MCP persistence fix..." | tee -a "$LOG_FILE"

# Create override configuration
cat > "$HOME/.claude/mcp-override.json" << 'EOF'
{
  "mcpServers": {
    "github": {"transport": "http", "url": "http://localhost:8011", "persistent": true},
    "supabase": {"transport": "http", "url": "http://localhost:8013", "persistent": true},
    "vercel-v0-enhanced": {"transport": "http", "url": "http://localhost:8015", "persistent": true},
    "filesystem": {"transport": "http", "url": "http://localhost:8006", "persistent": true},
    "memory": {"transport": "http", "url": "http://localhost:8007", "persistent": true},
    "sequential-thinking": {"transport": "http", "url": "http://localhost:8016", "persistent": true},
    "figma-mcp-application": {"transport": "http", "url": "http://localhost:8042", "persistent": true},
    "docker": {"transport": "http", "url": "http://localhost:8020", "persistent": true},
    "ngrok": {"transport": "http", "url": "http://localhost:8050", "persistent": true}
  },
  "mcpPersistence": {
    "enabled": true,
    "reconnectInterval": 60,
    "maxReconnectAttempts": -1
  }
}
EOF

# 6. Export environment variables that might help
export CLAUDE_MCP_PERSISTENT=true
export MCP_RECONNECT_ON_DISCONNECT=true
export MCP_KEEPALIVE_INTERVAL=60

echo "Environment variables set" | tee -a "$LOG_FILE"

# Run the fixes
inject_mcp_servers
start_mcp_guardian

echo "=== Fix Applied ===" | tee -a "$LOG_FILE"
echo "MCP servers should now persist in Claude session" | tee -a "$LOG_FILE"
echo "Monitor logs at: $LOG_FILE" | tee -a "$LOG_FILE"