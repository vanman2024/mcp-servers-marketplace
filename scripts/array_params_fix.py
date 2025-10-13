#!/usr/bin/env python3
"""
Fix for array/object parameters in MCP HTTP transport layer.

This module provides a middleware solution that intercepts and fixes
array/object parameters that are incorrectly passed as JSON strings
instead of proper Python types.
"""

import json
import logging
from typing import Any, Dict, List, Union

logger = logging.getLogger(__name__)


def fix_json_params(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fix JSON string parameters by converting them to proper Python types.
    
    This function handles cases where arrays and objects are passed as JSON
    strings instead of proper Python lists/dicts.
    
    Args:
        arguments: Dictionary of arguments to fix
        
    Returns:
        Fixed arguments dictionary
    """
    fixed_args = {}
    
    for key, value in arguments.items():
        if isinstance(value, str):
            # Try to parse as JSON if it looks like JSON
            if (value.startswith('[') and value.endswith(']')) or \
               (value.startswith('{') and value.endswith('}')):
                try:
                    parsed_value = json.loads(value)
                    fixed_args[key] = parsed_value
                    logger.debug(f"Parsed JSON parameter '{key}': {type(value).__name__} -> {type(parsed_value).__name__}")
                except json.JSONDecodeError:
                    # Not valid JSON, keep as string
                    fixed_args[key] = value
            else:
                fixed_args[key] = value
        else:
            fixed_args[key] = value
    
    return fixed_args


def patch_fastmcp_tool_run():
    """
    Monkey patch FastMCP's FunctionTool.run method to fix array parameters.
    
    This is a temporary fix until the issue is resolved in FastMCP itself.
    """
    try:
        from fastmcp.tools.tool import FunctionTool
        original_run = FunctionTool.run
        
        async def patched_run(self, arguments: dict[str, Any]) -> list:
            # Fix JSON parameters before processing
            fixed_arguments = fix_json_params(arguments)
            logger.debug(f"Fixed arguments for tool '{self.name}': {arguments} -> {fixed_arguments}")
            
            # Call original run method with fixed arguments
            return await original_run(self, fixed_arguments)
        
        # Apply the patch
        FunctionTool.run = patched_run
        logger.info("Successfully patched FastMCP FunctionTool.run to fix array parameters")
        
    except ImportError as e:
        logger.error(f"Failed to import FastMCP for patching: {e}")
    except Exception as e:
        logger.error(f"Failed to patch FastMCP: {e}")


def create_array_fix_middleware():
    """
    Create a middleware function that fixes array parameters.
    
    This can be used with FastMCP's middleware system.
    """
    from typing import Callable, Awaitable
    
    async def array_fix_middleware(context: Any, call_next: Callable[[Any], Awaitable[Any]]) -> Any:
        """Middleware that fixes array/object parameters passed as JSON strings."""
        
        # Check if this is a tool call
        if hasattr(context, 'message') and hasattr(context.message, 'arguments'):
            # Fix the arguments
            original_args = context.message.arguments or {}
            fixed_args = fix_json_params(original_args)
            
            # Update the context with fixed arguments
            context.message.arguments = fixed_args
            
            logger.debug(f"Middleware fixed arguments: {original_args} -> {fixed_args}")
        
        # Continue with the request
        return await call_next(context)
    
    return array_fix_middleware


# Utility function to be imported by servers
def apply_array_params_fix():
    """
    Apply the array parameters fix.
    
    Call this function at the start of your MCP server to fix the issue.
    """
    # Apply the monkey patch
    patch_fastmcp_tool_run()
    
    # Log that the fix has been applied
    logger.info("Array parameters fix has been applied")


# Auto-apply the fix when imported
if __name__ != "__main__":
    apply_array_params_fix()