#!/usr/bin/env python3
"""
OpenAI Tools MCP Server - HTTP Version
Provides essential OpenAI API tools for embeddings, images, audio, and moderation
"""

import os
import logging
from typing import List, Dict, Any, Optional
import base64
from PIL import Image
import io

from fastmcp import FastMCP
from openai import AsyncOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("openai-tools")

# Initialize OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")

client = AsyncOpenAI(api_key=api_key)

# Embedding Operations

@mcp.tool()
async def create_embeddings(
    texts: List[str],
    model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """
    Create embeddings for a list of texts using OpenAI's embedding models
    
    Args:
        texts: List of texts to embed (max 2048 texts)
        model: Model to use (text-embedding-3-small or text-embedding-3-large)
    
    Returns:
        Embeddings and usage information
    """
    try:
        if len(texts) > 2048:
            raise ValueError("Maximum 2048 texts allowed per request")
        
        response = await client.embeddings.create(
            input=texts,
            model=model
        )
        
        embeddings = [e.embedding for e in response.data]
        
        return {
            "success": True,
            "embeddings": embeddings,
            "model": model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
    except Exception as e:
        logger.error(f"Failed to create embeddings: {e}")
        raise ValueError(f"Failed to create embeddings: {str(e)}")

@mcp.tool()
async def calculate_similarity(
    embedding1: List[float],
    embedding2: List[float]
) -> Dict[str, Any]:
    """
    Calculate cosine similarity between two embeddings
    
    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector
    
    Returns:
        Cosine similarity score between -1 and 1
    """
    try:
        import numpy as np
        
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        similarity = dot_product / (norm1 * norm2)
        
        return {
            "success": True,
            "similarity": float(similarity),
            "percentage": float((similarity + 1) / 2 * 100)  # Convert to 0-100%
        }
    except Exception as e:
        logger.error(f"Failed to calculate similarity: {e}")
        raise ValueError(f"Failed to calculate similarity: {str(e)}")

# Image Operations

@mcp.tool()
async def generate_image(
    prompt: str,
    model: str = "dall-e-3",
    size: str = "1024x1024",
    quality: str = "standard",
    n: int = 1
) -> Dict[str, Any]:
    """
    Generate images using DALL-E
    
    Args:
        prompt: Text description of the image to generate
        model: Model to use (dall-e-2 or dall-e-3)
        size: Image size (1024x1024, 1792x1024, or 1024x1792 for dall-e-3)
        quality: Image quality (standard or hd for dall-e-3)
        n: Number of images to generate (1-10 for dall-e-2, only 1 for dall-e-3)
    
    Returns:
        Generated image URLs
    """
    try:
        response = await client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n
        )
        
        images = []
        for image in response.data:
            images.append({
                "url": image.url,
                "revised_prompt": getattr(image, 'revised_prompt', None)
            })
        
        return {
            "success": True,
            "images": images,
            "model": model,
            "size": size
        }
    except Exception as e:
        logger.error(f"Failed to generate image: {e}")
        raise ValueError(f"Failed to generate image: {str(e)}")

@mcp.tool()
async def edit_image(
    image_base64: str,
    prompt: str,
    mask_base64: Optional[str] = None,
    model: str = "dall-e-2",
    size: str = "1024x1024",
    n: int = 1
) -> Dict[str, Any]:
    """
    Edit an image using DALL-E 2
    
    Args:
        image_base64: Base64 encoded PNG image to edit (must be square, <4MB)
        prompt: Description of how to edit the image
        mask_base64: Optional base64 encoded PNG mask indicating areas to edit
        model: Model to use (only dall-e-2 supports edits)
        size: Output size (256x256, 512x512, or 1024x1024)
        n: Number of variations to generate (1-10)
    
    Returns:
        Edited image URLs
    """
    try:
        # Decode base64 images
        image_data = base64.b64decode(image_base64)
        mask_data = base64.b64decode(mask_base64) if mask_base64 else None
        
        # Create image files
        image_file = io.BytesIO(image_data)
        mask_file = io.BytesIO(mask_data) if mask_data else None
        
        response = await client.images.edit(
            image=image_file,
            prompt=prompt,
            mask=mask_file,
            model=model,
            size=size,
            n=n
        )
        
        images = [{"url": image.url} for image in response.data]
        
        return {
            "success": True,
            "images": images,
            "model": model,
            "size": size
        }
    except Exception as e:
        logger.error(f"Failed to edit image: {e}")
        raise ValueError(f"Failed to edit image: {str(e)}")

# Audio Operations

@mcp.tool()
async def text_to_speech(
    text: str,
    voice: str = "alloy",
    model: str = "tts-1",
    response_format: str = "mp3",
    speed: float = 1.0
) -> Dict[str, Any]:
    """
    Convert text to speech using OpenAI TTS
    
    Args:
        text: Text to convert to speech (max 4096 chars)
        voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        model: Model to use (tts-1 or tts-1-hd)
        response_format: Audio format (mp3, opus, aac, flac, wav, pcm)
        speed: Speed of speech (0.25 to 4.0)
    
    Returns:
        Base64 encoded audio data
    """
    try:
        if len(text) > 4096:
            raise ValueError("Text must be less than 4096 characters")
        
        response = await client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            response_format=response_format,
            speed=speed
        )
        
        # Get audio data as bytes
        audio_data = response.content
        
        # Encode to base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return {
            "success": True,
            "audio_base64": audio_base64,
            "format": response_format,
            "model": model,
            "voice": voice
        }
    except Exception as e:
        logger.error(f"Failed to convert text to speech: {e}")
        raise ValueError(f"Failed to convert text to speech: {str(e)}")

