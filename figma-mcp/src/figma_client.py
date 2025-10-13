"""
Figma API Client
Handles all interactions with Figma REST API
"""

import aiohttp
import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class FigmaClient:
    """Async client for Figma REST API"""
    
    BASE_URL = "https://api.figma.com/v1"
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "X-FIGMA-TOKEN": access_token,
            "Content-Type": "application/json"
        }
        self._session = None
        self._rate_limit_remaining = 1000
        self._rate_limit_reset = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session with timeout"""
        if self._session is None or self._session.closed:
            # Set 30 second timeout for large Figma files
            timeout = aiohttp.ClientTimeout(total=30)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session
    
    async def close(self):
        """Close the session"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make request to Figma API with rate limiting"""
        url = f"{self.BASE_URL}{endpoint}"
        session = await self._get_session()
        
        # Check rate limit
        if self._rate_limit_remaining <= 10:
            if self._rate_limit_reset:
                wait_time = (self._rate_limit_reset - datetime.now()).total_seconds()
                if wait_time > 0:
                    logger.warning(f"Rate limit approaching, waiting {wait_time}s")
                    await asyncio.sleep(wait_time)
        
        try:
            async with session.request(method, url, headers=self.headers, **kwargs) as response:
                # Update rate limit info
                self._rate_limit_remaining = int(response.headers.get("X-RateLimit-Remaining", 1000))
                reset_time = response.headers.get("X-RateLimit-Reset")
                if reset_time:
                    self._rate_limit_reset = datetime.fromtimestamp(int(reset_time))
                
                # Handle rate limiting
                if response.status == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    logger.warning(f"Rate limited, retrying after {retry_after}s")
                    await asyncio.sleep(retry_after)
                    return await self._request(method, endpoint, **kwargs)
                
                response.raise_for_status()
                return await response.json()
                
        except aiohttp.ClientError as e:
            logger.error(f"Figma API request failed: {str(e)}")
            raise
    
    async def get_current_user(self) -> Dict[str, Any]:
        """Get current user information"""
        return await self._request("GET", "/me")
    
    async def get_file_info(self, file_key: str) -> Dict[str, Any]:
        """Get file metadata"""
        data = await self._request("GET", f"/files/{file_key}")
        return {
            "name": data.get("name"),
            "lastModified": data.get("lastModified"),
            "version": data.get("version"),
            "thumbnailUrl": data.get("thumbnailUrl")
        }
    
    async def get_file(self, file_key: str, node_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get file data with optional node filtering"""
        params = {}
        if node_ids:
            params["ids"] = ",".join(node_ids)
        
        return await self._request("GET", f"/files/{file_key}", params=params)
    
    async def get_file_components(self, file_key: str) -> Dict[str, Any]:
        """Get all components in a file"""
        # Get file with components metadata
        file_data = await self._request("GET", f"/files/{file_key}")
        
        # Extract components from the document
        components = {}
        
        def extract_components(node: Dict[str, Any]):
            """Recursively extract components from node tree"""
            if node.get("type") == "COMPONENT" or node.get("type") == "COMPONENT_SET":
                components[node["id"]] = {
                    "name": node.get("name", ""),
                    "description": node.get("description", ""),
                    "type": node.get("type"),
                    "node": node
                }
            
            # Process children
            if "children" in node:
                for child in node["children"]:
                    extract_components(child)
        
        # Start extraction from document root
        if "document" in file_data:
            extract_components(file_data["document"])
        
        return {"components": components}
    
    async def get_node_data(self, file_key: str, node_id: str) -> Dict[str, Any]:
        """Get detailed data for a specific node"""
        file_data = await self.get_file(file_key, [node_id])
        
        # Find the node in the response
        def find_node(node: Dict[str, Any], target_id: str) -> Optional[Dict[str, Any]]:
            if node.get("id") == target_id:
                return node
            if "children" in node:
                for child in node["children"]:
                    result = find_node(child, target_id)
                    if result:
                        return result
            return None
        
        if "document" in file_data:
            node = find_node(file_data["document"], node_id)
            if node:
                return node
        
        raise ValueError(f"Node {node_id} not found in file")
    
    async def get_image_urls(self, file_key: str, node_ids: List[str], 
                           format: str = "png", scale: float = 2.0) -> Dict[str, str]:
        """Get image export URLs for nodes"""
        params = {
            "ids": ",".join(node_ids),
            "format": format,
            "scale": scale
        }
        
        response = await self._request("GET", f"/images/{file_key}", params=params)
        return response.get("images", {})
    
    async def get_file_versions(self, file_key: str) -> List[Dict[str, Any]]:
        """Get version history of a file"""
        response = await self._request("GET", f"/files/{file_key}/versions")
        return response.get("versions", [])
    
    async def get_team_projects(self, team_id: str) -> List[Dict[str, Any]]:
        """Get all projects in a team"""
        response = await self._request("GET", f"/teams/{team_id}/projects")
        return response.get("projects", [])
    
    async def get_project_files(self, project_id: str) -> List[Dict[str, Any]]:
        """Get all files in a project"""
        response = await self._request("GET", f"/projects/{project_id}/files")
        return response.get("files", [])