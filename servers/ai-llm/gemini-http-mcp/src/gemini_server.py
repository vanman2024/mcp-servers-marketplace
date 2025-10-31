#!/usr/bin/env python3
"""
Gemini MCP Server - HTTP Implementation
Google Gemini AI for text generation, vision, code analysis, and structured outputs

Focus on useful Gemini capabilities that complement other MCP servers
"""

import os
import base64
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import json
import asyncio
from pathlib import Path

# Google Gemini client
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# FastMCP for HTTP serving
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for Google Gemini AI operations"""
    
    def __init__(self, api_key: str):
        """Initialize Gemini client"""
        genai.configure(api_key=api_key)
        self.api_key = api_key
        logger.info("Gemini client initialized")
    
    def _get_model(self, model_name: str):
        """Get Gemini model instance"""
        return genai.GenerativeModel(model_name)
    
    def _prepare_safety_settings(self, safety_level: str = "moderate"):
        """Prepare safety settings based on level"""
        if safety_level == "strict":
            return {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            }
        elif safety_level == "moderate":
            return {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
        else:  # permissive
            return {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            }


# Initialize FastMCP server
mcp = FastMCP("gemini")

# Get API key from environment
gemini_api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
if not gemini_api_key:
    raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY environment variable required")

# Initialize Gemini client
gemini_client = GeminiClient(gemini_api_key)

# Text Generation Tools

@mcp.tool()
async def generate_text(
    prompt: str,
    model: Optional[str] = "gemini-2.0-flash",
    temperature: Optional[float] = 0.7,
    max_output_tokens: Optional[int] = 2048,
    safety_level: Optional[str] = "moderate"
) -> Dict[str, Any]:
    """
    Generate text using Gemini models
    
    Args:
        prompt: Text prompt for generation
        model: Gemini model (gemini-2.0-flash, gemini-1.5-pro, gemini-1.5-flash)
        temperature: Creativity level (0.0-2.0)
        max_output_tokens: Maximum tokens to generate
        safety_level: Safety filtering (strict, moderate, permissive)
    
    Returns:
        Generated text and metadata
    """
    try:
        # Configure generation parameters
        generation_config = genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )
        
        # Get safety settings
        safety_settings = gemini_client._prepare_safety_settings(safety_level)
        
        # Get model and generate
        model_instance = gemini_client._get_model(model)
        response = model_instance.generate_content(
            prompt,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        return {
            "success": True,
            "model": model,
            "prompt": prompt[:200] + "..." if len(prompt) > 200 else prompt,
            "generated_text": response.text,
            "finish_reason": response.candidates[0].finish_reason.name if response.candidates else None,
            "safety_ratings": [
                {
                    "category": rating.category.name,
                    "probability": rating.probability.name
                }
                for rating in response.candidates[0].safety_ratings
            ] if response.candidates else [],
            "usage": {
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
                "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else None,
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else None
            }
        }
    except Exception as e:
        logger.error(f"Text generation failed: {e}")
        raise ValueError(f"Text generation failed: {str(e)}")

@mcp.tool()
async def analyze_code(
    code: str,
    language: Optional[str] = None,
    analysis_type: Optional[str] = "comprehensive",
    model: Optional[str] = "gemini-1.5-flash"
) -> Dict[str, Any]:
    """
    Analyze code for bugs, improvements, and explanations
    
    Args:
        code: Code to analyze
        language: Programming language (auto-detected if not provided)
        analysis_type: Type of analysis (comprehensive, bugs, performance, security, explain)
        model: Gemini model to use
    
    Returns:
        Code analysis results
    """
    try:
        # Build analysis prompt based on type
        if analysis_type == "bugs":
            analysis_prompt = "Analyze this code for potential bugs, errors, and issues. Provide specific fixes."
        elif analysis_type == "performance":
            analysis_prompt = "Analyze this code for performance issues and optimization opportunities."
        elif analysis_type == "security":
            analysis_prompt = "Analyze this code for security vulnerabilities and best practices."
        elif analysis_type == "explain":
            analysis_prompt = "Explain what this code does, how it works, and document each major section."
        else:  # comprehensive
            analysis_prompt = "Provide a comprehensive analysis of this code including: bugs, performance, security, readability, and suggestions for improvement."
        
        language_hint = f"\n\nThis appears to be {language} code." if language else ""
        
        full_prompt = f"""{analysis_prompt}{language_hint}

