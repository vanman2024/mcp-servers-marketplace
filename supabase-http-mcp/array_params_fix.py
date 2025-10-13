"""
Array parameters fix for FastMCP to handle JSON strings as lists
"""

import json
import logging
from typing import Any, Dict
from pydantic import BaseModel, Field, validator
import pydantic_core

logger = logging.getLogger(__name__)

original_validate_python = None

def patched_validate_python(self, obj, *, strict=None, from_attributes=None, context=None):
    """Patched validate_python that converts JSON strings to lists when needed"""
    # If obj is a dict and we're validating a list type, check for JSON strings
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and value.strip().startswith('['):
                try:
                    # Try to parse as JSON array
                    parsed = json.loads(value)
                    if isinstance(parsed, list):
                        obj[key] = parsed
                        logger.debug(f"Converted JSON string to list for key '{key}': {value} -> {parsed}")
                except json.JSONDecodeError:
                    # Not valid JSON, leave as string
                    pass
    
    # Call original method
    return original_validate_python(self, obj, strict=strict, from_attributes=from_attributes, context=context)

def apply_array_params_fix():
    """Apply the array parameters fix to pydantic TypeAdapter"""
    global original_validate_python
    
    try:
        from pydantic import TypeAdapter
        
        # Store original method
        original_validate_python = TypeAdapter.validate_python
        
        # Replace with patched version
        TypeAdapter.validate_python = patched_validate_python
        
        logger.info("Array parameters fix applied successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to apply array parameters fix: {e}")
        return False