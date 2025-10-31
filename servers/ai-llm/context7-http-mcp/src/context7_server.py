#!/usr/bin/env python3
"""
Context7 MCP Server - HTTP Implementation
Library documentation lookup and developer resources via Context7 API

Converted from official MCP TypeScript stdio server to FastMCP HTTP server
"""

import os
import logging
from typing import Dict, Any, Optional
import httpx
from datetime import datetime

# FastMCP for HTTP serving
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("context7-http-mcp")

# Context7 API base URL
CONTEXT7_API_BASE = "https://api.context7.ai"

@mcp.tool()
async def resolve_library_id(library_name: str) -> Dict[str, Any]:
    """
    Resolves a package/product name to a Context7-compatible library ID and returns a list of matching libraries.

    You MUST call this function before 'get-library-docs' to obtain a valid Context7-compatible library ID 
    UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query.

    Selection Process:
    1. Analyze the query to understand what library/package the user is looking for
    2. Return the most relevant match based on:
    - Name similarity to the query (exact matches prioritized)
    - Description relevance to the query's intent
    - Documentation coverage (prioritize libraries with higher Code Snippet counts)
    - Trust score (consider libraries with scores of 7-10 more authoritative)

    Response Format:
    - Return the selected library ID in a clearly marked section
    - Provide a brief explanation for why this library was chosen
    - If multiple good matches exist, acknowledge this but proceed with the most relevant one
    - If no good matches exist, clearly state this and suggest query refinements

    For ambiguous queries, request clarification before proceeding with a best-guess match.
    
    Args:
        library_name: Library name to search for and retrieve a Context7-compatible library ID.
    
    Returns:
        List of matching libraries with their Context7 IDs and metadata
    """
    try:
        if not library_name:
            raise ValueError("library_name is required")
        
        # Search for libraries matching the name
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CONTEXT7_API_BASE}/search",
                params={
                    "q": library_name,
                    "type": "library",
                    "limit": 10
                },
                timeout=30.0
            )
            
        if response.status_code != 200:
            raise ValueError(f"Context7 API error: {response.status_code} - {response.text}")
        
        data = response.json()
        libraries = data.get("results", [])
        
        if not libraries:
            return {
                "success": True,
                "query": library_name,
                "libraries": [],
                "selected_library_id": None,
                "message": f"No libraries found matching '{library_name}'. Try a more specific or alternative name.",
                "suggestions": [
                    "Check spelling and try alternative names",
                    "Use the full package name (e.g., 'react' instead of 'reactjs')",
                    "Try the organization/project format (e.g., 'facebook/react')"
                ]
            }
        
        # Score and rank libraries
        scored_libraries = []
        for lib in libraries:
            name = lib.get("name", "")
            description = lib.get("description", "")
            library_id = lib.get("id", "")
            code_snippets = lib.get("code_snippets", 0)
            trust_score = lib.get("trust_score", 0)
            
            # Calculate relevance score
            name_similarity = 0
            if library_name.lower() in name.lower():
                name_similarity = 50
            if library_name.lower() == name.lower():
                name_similarity = 100
            
            desc_relevance = 0
            if library_name.lower() in description.lower():
                desc_relevance = 25
            
            # Bonus for good documentation and trust
            doc_bonus = min(code_snippets / 10, 20)  # Max 20 points
            trust_bonus = min(trust_score, 10)  # Max 10 points
            
            total_score = name_similarity + desc_relevance + doc_bonus + trust_bonus
            
            scored_libraries.append({
                "library_id": library_id,
                "name": name,
                "description": description,
                "code_snippets": code_snippets,
                "trust_score": trust_score,
                "relevance_score": total_score,
                "url": lib.get("url", "")
            })
        
        # Sort by relevance score
        scored_libraries.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Select the best match
        best_match = scored_libraries[0] if scored_libraries else None
        
        return {
            "success": True,
            "query": library_name,
            "libraries": scored_libraries,
            "selected_library_id": best_match["library_id"] if best_match else None,
            "selection_reason": f"Selected '{best_match['name']}' (score: {best_match['relevance_score']:.1f}) - best name match with {best_match['code_snippets']} code snippets and trust score {best_match['trust_score']}" if best_match else "No suitable match found",
            "total_matches": len(libraries)
        }
        
    except Exception as e:
        logger.error(f"Failed to resolve library ID for '{library_name}': {e}")
        raise ValueError(f"Failed to resolve library ID: {str(e)}")

