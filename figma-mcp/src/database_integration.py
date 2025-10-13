#!/usr/bin/env python3
"""
Database Integration for Figma MCP Server
Provides hybrid functionality: direct Figma API + database caching
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timezone
import hashlib
from supabase import create_client, Client

logger = logging.getLogger(__name__)

class FigmaDatabase:
    """Manages Figma component data in Supabase database"""
    
    def __init__(self, project_id: str = None):
        """Initialize database connection"""
        # Get Supabase credentials from environment
        self.project_id = project_id or os.getenv('FIGMA_DB_PROJECT_ID', 'wsmhiiharnhqupdniwgw')
        self.supabase_url = f"https://{self.project_id}.supabase.co"
        self.supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not self.supabase_key:
            logger.warning("SUPABASE_SERVICE_KEY not found - database features disabled")
            self.client = None
        else:
            self.client: Client = create_client(self.supabase_url, self.supabase_key)
            logger.info(f"Connected to Figma database at {self.supabase_url}")
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self.client is not None
    
    async def cache_component(self, component_data: Dict[str, Any]) -> bool:
        """Cache a Figma component in the database"""
        if not self.is_connected():
            return False
            
        try:
            # Extract component information
            figma_id = component_data.get('id', '')
            name = component_data.get('name', 'Unnamed Component')
            
            # Determine component type and category
            component_type = self._infer_component_type(name, component_data)
            category_id = await self._get_or_create_category(component_type)
            
            # Prepare component record
            component_record = {
                'figma_id': figma_id,
                'name': name,
                'description': component_data.get('description', ''),
                'category_id': category_id,
                'figma_url': component_data.get('figma_url', ''),
                'thumbnail_url': component_data.get('thumbnail_url'),
                'component_type': component_type,
                'tags': self._extract_tags(name, component_data),
                'complexity_score': self._calculate_complexity(component_data),
                'props': component_data.get('properties', {}),
                'figma_node_type': component_data.get('type', ''),
                'width': component_data.get('absoluteBoundingBox', {}).get('width'),
                'height': component_data.get('absoluteBoundingBox', {}).get('height'),
                'status': 'active',
                'last_synced': datetime.now(timezone.utc).isoformat()
            }
            
            # Upsert component (insert or update)
            result = self.client.table('figma_components').upsert(
                component_record,
                on_conflict='figma_id'
            ).execute()
            
            # Track usage
            if result.data:
                await self._track_usage(result.data[0]['id'], 'cached')
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to cache component: {e}")
            return False
    
    async def get_component(self, figma_id: str) -> Optional[Dict[str, Any]]:
        """Get a cached component from database"""
        if not self.is_connected():
            return None
            
        try:
            result = self.client.table('figma_components').select('*').eq('figma_id', figma_id).execute()
            
            if result.data:
                component = result.data[0]
                # Track usage
                await self._track_usage(component['id'], 'retrieved')
                return component
                
            return None
            
        except Exception as e:
            logger.error(f"Failed to get component from database: {e}")
            return None
    
    async def search_components(self, 
                              search_term: Optional[str] = None,
                              category: Optional[str] = None,
                              tags: Optional[List[str]] = None,
                              limit: int = 20) -> List[Dict[str, Any]]:
        """Search components in database"""
        if not self.is_connected():
            return []
            
        try:
            query = self.client.table('figma_components').select('*')
            
            # Apply filters
            if search_term:
                query = query.ilike('name', f'%{search_term}%')
            
            if category:
                # Get category ID
                cat_result = self.client.table('component_categories').select('id').eq('name', category).execute()
                if cat_result.data:
                    query = query.eq('category_id', cat_result.data[0]['id'])
            
            if tags:
                query = query.contains('tags', tags)
            
            # Order by popularity and limit
            query = query.order('popularity_score', desc=True).limit(limit)
            
            result = query.execute()
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Failed to search components: {e}")
            return []
    
    async def save_generated_file(self, 
                                component_id: str,
                                file_path: str,
                                content: str,
                                file_type: str = 'tsx',
                                framework: str = 'react') -> bool:
        """Save generated file content to database"""
        if not self.is_connected():
            return False
            
        try:
            # Calculate content hash
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            # Get component UUID from figma_id
            comp_result = self.client.table('figma_components').select('id').eq('figma_id', component_id).execute()
            if not comp_result.data:
                logger.error(f"Component {component_id} not found in database")
                return False
                
            db_component_id = comp_result.data[0]['id']
            
            # Save generated file
            file_record = {
                'component_id': db_component_id,
                'file_path': file_path,
                'file_type': file_type,
                'content': content,
                'framework': framework,
                'hash': content_hash,
                'generator_version': '1.0.0',
                'generation_options': {
                    'typescript': True,
                    'shadcn': True
                }
            }
            
            result = self.client.table('generated_files').upsert(
                file_record,
                on_conflict='component_id,file_path'
            ).execute()
            
            return bool(result.data)
            
        except Exception as e:
            logger.error(f"Failed to save generated file: {e}")
            return False
    
    async def get_categories(self) -> List[Dict[str, Any]]:
        """Get all component categories"""
        if not self.is_connected():
            return []
            
        try:
            result = self.client.table('component_categories').select('*').order('sort_order').execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Failed to get categories: {e}")
            return []
    
    async def sync_from_figma(self, components: List[Dict[str, Any]]) -> Dict[str, int]:
        """Sync multiple components from Figma to database"""
        if not self.is_connected():
            return {'processed': 0, 'added': 0, 'updated': 0, 'failed': 0}
            
        stats = {'processed': 0, 'added': 0, 'updated': 0, 'failed': 0}
        
        # Start sync history record
        sync_record = {
            'figma_file_key': components[0].get('file_key', 'unknown') if components else 'unknown',
            'sync_type': 'bulk',
            'sync_status': 'running',
            'started_at': datetime.now(timezone.utc).isoformat()
        }
        
        sync_result = self.client.table('sync_history').insert(sync_record).execute()
        sync_id = sync_result.data[0]['id'] if sync_result.data else None
        
        # Process each component
        for component in components:
            stats['processed'] += 1
            
            # Check if component exists
            existing = await self.get_component(component.get('id', ''))
            
            if await self.cache_component(component):
                if existing:
                    stats['updated'] += 1
                else:
                    stats['added'] += 1
            else:
                stats['failed'] += 1
        
        # Update sync history
        if sync_id:
            self.client.table('sync_history').update({
                'components_processed': stats['processed'],
                'components_added': stats['added'],
                'components_updated': stats['updated'],
                'sync_status': 'completed',
                'completed_at': datetime.now(timezone.utc).isoformat(),
                'sync_duration_ms': 0  # Calculate if needed
            }).eq('id', sync_id).execute()
        
        return stats
    
    # Private helper methods
    
    def _infer_component_type(self, name: str, data: Dict[str, Any]) -> str:
        """Infer component type from name and data"""
        name_lower = name.lower()
        
        # Check common patterns
        if 'button' in name_lower:
            return 'button'
        elif 'card' in name_lower:
            return 'card'
        elif 'input' in name_lower or 'field' in name_lower:
            return 'input'
        elif 'modal' in name_lower or 'dialog' in name_lower:
            return 'modal'
        elif 'nav' in name_lower or 'menu' in name_lower:
            return 'navigation'
        elif 'table' in name_lower or 'grid' in name_lower:
            return 'data-display'
        elif 'icon' in name_lower:
            return 'icon'
        elif 'badge' in name_lower or 'tag' in name_lower:
            return 'badge'
        elif 'toast' in name_lower or 'alert' in name_lower:
            return 'feedback'
        else:
            return 'component'
    
    async def _get_or_create_category(self, component_type: str) -> Optional[str]:
        """Get or create category for component type"""
        if not self.is_connected():
            return None
            
        # Map component types to categories
        type_to_category = {
            'button': 'UI Elements',
            'card': 'Layout',
            'input': 'Forms',
            'modal': 'Overlays',
            'navigation': 'Navigation',
            'data-display': 'Data Display',
            'icon': 'Icons',
            'badge': 'UI Elements',
            'feedback': 'Feedback',
            'component': 'UI Elements'
        }
        
        category_name = type_to_category.get(component_type, 'UI Elements')
        
        try:
            result = self.client.table('component_categories').select('id').eq('name', category_name).execute()
            
            if result.data:
                return result.data[0]['id']
            
            # Create category if it doesn't exist
            new_category = {
                'name': category_name,
                'description': f'{category_name} components',
                'sort_order': 99
            }
            
            create_result = self.client.table('component_categories').insert(new_category).execute()
            return create_result.data[0]['id'] if create_result.data else None
            
        except Exception as e:
            logger.error(f"Failed to get/create category: {e}")
            return None
    
    def _extract_tags(self, name: str, data: Dict[str, Any]) -> List[str]:
        """Extract relevant tags from component"""
        tags = []
        name_lower = name.lower()
        
        # Extract from name
        keywords = ['primary', 'secondary', 'large', 'small', 'icon', 'outline', 
                   'filled', 'rounded', 'square', 'disabled', 'loading', 'error',
                   'success', 'warning', 'info', 'dark', 'light']
        
        for keyword in keywords:
            if keyword in name_lower:
                tags.append(keyword)
        
        # Add component type as tag
        tags.append(self._infer_component_type(name, data))
        
        return list(set(tags))  # Remove duplicates
    
    def _calculate_complexity(self, data: Dict[str, Any]) -> int:
        """Calculate component complexity score (1-5)"""
        score = 1
        
        # Check for nested components
        if data.get('children'):
            score += min(len(data['children']) // 2, 2)
        
        # Check for variants
        if data.get('componentPropertyDefinitions'):
            score += 1
        
        # Check for complex properties
        if data.get('layoutMode') or data.get('primaryAxisSizingMode'):
            score += 1
        
        return min(score, 5)
    
    async def _track_usage(self, component_id: str, action: str) -> None:
        """Track component usage for analytics"""
        if not self.is_connected():
            return
            
        try:
            usage_record = {
                'component_id': component_id,
                'action_type': action,
                'project_name': 'figma-mcp',
                'user_session': 'mcp-server',
                'metadata': {
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            }
            
            self.client.table('component_usage').insert(usage_record).execute()
            
            # Update popularity score
            if action in ['generated', 'retrieved']:
                self.client.rpc('increment', {
                    'table_name': 'figma_components',
                    'column_name': 'popularity_score',
                    'row_id': component_id
                }).execute()
                
        except Exception as e:
            logger.debug(f"Failed to track usage: {e}")