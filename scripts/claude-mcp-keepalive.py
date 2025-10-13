#!/usr/bin/env python3
"""
Claude MCP Keep-Alive Service
Forces Claude to maintain MCP connections by periodically refreshing them
"""

import asyncio
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/gotime2022/.mcp-persistent/claude-keepalive.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ClaudeMCPKeepAlive:
    def __init__(self):
        self.interval = 300  # 5 minutes
        self.claude_config = Path.home() / '.claude.json'
        self.project_root = os.getcwd()
        self.mcp_servers = {
            "github": "http://localhost:8011",
            "supabase": "http://localhost:8013",
            "vercel-v0-enhanced": "http://localhost:8015",
            "filesystem": "http://localhost:8006",
            "memory": "http://localhost:8007",
            "sequential-thinking": "http://localhost:8016",
            "figma-mcp-application": "http://localhost:8042",
            "docker": "http://localhost:8020",
            "ngrok": "http://localhost:8050"
        }
        
    def refresh_mcp_config(self):
        """Refresh MCP configuration in current project"""
        try:
            config_file = Path(self.project_root) / '.claude' / 'mcp_config.json'
            
            # Read current config
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
            else:
                config = {"mcpServers": {}}
            
            # Update with all servers
            for name, url in self.mcp_servers.items():
                config['mcpServers'][name] = {
                    "transport": "http",
                    "url": url,
                    "description": f"{name} MCP server"
                }
            
            # Write back with timestamp
            config['_lastRefresh'] = datetime.now().isoformat()
            
            config_file.parent.mkdir(exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
                
            logger.info(f"Refreshed MCP config at {config_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to refresh config: {e}")
            return False
    
    def force_claude_refresh(self):
        """Force Claude to re-read MCP configuration"""
        try:
            # Touch the Claude config to trigger reload
            if self.claude_config.exists():
                self.claude_config.touch()
                logger.info("Touched Claude config to trigger reload")
            
            # Also touch project config
            project_config = Path(self.project_root) / '.claude' / 'mcp_config.json'
            if project_config.exists():
                project_config.touch()
                logger.info("Touched project MCP config")
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to force refresh: {e}")
            return False
    
    def check_mcp_in_session(self):
        """Check if MCP servers are registered in current session"""
        try:
            # Try to get MCP list from Claude CLI
            result = subprocess.run(
                ['claude', 'mcp', 'list', '--json'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                servers = json.loads(result.stdout)
                active_count = len(servers)
                logger.info(f"Found {active_count} active MCP servers in session")
                
                # If less than expected, re-sync
                if active_count < len(self.mcp_servers):
                    logger.warning(f"Only {active_count}/{len(self.mcp_servers)} servers active, re-syncing...")
                    self.sync_claude_mcp()
                    
                return active_count
            else:
                logger.warning("Failed to get MCP list from Claude")
                return 0
                
        except Exception as e:
            logger.error(f"Error checking MCP session: {e}")
            return 0
    
    def sync_claude_mcp(self):
        """Re-sync all MCP servers with Claude"""
        try:
            logger.info("Re-syncing MCP servers with Claude...")
            
            # Run sync command
            result = subprocess.run(
                ['/home/gotime2022/mcp-kernel-new/scripts/mcp-manager.sh', 'sync-claude', '.'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                logger.info("Successfully re-synced MCP servers")
                return True
            else:
                logger.error(f"Failed to sync: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error syncing MCP: {e}")
            return False
    
    async def keepalive_loop(self):
        """Main keep-alive loop"""
        logger.info("Starting Claude MCP keep-alive service")
        logger.info(f"Monitoring {len(self.mcp_servers)} servers")
        logger.info(f"Refresh interval: {self.interval} seconds")
        
        while True:
            try:
                # 1. Refresh MCP config
                self.refresh_mcp_config()
                
                # 2. Force Claude to reload
                self.force_claude_refresh()
                
                # 3. Check active servers
                active = self.check_mcp_in_session()
                
                # 4. Re-sync if needed
                if active < len(self.mcp_servers):
                    self.sync_claude_mcp()
                
                logger.info(f"Keep-alive cycle complete - {active}/{len(self.mcp_servers)} servers active")
                
            except Exception as e:
                logger.error(f"Error in keep-alive loop: {e}")
            
            # Wait for next cycle
            await asyncio.sleep(self.interval)
    
    def run(self):
        """Run the keep-alive service"""
        try:
            asyncio.run(self.keepalive_loop())
        except KeyboardInterrupt:
            logger.info("Keep-alive service stopped by user")
        except Exception as e:
            logger.error(f"Keep-alive service error: {e}")

if __name__ == "__main__":
    service = ClaudeMCPKeepAlive()
    service.run()