```
{code}
```

Please provide your analysis in a structured format with clear sections and actionable recommendations."""

        # Generate analysis
        model_instance = gemini_client._get_model(model)
        response = model_instance.generate_content(full_prompt)
        
        return {
            "success": True,
            "model": model,
            "language": language,
            "analysis_type": analysis_type,
            "code_preview": code[:300] + "..." if len(code) > 300 else code,
            "analysis": response.text,
            "usage": {
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
                "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else None,
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else None
            }
        }
    except Exception as e:
        logger.error(f"Code analysis failed: {e}")
        raise ValueError(f"Code analysis failed: {str(e)}")

# Vision and Multimodal Tools

@mcp.tool()
async def analyze_image(
    image_path: str,
    prompt: str,
    model: Optional[str] = "gemini-1.5-flash"
) -> Dict[str, Any]:
    """
    Analyze an image with a text prompt using Gemini Vision
    
    Args:
        image_path: Path to the image file
        prompt: Text prompt describing what to analyze
        model: Gemini model with vision capabilities
    
    Returns:
        Image analysis results
    """
    try:
        from PIL import Image
        
        # Load and prepare image
        image = Image.open(image_path)
        
        # Get model and analyze
        model_instance = gemini_client._get_model(model)
        response = model_instance.generate_content([prompt, image])
        
        return {
            "success": True,
            "model": model,
            "image_path": image_path,
            "prompt": prompt,
            "analysis": response.text,
            "image_info": {
                "size": image.size,
                "format": image.format,
                "mode": image.mode
            },
            "usage": {
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
                "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else None,
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else None
            }
        }
    except FileNotFoundError:
        raise ValueError(f"Image file not found: {image_path}")
    except Exception as e:
        logger.error(f"Image analysis failed: {e}")
        raise ValueError(f"Image analysis failed: {str(e)}")

@mcp.tool()
async def compare_images(
    image1_path: str,
    image2_path: str,
    comparison_prompt: Optional[str] = "Compare these two images and describe the differences and similarities.",
    model: Optional[str] = "gemini-1.5-flash"
) -> Dict[str, Any]:
    """
    Compare two images using Gemini Vision
    
    Args:
        image1_path: Path to the first image
        image2_path: Path to the second image
        comparison_prompt: Prompt describing how to compare
        model: Gemini model with vision capabilities
    
    Returns:
        Image comparison results
    """
    try:
        from PIL import Image
        
        # Load both images
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        
        # Get model and compare
        model_instance = gemini_client._get_model(model)
        response = model_instance.generate_content([
            comparison_prompt,
            "Image 1:", image1,
            "Image 2:", image2
        ])
        
        return {
            "success": True,
            "model": model,
            "image1_path": image1_path,
            "image2_path": image2_path,
            "comparison_prompt": comparison_prompt,
            "comparison": response.text,
            "image1_info": {
                "size": image1.size,
                "format": image1.format
            },
            "image2_info": {
                "size": image2.size,
                "format": image2.format
            },
            "usage": {
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
                "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else None,
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else None
            }
        }
    except FileNotFoundError as e:
        raise ValueError(f"Image file not found: {str(e)}")
    except Exception as e:
        logger.error(f"Image comparison failed: {e}")
        raise ValueError(f"Image comparison failed: {str(e)}")

# Structured Output Tools

@mcp.tool()
async def generate_json(
    prompt: str,
    schema: Dict[str, Any],
    model: Optional[str] = "gemini-1.5-flash"
) -> Dict[str, Any]:
    """
    Generate structured JSON output based on a schema
    
    Args:
        prompt: Prompt describing what data to generate
        schema: JSON schema defining the expected structure
        model: Gemini model to use
    
    Returns:
        Generated JSON data matching the schema
    """
    try:
        # Build structured prompt
        schema_str = json.dumps(schema, indent=2)
        structured_prompt = f"""{prompt}

