#!/usr/bin/env python3
"""
Figma MCP Server - Hybrid Implementation
Combines direct Figma API access with database caching for optimal performance

Features:
- Direct Figma API for fresh data
- Database caching for fast access
- Automatic sync and cache management
- Fallback mechanisms for reliability
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timezone
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("=== Figma MCP Server (Hybrid Mode) Starting ===")

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import array params fix
try:
    from array_params_fix import apply_array_params_fix
    apply_array_params_fix()
    logger.info("Array parameters fix applied successfully")
except ImportError:
    logger.warning("Could not import array_params_fix")

# FastMCP for HTTP serving
from fastmcp import FastMCP

# Import our modules
from figma_client import FigmaClient
from file_generator import FileGenerator
from database_integration import FigmaDatabase

# Initialize FastMCP server
mcp = FastMCP("figma-design-hybrid")

# Get configuration
FIGMA_TOKEN = os.getenv('FIGMA_PAT') or os.getenv('FIGMA_ACCESS_TOKEN')
if not FIGMA_TOKEN:
    logger.error("No Figma authentication token found!")
    logger.error("Set FIGMA_PAT or FIGMA_ACCESS_TOKEN environment variable")
    sys.exit(1)

# Initialize components
figma_client = FigmaClient(FIGMA_TOKEN)
file_generator = FileGenerator()
database = FigmaDatabase()

# Tool: Validate access to both Figma API and database
@mcp.tool()
async def validate_hybrid_access() -> Dict[str, Any]:
    """
    Validates access to both Figma API and database.
    Checks authentication, permissions, and connectivity.
    
    Returns:
        Status of Figma API and database connections
    """
    try:
        # Check Figma API
        figma_status = await figma_client.validate_token()
        
        # Check database
        db_connected = database.is_connected()
        db_status = {
            "connected": db_connected,
            "url": database.supabase_url if db_connected else None
        }
        
        # Get database stats if connected
        if db_connected:
            try:
                # Count components
                result = database.client.table('figma_components').select('count', count='exact').execute()
                db_status['component_count'] = result.count if hasattr(result, 'count') else 0
                
                # Get categories
                categories = await database.get_categories()
                db_status['categories'] = len(categories)
                
            except Exception as e:
                logger.error(f"Failed to get database stats: {e}")
                db_status['error'] = str(e)
        
        return {
            "success": True,
            "figma_api": figma_status,
            "database": db_status,
            "mode": "hybrid" if db_connected else "api-only"
        }
        
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "mode": "error"
        }

# Tool: Smart component search (DB first, then API)
@mcp.tool()
async def search_components(
    search_term: Optional[str] = None,
    category: Optional[str] = None,
    file_url: Optional[str] = None,
    use_cache: bool = True,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Search for Figma components using database cache first, then API if needed.
    
    Args:
        search_term: Search query for component names
        category: Filter by category (ui, layout, forms, etc.)
        file_url: Figma file URL to search within
        use_cache: Whether to use database cache (default: True)
        limit: Maximum results to return
        
    Returns:
        List of matching components with metadata
    """
    try:
        results = []
        
        # Try database first if cache is enabled
        if use_cache and database.is_connected():
            logger.info(f"Searching database for: {search_term}")
            results = await database.search_components(
                search_term=search_term,
                category=category,
                limit=limit
            )
            
            if results:
                logger.info(f"Found {len(results)} components in cache")
                return {
                    "success": True,
                    "source": "database",
                    "components": results,
                    "count": len(results)
                }
        
        # Fallback to API if no cache results or cache disabled
        if file_url:
            logger.info("Fetching components from Figma API")
            
            # Parse file URL
            file_key = figma_client._extract_file_key(file_url)
            if not file_key:
                return {
                    "success": False,
                    "error": "Invalid Figma file URL"
                }
            
            # Get components from API
            api_components = await figma_client.get_file_components(file_key)
            
            # Filter by search term if provided
            if search_term and api_components:
                search_lower = search_term.lower()
                api_components = [
                    c for c in api_components 
                    if search_lower in c.get('name', '').lower()
                ]
            
            # Cache results in database if connected
            if database.is_connected() and api_components:
                logger.info(f"Caching {len(api_components)} components")
                stats = await database.sync_from_figma(api_components)
                logger.info(f"Cache stats: {stats}")
            
            return {
                "success": True,
                "source": "figma-api",
                "components": api_components[:limit],
                "count": len(api_components),
                "cached": database.is_connected()
            }
        
        # No results
        return {
            "success": True,
            "source": "none",
            "components": [],
            "count": 0,
            "message": "No components found. Provide a file_url to search Figma directly."
        }
        
    except Exception as e:
        logger.error(f"Component search failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# Tool: Get component details with caching
@mcp.tool()
async def get_component_details(
    component_id: str,
    file_url: Optional[str] = None,
    refresh: bool = False
) -> Dict[str, Any]:
    """
    Get detailed information about a specific component.
    
    Args:
        component_id: Figma node ID of the component
        file_url: Figma file URL containing the component
        refresh: Force refresh from API instead of cache
        
    Returns:
        Detailed component information including properties and code
    """
    try:
        component_data = None
        
        # Try database first unless refresh requested
        if not refresh and database.is_connected():
            logger.info(f"Checking cache for component: {component_id}")
            component_data = await database.get_component(component_id)
            
            if component_data:
                logger.info("Component found in cache")
                
                # Generate code preview
                code_preview = file_generator.generate_component_preview(component_data)
                
                return {
                    "success": True,
                    "source": "database",
                    "component": component_data,
                    "code_preview": code_preview
                }
        
        # Fetch from API if not in cache or refresh requested
        if file_url:
            logger.info(f"Fetching component {component_id} from Figma API")
            
            file_key = figma_client._extract_file_key(file_url)
            if not file_key:
                return {
                    "success": False,
                    "error": "Invalid Figma file URL"
                }
            
            # Get component from API
            component_data = await figma_client.get_node_data(file_key, component_id)
            
            if component_data:
                # Cache in database
                if database.is_connected():
                    await database.cache_component(component_data)
                
                # Generate code preview
                code_preview = file_generator.generate_component_preview(component_data)
                
                return {
                    "success": True,
                    "source": "figma-api",
                    "component": component_data,
                    "code_preview": code_preview,
                    "cached": database.is_connected()
                }
        
        return {
            "success": False,
            "error": "Component not found. Provide file_url to fetch from Figma."
        }
        
    except Exception as e:
        logger.error(f"Failed to get component details: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# Tool: Generate component with database tracking
@mcp.tool()
async def generate_component_with_tracking(
    component_id: str,
    output_dir: str = "./generated/components",
    component_name: Optional[str] = None,
    file_url: Optional[str] = None,
    framework: str = "react",
    typescript: bool = True,
    include_stories: bool = True,
    include_tests: bool = True
) -> Dict[str, Any]:
    """
    Generate component files from Figma with database tracking.
    
    Args:
        component_id: Figma node ID of the component
        output_dir: Directory to write the generated files
        component_name: Custom name for the component
        file_url: Figma file URL containing the component
        framework: Target framework (react, vue, angular)
        typescript: Generate TypeScript files
        include_stories: Generate Storybook stories
        include_tests: Generate test files
        
    Returns:
        Generated file paths and content
    """
    try:
        # Get component data (from cache or API)
        details_result = await get_component_details(component_id, file_url)
        
        if not details_result.get('success'):
            return details_result
        
        component_data = details_result.get('component')
        
        # Generate files
        generation_result = await file_generator.generate_component(
            component_data,
            output_dir=output_dir,
            component_name=component_name,
            typescript=typescript,
            include_stories=include_stories,
            include_tests=include_tests
        )
        
        # Save to database if connected
        if database.is_connected() and generation_result.get('success'):
            files = generation_result.get('files', [])
            
            for file_info in files:
                await database.save_generated_file(
                    component_id=component_id,
                    file_path=file_info['path'],
                    content=file_info.get('content', ''),
                    file_type=file_info['type'],
                    framework=framework
                )
            
            # Track usage
            db_component = await database.get_component(component_id)
            if db_component:
                await database._track_usage(db_component['id'], 'generated')
        
        return {
            "success": True,
            "component_id": component_id,
            "component_name": component_data.get('name'),
            "files": generation_result.get('files', []),
            "source": details_result.get('source'),
            "tracked": database.is_connected()
        }
        
    except Exception as e:
        logger.error(f"Component generation failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# Tool: Sync Figma file to database
@mcp.tool()
async def sync_figma_to_database(
    file_url: str,
    sync_type: str = "full",
    component_filter: Optional[str] = None
) -> Dict[str, Any]:
    """
    Sync components from a Figma file to the database.
    
    Args:
        file_url: Figma file URL to sync
        sync_type: Type of sync (full, incremental)
        component_filter: Optional filter for component names
        
    Returns:
        Sync statistics and status
    """
    try:
        if not database.is_connected():
            return {
                "success": False,
                "error": "Database not connected. Set SUPABASE_SERVICE_KEY environment variable."
            }
        
        # Extract file key
        file_key = figma_client._extract_file_key(file_url)
        if not file_key:
            return {
                "success": False,
                "error": "Invalid Figma file URL"
            }
        
        logger.info(f"Starting {sync_type} sync for file: {file_key}")
        
        # Get all components from Figma
        components = await figma_client.get_file_components(file_key)
        
        # Apply filter if provided
        if component_filter:
            filter_lower = component_filter.lower()
            components = [
                c for c in components
                if filter_lower in c.get('name', '').lower()
            ]
        
        logger.info(f"Found {len(components)} components to sync")
        
        # Sync to database
        stats = await database.sync_from_figma(components)
        
        return {
            "success": True,
            "file_key": file_key,
            "sync_type": sync_type,
            "stats": stats,
            "message": f"Synced {stats['added']} new and {stats['updated']} updated components"
        }
        
    except Exception as e:
        logger.error(f"Sync failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# Tool: Get database statistics
@mcp.tool()
async def get_database_stats() -> Dict[str, Any]:
    """
    Get statistics about the component database.
    
    Returns:
        Database statistics including counts and categories
    """
    try:
        if not database.is_connected():
            return {
                "success": False,
                "error": "Database not connected"
            }
        
        stats = {}
        
        # Get component count
        comp_result = database.client.table('figma_components').select('count', count='exact').execute()
        stats['total_components'] = comp_result.count if hasattr(comp_result, 'count') else 0
        
        # Get category breakdown
        categories = await database.get_categories()
        stats['categories'] = len(categories)
        stats['category_list'] = [cat['name'] for cat in categories]
        
        # Get recent syncs
        sync_result = database.client.table('sync_history').select('*').order('started_at', desc=True).limit(5).execute()
        stats['recent_syncs'] = len(sync_result.data) if sync_result.data else 0
        
        # Get popular components
        popular_result = database.client.table('figma_components').select('name,popularity_score').order('popularity_score', desc=True).limit(10).execute()
        stats['popular_components'] = [
            {"name": comp['name'], "score": comp['popularity_score']}
            for comp in (popular_result.data or [])
        ]
        
        return {
            "success": True,
            "stats": stats,
            "database_url": database.supabase_url
        }
        
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# Server startup
if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Figma MCP Server in Hybrid Mode")
    logger.info(f"Database: {'Connected' if database.is_connected() else 'Not connected'}")
    logger.info("Server ready for connections")
    
    # Get the FastAPI app from FastMCP
    app = mcp.get_app()
    
    # Run with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)