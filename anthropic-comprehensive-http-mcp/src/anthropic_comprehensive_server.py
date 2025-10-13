#!/usr/bin/env python3
"""
Anthropic Comprehensive MCP Server - HTTP Version
Provides essential Anthropic Claude API tools for chat, vision, computer use, and more
"""

import os
import logging
from typing import List, Dict, Any, Optional, AsyncIterator
import base64
import json
from datetime import datetime

from fastmcp import FastMCP
import anthropic
from anthropic import AsyncAnthropic
from anthropic.types import Message, ContentBlock, TextBlock, ToolUseBlock

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("anthropic-comprehensive")

# Initialize Anthropic client
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is required")

client = AsyncAnthropic(api_key=api_key)

# Core Chat Operations

@mcp.tool()
async def chat_completion(
    messages: List[Dict[str, str]],
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 4096,
    temperature: float = 0.7,
    system: Optional[str] = None,
    stop_sequences: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Generate a chat completion using Claude
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Claude model to use (claude-3-5-sonnet-20241022, claude-3-5-haiku-20241022)
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature (0-1)
        system: System prompt
        stop_sequences: List of sequences that will stop generation
    
    Returns:
        Generated response with usage information
    """
    try:
        # Convert messages to Anthropic format
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        kwargs = {
            "model": model,
            "messages": anthropic_messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        if system:
            kwargs["system"] = system
        if stop_sequences:
            kwargs["stop_sequences"] = stop_sequences
        
        response = await client.messages.create(**kwargs)
        
        # Extract text content
        content = ""
        for block in response.content:
            if isinstance(block, TextBlock):
                content += block.text
        
        return {
            "success": True,
            "content": content,
            "model": response.model,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens
            },
            "stop_reason": response.stop_reason
        }
    except Exception as e:
        logger.error(f"Failed to generate chat completion: {e}")
        raise ValueError(f"Failed to generate chat completion: {str(e)}")

@mcp.tool()
async def streaming_chat(
    messages: List[Dict[str, str]],
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 4096,
    temperature: float = 0.7,
    system: Optional[str] = None
) -> AsyncIterator[Dict[str, Any]]:
    """
    Generate a streaming chat completion using Claude
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Claude model to use
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature (0-1)
        system: System prompt
    
    Yields:
        Streaming response chunks
    """
    try:
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        kwargs = {
            "model": model,
            "messages": anthropic_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True
        }
        
        if system:
            kwargs["system"] = system
        
        async with client.messages.stream(**kwargs) as stream:
            async for event in stream:
                if hasattr(event, 'type'):
                    yield {
                        "type": event.type,
                        "data": event.model_dump() if hasattr(event, 'model_dump') else str(event)
                    }
    except Exception as e:
        logger.error(f"Failed to stream chat completion: {e}")
        yield {"error": str(e)}

# Token Management

@mcp.tool()
async def count_tokens(
    text: str,
    model: str = "claude-3-5-sonnet-20241022"
) -> Dict[str, Any]:
    """
    Count tokens in text for a specific Claude model
    
    Args:
        text: Text to count tokens for
        model: Claude model to use for tokenization
    
    Returns:
        Token count information
    """
    try:
        # Use the client's token counting method
        token_count = await client.count_tokens(text)
        
        return {
            "success": True,
            "token_count": token_count,
            "model": model,
            "text_length": len(text)
        }
    except Exception as e:
        # Fallback to estimation if direct counting fails
        # Claude's tokenizer roughly follows: ~4 chars per token
        estimated_tokens = len(text) // 4
        
        return {
            "success": True,
            "token_count": estimated_tokens,
            "model": model,
            "text_length": len(text),
            "is_estimate": True
        }

# Vision and Multimodal

@mcp.tool()
async def analyze_image(
    image_base64: str,
    prompt: str,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 1024
) -> Dict[str, Any]:
    """
    Analyze an image using Claude's vision capabilities
    
    Args:
        image_base64: Base64 encoded image
        prompt: Question or instruction about the image
        model: Claude model to use (must support vision)
        max_tokens: Maximum tokens to generate
    
    Returns:
        Analysis results
    """
    try:
        # Detect image format from base64 header if present
        if image_base64.startswith('data:image/'):
            media_type = image_base64.split(';')[0].split(':')[1]
            image_base64 = image_base64.split(',')[1]
        else:
            # Default to JPEG if not specified
            media_type = "image/jpeg"
        
        response = await client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }]
        )
        
        content = ""
        for block in response.content:
            if isinstance(block, TextBlock):
                content += block.text
        
        return {
            "success": True,
            "analysis": content,
            "model": response.model,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        }
    except Exception as e:
        logger.error(f"Failed to analyze image: {e}")
        raise ValueError(f"Failed to analyze image: {str(e)}")

# Computer Use (Beta)

@mcp.tool()
async def computer_use(
    instruction: str,
    screenshot_base64: Optional[str] = None,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 4096
) -> Dict[str, Any]:
    """
    Use Claude's computer use capability to interact with desktop applications
    
    Args:
        instruction: What action to perform
        screenshot_base64: Optional screenshot of current screen state
        model: Claude model to use (must support computer use)
        max_tokens: Maximum tokens to generate
    
    Returns:
        Computer use action instructions
    """
    try:
        messages = []
        content = [{"type": "text", "text": instruction}]
        
        if screenshot_base64:
            # Add screenshot for context
            if screenshot_base64.startswith('data:image/'):
                media_type = screenshot_base64.split(';')[0].split(':')[1]
                screenshot_base64 = screenshot_base64.split(',')[1]
            else:
                media_type = "image/png"
            
            content.insert(0, {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": screenshot_base64
                }
            })
        
        messages.append({
            "role": "user",
            "content": content
        })
        
        # Enable computer use tools
        response = await client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages,
            tools=[
                {
                    "type": "computer_20241022",
                    "name": "computer",
                    "description": "Control computer interactions",
                    "display_width_px": 1920,
                    "display_height_px": 1080
                }
            ],
            tool_choice={"type": "auto"}
        )
        
        # Extract actions and text
        actions = []
        text_content = ""
        
        for block in response.content:
            if isinstance(block, TextBlock):
                text_content += block.text
            elif isinstance(block, ToolUseBlock):
                actions.append({
                    "tool": block.name,
                    "input": block.input
                })
        
        return {
            "success": True,
            "actions": actions,
            "explanation": text_content,
            "model": response.model,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        }
    except Exception as e:
        logger.error(f"Failed to use computer capability: {e}")
        raise ValueError(f"Failed to use computer capability: {str(e)}")

# Function Calling

@mcp.tool()
async def function_calling(
    messages: List[Dict[str, str]],
    tools: List[Dict[str, Any]],
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 4096,
    tool_choice: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Use Claude's function calling capability for structured outputs
    
    Args:
        messages: Conversation messages
        tools: List of tool definitions with name, description, and parameters
        model: Claude model to use
        max_tokens: Maximum tokens to generate
        tool_choice: Force specific tool use (auto, any, or specific tool)
    
    Returns:
        Function call results and explanations
    """
    try:
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        kwargs = {
            "model": model,
            "messages": anthropic_messages,
            "max_tokens": max_tokens,
            "tools": tools
        }
        
        if tool_choice:
            kwargs["tool_choice"] = tool_choice
        else:
            kwargs["tool_choice"] = {"type": "auto"}
        
        response = await client.messages.create(**kwargs)
        
        # Extract function calls and text
        function_calls = []
        text_content = ""
        
        for block in response.content:
            if isinstance(block, TextBlock):
                text_content += block.text
            elif isinstance(block, ToolUseBlock):
                function_calls.append({
                    "id": block.id,
                    "name": block.name,
                    "arguments": block.input
                })
        
        return {
            "success": True,
            "function_calls": function_calls,
            "content": text_content,
            "model": response.model,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        }
    except Exception as e:
        logger.error(f"Failed to perform function calling: {e}")
        raise ValueError(f"Failed to perform function calling: {str(e)}")

# Batch Processing

@mcp.tool()
async def batch_messages(
    batch_requests: List[Dict[str, Any]],
    model: str = "claude-3-5-sonnet-20241022"
) -> Dict[str, Any]:
    """
    Process multiple message requests in batch for efficiency
    
    Args:
        batch_requests: List of request dicts, each with messages and optional params
        model: Default model to use for all requests
    
    Returns:
        Batch processing results
    """
    try:
        results = []
        total_input_tokens = 0
        total_output_tokens = 0
        
        for i, request in enumerate(batch_requests):
            try:
                # Extract parameters for this request
                messages = request.get("messages", [])
                req_model = request.get("model", model)
                max_tokens = request.get("max_tokens", 1024)
                temperature = request.get("temperature", 0.7)
                system = request.get("system")
                
                # Make the request
                kwargs = {
                    "model": req_model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
                
                if system:
                    kwargs["system"] = system
                
                response = await client.messages.create(**kwargs)
                
                # Extract content
                content = ""
                for block in response.content:
                    if isinstance(block, TextBlock):
                        content += block.text
                
                results.append({
                    "index": i,
                    "success": True,
                    "content": content,
                    "usage": {
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens
                    }
                })
                
                total_input_tokens += response.usage.input_tokens
                total_output_tokens += response.usage.output_tokens
                
            except Exception as e:
                results.append({
                    "index": i,
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "success": True,
            "results": results,
            "total_usage": {
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "total_tokens": total_input_tokens + total_output_tokens
            },
            "batch_size": len(batch_requests)
        }
    except Exception as e:
        logger.error(f"Failed to process batch: {e}")
        raise ValueError(f"Failed to process batch: {str(e)}")

# Context Management

@mcp.tool()
async def create_cached_context(
    context: str,
    context_id: str,
    model: str = "claude-3-5-sonnet-20241022"
) -> Dict[str, Any]:
    """
    Create a cached context for efficient reuse in conversations
    
    Args:
        context: The context to cache (system prompts, docs, etc)
        context_id: Unique ID for this context
        model: Model to optimize caching for
    
    Returns:
        Caching confirmation and token information
    """
    try:
        # Note: Anthropic doesn't have direct context caching API yet
        # This is a placeholder for future functionality
        # For now, we'll return token count and store guidance
        
        token_count = len(context) // 4  # Rough estimation
        
        return {
            "success": True,
            "context_id": context_id,
            "token_count": token_count,
            "model": model,
            "recommendation": "Store this context client-side and prepend to messages for efficiency",
            "cache_strategy": {
                "method": "client_side",
                "max_size_tokens": 100000,
                "ttl_minutes": 60
            }
        }
    except Exception as e:
        logger.error(f"Failed to create cached context: {e}")
        raise ValueError(f"Failed to create cached context: {str(e)}")

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv('ANTHROPIC_COMPREHENSIVE_MCP_PORT', '8026'))
    
    logger.info(f"Starting Anthropic Comprehensive MCP Server on port {port}")
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")