Please respond with valid JSON that matches this exact schema:

{schema_str}

Respond ONLY with the JSON object, no additional text or formatting."""

        # Generate response
        model_instance = gemini_client._get_model(model)
        response = model_instance.generate_content(structured_prompt)
        
        # Parse JSON response
        try:
            generated_json = json.loads(response.text.strip())
        except json.JSONDecodeError:
            # Try to extract JSON from response
            text = response.text.strip()
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                generated_json = json.loads(text[start:end])
            else:
                raise ValueError("Response was not valid JSON")
        
        return {
            "success": True,
            "model": model,
            "prompt": prompt[:200] + "..." if len(prompt) > 200 else prompt,
            "schema": schema,
            "generated_json": generated_json,
            "raw_response": response.text,
            "usage": {
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
                "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else None,
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else None
            }
        }
    except Exception as e:
        logger.error(f"JSON generation failed: {e}")
        raise ValueError(f"JSON generation failed: {str(e)}")

@mcp.tool()
async def extract_entities(
    text: str,
    entity_types: List[str],
    model: Optional[str] = "gemini-1.5-flash"
) -> Dict[str, Any]:
    """
    Extract named entities from text
    
    Args:
        text: Text to extract entities from
        entity_types: Types of entities to extract (person, organization, location, date, etc.)
        model: Gemini model to use
    
    Returns:
        Extracted entities organized by type
    """
    try:
        entity_list = ", ".join(entity_types)
        prompt = f"""Extract the following types of entities from this text: {entity_list}

Text:
{text}

Please respond with a JSON object where each key is an entity type and the value is an array of entities found:

{{
  "person": ["John Smith", "Jane Doe"],
  "organization": ["Acme Corp"],
  "location": ["New York"],
  "date": ["2024-01-15"]
}}

