#!/usr/bin/env python3
"""
MCP HTTP Server Connection Monitor
Ensures persistent connections for HTTP MCP servers by monitoring and auto-restarting
"""

import asyncio
import aiohttp
import os
import sys
import json
import logging
import subprocess
import signal
from typing import Dict, Any, Optional, Set
from datetime import datetime, timedelta
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/gotime2022/.mcp-persistent/connection-monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MCPConnectionMonitor:
    """Monitor and maintain MCP HTTP server connections"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or "/home/gotime2022/mcp-kernel-new/.claude/mcp_master_config.json"
        self.servers = {}
        self.health_check_interval = 30  # seconds
        self.restart_delay = 5  # seconds
        self.max_restart_attempts = 3
        self.restart_counts = {}
        self.running = True
        self.session = None
        self.failed_servers: Set[str] = set()
        
    async def load_config(self):
        """Load MCP server configuration"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                
            for name, server_config in config.get('mcpServers', {}).items():
                if server_config.get('transport') == 'http':
                    self.servers[name] = {
                        'url': server_config.get('url'),
                        'port': int(server_config.get('url', '').split(':')[-1]) if ':' in server_config.get('url', '') else None,
                        'last_check': None,
                        'status': 'unknown',
                        'restart_count': 0
                    }
            
            logger.info(f"Loaded {len(self.servers)} HTTP MCP servers from config")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return False
    
    async def check_server_health(self, name: str, server_info: Dict[str, Any]) -> bool:
        """Check if a server is responding to health checks"""
        url = server_info['url']
        
        # Skip if server has failed too many times
        if name in self.failed_servers:
            return False
            
        try:
            # Try multiple health check endpoints
            health_endpoints = [
                f"{url}/health",
                f"{url}/",
                f"{url}/mcp/health"
            ]
            
            for endpoint in health_endpoints:
                try:
                    async with self.session.get(endpoint, timeout=aiohttp.ClientTimeout(total=5)) as response:
                        if response.status in [200, 404]:  # 404 means server is up but no health endpoint
                            server_info['status'] = 'healthy'
                            server_info['last_check'] = datetime.now()
                            server_info['restart_count'] = 0  # Reset on success
                            return True
                except:
                    continue
            
            # All endpoints failed
            server_info['status'] = 'unhealthy'
            return False
            
        except Exception as e:
            logger.warning(f"Health check failed for {name}: {e}")
            server_info['status'] = 'unhealthy'
            return False
    
    def get_server_process(self, port: int) -> Optional[psutil.Process]:
        """Find process listening on given port"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    for conn in proc.connections():
                        if conn.laddr.port == port and conn.status == 'LISTEN':
                            return proc
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logger.error(f"Error finding process on port {port}: {e}")
        return None
    
    async def restart_server(self, name: str, server_info: Dict[str, Any]):
        """Restart a failed MCP server"""
        port = server_info.get('port')
        if not port:
            logger.error(f"No port info for {name}")
            return False
            
        # Check restart limit
        if server_info['restart_count'] >= self.max_restart_attempts:
            logger.error(f"Server {name} exceeded restart limit ({self.max_restart_attempts})")
            self.failed_servers.add(name)
            return False
        
        try:
            # Kill existing process if any
            proc = self.get_server_process(port)
            if proc:
                logger.info(f"Killing existing process for {name} (PID: {proc.pid})")
                proc.terminate()
                await asyncio.sleep(2)
                if proc.is_running():
                    proc.kill()
            
            # Use mcp-manager.sh to restart
            logger.info(f"Restarting {name} via mcp-manager.sh")
            
            # Map clean names to server keys for mcp-manager.sh
            server_key_map = {
                'github': 'github-http',
                'supabase': 'supabase-v4',
                'vercel-v0': 'vercel-v0',
                'vercel-v0-enhanced': 'vercel-v0-enhanced',
                'filesystem': 'filesystem-http',
                'memory': 'memory-http',
                'sequential-thinking': 'sequential-thinking-http',
                'docker': 'docker-http',
                'figma-db': 'figma-db-http',
                'figma-mcp-application': 'figma-mcp-application',
                'figma-mcp-marketing': 'figma-mcp-marketing',
                'figma-mcp-ecommerce': 'figma-mcp-ecommerce',
                'ngrok': 'ngrok-http'
            }
            
            server_key = server_key_map.get(name, f"{name}-http")
            
            cmd = [
                '/home/gotime2022/mcp-kernel-new/scripts/mcp-manager.sh',
                'start',
                server_key
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully restarted {name}")
                server_info['restart_count'] += 1
                
                # Wait for server to start
                await asyncio.sleep(self.restart_delay)
                
                # Verify it's running
                if await self.check_server_health(name, server_info):
                    logger.info(f"Server {name} is healthy after restart")
                    return True
                else:
                    logger.warning(f"Server {name} still unhealthy after restart")
                    return False
            else:
                logger.error(f"Failed to restart {name}: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error restarting {name}: {e}")
            return False
    
    async def monitor_loop(self):
        """Main monitoring loop"""
        self.session = aiohttp.ClientSession()
        
        try:
            while self.running:
                for name, server_info in self.servers.items():
                    if name in self.failed_servers:
                        continue
                        
                    # Check health
                    is_healthy = await self.check_server_health(name, server_info)
                    
                    if not is_healthy:
                        logger.warning(f"Server {name} is unhealthy, attempting restart...")
                        await self.restart_server(name, server_info)
                    else:
                        if server_info['restart_count'] > 0:
                            logger.info(f"Server {name} recovered after {server_info['restart_count']} restarts")
                
                # Log status summary
                healthy_count = sum(1 for s in self.servers.values() if s['status'] == 'healthy')
                logger.info(f"Status: {healthy_count}/{len(self.servers)} servers healthy, {len(self.failed_servers)} failed")
                
                # Wait before next check
                await asyncio.sleep(self.health_check_interval)
                
        finally:
            await self.session.close()
    
    def stop(self):
        """Stop monitoring"""
        logger.info("Stopping connection monitor")
        self.running = False
    
    async def run(self):
        """Run the monitor"""
        if not await self.load_config():
            logger.error("Failed to load configuration")
            return
        
        logger.info("Starting MCP Connection Monitor")
        logger.info(f"Monitoring {len(self.servers)} servers")
        logger.info(f"Health check interval: {self.health_check_interval}s")
        
        # Set up signal handlers
        def signal_handler(sig, frame):
            logger.info(f"Received signal {sig}")
            self.stop()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Run monitoring loop
        await self.monitor_loop()


async def main():
    """Main entry point"""
    monitor = MCPConnectionMonitor()
    await monitor.run()


if __name__ == "__main__":
    asyncio.run(main())