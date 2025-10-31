#!/usr/bin/env python3
"""
Brave Search MCP Server - HTTP Implementation
Web and local search capabilities using Brave Search API

Converted from official MCP TypeScript stdio server to FastMCP HTTP server
Based on: https://github.com/modelcontextprotocol/servers-archived/blob/main/src/brave-search/index.ts
"""

import os
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import httpx

# FastMCP for HTTP serving
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BraveSearchClient:
    """Client for interacting with Brave Search API"""
    
    def __init__(self, api_key: str):
        """Initialize with API key"""
        self.api_key = api_key
        self.base_url = "https://api.search.brave.com/res/v1"
        self.headers = {
            "X-Subscription-Token": api_key,
            "Accept": "application/json"
        }
        
        # Rate limiting
        self.last_request_time = None
        self.min_request_interval = timedelta(seconds=1)  # 1 request per second
        
        logger.info("Brave Search client initialized")
    
    async def _enforce_rate_limit(self):
        """Enforce rate limiting between requests"""
        if self.last_request_time:
            elapsed = datetime.now() - self.last_request_time
            if elapsed < self.min_request_interval:
                sleep_time = (self.min_request_interval - elapsed).total_seconds()
                logger.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
                await asyncio.sleep(sleep_time)
        
        self.last_request_time = datetime.now()
    
    async def web_search(
        self, 
        query: str, 
        count: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Perform a web search using Brave Search API
        
        Args:
            query: Search query (max 400 chars, 50 words)
            count: Number of results (1-20, default 10)
            offset: Pagination offset (max 9, default 0)
        
        Returns:
            Search results with web pages
        """
        # Validate parameters
        if len(query) > 400:
            query = query[:400]
        
        count = max(1, min(20, count))
        offset = max(0, min(9, offset))
        
        # Enforce rate limiting
        await self._enforce_rate_limit()
        
        # Prepare request
        params = {
            "q": query,
            "count": count,
            "offset": offset
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/web/search",
                    headers=self.headers,
                    params=params,
                    timeout=30.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                # Process results
                results = []
                if "web" in data and "results" in data["web"]:
                    for result in data["web"]["results"]:
                        results.append({
                            "title": result.get("title", ""),
                            "url": result.get("url", ""),
                            "description": result.get("description", ""),
                            "age": result.get("age", ""),
                            "language": result.get("language", "en")
                        })
                
                logger.info(f"Web search for '{query}' returned {len(results)} results")
                
                return {
                    "success": True,
                    "query": query,
                    "count": len(results),
                    "offset": offset,
                    "results": results
                }
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during web search: {e.response.status_code}")
            if e.response.status_code == 401:
                raise ValueError("Invalid API key")
            elif e.response.status_code == 429:
                raise ValueError("Rate limit exceeded")
            else:
                raise ValueError(f"Search failed: {e.response.text}")
                
        except Exception as e:
            logger.error(f"Error during web search: {e}")
            raise ValueError(f"Search failed: {str(e)}")
    
    async def local_search(
        self,
        query: str,
        count: int = 5
    ) -> Dict[str, Any]:
        """
        Search for local businesses and places
        
        Args:
            query: Local search query (e.g., 'pizza near Central Park')
            count: Number of results (1-20, default 5)
        
        Returns:
            Local business results with details
        """
        # Validate parameters
        if len(query) > 400:
            query = query[:400]
        
        count = max(1, min(20, count))
        
        # Enforce rate limiting
        await self._enforce_rate_limit()
        
        # First try local search
        params = {
            "q": query,
            "count": count,
            "search_type": "local"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                # Try local search endpoint
                response = await client.get(
                    f"{self.base_url}/local/search",
                    headers=self.headers,
                    params=params,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Process local results
                    results = []
                    if "results" in data:
                        for result in data["results"]:
                            results.append({
                                "name": result.get("name", ""),
                                "address": result.get("address", ""),
                                "phone": result.get("phone", ""),
                                "rating": result.get("rating", None),
                                "review_count": result.get("review_count", 0),
                                "category": result.get("category", ""),
                                "url": result.get("url", ""),
                                "hours": result.get("hours", []),
                                "coordinates": {
                                    "latitude": result.get("latitude"),
                                    "longitude": result.get("longitude")
                                } if "latitude" in result else None
                            })
                    
                    if results:
                        logger.info(f"Local search for '{query}' returned {len(results)} results")
                        return {
                            "success": True,
                            "query": query,
                            "count": len(results),
                            "type": "local",
                            "results": results
                        }
                
                # If no local results or endpoint doesn't exist, fall back to web search
                logger.info(f"No local results for '{query}', falling back to web search")
                web_results = await self.web_search(query, count)
                web_results["type"] = "web_fallback"
                web_results["message"] = "No local results found, showing web results instead"
                return web_results
                
        except httpx.HTTPStatusError as e:
            # If local search fails, try web search as fallback
            logger.warning(f"Local search failed, falling back to web search: {e}")
            web_results = await self.web_search(query, count)
            web_results["type"] = "web_fallback"
            web_results["message"] = "Local search unavailable, showing web results instead"
            return web_results
            
        except Exception as e:
            logger.error(f"Error during local search: {e}")
            raise ValueError(f"Search failed: {str(e)}")


# Initialize FastMCP server
mcp = FastMCP("brave-search")

# Get API key from environment
api_key = os.getenv('BRAVE_API_KEY')
if not api_key:
    raise ValueError("BRAVE_API_KEY environment variable required")

# Initialize search client
search_client = BraveSearchClient(api_key)

# Register tools
@mcp.tool()
async def brave_web_search(
    query: str,
    count: Optional[int] = 10,
    offset: Optional[int] = 0
) -> Dict[str, Any]:
    """
    Performs a web search using the Brave Search API, ideal for general queries,
    news, articles, and online content. Use this for broad information gathering,
    recent events, or when you need diverse web sources. Supports pagination,
    content filtering, and freshness controls. Maximum 20 results per request,
    with offset for pagination.
    
    Args:
        query: Search query (max 400 chars, 50 words)
        count: Number of results (1-20, default 10)
        offset: Pagination offset (max 9, default 0)
    
    Returns:
        Web search results with title, URL, description
    """
    return await search_client.web_search(query, count or 10, offset or 0)

@mcp.tool()
async def brave_local_search(
    query: str,
    count: Optional[int] = 5
) -> Dict[str, Any]:
    """
    Searches for local businesses and places using Brave's Local Search API.
    Best for queries related to physical locations, businesses, restaurants,
    services, etc. Returns detailed information including:
    - Business names and addresses
    - Ratings and review counts
    - Phone numbers and opening hours
    Use this when the query implies 'near me' or mentions specific locations.
    Automatically falls back to web search if no local results are found.
    
    Args:
        query: Local search query (e.g. 'pizza near Central Park')
        count: Number of results (1-20, default 5)
    
    Returns:
        Local business results or web results as fallback
    """
    return await search_client.local_search(query, count or 5)

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv('BRAVE_SEARCH_MCP_PORT', '8003'))
    
    logger.info(f"Starting Brave Search MCP Server on port {port}")
    logger.info("Rate limits: 1 request/second, 15,000 requests/month")
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")