Respond ONLY with the JSON object."""

        # Generate response
        model_instance = gemini_client._get_model(model)
        response = model_instance.generate_content(prompt)
        
        # Parse JSON response
        try:
            entities = json.loads(response.text.strip())
        except json.JSONDecodeError:
            # Try to extract JSON from response
            text_resp = response.text.strip()
            start = text_resp.find('{')
            end = text_resp.rfind('}') + 1
            if start != -1 and end > start:
                entities = json.loads(text_resp[start:end])
            else:
                raise ValueError("Response was not valid JSON")
        
        return {
            "success": True,
            "model": model,
            "text_preview": text[:300] + "..." if len(text) > 300 else text,
            "entity_types_requested": entity_types,
            "entities": entities,
            "total_entities": sum(len(ents) for ents in entities.values()),
            "usage": {
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
                "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else None,
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else None
            }
        }
    except Exception as e:
        logger.error(f"Entity extraction failed: {e}")
        raise ValueError(f"Entity extraction failed: {str(e)}")

# Conversation and Chat Tools

@mcp.tool()
async def chat_conversation(
    messages: List[Dict[str, str]],
    model: Optional[str] = "gemini-2.0-flash",
    temperature: Optional[float] = 0.7
) -> Dict[str, Any]:
    """
    Have a multi-turn conversation with Gemini
    
    Args:
        messages: List of messages with 'role' (user/assistant) and 'content'
        model: Gemini model to use
        temperature: Response creativity level
    
    Returns:
        Conversation response
    """
    try:
        # Configure generation
        generation_config = genai.GenerationConfig(temperature=temperature)
        
        # Get model and start chat
        model_instance = gemini_client._get_model(model)
        
        # Convert messages to Gemini format
        history = []
        current_message = None
        
        for msg in messages:
            if msg['role'] == 'user':
                if current_message:
                    history.append(current_message)
                current_message = {'role': 'user', 'parts': [msg['content']]}
            elif msg['role'] == 'assistant':
                history.append({'role': 'model', 'parts': [msg['content']]})
        
        # Start chat with history
        chat = model_instance.start_chat(history=history[:-1] if history else [])
        
        # Send the last user message
        if current_message:
            response = chat.send_message(
                current_message['parts'][0],
                generation_config=generation_config
            )
        else:
            raise ValueError("No user message found in conversation")
        
        return {
            "success": True,
            "model": model,
            "conversation_length": len(messages),
            "response": response.text,
            "usage": {
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
                "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else None,
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else None
            }
        }
    except Exception as e:
        logger.error(f"Chat conversation failed: {e}")
        raise ValueError(f"Chat conversation failed: {str(e)}")

# Content Analysis Tools

@mcp.tool()
async def summarize_text(
    text: str,
    length: Optional[str] = "medium",
    focus: Optional[str] = "main_points",
    model: Optional[str] = "gemini-1.5-flash"
) -> Dict[str, Any]:
    """
    Summarize long text content
    
    Args:
        text: Text to summarize
        length: Summary length (brief, medium, detailed)
        focus: What to focus on (main_points, key_facts, actionable_items, conclusions)
        model: Gemini model to use
    
    Returns:
        Text summary
    """
    try:
        # Build summary prompt
        length_instructions = {
            "brief": "in 2-3 sentences",
            "medium": "in 1-2 paragraphs", 
            "detailed": "in 3-5 paragraphs with key details"
        }
        
        focus_instructions = {
            "main_points": "focusing on the main points and key themes",
            "key_facts": "focusing on important facts and data",
            "actionable_items": "focusing on actionable items and next steps",
            "conclusions": "focusing on conclusions and outcomes"
        }
        
        length_instruction = length_instructions.get(length, "in 1-2 paragraphs")
        focus_instruction = focus_instructions.get(focus, "focusing on the main points")
        
        prompt = f"""Please summarize the following text {length_instruction}, {focus_instruction}:

{text}

Summary:"""

        # Generate summary
        model_instance = gemini_client._get_model(model)
        response = model_instance.generate_content(prompt)
        
        return {
            "success": True,
            "model": model,
            "original_length": len(text),
            "length_setting": length,
            "focus_setting": focus,
            "summary": response.text,
            "compression_ratio": round(len(response.text) / len(text), 2),
            "usage": {
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
                "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else None,
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else None
            }
        }
    except Exception as e:
        logger.error(f"Text summarization failed: {e}")
        raise ValueError(f"Text summarization failed: {str(e)}")

@mcp.tool()
async def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = "auto",
    model: Optional[str] = "gemini-1.5-flash"
) -> Dict[str, Any]:
    """
    Translate text between languages
    
    Args:
        text: Text to translate
        target_language: Target language (e.g., 'Spanish', 'French', 'Japanese')
        source_language: Source language ('auto' for auto-detection)
        model: Gemini model to use
    
    Returns:
        Translated text
    """
    try:
        if source_language == "auto":
            prompt = f"Translate the following text to {target_language}:\n\n{text}"
        else:
            prompt = f"Translate the following text from {source_language} to {target_language}:\n\n{text}"
        
        # Generate translation
        model_instance = gemini_client._get_model(model)
        response = model_instance.generate_content(prompt)
        
        return {
            "success": True,
            "model": model,
            "source_language": source_language,
            "target_language": target_language,
            "original_text": text,
            "translated_text": response.text,
            "usage": {
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
                "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else None,
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else None
            }
        }
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        raise ValueError(f"Translation failed: {str(e)}")

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv('GEMINI_MCP_PORT', '8014'))
    
    logger.info(f"Starting Gemini MCP Server on port {port}")
    logger.info("Available capabilities: text generation, vision, code analysis, structured output, conversation")
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")