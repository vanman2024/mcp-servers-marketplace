"""
Digital Ocean HTTP MCP Server

A comprehensive MCP server for managing Digital Ocean cloud infrastructure.
"""

from .digitalocean_server import mcp, DigitalOceanClient

__version__ = "1.0.0"
__all__ = ["mcp", "DigitalOceanClient"]