@mcp.tool()
async def get_library_docs(
    context7_compatible_library_id: str,
    tokens: Optional[int] = 10000,
    topic: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetches up-to-date documentation for a library. You must call 'resolve-library-id' first to obtain the exact 
    Context7-compatible library ID required to use this tool, UNLESS the user explicitly provides a library ID 
    in the format '/org/project' or '/org/project/version' in their query.
    
    Args:
        context7_compatible_library_id: Exact Context7-compatible library ID (e.g., '/mongodb/docs', '/vercel/next.js', 
                                       '/supabase/supabase', '/vercel/next.js/v14.3.0-canary.87') retrieved from 
                                       'resolve-library-id' or directly from user query in the format '/org/project' 
                                       or '/org/project/version'.
        tokens: Maximum number of tokens of documentation to retrieve (default: 10000). Higher values provide more 
               context but consume more tokens.
        topic: Topic to focus documentation on (e.g., 'hooks', 'routing').
    
    Returns:
        Library documentation content and metadata
    """
    try:
        if not context7_compatible_library_id:
            raise ValueError("context7_compatible_library_id is required")
        
        # Validate library ID format
        if not context7_compatible_library_id.startswith('/'):
            raise ValueError("Library ID must start with '/' (e.g., '/org/project')")
        
        # Prepare request parameters
        params = {
            "library_id": context7_compatible_library_id,
            "max_tokens": min(tokens or 10000, 50000)  # Cap at 50k tokens
        }
        
        if topic:
            params["topic"] = topic
        
        # Fetch documentation
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CONTEXT7_API_BASE}/docs",
                params=params,
                timeout=60.0  # Longer timeout for doc retrieval
            )
            
        if response.status_code == 404:
            return {
                "success": False,
                "library_id": context7_compatible_library_id,
                "error": "Library not found",
                "message": f"No documentation found for library '{context7_compatible_library_id}'. Please check the library ID format or use resolve-library-id first.",
                "suggestions": [
                    "Use resolve-library-id to find the correct library ID",
                    "Check if the library ID format is correct (e.g., '/org/project')",
                    "Verify the library exists in the Context7 database"
                ]
            }
        
        if response.status_code != 200:
            raise ValueError(f"Context7 API error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        # Extract documentation content
        content = data.get("content", "")
        metadata = data.get("metadata", {})
        
        return {
            "success": True,
            "library_id": context7_compatible_library_id,
            "topic": topic,
            "content": content,
            "metadata": {
                "library_name": metadata.get("name"),
                "version": metadata.get("version"),
                "last_updated": metadata.get("last_updated"),
                "content_type": metadata.get("content_type"),
                "token_count": len(content.split()) if content else 0,
                "sections": metadata.get("sections", []),
                "tags": metadata.get("tags", [])
            },
            "usage": {
                "tokens_requested": tokens,
                "tokens_returned": len(content.split()) if content else 0,
                "topic_filter": topic is not None
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get library docs for '{context7_compatible_library_id}': {e}")
        raise ValueError(f"Failed to get library docs: {str(e)}")

@mcp.tool()
async def search_documentation(
    query: str,
    library_filter: Optional[str] = None,
    limit: Optional[int] = 5
) -> Dict[str, Any]:
    """
    Search across documentation for specific topics or code examples
    
    Args:
        query: Search query for documentation content
        library_filter: Optional library ID to limit search scope
        limit: Maximum number of results to return (default: 5, max: 20)
    
    Returns:
        Search results with relevant documentation snippets
    """
    try:
        if not query:
            raise ValueError("query is required")
        
        # Validate limit
        limit = min(limit or 5, 20)
        
        params = {
            "q": query,
            "limit": limit,
            "type": "documentation"
        }
        
        if library_filter:
            params["library"] = library_filter
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CONTEXT7_API_BASE}/search",
                params=params,
                timeout=30.0
            )
            
        if response.status_code != 200:
            raise ValueError(f"Context7 API error: {response.status_code} - {response.text}")
        
        data = response.json()
        results = data.get("results", [])
        
        # Format search results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "library_id": result.get("library_id"),
                "library_name": result.get("library_name"),
                "title": result.get("title"),
                "snippet": result.get("snippet"),
                "relevance_score": result.get("score", 0),
                "url": result.get("url"),
                "section": result.get("section"),
                "tags": result.get("tags", [])
            })
        
        return {
            "success": True,
            "query": query,
            "library_filter": library_filter,
            "results": formatted_results,
            "total_results": len(formatted_results),
            "has_more": data.get("has_more", False)
        }
        
    except Exception as e:
        logger.error(f"Failed to search documentation for '{query}': {e}")
        raise ValueError(f"Failed to search documentation: {str(e)}")

@mcp.tool()
async def get_code_examples(
    library_id: str,
    topic: Optional[str] = None,
    language: Optional[str] = None,
    limit: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Get code examples for a specific library
    
    Args:
        library_id: Context7-compatible library ID
        topic: Optional topic filter (e.g., 'authentication', 'routing')
        language: Optional programming language filter (e.g., 'javascript', 'python')
        limit: Maximum number of examples to return (default: 10, max: 50)
    
    Returns:
        Code examples with explanations and usage context
    """
    try:
        if not library_id:
            raise ValueError("library_id is required")
        
        # Validate limit
        limit = min(limit or 10, 50)
        
        params = {
            "library_id": library_id,
            "limit": limit,
            "type": "code_examples"
        }
        
        if topic:
            params["topic"] = topic
        if language:
            params["language"] = language
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CONTEXT7_API_BASE}/examples",
                params=params,
                timeout=30.0
            )
            
        if response.status_code != 200:
            raise ValueError(f"Context7 API error: {response.status_code} - {response.text}")
        
        data = response.json()
        examples = data.get("examples", [])
        
        # Format code examples
        formatted_examples = []
        for example in examples:
            formatted_examples.append({
                "title": example.get("title"),
                "description": example.get("description"),
                "code": example.get("code"),
                "language": example.get("language"),
                "topic": example.get("topic"),
                "complexity": example.get("complexity", "beginner"),
                "tags": example.get("tags", []),
                "url": example.get("url")
            })
        
        return {
            "success": True,
            "library_id": library_id,
            "topic": topic,
            "language": language,
            "examples": formatted_examples,
            "total_examples": len(formatted_examples),
            "filters_applied": {
                "topic": topic is not None,
                "language": language is not None
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get code examples for '{library_id}': {e}")
        raise ValueError(f"Failed to get code examples: {str(e)}")

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv('CONTEXT7_MCP_PORT', '8019'))
    
    logger.info(f"Starting Context7 MCP Server on port {port}")
    logger.info("Context7 API: Library documentation and code examples")
    logger.info("Available tools: resolve_library_id, get_library_docs, search_documentation, get_code_examples")
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")