#!/usr/bin/env python3
"""
Master Orchestration Script for All Figma MCP Servers
Starts all three specialized Figma MCP servers with comprehensive monitoring
"""

import os
import sys
import json
import time
import asyncio
import logging
import subprocess
import signal
from pathlib import Path
from typing import List, Dict, Any
import httpx

# Server configurations
SERVERS = {
    "marketing": {
        "name": "Figma Marketing MCP Server",
        "port": 8040,
        "directory": "figma-mcp-marketing",
        "script": "start_server.py",
        "health_endpoint": "/health",
        "specialization": "Marketing & Conversion Optimization"
    },
    "ecommerce": {
        "name": "Figma E-commerce MCP Server", 
        "port": 8041,
        "directory": "figma-mcp-ecommerce",
        "script": "start_server.py",
        "health_endpoint": "/health",
        "specialization": "E-commerce & Online Retail"
    },
    "application": {
        "name": "Figma Application UI MCP Server",
        "port": 8042,
        "directory": "figma-mcp-application", 
        "script": "start_server.py",
        "health_endpoint": "/health",
        "specialization": "Application UI & Dashboards"
    }
}

class FigmaMCPOrchestrator:
    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
        self.setup_logging()
        
    def setup_logging(self):
        """Configure orchestrator logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("figma_mcp_orchestrator.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger("FigmaMCPOrchestrator")

    def validate_environment(self) -> bool:
        """Validate required environment variables"""
        required_vars = [
            "SUPABASE_URL",
            "SUPABASE_SERVICE_KEY"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            self.logger.error(f"❌ Missing required environment variables: {missing_vars}")
            return False
            
        self.logger.info("✅ Environment validation passed")
        return True

    def check_port_availability(self, port: int) -> bool:
        """Check if a port is available"""
        import socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                return result != 0
        except Exception:
            return False

    def start_server(self, server_key: str, server_config: Dict[str, Any]) -> bool:
        """Start an individual server"""
        try:
            server_dir = Path(__file__).parent / server_config["directory"]
            
            if not server_dir.exists():
                self.logger.error(f"❌ Server directory not found: {server_dir}")
                return False
            
            # Check port availability
            if not self.check_port_availability(server_config["port"]):
                self.logger.warning(f"⚠️  Port {server_config['port']} already in use")
                return False
            
            # Start server process
            cmd = [sys.executable, server_config["script"]]
            process = subprocess.Popen(
                cmd,
                cwd=server_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes[server_key] = process
            self.logger.info(f"🚀 Started {server_config['name']} (PID: {process.pid})")
            return True
            
        except Exception as e:
            self.logger.error(f"💥 Failed to start {server_config['name']}: {e}")
            return False

    async def wait_for_health(self, server_key: str, server_config: Dict[str, Any], timeout: int = 30) -> bool:
        """Wait for server to become healthy"""
        url = f"http://localhost:{server_config['port']}{server_config['health_endpoint']}"
        
        for attempt in range(timeout):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, timeout=2.0)
                    if response.status_code == 200:
                        self.logger.info(f"✅ {server_config['name']} is healthy")
                        return True
            except Exception:
                pass
            
            await asyncio.sleep(1)
        
        self.logger.error(f"❌ {server_config['name']} failed health check")
        return False

    async def start_all_servers(self) -> bool:
        """Start all servers and wait for them to become healthy"""
        self.logger.info("🚀 Starting all Figma MCP servers...")
        
        # Start all servers
        started_servers = []
        for server_key, server_config in SERVERS.items():
            if self.start_server(server_key, server_config):
                started_servers.append(server_key)
                # Small delay between starts
                time.sleep(2)
        
        if not started_servers:
            self.logger.error("💥 No servers started successfully")
            return False
        
        # Wait for health checks
        self.logger.info("⏳ Waiting for servers to become healthy...")
        health_tasks = []
        for server_key in started_servers:
            task = self.wait_for_health(server_key, SERVERS[server_key])
            health_tasks.append(task)
        
        results = await asyncio.gather(*health_tasks, return_exceptions=True)
        healthy_count = sum(1 for result in results if result is True)
        
        if healthy_count == len(started_servers):
            self.logger.info(f"✅ All {healthy_count} servers are healthy and ready!")
            self.print_server_status()
            return True
        else:
            self.logger.error(f"❌ Only {healthy_count}/{len(started_servers)} servers are healthy")
            return False

    def print_server_status(self):
        """Print status of all servers"""
        print("\n" + "="*80)
        print("🎉 FIGMA MCP SERVERS SUCCESSFULLY STARTED")
        print("="*80)
        
        for server_key, server_config in SERVERS.items():
            if server_key in self.processes:
                print(f"""
📊 {server_config['name']}
   🌐 URL: http://localhost:{server_config['port']}
   🎯 Focus: {server_config['specialization']}
   🔄 PID: {self.processes[server_key].pid}
   ✅ Status: Running
""")
        
        print("="*80)
        print("🔗 Master Registry: http://localhost:8031/mcp/")
        print("📊 Monitoring: http://localhost:3000 (Grafana)")
        print("🎛️  Metrics: http://localhost:9090 (Prometheus)")
        print("⚡ Load Balancer: http://localhost:8080 (Traefik)")
        print("="*80)

    def stop_all_servers(self):
        """Stop all running servers"""
        self.logger.info("🛑 Stopping all servers...")
        
        for server_key, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=10)
                self.logger.info(f"✅ Stopped {SERVERS[server_key]['name']}")
            except subprocess.TimeoutExpired:
                process.kill()
                self.logger.warning(f"⚠️  Force killed {SERVERS[server_key]['name']}")
            except Exception as e:
                self.logger.error(f"❌ Error stopping {SERVERS[server_key]['name']}: {e}")

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"🛑 Received signal {signum}, shutting down...")
        self.stop_all_servers()
        sys.exit(0)

    async def monitor_servers(self):
        """Monitor server health and restart if needed"""
        self.logger.info("👁️  Starting server monitoring...")
        
        while True:
            try:
                for server_key, server_config in SERVERS.items():
                    if server_key in self.processes:
                        process = self.processes[server_key]
                        
                        # Check if process is still running
                        if process.poll() is not None:
                            self.logger.error(f"💥 {server_config['name']} crashed! Restarting...")
                            if self.start_server(server_key, server_config):
                                await self.wait_for_health(server_key, server_config)
                        
                        # Check health endpoint
                        else:
                            healthy = await self.wait_for_health(server_key, server_config, timeout=5)
                            if not healthy:
                                self.logger.warning(f"⚠️  {server_config['name']} failed health check")
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"❌ Monitoring error: {e}")
                await asyncio.sleep(60)

async def main():
    """Main orchestration function"""
    orchestrator = FigmaMCPOrchestrator()
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, orchestrator.signal_handler)
    signal.signal(signal.SIGTERM, orchestrator.signal_handler)
    
    try:
        # Validate environment
        if not orchestrator.validate_environment():
            sys.exit(1)
        
        # Start all servers
        if not await orchestrator.start_all_servers():
            sys.exit(1)
        
        # Start monitoring
        await orchestrator.monitor_servers()
        
    except KeyboardInterrupt:
        orchestrator.logger.info("🛑 Received keyboard interrupt")
    except Exception as e:
        orchestrator.logger.error(f"💥 Orchestrator error: {e}")
    finally:
        orchestrator.stop_all_servers()

if __name__ == "__main__":
    asyncio.run(main())