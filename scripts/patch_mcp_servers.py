#!/usr/bin/env python3
"""
Patch existing MCP servers to use enhanced connection persistence
"""

import os
import sys
import shutil
from pathlib import Path

# Server files to patch
SERVERS_TO_PATCH = {
    'github-http-mcp/src/github_server.py': {
        'port_var': 'GITHUB_MCP_PORT',
        'default_port': '8011'
    },
    'supabase-http-mcp/src/supabase_server_v4.py': {
        'port_var': 'SUPABASE_MCP_PORT',
        'default_port': '8013'
    },
    'vercel-v0-mcp/src/vercel_v0_server.py': {
        'port_var': 'V0_MCP_PORT',
        'default_port': '8010'
    },
    'vercel-v0-enhanced-mcp/src/vercel_v0_server.py': {
        'port_var': 'V0_MCP_PORT',
        'default_port': '8015'
    },
    'filesystem-http-mcp/src/filesystem_server.py': {
        'port_var': 'FILESYSTEM_MCP_PORT',
        'default_port': '8006'
    },
    'memory-http-mcp/src/memory_server.py': {
        'port_var': 'MEMORY_MCP_PORT',
        'default_port': '8007'
    },
    'sequential-thinking-http-mcp/src/sequential_thinking_server.py': {
        'port_var': 'SEQUENTIAL_MCP_PORT',
        'default_port': '8016'
    },
    'docker-http-mcp/docker_server.py': {
        'port_var': 'DOCKER_MCP_PORT',
        'default_port': '8020'
    },
    'ngrok-http-mcp/src/ngrok_server.py': {
        'port_var': 'NGROK_MCP_PORT',
        'default_port': '8050'
    },
    'figma-mcp-application/src/figma_application_server.py': {
        'port_var': 'FIGMA_MCP_PORT',
        'default_port': '8042'
    }
}

PATCH_TEMPLATE = '''
# Import enhanced base
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from enhanced_fastmcp_base import add_health_check, create_enhanced_mcp_wrapper

# Add health check endpoints
add_health_check(mcp)

# Use enhanced runner
if __name__ == "__main__":
    port = int(os.getenv('{port_var}', '{default_port}'))
    logger.info(f"Starting {server_name} MCP Server on port {{port}} with enhanced persistence")
    
    # Create enhanced runner
    run_enhanced = create_enhanced_mcp_wrapper(mcp, heartbeat_interval=30)
    
    # Run with persistence features
    run_enhanced(transport="streamable-http", host="0.0.0.0", port=port, path="/")
'''

def patch_server(server_path: str, config: dict) -> bool:
    """Patch a single server file"""
    full_path = Path(f"/home/gotime2022/mcp-kernel-new/servers/http/{server_path}")
    
    if not full_path.exists():
        print(f"❌ Server file not found: {full_path}")
        return False
    
    # Create backup
    backup_path = full_path.with_suffix('.py.bak')
    if not backup_path.exists():
        shutil.copy2(full_path, backup_path)
        print(f"✅ Created backup: {backup_path}")
    
    # Read original content
    with open(full_path, 'r') as f:
        content = f.read()
    
    # Check if already patched
    if 'enhanced_fastmcp_base' in content:
        print(f"⚠️  Already patched: {full_path}")
        return True
    
    # Find the main block
    main_block_start = content.find('if __name__ == "__main__":')
    if main_block_start == -1:
        print(f"❌ No main block found in: {full_path}")
        return False
    
    # Extract server name from mcp variable
    import re
    mcp_match = re.search(r'mcp\s*=\s*FastMCP\s*\(\s*["\']([^"\']+)["\']', content)
    server_name = mcp_match.group(1) if mcp_match else "Unknown"
    
    # Create patched content
    new_content = content[:main_block_start]
    
    # Add patch with proper indentation
    patch = PATCH_TEMPLATE.format(
        port_var=config['port_var'],
        default_port=config['default_port'],
        server_name=server_name
    )
    
    new_content += patch
    
    # Write patched content
    with open(full_path, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Patched: {full_path}")
    return True

def main():
    """Patch all configured servers"""
    print("🔧 Patching MCP servers for enhanced connection persistence...")
    print("=" * 60)
    
    success_count = 0
    fail_count = 0
    
    for server_path, config in SERVERS_TO_PATCH.items():
        if patch_server(server_path, config):
            success_count += 1
        else:
            fail_count += 1
    
    print("=" * 60)
    print(f"✅ Successfully patched: {success_count} servers")
    if fail_count > 0:
        print(f"❌ Failed to patch: {fail_count} servers")
    
    print("\n📝 Next steps:")
    print("1. Restart the patched servers using: ./scripts/mcp-manager.sh restart")
    print("2. Start the connection monitor: python servers/http/mcp-connection-monitor.py")
    print("3. Monitor logs in: ~/.mcp-persistent/")

if __name__ == "__main__":
    main()