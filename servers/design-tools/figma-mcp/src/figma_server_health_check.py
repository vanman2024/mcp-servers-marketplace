#!/usr/bin/env python3
"""
Minimal health check server for CI/CD testing.
Provides basic MCP endpoints without database dependencies.
"""

import asyncio
import json
import os
import logging
from typing import Dict, Any
from fastmcp import FastMCP
from fastmcp.server import MCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("figma-health-check")

# Initialize MCP server
mcp_server = MCPServer(
    name="figma-db-http-health-check",
    version="1.0.0"
)
mcp = FastMCP(mcp_server)

# Basic health check tool
@mcp.tool(
    description="Check if Figma MCP server is running and healthy"
)
async def health_check() -> Dict[str, Any]:
    """Basic health check without database dependency"""
    return {
        "status": "healthy",
        "server": "figma-db-http",
        "version": "1.0.0",
        "database_connected": False,
        "mode": "health-check-only"
    }

# List categories without database
@mcp.tool(
    description="List available component categories"
)
async def list_component_categories() -> Dict[str, Any]:
    """Return mock categories for health check"""
    return {
        "categories": [
            {"name": "ui", "description": "UI Components (health check mode)"},
            {"name": "layout", "description": "Layout Components (health check mode)"},
            {"name": "forms", "description": "Form Components (health check mode)"}
        ],
        "mode": "health-check-only"
    }

if __name__ == "__main__":
    port = int(os.getenv("FIGMA_MCP_PORT", 8031))
    logger.info(f"Starting Figma MCP health check server on port {port}")
    logger.info("Running in health-check mode without database")
    
    try:
        mcp.run(port=port)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise