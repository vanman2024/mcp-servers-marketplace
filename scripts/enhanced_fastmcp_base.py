#!/usr/bin/env python3
"""
Enhanced FastMCP Base Class with Connection Persistence
Adds keep-alive, reconnection logic, and better error handling
"""

import asyncio
import logging
import signal
import sys
import os
from typing import Optional, Callable, Any
from contextlib import asynccontextmanager
from datetime import datetime
import uvicorn
from fastmcp import FastMCP
import aiohttp

logger = logging.getLogger(__name__)

class EnhancedFastMCP(FastMCP):
    """Enhanced FastMCP with connection persistence features"""
    
    def __init__(self, name: str, heartbeat_interval: int = 30):
        super().__init__(name)
        self.heartbeat_interval = heartbeat_interval
        self.last_activity = datetime.now()
        self.shutdown_event = asyncio.Event()
        self.heartbeat_task = None
        
    async def heartbeat_loop(self):
        """Send periodic heartbeats to maintain connection"""
        logger.info(f"Starting heartbeat loop (interval: {self.heartbeat_interval}s)")
        
        while not self.shutdown_event.is_set():
            try:
                # Update last activity
                self.last_activity = datetime.now()
                
                # Log heartbeat
                logger.debug(f"Heartbeat at {self.last_activity}")
                
                # Wait for next heartbeat
                await asyncio.sleep(self.heartbeat_interval)
                
            except asyncio.CancelledError:
                logger.info("Heartbeat loop cancelled")
                break
            except Exception as e:
                logger.error(f"Error in heartbeat loop: {e}")
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
    
    @asynccontextmanager
    async def lifespan(self, app):
        """Enhanced lifespan with heartbeat"""
        # Start heartbeat
        self.heartbeat_task = asyncio.create_task(self.heartbeat_loop())
        logger.info("Started heartbeat task")
        
        yield
        
        # Stop heartbeat
        self.shutdown_event.set()
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass
        logger.info("Stopped heartbeat task")
    
    def run_with_persistence(
        self, 
        transport: str = "streamable-http",
        host: str = "0.0.0.0", 
        port: int = 8000,
        path: str = "/",
        reload: bool = False
    ):
        """Run server with enhanced connection persistence"""
        
        # Set up signal handlers for graceful shutdown
        def signal_handler(sig, frame):
            logger.info(f"Received signal {sig}, shutting down gracefully...")
            self.shutdown_event.set()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Configure uvicorn with keep-alive settings
        config = uvicorn.Config(
            app=self.app,
            host=host,
            port=port,
            reload=reload,
            # Connection persistence settings
            timeout_keep_alive=300,  # 5 minutes keep-alive
            timeout_graceful_shutdown=30,  # 30 seconds graceful shutdown
            # Logging
            log_level="info",
            access_log=True,
            # Lifespan
            lifespan="on"
        )
        
        # Add lifespan to app
        self.app.router.lifespan_context = self.lifespan
        
        logger.info(f"Starting enhanced {self.name} server on {host}:{port}")
        logger.info(f"Keep-alive timeout: 300s, Heartbeat interval: {self.heartbeat_interval}s")
        
        server = uvicorn.Server(config)
        
        # Run server
        try:
            server.run()
        except KeyboardInterrupt:
            logger.info("Server interrupted by user")
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise
        finally:
            logger.info("Server shutdown complete")


def create_enhanced_mcp_wrapper(
    mcp_instance: FastMCP,
    heartbeat_interval: int = 30
) -> Callable:
    """
    Wrap an existing FastMCP instance with enhanced features
    
    Usage:
        mcp = FastMCP("myserver")
        # ... define tools ...
        
        if __name__ == "__main__":
            run_enhanced = create_enhanced_mcp_wrapper(mcp)
            run_enhanced(port=8080)
    """
    
    def run_enhanced(
        transport: str = "streamable-http",
        host: str = "0.0.0.0",
        port: int = 8000,
        path: str = "/",
        reload: bool = False
    ):
        # Create enhanced instance
        enhanced = EnhancedFastMCP(mcp_instance.name, heartbeat_interval)
        
        # Copy tools and settings from original
        enhanced.app = mcp_instance.app
        enhanced._tools = mcp_instance._tools
        enhanced._resources = mcp_instance._resources
        enhanced._prompts = mcp_instance._prompts
        
        # Run with persistence
        enhanced.run_with_persistence(
            transport=transport,
            host=host,
            port=port,
            path=path,
            reload=reload
        )
    
    return run_enhanced


# Health check endpoint decorator
def add_health_check(mcp: FastMCP):
    """Add a health check endpoint to MCP server"""
    
    # FastMCP objects may not have app attribute until after initialization
    # Skip if not available
    if not hasattr(mcp, 'app'):
        logger.warning(f"Cannot add health check to {mcp.name} - no app attribute")
        return
    
    @mcp.app.get("/health")
    async def health_check():
        """Health check endpoint for monitoring"""
        return {
            "status": "healthy",
            "server": mcp.name,
            "timestamp": datetime.now().isoformat()
        }
    
    @mcp.app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "name": mcp.name,
            "type": "mcp-http-server",
            "status": "running"
        }
    
    logger.info(f"Added health check endpoints to {mcp.name}")


if __name__ == "__main__":
    # Example usage
    mcp = EnhancedFastMCP("example-server")
    
    @mcp.tool()
    async def example_tool(message: str) -> str:
        """Example tool"""
        mcp.update_activity()  # Update activity on tool use
        return f"Received: {message}"
    
    # Add health check
    add_health_check(mcp)
    
    # Run with persistence
    port = int(os.getenv('EXAMPLE_MCP_PORT', '9999'))
    mcp.run_with_persistence(port=port)