@mcp.tool()
async def speech_to_text(
    audio_base64: str,
    model: str = "whisper-1",
    language: Optional[str] = None,
    response_format: str = "json",
    temperature: float = 0
) -> Dict[str, Any]:
    """
    Transcribe audio to text using Whisper
    
    Args:
        audio_base64: Base64 encoded audio file (mp3, mp4, mpeg, mpga, m4a, wav, webm)
        model: Model to use (whisper-1)
        language: Language of the audio (ISO-639-1 format)
        response_format: Output format (json, text, srt, verbose_json, vtt)
        temperature: Sampling temperature (0-1)
    
    Returns:
        Transcribed text
    """
    try:
        # Decode base64 audio
        audio_data = base64.b64decode(audio_base64)
        audio_file = io.BytesIO(audio_data)
        audio_file.name = "audio.mp3"  # Required for API
        
        response = await client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            language=language,
            response_format=response_format,
            temperature=temperature
        )
        
        return {
            "success": True,
            "text": response.text if hasattr(response, 'text') else response,
            "model": model,
            "language": language or "auto-detected"
        }
    except Exception as e:
        logger.error(f"Failed to transcribe audio: {e}")
        raise ValueError(f"Failed to transcribe audio: {str(e)}")

# Moderation

@mcp.tool()
async def moderate_content(
    text: str,
    model: str = "text-moderation-latest"
) -> Dict[str, Any]:
    """
    Check if text complies with OpenAI usage policies
    
    Args:
        text: Text to moderate
        model: Model to use (text-moderation-latest or text-moderation-stable)
    
    Returns:
        Moderation results with category scores and flags
    """
    try:
        response = await client.moderations.create(
            input=text,
            model=model
        )
        
        result = response.results[0]
        
        return {
            "success": True,
            "flagged": result.flagged,
            "categories": result.categories.model_dump(),
            "category_scores": result.category_scores.model_dump(),
            "model": model
        }
    except Exception as e:
        logger.error(f"Failed to moderate content: {e}")
        raise ValueError(f"Failed to moderate content: {str(e)}")

# Utility Operations

@mcp.tool()
async def extract_structured_data(
    text: str,
    schema: Dict[str, Any],
    model: str = "gpt-4-turbo-preview"
) -> Dict[str, Any]:
    """
    Extract structured data from text using GPT models
    
    Args:
        text: Text to extract data from
        schema: JSON schema describing the expected output structure
        model: GPT model to use
    
    Returns:
        Extracted structured data matching the schema
    """
    try:
        prompt = f"""Extract structured data from the following text according to the provided JSON schema.
        
Schema: {schema}

Text: {text}

Return only valid JSON that matches the schema."""

        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a data extraction assistant. Extract structured data and return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        import json
        extracted_data = json.loads(response.choices[0].message.content)
        
        return {
            "success": True,
            "data": extracted_data,
            "model": model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
    except Exception as e:
        logger.error(f"Failed to extract structured data: {e}")
        raise ValueError(f"Failed to extract structured data: {str(e)}")

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv('OPENAI_TOOLS_MCP_PORT', '8012'))
    
    logger.info(f"Starting OpenAI Tools MCP Server on port {port}")
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")