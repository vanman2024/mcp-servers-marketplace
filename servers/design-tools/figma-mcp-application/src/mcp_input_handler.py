"""
MCP Input Handler - Fixes the JSON string input issue with FastMCP
"""
import json
from typing import Any, Dict, Union, Type
from pydantic import BaseModel
import functools

def handle_mcp_input(model_class: Type[BaseModel]):
    """
    Decorator to handle MCP protocol's JSON string inputs.
    Converts JSON strings to proper Pydantic models.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(input: Union[str, Dict[str, Any], BaseModel]) -> Dict[str, Any]:
            # Handle different input types
            if isinstance(input, str):
                # Parse JSON string
                try:
                    input_dict = json.loads(input)
                    input_obj = model_class(**input_dict)
                except json.JSONDecodeError:
                    # Try direct model validation for JSON strings
                    input_obj = model_class.model_validate_json(input)
            elif isinstance(input, dict):
                # Create model from dictionary
                input_obj = model_class(**input)
            elif isinstance(input, model_class):
                # Already the correct type
                input_obj = input
            else:
                # Fallback to model validation
                input_obj = model_class.model_validate(input)
            
            # Call the original function with the validated model
            return await func(input_obj)
        
        return wrapper
    return decorator