"""
Supabase Storage Module
Handles all database operations for Figma components
"""

import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from supabase import create_client, Client
import asyncio

logger = logging.getLogger(__name__)


class SupabaseStorage:
    """Handles Supabase database operations for design components"""
    
    def __init__(self, url: str, key: str):
        self.client: Client = create_client(url, key)
        logger.info("Supabase client initialized")
    
    # Design Files Operations
    
    async def create_design_file(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new design file record"""
        try:
            response = self.client.table("design_files").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating design file: {str(e)}")
            raise
    
    async def get_design_file(self, file_key: str) -> Optional[Dict[str, Any]]:
        """Get design file by file key"""
        try:
            response = self.client.table("design_files").select("*").eq("file_key", file_key).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting design file: {str(e)}")
            raise
    
    async def update_design_file(self, file_key: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update design file"""
        try:
            response = self.client.table("design_files").update(updates).eq("file_key", file_key).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error updating design file: {str(e)}")
            raise
    
    async def list_design_files(self) -> List[Dict[str, Any]]:
        """List all design files"""
        try:
            response = self.client.table("design_files").select("*").order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error listing design files: {str(e)}")
            raise
    
    # Design Components Operations
    
    async def create_or_update_component(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update a component (upsert by file_id and node_id)"""
        try:
            response = self.client.table("design_components").upsert(
                data,
                on_conflict="file_id,node_id"
            ).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating/updating component: {str(e)}")
            raise
    
    async def get_component(self, component_id: str) -> Optional[Dict[str, Any]]:
        """Get component by ID"""
        try:
            response = self.client.table("design_components").select("*").eq("id", component_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting component: {str(e)}")
            raise
    
    async def update_component(self, component_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update component"""
        try:
            response = self.client.table("design_components").update(updates).eq("id", component_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error updating component: {str(e)}")
            raise
    
    async def delete_component(self, component_id: str) -> bool:
        """Delete component"""
        try:
            response = self.client.table("design_components").delete().eq("id", component_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error deleting component: {str(e)}")
            raise
    
    async def search_components(self, filters: Dict[str, Any], 
                              limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """Search components with filters"""
        try:
            query = self.client.table("design_components").select(
                "*, design_files(name)"
            )
            
            # Apply filters
            for key, value in filters.items():
                if "__" in key:  # Handle operators like name__ilike
                    field, op = key.rsplit("__", 1)
                    if op == "ilike":
                        query = query.ilike(field, value)
                    elif op == "contains":
                        query = query.contains(field, value)
                    else:
                        query = query.filter(field, op, value)
                else:
                    query = query.eq(key, value)
            
            # Apply pagination
            query = query.range(offset, offset + limit - 1)
            query = query.order("created_at", desc=True)
            
            response = query.execute()
            
            # Format results with file name
            results = []
            for item in response.data:
                if "design_files" in item and item["design_files"]:
                    item["file_name"] = item["design_files"]["name"]
                    del item["design_files"]
                results.append(item)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching components: {str(e)}")
            raise
    
    async def count_components(self, filters: Dict[str, Any]) -> int:
        """Count components matching filters"""
        try:
            query = self.client.table("design_components").select("id", count="exact")
            
            # Apply filters
            for key, value in filters.items():
                if "__" in key:
                    field, op = key.rsplit("__", 1)
                    if op == "ilike":
                        query = query.ilike(field, value)
                    elif op == "contains":
                        query = query.contains(field, value)
                    else:
                        query = query.filter(field, op, value)
                else:
                    query = query.eq(key, value)
            
            response = query.execute()
            return response.count if response.count is not None else 0
            
        except Exception as e:
            logger.error(f"Error counting components: {str(e)}")
            raise
    
    async def get_file_components(self, file_id: str) -> List[Dict[str, Any]]:
        """Get all components for a file"""
        try:
            response = self.client.table("design_components").select("*").eq("file_id", file_id).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error getting file components: {str(e)}")
            raise
    
    # Component Variants Operations
    
    async def create_component_variant(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a component variant"""
        try:
            response = self.client.table("component_variants").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating component variant: {str(e)}")
            raise
    
    async def get_component_variants(self, component_id: str) -> List[Dict[str, Any]]:
        """Get all variants for a component"""
        try:
            response = self.client.table("component_variants").select("*").eq("component_id", component_id).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error getting component variants: {str(e)}")
            raise
    
    # Design Tokens Operations
    
    async def upsert_design_tokens(self, file_id: str, tokens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Bulk upsert design tokens"""
        try:
            # Add file_id to all tokens
            for token in tokens:
                token["file_id"] = file_id
            
            response = self.client.table("design_tokens").upsert(
                tokens,
                on_conflict="file_id,token_type,name"
            ).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error upserting design tokens: {str(e)}")
            raise
    
    async def get_design_tokens(self, file_id: str, token_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get design tokens for a file"""
        try:
            query = self.client.table("design_tokens").select("*").eq("file_id", file_id)
            if token_type:
                query = query.eq("token_type", token_type)
            
            response = query.order("token_type").order("name").execute()
            return response.data
        except Exception as e:
            logger.error(f"Error getting design tokens: {str(e)}")
            raise
    
    # Analytics Operations
    
    async def track_component_usage(self, component_id: str, action: str, 
                                   user_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        """Track component usage for analytics"""
        try:
            data = {
                "component_id": component_id,
                "action": action,
                "user_id": user_id,
                "metadata": metadata or {}
            }
            response = self.client.table("component_usage").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error tracking component usage: {str(e)}")
            # Don't raise - analytics shouldn't break the flow
            return None
    
    async def get_component_usage_stats(self, component_id: str) -> Dict[str, Any]:
        """Get usage statistics for a component"""
        try:
            # Get total usage count
            total_response = self.client.table("component_usage").select("id", count="exact").eq("component_id", component_id).execute()
            
            # Get usage by action
            action_response = self.client.rpc("get_component_usage_by_action", {"p_component_id": component_id}).execute()
            
            return {
                "total_usage": total_response.count or 0,
                "by_action": action_response.data if action_response.data else []
            }
        except Exception as e:
            logger.error(f"Error getting component usage stats: {str(e)}")
            return {"total_usage": 0, "by_action": []}