"""
Miro HTTP MCP Server Package

This package provides comprehensive Miro board management capabilities
through the Model Context Protocol (MCP) framework.
"""

__version__ = "1.0.0"
__author__ = "MCP Development Team"

# Export main components
try:
    from .miro_server import MiroClient, MiroBoardTools, MiroWorkflowTools
    __all__ = ['MiroClient', 'MiroBoardTools', 'MiroWorkflowTools']
except ImportError:
    # Fallback for old structure
    from .miro_mcp_server import server
    __all__ = ["server"]