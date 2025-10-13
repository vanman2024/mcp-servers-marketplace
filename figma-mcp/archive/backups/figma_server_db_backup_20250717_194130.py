#!/usr/bin/env python3
"""
Figma MCP Server - Database-Powered Implementation
Fast component access through Supabase database instead of direct Figma API

Provides tools for:
- Fast component search and filtering through database
- Component preview with metadata from database  
- Code generation using cached component data
- Design system management with 981+ ShadCN components
- High-performance operations without API timeouts
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timezone
import asyncio
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("=== Figma MCP Server (Database-Powered) Starting ===")
logger.info("Python version: %s", sys.version)
logger.info("Working directory: %s", os.getcwd())

# Add parent directory to path for array_params_fix import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import and apply the array parameters fix
try:
    from array_params_fix import apply_array_params_fix
    apply_array_params_fix()
    logger.info("Array parameters fix applied successfully")
except ImportError:
    logger.warning("Could not import array_params_fix - array parameters may not work correctly")

# FastMCP for HTTP serving
from fastmcp import FastMCP

# Supabase client for database operations
from supabase import create_client, Client
import httpx

# Initialize FastMCP server
mcp = FastMCP("figma-design")

# ===================================================================
# PLANNING DOCUMENT STORAGE (Simple PRD approach)
# ===================================================================

# Planning docs directory
PLANNING_DIR = os.path.join(os.path.dirname(__file__), "../planning_docs")

def _ensure_planning_dir():
    """Ensure planning docs directory exists"""
    os.makedirs(PLANNING_DIR, exist_ok=True)

def save_planning_doc(app_name: str, content: str) -> str:
    """Save a planning document (PRD) for an application"""
    _ensure_planning_dir()
    
    doc_file = os.path.join(PLANNING_DIR, f"{app_name}_prd.md")
    with open(doc_file, 'w') as f:
        f.write(content)
    
    logger.info(f"Saved planning doc for {app_name}")
    return doc_file

def load_planning_doc(app_name: str) -> Optional[str]:
    """Load planning document for an application"""
    doc_file = os.path.join(PLANNING_DIR, f"{app_name}_prd.md")
    
    if os.path.exists(doc_file):
        try:
            with open(doc_file, 'r') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to load planning doc for {app_name}: {e}")
            return None
    
    return None

@mcp.resource("figma-db://conversation/context/{session_id}")
def get_conversation_context_resource(session_id: str) -> str:
    """MCP Resource: Get conversation context for intelligent app generation"""
    context = get_conversation_context(session_id)
    if context:
        return json.dumps(context, indent=2)
    else:
        # List available session files
        available_sessions = []
        if os.path.exists(CONTEXT_DIR):
            for filename in os.listdir(CONTEXT_DIR):
                if filename.endswith('.json'):
                    available_sessions.append(filename.replace('.json', ''))
        
        return json.dumps({
            "error": "No context found for this session",
            "session_id": session_id,
            "available_sessions": available_sessions,
            "context_storage_location": CONTEXT_DIR
        }, indent=2)

# ===================================================================
# SUPABASE DATABASE CLIENT
# ===================================================================

class FigmaComponentDatabase:
    """Database client for Figma components stored in Supabase"""
    
    def __init__(self, url: str, service_key: str):
        self.url = url
        self.service_key = service_key
        self.supabase: Client = create_client(url, service_key)
        logger.info(f"Figma component database initialized: {url}")
    
    async def search_components(self, search_term: Optional[str] = None, 
                              category_filter: Optional[str] = None,
                              limit: int = 20) -> List[Dict[str, Any]]:
        """Search components using the database search function"""
        try:
            # Use the search_components function we created in the schema
            result = self.supabase.rpc(
                'search_components',
                {
                    'search_term': search_term,
                    'category_filter': category_filter, 
                    'limit_results': limit
                }
            ).execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Component search failed: {e}")
            return []
    
    async def get_component_by_id(self, component_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific component by ID"""
        try:
            result = self.supabase.table('figma_components').select('*').eq('id', component_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to get component {component_id}: {e}")
            return None
    
    async def get_component_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a component by exact name match"""
        try:
            result = self.supabase.table('figma_components').select('*').eq('name', name).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to get component by name {name}: {e}")
            return None
    
    async def get_components_by_type(self, component_type: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get components by type (button, card, input, etc.) using name pattern matching"""
        try:
            # Map component types to search patterns
            search_patterns = {
                'button': '%button%',
                'card': '%card%', 
                'input': '%input%',
                'form': '%form%',
                'modal': '%modal%',
                'dropdown': '%dropdown%',
                'navigation': '%nav%',
                'avatar': '%avatar%',
                'badge': '%badge%',
                'tab': '%tab%',
                'slider': '%slider%',
                'checkbox': '%checkbox%',
                'radio': '%radio%',
                'toggle': '%toggle%',
                'list': '%list%',
                'table': '%table%',
                'grid': '%grid%',
                'icon': '%icon%',
                'tooltip': '%tooltip%',
                'alert': '%alert%'
            }
            
            pattern = search_patterns.get(component_type.lower(), f'%{component_type}%')
            
            result = self.supabase.table('figma_components')\
                .select('*')\
                .ilike('name', pattern)\
                .order('popularity_score', desc=True)\
                .limit(limit)\
                .execute()
            
            components = result.data if result.data else []
            logger.info(f"Found {len(components)} components for type: {component_type}")
            return components
        except Exception as e:
            logger.error(f"Failed to get components by type {component_type}: {e}")
            return []
    
    async def get_categories(self) -> List[Dict[str, Any]]:
        """Get all component categories"""
        try:
            result = self.supabase.table('figma_component_categories')\
                .select('*')\
                .order('sort_order')\
                .execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Failed to get categories: {e}")
            return []
    
    async def record_component_usage(self, component_id: str, action_type: str = 'previewed', 
                                   project_name: Optional[str] = None) -> bool:
        """Record component usage for analytics"""
        try:
            # Try to insert usage record, handle gracefully if table doesn't exist
            try:
                self.supabase.table('component_usage').insert({
                    'component_id': component_id,
                    'action_type': action_type,
                    'project_name': project_name,
                    'user_session': 'mcp-session',
                    'metadata': {'source': 'figma-mcp'}
                }).execute()
            except Exception as usage_e:
                logger.debug(f"Usage tracking skipped (table may not exist): {usage_e}")
            
            # Update usage frequency - this should work as it's in the main table
            try:
                self.supabase.rpc('increment_popularity_score', {'comp_id': component_id}).execute()
            except Exception as pop_e:
                logger.debug(f"Popularity score update skipped: {pop_e}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to record usage: {e}")
            return False

# Environment variable checking
logger.info("Checking environment variables...")

supabase_url = os.getenv('SUPABASE_URL')
supabase_service_key = os.getenv('SUPABASE_SERVICE_KEY')

if not supabase_url or not supabase_service_key:
    logger.error("SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables required")
    raise ValueError("Supabase configuration missing")

logger.info("✓ SUPABASE_URL detected")
logger.info("✓ SUPABASE_SERVICE_KEY detected")

# Initialize database client
db_client = FigmaComponentDatabase(supabase_url, supabase_service_key)

# ===================================================================
# MCP TOOLS - Database-Powered Figma Operations
# ===================================================================

@mcp.tool()
async def validate_database_access() -> Dict[str, Any]:
    """
    Validates database connection and component data availability
    
    Returns:
        Database status and component count
    """
    try:
        logger.info("Validating database access...")
        
        # Test database connection by getting component count
        result = db_client.supabase.table('figma_components').select('id', count='exact').execute()
        component_count = result.count if hasattr(result, 'count') else 0
        
        # Get categories count
        categories = await db_client.get_categories()
        category_count = len(categories)
        
        logger.info(f"Database validation successful: {component_count} components, {category_count} categories")
        
        return {
            "success": True,
            "status": "connected",
            "database_connected": True,
            "component_count": component_count,
            "category_count": category_count,
            "categories": [cat['name'] for cat in categories],
            "message": f"Database access validated - {component_count} components available"
        }
        
    except Exception as e:
        logger.error(f"Database validation failed: {e}")
        return {
            "success": False,
            "database_connected": False,
            "error": str(e),
            "message": "Database connection failed"
        }

@mcp.tool()
async def preview_figma_components(
    component_filter: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Preview and search Figma components from database with fast filtering
    
    Args:
        component_filter: Search term to filter components (name, description, tags)
        category: Filter by category (ui, layout, forms, etc.)
        limit: Maximum number of components to return (default: 20)
    
    Returns:
        List of matching components with metadata
    """
    try:
        logger.info(f"Searching components: filter='{component_filter}', category='{category}', limit={limit}")
        
        # Search components using database
        components = await db_client.search_components(
            search_term=component_filter,
            category_filter=category,
            limit=limit
        )
        
        if not components:
            return {
                "success": True,
                "components": [],
                "count": 0,
                "message": f"No components found matching filter: '{component_filter}'"
            }
        
        # Record usage analytics for previewed components
        # TODO: Implement component_usage table
        # for component in components[:5]:  # Track top 5 for analytics
        #     await db_client.record_component_usage(component['id'], 'previewed')
        
        # Format response
        formatted_components = []
        for comp in components:
            formatted_components.append({
                "id": comp['id'],
                "name": comp['name'],
                "description": comp.get('description', ''),
                "type": comp['component_type'],
                "category": comp.get('category_name', ''),
                "tags": comp.get('tags', []),
                "figma_url": comp['figma_url'],
                "popularity_score": comp.get('popularity_score', 0),
                "complexity_level": comp.get('complexity_level', 1),
                "shadcn_mapping": comp.get('shadcn_mapping'),
                "last_synced": comp.get('last_synced_at')
            })
        
        logger.info(f"Found {len(components)} components")
        
        return {
            "success": True,
            "components": formatted_components,
            "count": len(components),
            "filter_applied": component_filter,
            "category_applied": category,
            "message": f"Found {len(components)} components"
        }
        
    except Exception as e:
        logger.error(f"Component preview failed: {e}")
        return {
            "success": False,
            "components": [],
            "error": str(e),
            "message": "Component preview failed"
        }

@mcp.tool()
async def get_component_details(
    component_name: str
) -> Dict[str, Any]:
    """
    Get detailed information about a specific component
    
    Args:
        component_name: The exact name of the component
    
    Returns:
        Detailed component information including properties and generated code
    """
    try:
        logger.info(f"Getting details for component: {component_name}")
        
        # Get component from database
        component = await db_client.get_component_by_name(component_name)
        
        if not component:
            return {
                "success": False,
                "error": f"Component '{component_name}' not found",
                "message": "Component not found in database"
            }
        
        # Record usage
        await db_client.record_component_usage(component['id'], 'detailed_view')
        
        # Get generated files if any
        try:
            files_result = db_client.supabase.table('generated_files')\
                .select('*')\
                .eq('component_id', component['id'])\
                .execute()
            generated_files = files_result.data if files_result.data else []
        except:
            generated_files = []
        
        return {
            "success": True,
            "component": {
                "id": component['id'],
                "name": component['name'],
                "description": component.get('description', ''),
                "component_type": component['component_type'],
                "category": component['category'],
                "tags": component.get('tags', []),
                "figma_url": component['figma_url'],
                "figma_node_id": component['figma_node_id'],
                "figma_properties": component.get('figma_properties', {}),
                "design_tokens": component.get('design_tokens', {}),
                "variants": component.get('variants', {}),
                "shadcn_mapping": component.get('shadcn_mapping'),
                "complexity_level": component.get('complexity_level', 1),
                "popularity_score": component.get('popularity_score', 0),
                "react_generated": component.get('react_generated', False),
                "vue_generated": component.get('vue_generated', False),
                "last_synced_at": component.get('last_synced_at'),
                "generated_files": generated_files
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get component details: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve component details"
        }

@mcp.tool()
async def list_component_categories() -> Dict[str, Any]:
    """
    List all available component categories with descriptions
    
    Returns:
        List of categories with details
    """
    try:
        logger.info("Retrieving component categories")
        
        categories = await db_client.get_categories()
        
        return {
            "success": True,
            "categories": categories,
            "count": len(categories),
            "message": f"Found {len(categories)} categories"
        }
        
    except Exception as e:
        logger.error(f"Failed to get categories: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve categories"
        }

@mcp.tool()
async def get_components_by_type(
    component_type: str,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Get all components of a specific type (button, card, input, etc.)
    
    Args:
        component_type: The type of component to retrieve
        limit: Maximum number of components to return
    
    Returns:
        List of components of the specified type
    """
    try:
        logger.info(f"Getting components of type: {component_type}")
        
        components = await db_client.get_components_by_type(component_type, limit)
        
        if not components:
            return {
                "success": True,
                "components": [],
                "count": 0,
                "message": f"No components found of type: {component_type}"
            }
        
        return {
            "success": True,
            "components": components,
            "count": len(components),
            "component_type": component_type,
            "message": f"Found {len(components)} {component_type} components"
        }
        
    except Exception as e:
        logger.error(f"Failed to get components by type: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to retrieve {component_type} components"
        }

@mcp.tool()
async def bulk_create_component_files(
    app_type: str,
    output_directory: str,
    create_index: bool = True
) -> Dict[str, Any]:
    """
    Generate and SAVE React component files to disk for a complete app
    Creates actual .tsx files in your project directory
    
    Args:
        app_type: Type of app to build (todo, dashboard, blog, ecommerce, etc.)
        output_directory: Directory path where files should be created
        create_index: Whether to create an index.ts file exporting all components
    
    Returns:
        List of created files and their paths
    
    Example:
        bulk_create_component_files("todo", "./src/components")
        Creates: ./src/components/TodoButton.tsx, TodoCard.tsx, etc.
    """
    import os
    import json
    
    try:
        logger.info(f"Bulk creating component files for {app_type} app in {output_directory}")
        
        # First generate all components
        components_result = await _build_app_components_internal(app_type, include_dependencies=True)
        
        if not components_result["success"]:
            return components_result
        
        # Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
        components_dir = os.path.join(output_directory, "components")
        ui_components_dir = os.path.join(components_dir, "ui")
        os.makedirs(components_dir, exist_ok=True)
        os.makedirs(ui_components_dir, exist_ok=True)
        
        created_files = []
        
        # Write each component file
        for file_data in components_result["generated_files"]:
            filename = file_data["filename"]
            component_type = file_data.get("component_type", "").lower()
            
            # Handle different file placements
            if filename.startswith("lib/"):
                # Create lib directory and place file there
                lib_dir = os.path.join(output_directory, "lib")
                os.makedirs(lib_dir, exist_ok=True)
                file_path = os.path.join(output_directory, filename)
            elif component_type in ["button", "card", "input", "label", "select", "textarea", "checkbox", "radio"]:
                # Place UI components in components/ui/
                file_path = os.path.join(ui_components_dir, filename)
            elif component_type in ["config", "docs", "index"]:
                # Place config files at root level
                file_path = os.path.join(output_directory, filename)
            elif component_type in ["page"]:
                # Place pages in pages/ directory
                pages_dir = os.path.join(output_directory, "pages")
                os.makedirs(pages_dir, exist_ok=True)
                file_path = os.path.join(pages_dir, filename)
            elif component_type in ["hook", "context"]:
                # Place hooks and contexts in hooks/ directory
                hooks_dir = os.path.join(output_directory, "hooks")
                os.makedirs(hooks_dir, exist_ok=True)
                file_path = os.path.join(hooks_dir, filename)
            elif component_type in ["header", "footer", "layout", "form", "list"]:
                # Place layout and complex components in components/
                file_path = os.path.join(components_dir, filename)
            else:
                # Place app-specific components in components/
                file_path = os.path.join(components_dir, filename)
            
            try:
                # Ensure parent directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_data["content"])
                
                created_files.append({
                    "path": file_path,
                    "filename": file_data["filename"],
                    "component_type": file_data["component_type"],
                    "size": len(file_data["content"])
                })
                
                logger.info(f"Created: {file_path}")
                
            except Exception as e:
                logger.error(f"Failed to write {file_path}: {e}")
        
        # Create index.ts file if requested
        if create_index and created_files:
            index_content = "// Auto-generated component exports\n\n"
            
            for file_info in created_files:
                component_name = file_info["filename"].replace(".tsx", "")
                index_content += f'export {{ {component_name} }} from "./{component_name}";\n'
            
            index_path = os.path.join(components_dir, "index.ts")
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            created_files.append({
                "path": index_path,
                "filename": "index.ts", 
                "component_type": "index",
                "size": len(index_content)
            })
        
        # Create package.json if we have dependencies
        if components_result.get("dependencies"):
            package_json = {
                "name": f"{app_type}-components",
                "version": "1.0.0",
                "description": f"Generated {app_type} components from Figma",
                "dependencies": {
                    dep: "latest" for dep in components_result["dependencies"]
                }
            }
            
            package_path = os.path.join(output_directory, "package.json")
            with open(package_path, 'w', encoding='utf-8') as f:
                json.dump(package_json, f, indent=2)
            
            created_files.append({
                "path": package_path,
                "filename": "package.json",
                "component_type": "config",
                "size": len(json.dumps(package_json))
            })
        
        # Create tsconfig.json for TypeScript
        tsconfig = {
            "compilerOptions": {
                "target": "ES2020",
                "useDefineForClassFields": True,
                "lib": ["ES2020", "DOM", "DOM.Iterable"],
                "module": "ESNext",
                "skipLibCheck": True,
                "moduleResolution": "bundler",
                "allowImportingTsExtensions": True,
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx",
                "strict": True,
                "noUnusedLocals": True,
                "noUnusedParameters": True,
                "noFallthroughCasesInSwitch": True,
                "paths": {
                    "@/*": ["./*"]
                }
            },
            "include": ["components"],
        }
        
        tsconfig_path = os.path.join(output_directory, "tsconfig.json")
        with open(tsconfig_path, 'w', encoding='utf-8') as f:
            json.dump(tsconfig, f, indent=2)
        
        created_files.append({
            "path": tsconfig_path,
            "filename": "tsconfig.json",
            "component_type": "config",
            "size": len(json.dumps(tsconfig))
        })
        
        # Create README.md
        readme_content = f"""# {app_type.title()} App Components

Generated from Figma design system using figma-db-http MCP server.

## Components

"""
        for file_info in created_files:
            if file_info["component_type"] not in ["config", "index"]:
                readme_content += f"- **{file_info['filename']}** - {file_info['component_type']} component\n"
        
        readme_content += f"""
## Installation

```bash
npm install
```

## Usage

```tsx
import {{ {', '.join([f['filename'].replace('.tsx', '') for f in created_files if f['component_type'] not in ['config', 'index']])} }} from './components';
```

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        readme_path = os.path.join(output_directory, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        created_files.append({
            "path": readme_path,
            "filename": "README.md",
            "component_type": "docs",
            "size": len(readme_content)
        })
        
        total_size = sum(f["size"] for f in created_files)
        
        logger.info(f"Successfully created {len(created_files)} files totaling {total_size} bytes")
        
        return {
            "success": True,
            "app_type": app_type,
            "output_directory": output_directory,
            "created_files": created_files,
            "file_count": len(created_files),
            "total_size": total_size,
            "dependencies": components_result.get("dependencies", []),
            "message": f"Successfully created {len(created_files)} files in {output_directory}"
        }
        
    except Exception as e:
        logger.error(f"Failed to bulk create files: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to create component files for {app_type} app"
        }

async def _build_app_components_internal(
    app_type: str,
    include_dependencies: bool = True
) -> Dict[str, Any]:
    """Internal function to generate React components using curated templates"""
    try:
        logger.info(f"Building components for app type: {app_type}")
        
        # Get components from database based on app requirements
        app_requirements = {
            "todo": ["button", "card", "input", "form", "list"],
            "dashboard": ["card", "button", "chart", "table", "sidebar"],
            "blog": ["card", "button", "input", "form", "list", "editor"],
            "ecommerce": ["card", "button", "input", "form", "list", "cart"],
            "landing": ["button", "card", "hero", "pricing"],
            "admin": ["button", "card", "input", "table", "form", "sidebar"],
            "full": ["button", "card", "input", "form", "list", "table", "chart", "modal", "dropdown"]
        }
        
        # Get required component types for this app
        required_types = app_requirements.get(app_type.lower(), ["button", "card", "input"])
        
        # Generate components from database
        generated_files = []
        dependencies_set = set()
        
        for comp_type in required_types:
            # Smart component selection based on application context
            components = await _smart_component_selection(app_type, comp_type, limit=1)
            
            if not components:
                logger.warning(f"No components found in database for type: {comp_type}")
                continue
                
            # Use the first (best) component for this type
            component = components[0]
            component_name = f"{app_type.title()}{comp_type.title()}"
            
            # Generate React component from database component
            react_code = await _generate_react_from_database_component(component, component_name)
            
            if react_code:
                # Since this is in-memory generation, just store the component data
                filename = f"{component_name}.tsx"
                
                generated_files.append({
                    "filename": filename,
                    "component_type": comp_type,
                    "component_name": component_name,
                    "content": react_code,
                    "size": len(react_code)
                })
                
                # Add React dependency
                dependencies_set.add("react")
                dependencies_set.add("clsx")
                dependencies_set.add("tailwind-merge")
        
        # Include dependency management if requested
        if include_dependencies:
            # Add utility files
            generated_files.extend([
                {
                    "filename": "lib/utils.ts",
                    "component_type": "util",
                    "content": """import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
""",
                    "size": 159
                },
                {
                    "filename": "package.json",
                    "component_type": "config", 
                    "content": json.dumps({
                        "name": f"{app_type}-app",
                        "version": "0.1.0",
                        "dependencies": {
                            "react": "^18.0.0",
                            "clsx": "^2.0.0",
                            "tailwind-merge": "^2.0.0"
                        }
                    }, indent=2),
                    "size": 200
                }
            ])
        
        return {
            "success": True,
            "generated_files": generated_files,
            "total_files": len(generated_files),
            "message": f"Generated {len(generated_files)} components for {app_type} app"
        }
        
    except Exception as e:
        logger.error(f"Component generation failed: {e}")
        return {"success": False, "error": str(e)}

async def _smart_component_selection(app_type, comp_type, limit=1):
    """Intelligently select components based on application context"""
    try:
        # Application-specific component preferences
        app_component_preferences = {
            "dashboard": {
                "button": ["primary action", "secondary", "ghost"],
                "card": ["data card", "metric card", "dashboard card", "stats card", "analytics card"],
                "chart": ["line chart", "bar chart", "pie chart", "area chart"],
                "table": ["data table", "sortable table", "paginated table"],
                "navigation": ["top nav", "sidebar nav", "breadcrumb"],
                "header": ["page header", "dashboard header"],
                "form": ["filter form", "search form", "settings form"]
            },
            "ecommerce": {
                "button": ["add to cart", "buy now", "primary", "checkout"],
                "card": ["product card", "shopping card", "price card", "category card"],
                "form": ["checkout form", "shipping form", "payment form", "review form"],
                "navigation": ["shop nav", "category nav", "breadcrumb"],
                "header": ["shop header", "product header"],
                "list": ["product list", "cart items", "order list"]
            },
            "todo": {
                "button": ["primary", "ghost", "destructive", "add task"],
                "card": ["task card", "simple card", "todo item"],
                "form": ["add task", "edit form", "filter form"],
                "list": ["task list", "todo list", "completed list"],
                "navigation": ["simple nav", "tab nav"],
                "header": ["app header", "minimal header"]
            },
            "blog": {
                "button": ["read more", "primary", "ghost", "subscribe"],
                "card": ["article card", "post card", "blog card", "author card"],
                "form": ["comment form", "contact form", "newsletter form"],
                "navigation": ["blog nav", "category nav", "pagination"],
                "header": ["blog header", "article header"],
                "list": ["post list", "comment list", "category list"]
            },
            "saas": {
                "button": ["get started", "primary", "secondary", "upgrade"],
                "card": ["pricing card", "feature card", "testimonial card"],
                "form": ["signup form", "contact form", "demo form"],
                "navigation": ["landing nav", "app nav", "footer nav"],
                "header": ["hero header", "feature header"],
                "section": ["hero section", "feature section", "pricing section"]
            }
        }
        
        # Get application preferences
        app_prefs = app_component_preferences.get(app_type, {})
        comp_prefs = app_prefs.get(comp_type, [])
        
        # Search with semantic context
        if comp_prefs:
            # Try to find components matching application context
            for pref in comp_prefs:
                components = await db_client.search_components(
                    search_term=f"{comp_type} {pref}",
                    category_filter=comp_type,
                    limit=limit
                )
                if components:
                    logger.info(f"Found {len(components)} {comp_type} components for {app_type} app with preference '{pref}'")
                    return components
        
        # Fallback to best rated components of this type
        components = await db_client.get_components_by_type(comp_type, limit=limit*3)
        if components:
            # Sort by quality indicators (name length, description quality, etc.)
            sorted_components = sorted(components, key=lambda c: (
                -len(c.get('description', '')),  # Prefer detailed descriptions
                -len(c.get('properties', {})),   # Prefer more props
                c.get('name', '').lower()        # Alphabetical for consistency
            ))
            return sorted_components[:limit]
        
        return []
        
    except Exception as e:
        logger.error(f"Smart component selection failed: {e}")
        return []

async def _generate_react_from_database_component(component, component_name):
    """Generate React TypeScript component code from database component data"""
    try:
        # Extract component properties from database
        component_props = component.get('properties', {})
        component_description = component.get('description', '')
        component_code = component.get('code', '')
        
        # If we have existing code, use it as base
        if component_code:
            # Replace template variables in existing code
            react_code = component_code.replace('{{ComponentName}}', component_name)
            react_code = react_code.replace('{{componentName}}', component_name.lower())
            return react_code
        
        # Otherwise generate from properties
        props_interface = ""
        if component_props:
            props_list = []
            for prop_name, prop_data in component_props.items():
                prop_type = prop_data.get('type', 'string')
                is_optional = prop_data.get('optional', True)
                optional_marker = '?' if is_optional else ''
                props_list.append(f"  {prop_name}{optional_marker}: {prop_type};")
            
            if props_list:
                props_interface = f"""
export interface {component_name}Props {{
{chr(10).join(props_list)}
}}
"""
        
        # Generate base React component template
        react_template = f"""import React from 'react';
import {{ cn }} from '@/lib/utils';
{props_interface}
const {component_name} = React.forwardRef<HTMLDivElement, {component_name}Props>(
  ({{ className, ...props }}, ref) => {{
    return (
      <div
        ref={{ref}}
        className={{cn(
          "rounded-lg border bg-card text-card-foreground shadow-sm",
          className
        )}}
        {{...props}}
      />
    );
  }}
);

{component_name}.displayName = "{component_name}";

export {{ {component_name} }};"""
        
        return react_template
        
    except Exception as e:
        logger.error(f"Failed to generate React code for component: {e}")
        return None

        # Keep the application structure templates for non-UI components
        structure_templates = {
            "button": {
                "template": '''import React from 'react';
import { cn } from '@/lib/utils';

export interface {{ComponentName}}Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
}

const {{ComponentName}} = React.forwardRef<HTMLButtonElement, {{ComponentName}}Props>(
  ({ className, variant = 'default', size = 'default', ...props }, ref) => {
    const baseClasses = "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none";
    
    const variantClasses = {
      default: "bg-primary text-primary-foreground hover:bg-primary/90",
      destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
      outline: "border border-input hover:bg-accent hover:text-accent-foreground",
      secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
      ghost: "hover:bg-accent hover:text-accent-foreground",
      link: "underline-offset-4 hover:underline text-primary"
    };
    
    const sizeClasses = {
      default: "h-10 px-4 py-2",
      sm: "h-9 rounded-md px-3",
      lg: "h-11 rounded-md px-8",
      icon: "h-10 w-10"
    };

    return (
      <button
        className={cn(baseClasses, variantClasses[variant], sizeClasses[size], className)}
        ref={ref}
        {...props}
      />
    );
  }
);

{{ComponentName}}.displayName = "{{ComponentName}}";

export { {{ComponentName}} };''',
                "dependencies": ["class-variance-authority", "clsx", "tailwind-merge"]
            },
            "card": {
                "template": '''import React from 'react';
import { cn } from '@/lib/utils';

const {{ComponentName}} = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("rounded-lg border bg-card text-card-foreground shadow-sm", className)}
      {...props}
    />
  )
);
{{ComponentName}}.displayName = "{{ComponentName}}";

const {{ComponentName}}Header = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
  )
);
{{ComponentName}}Header.displayName = "{{ComponentName}}Header";

const {{ComponentName}}Title = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn("text-2xl font-semibold leading-none tracking-tight", className)}
      {...props}
    />
  )
);
{{ComponentName}}Title.displayName = "{{ComponentName}}Title";

const {{ComponentName}}Description = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
  )
);
{{ComponentName}}Description.displayName = "{{ComponentName}}Description";

const {{ComponentName}}Content = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
  )
);
{{ComponentName}}Content.displayName = "{{ComponentName}}Content";

const {{ComponentName}}Footer = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex items-center p-6 pt-0", className)} {...props} />
  )
);
{{ComponentName}}Footer.displayName = "{{ComponentName}}Footer";

export { {{ComponentName}}, {{ComponentName}}Header, {{ComponentName}}Footer, {{ComponentName}}Title, {{ComponentName}}Description, {{ComponentName}}Content };''',
                "dependencies": ["clsx", "tailwind-merge"]
            },
            "input": {
                "template": '''import React from 'react';
import { cn } from '@/lib/utils';

export interface {{ComponentName}}Props extends React.InputHTMLAttributes<HTMLInputElement> {}

const {{ComponentName}} = React.forwardRef<HTMLInputElement, {{ComponentName}}Props>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);
{{ComponentName}}.displayName = "{{ComponentName}}";

export { {{ComponentName}} };''',
                "dependencies": ["clsx", "tailwind-merge"]
            },
            "header": {
                "template": '''import React from 'react';
import { {{ComponentName}}Button } from '@/components/ui/{{ComponentName}}Button';
import { cn } from '@/lib/utils';

export function {{ComponentName}}Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 flex">
          <a className="mr-6 flex items-center space-x-2" href="/">
            <span className="hidden font-bold sm:inline-block">{{AppName}}</span>
          </a>
        </div>
        
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <nav className="flex items-center space-x-6 text-sm font-medium">
            <a href="/" className="transition-colors hover:text-foreground/80">Home</a>
            <a href="/dashboard" className="transition-colors hover:text-foreground/80">Dashboard</a>
            <a href="/settings" className="transition-colors hover:text-foreground/80">Settings</a>
          </nav>
          
          <div className="flex items-center space-x-2">
            <{{ComponentName}}Button variant="ghost" size="sm">
              Sign In
            </{{ComponentName}}Button>
            <{{ComponentName}}Button size="sm">
              Sign Up
            </{{ComponentName}}Button>
          </div>
        </div>
      </div>
    </header>
  );
}''',
                "dependencies": ["react"]
            },
            "footer": {
                "template": '''import React from 'react';

export function {{ComponentName}}Footer() {
  return (
    <footer className="border-t bg-background">
      <div className="container flex flex-col items-center justify-between gap-4 py-10 md:h-24 md:flex-row md:py-0">
        <div className="flex flex-col items-center gap-4 px-8 md:flex-row md:gap-2 md:px-0">
          <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
            Built with {{AppName}}. The source code is available on{" "}
            <a href="#" className="font-medium underline underline-offset-4">GitHub</a>.
          </p>
        </div>
        
        <div className="flex items-center space-x-4">
          <a href="#" className="text-sm text-muted-foreground hover:text-foreground">Privacy</a>
          <a href="#" className="text-sm text-muted-foreground hover:text-foreground">Terms</a>
          <a href="#" className="text-sm text-muted-foreground hover:text-foreground">Contact</a>
        </div>
      </div>
    </footer>
  );
}''',
                "dependencies": ["react"]
            },
            "form": {
                "template": '''import React, { useState } from 'react';
import { {{ComponentName}}Button } from '@/components/ui/{{ComponentName}}Button';
import { {{ComponentName}}Input } from '@/components/ui/{{ComponentName}}Input';
import { {{ComponentName}}Card, {{ComponentName}}CardContent, {{ComponentName}}CardHeader, {{ComponentName}}CardTitle } from '@/components/ui/{{ComponentName}}Card';

interface {{ComponentName}}FormProps {
  onSubmit: (data: any) => void;
  title?: string;
  fields?: Array<{
    name: string;
    label: string;
    type: string;
    required?: boolean;
    placeholder?: string;
  }>;
}

export function {{ComponentName}}Form({ 
  onSubmit, 
  title = "{{FormTitle}}", 
  fields = [
    { name: "name", label: "Name", type: "text", required: true, placeholder: "Enter your name" },
    { name: "email", label: "Email", type: "email", required: true, placeholder: "Enter your email" },
  ]
}: {{ComponentName}}FormProps) {
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: Record<string, string> = {};
    
    fields.forEach(field => {
      if (field.required && !formData[field.name]) {
        newErrors[field.name] = `${field.label} is required`;
      }
    });
    
    if (Object.keys(newErrors).length === 0) {
      onSubmit(formData);
    } else {
      setErrors(newErrors);
    }
  };

  const handleChange = (name: string, value: string) => {
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: "" }));
    }
  };

  return (
    <{{ComponentName}}Card className="w-full max-w-md">
      <{{ComponentName}}CardHeader>
        <{{ComponentName}}CardTitle>{title}</{{ComponentName}}CardTitle>
      </{{ComponentName}}CardHeader>
      <{{ComponentName}}CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {fields.map(field => (
            <div key={field.name} className="space-y-2">
              <label className="text-sm font-medium">{field.label}</label>
              <{{ComponentName}}Input
                type={field.type}
                placeholder={field.placeholder}
                value={formData[field.name] || ""}
                onChange={(e) => handleChange(field.name, e.target.value)}
                className={errors[field.name] ? "border-red-500" : ""}
              />
              {errors[field.name] && (
                <p className="text-sm text-red-500">{errors[field.name]}</p>
              )}
            </div>
          ))}
          <{{ComponentName}}Button type="submit" className="w-full">
            Submit
          </{{ComponentName}}Button>
        </form>
      </{{ComponentName}}CardContent>
    </{{ComponentName}}Card>
  );
}''',
                "dependencies": ["react"]
            },
            "list": {
                "template": '''import React from 'react';
import { {{ComponentName}}Card, {{ComponentName}}CardContent, {{ComponentName}}CardHeader, {{ComponentName}}CardTitle } from '@/components/ui/{{ComponentName}}Card';
import { {{ComponentName}}Button } from '@/components/ui/{{ComponentName}}Button';

interface {{ComponentName}}Item {
  id: string;
  title: string;
  description?: string;
  status?: string;
  createdAt?: Date;
}

interface {{ComponentName}}ListProps {
  items: {{ComponentName}}Item[];
  onItemClick?: (item: {{ComponentName}}Item) => void;
  onItemDelete?: (id: string) => void;
  onItemEdit?: (item: {{ComponentName}}Item) => void;
  emptyMessage?: string;
}

export function {{ComponentName}}List({ 
  items, 
  onItemClick, 
  onItemDelete, 
  onItemEdit,
  emptyMessage = "No items found"
}: {{ComponentName}}ListProps) {
  if (items.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-muted-foreground">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {items.map(item => (
        <{{ComponentName}}Card key={item.id} className="cursor-pointer hover:shadow-md transition-shadow">
          <{{ComponentName}}CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <{{ComponentName}}CardTitle 
              className="text-sm font-medium"
              onClick={() => onItemClick?.(item)}
            >
              {item.title}
            </{{ComponentName}}CardTitle>
            <div className="flex items-center space-x-2">
              {item.status && (
                <span className="px-2 py-1 text-xs rounded-full bg-muted">
                  {item.status}
                </span>
              )}
              {onItemEdit && (
                <{{ComponentName}}Button 
                  variant="ghost" 
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    onItemEdit(item);
                  }}
                >
                  Edit
                </{{ComponentName}}Button>
              )}
              {onItemDelete && (
                <{{ComponentName}}Button 
                  variant="ghost" 
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    onItemDelete(item.id);
                  }}
                >
                  Delete
                </{{ComponentName}}Button>
              )}
            </div>
          </{{ComponentName}}CardHeader>
          {item.description && (
            <{{ComponentName}}CardContent className="pt-0">
              <p className="text-sm text-muted-foreground">{item.description}</p>
              {item.createdAt && (
                <p className="text-xs text-muted-foreground mt-2">
                  {item.createdAt.toLocaleDateString()}
                </p>
              )}
            </{{ComponentName}}CardContent>
          )}
        </{{ComponentName}}Card>
      ))}
    </div>
  );
}''',
                "dependencies": ["react"]
            },
            "hook": {
                "template": '''import { useState, useEffect } from 'react';

// Custom hook for {{AppName}} state management
export function use{{ComponentName}}() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load items from localStorage on mount
  useEffect(() => {
    try {
      const savedItems = localStorage.getItem('{{componentName}}Items');
      if (savedItems) {
        setItems(JSON.parse(savedItems));
      }
    } catch (err) {
      console.error('Failed to load items from localStorage:', err);
    }
  }, []);

  // Save items to localStorage whenever items change
  useEffect(() => {
    try {
      localStorage.setItem('{{componentName}}Items', JSON.stringify(items));
    } catch (err) {
      console.error('Failed to save items to localStorage:', err);
    }
  }, [items]);

  const addItem = async (newItem: any) => {
    setLoading(true);
    setError(null);
    
    try {
      const item = {
        id: Date.now().toString(),
        createdAt: new Date(),
        ...newItem
      };
      
      setItems(prev => [...prev, item]);
      return item;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add item');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateItem = async (id: string, updates: any) => {
    setLoading(true);
    setError(null);
    
    try {
      setItems(prev => prev.map(item => 
        item.id === id ? { ...item, ...updates, updatedAt: new Date() } : item
      ));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update item');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteItem = async (id: string) => {
    setLoading(true);
    setError(null);
    
    try {
      setItems(prev => prev.filter(item => item.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete item');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const clearAll = () => {
    setItems([]);
  };

  return {
    items,
    loading,
    error,
    addItem,
    updateItem,
    deleteItem,
    clearAll
  };
}''',
                "dependencies": ["react"]
            },
            "context": {
                "template": '''import React, { createContext, useContext, useReducer, ReactNode } from 'react';

// State interface
interface {{ComponentName}}State {
  user: any | null;
  theme: 'light' | 'dark';
  settings: Record<string, any>;
}

// Action types
type {{ComponentName}}Action = 
  | { type: 'SET_USER'; payload: any }
  | { type: 'CLEAR_USER' }
  | { type: 'SET_THEME'; payload: 'light' | 'dark' }
  | { type: 'UPDATE_SETTINGS'; payload: Record<string, any> };

// Initial state
const initialState: {{ComponentName}}State = {
  user: null,
  theme: 'light',
  settings: {}
};

// Reducer
function {{componentName}}Reducer(state: {{ComponentName}}State, action: {{ComponentName}}Action): {{ComponentName}}State {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'CLEAR_USER':
      return { ...state, user: null };
    case 'SET_THEME':
      return { ...state, theme: action.payload };
    case 'UPDATE_SETTINGS':
      return { ...state, settings: { ...state.settings, ...action.payload } };
    default:
      return state;
  }
}

// Context
const {{ComponentName}}Context = createContext<{
  state: {{ComponentName}}State;
  dispatch: React.Dispatch<{{ComponentName}}Action>;
} | undefined>(undefined);

// Provider component
export function {{ComponentName}}Provider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer({{componentName}}Reducer, initialState);

  return (
    <{{ComponentName}}Context.Provider value={{ state, dispatch }}>
      {children}
    </{{ComponentName}}Context.Provider>
  );
}

// Custom hook to use the context
export function use{{ComponentName}}() {
  const context = useContext({{ComponentName}}Context);
  if (context === undefined) {
    throw new Error('use{{ComponentName}} must be used within a {{ComponentName}}Provider');
  }
  return context;
}

// Action creators
export const {{componentName}}Actions = {
  setUser: (user: any) => ({ type: 'SET_USER' as const, payload: user }),
  clearUser: () => ({ type: 'CLEAR_USER' as const }),
  setTheme: (theme: 'light' | 'dark') => ({ type: 'SET_THEME' as const, payload: theme }),
  updateSettings: (settings: Record<string, any>) => ({ type: 'UPDATE_SETTINGS' as const, payload: settings })
};''',
                "dependencies": ["react"]
            },
            "page": {
                "template": '''import React from 'react';
import { {{ComponentName}}Header } from '@/components/Header';
import { {{ComponentName}}Button } from '@/components/ui/{{ComponentName}}Button';
import { {{ComponentName}}Card } from '@/components/ui/{{ComponentName}}Card';

export default function {{ComponentName}}Page() {
  return (
    <div className="min-h-screen bg-background">
      <{{ComponentName}}Header />
      <main className="container mx-auto px-4 py-8">
        <div className="space-y-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">
              {{PageTitle}}
            </h1>
            <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
              {{PageDescription}}
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {{PageContent}}
          </div>
          
          <div className="text-center">
            <{{ComponentName}}Button size="lg">
              {{CallToAction}}
            </{{ComponentName}}Button>
          </div>
        </div>
      </main>
    </div>
  );
}''',
                "dependencies": ["react"]
            },
            "layout": {
                "template": '''import React from 'react';
import { {{ComponentName}}Header } from '@/components/Header';
import { {{ComponentName}}Footer } from '@/components/Footer';
import { {{ComponentName}}Sidebar } from '@/components/Sidebar';

interface {{ComponentName}}LayoutProps {
  children: React.ReactNode;
  showSidebar?: boolean;
}

export default function {{ComponentName}}Layout({ children, showSidebar = false }: {{ComponentName}}LayoutProps) {
  return (
    <div className="min-h-screen flex flex-col">
      <{{ComponentName}}Header />
      
      <div className="flex-1 flex">
        {showSidebar && (
          <aside className="w-64 bg-muted/50 border-r">
            <{{ComponentName}}Sidebar />
          </aside>
        )}
        
        <main className="flex-1 overflow-auto">
          <div className="container mx-auto px-4 py-8">
            {children}
          </div>
        </main>
      </div>
      
      <{{ComponentName}}Footer />
    </div>
  );
}''',
                "dependencies": ["react"]
            },
            "header": {
                "template": '''import React from 'react';
import { {{ComponentName}}Button } from '@/components/ui/{{ComponentName}}Button';
import { cn } from '@/lib/utils';

interface {{ComponentName}}HeaderProps {
  className?: string;
}

export function {{ComponentName}}Header({ className }: {{ComponentName}}HeaderProps) {
  return (
    <header className={cn("border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60", className)}>
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <h1 className="text-xl font-semibold">{{AppName}}</h1>
        </div>
        
        <nav className="hidden md:flex items-center space-x-6">
          <a href="#" className="text-sm font-medium hover:text-primary">Home</a>
          <a href="#" className="text-sm font-medium hover:text-primary">About</a>
          <a href="#" className="text-sm font-medium hover:text-primary">Contact</a>
        </nav>
        
        <div className="flex items-center space-x-2">
          <{{ComponentName}}Button variant="outline" size="sm">
            Sign In
          </{{ComponentName}}Button>
          <{{ComponentName}}Button size="sm">
            Sign Up
          </{{ComponentName}}Button>
        </div>
      </div>
    </header>
  );
}''',
                "dependencies": ["clsx", "tailwind-merge"]
            },
            "footer": {
                "template": '''import React from 'react';
import { cn } from '@/lib/utils';

interface {{ComponentName}}FooterProps {
  className?: string;
}

export function {{ComponentName}}Footer({ className }: {{ComponentName}}FooterProps) {
  return (
    <footer className={cn("border-t bg-background", className)}>
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">{{AppName}}</h3>
            <p className="text-sm text-muted-foreground">
              {{AppDescription}}
            </p>
          </div>
          
          <div>
            <h4 className="text-sm font-semibold mb-4">Product</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><a href="#" className="hover:text-primary">Features</a></li>
              <li><a href="#" className="hover:text-primary">Pricing</a></li>
              <li><a href="#" className="hover:text-primary">Documentation</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-sm font-semibold mb-4">Company</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><a href="#" className="hover:text-primary">About</a></li>
              <li><a href="#" className="hover:text-primary">Blog</a></li>
              <li><a href="#" className="hover:text-primary">Careers</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-sm font-semibold mb-4">Support</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><a href="#" className="hover:text-primary">Help Center</a></li>
              <li><a href="#" className="hover:text-primary">Contact</a></li>
              <li><a href="#" className="hover:text-primary">Privacy</a></li>
            </ul>
          </div>
        </div>
        
        <div className="mt-8 pt-8 border-t text-center text-sm text-muted-foreground">
          © 2024 {{AppName}}. All rights reserved.
        </div>
      </div>
    </footer>
  );
}''',
                "dependencies": ["clsx", "tailwind-merge"]
            },
            "hook": {
                "template": '''import { useState, useEffect } from 'react';

interface {{ComponentName}}Options {
  {{HookOptions}}
}

export function {{ComponentName}}(options: {{ComponentName}}Options = {}) {
  const [{{StateVariable}}, set{{StateVariable}}] = useState({{InitialValue}});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {{ActionName}} = async ({{ActionParams}}) => {
    setLoading(true);
    setError(null);
    
    try {
      // {{ActionLogic}}
      {{ActionImplementation}}
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // {{EffectLogic}}
  }, [{{EffectDependencies}}]);

  return {
    {{StateVariable}},
    set{{StateVariable}},
    {{ActionName}},
    loading,
    error,
  };
}''',
                "dependencies": ["react"]
            },
            "context": {
                "template": '''import React, { createContext, useContext, useReducer, ReactNode } from 'react';

interface {{ComponentName}}State {
  {{StateProperties}}
}

interface {{ComponentName}}Actions {
  {{ActionTypes}}
}

type {{ComponentName}}Action = {{ActionTypes}};

interface {{ComponentName}}ContextType {
  state: {{ComponentName}}State;
  dispatch: React.Dispatch<{{ComponentName}}Action>;
}

const {{ComponentName}}Context = createContext<{{ComponentName}}ContextType | undefined>(undefined);

const initialState: {{ComponentName}}State = {
  {{InitialStateValues}}
};

function {{ComponentName}}Reducer(state: {{ComponentName}}State, action: {{ComponentName}}Action): {{ComponentName}}State {
  switch (action.type) {
    {{ReducerCases}}
    default:
      return state;
  }
}

interface {{ComponentName}}ProviderProps {
  children: ReactNode;
}

export function {{ComponentName}}Provider({ children }: {{ComponentName}}ProviderProps) {
  const [state, dispatch] = useReducer({{ComponentName}}Reducer, initialState);

  return (
    <{{ComponentName}}Context.Provider value={{ state, dispatch }}>
      {children}
    </{{ComponentName}}Context.Provider>
  );
}

export function use{{ComponentName}}() {
  const context = useContext({{ComponentName}}Context);
  if (context === undefined) {
    throw new Error('use{{ComponentName}} must be used within a {{ComponentName}}Provider');
  }
  return context;
}''',
                "dependencies": ["react"]
            },
            "form": {
                "template": '''import React, { useState } from 'react';
import { {{ComponentName}}Button } from '@/components/ui/{{ComponentName}}Button';
import { {{ComponentName}}Input } from '@/components/ui/{{ComponentName}}Input';
import { {{ComponentName}}Card, {{ComponentName}}CardContent, {{ComponentName}}CardHeader, {{ComponentName}}CardTitle } from '@/components/ui/{{ComponentName}}Card';

interface {{ComponentName}}FormData {
  {{FormFields}}
}

interface {{ComponentName}}FormProps {
  onSubmit: (data: {{ComponentName}}FormData) => void;
  title?: string;
}

export function {{ComponentName}}Form({ onSubmit, title = "{{DefaultTitle}}" }: {{ComponentName}}FormProps) {
  const [formData, setFormData] = useState<{{ComponentName}}FormData>({
    {{InitialFormValues}}
  });
  const [errors, setErrors] = useState<Partial<{{ComponentName}}FormData>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      await onSubmit(formData);
      setFormData({ {{InitialFormValues}} });
      setErrors({});
    } catch (error) {
      console.error('Form submission error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (field: keyof {{ComponentName}}FormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  return (
    <{{ComponentName}}Card>
      <{{ComponentName}}CardHeader>
        <{{ComponentName}}CardTitle>{title}</{{ComponentName}}CardTitle>
      </{{ComponentName}}CardHeader>
      <{{ComponentName}}CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {{FormFieldComponents}}
          
          <{{ComponentName}}Button 
            type="submit" 
            disabled={isSubmitting}
            className="w-full"
          >
            {isSubmitting ? 'Submitting...' : '{{SubmitButtonText}}'}
          </{{ComponentName}}Button>
        </form>
      </{{ComponentName}}CardContent>
    </{{ComponentName}}Card>
  );
}''',
                "dependencies": ["react"]
            },
            "list": {
                "template": '''import React from 'react';
import { {{ComponentName}}Card } from '@/components/ui/{{ComponentName}}Card';
import { {{ComponentName}}Button } from '@/components/ui/{{ComponentName}}Button';

interface {{ComponentName}}Item {
  {{ItemProperties}}
}

interface {{ComponentName}}ListProps {
  items: {{ComponentName}}Item[];
  onItemClick?: (item: {{ComponentName}}Item) => void;
  onItemDelete?: (item: {{ComponentName}}Item) => void;
  emptyMessage?: string;
}

export function {{ComponentName}}List({ 
  items, 
  onItemClick, 
  onItemDelete, 
  emptyMessage = "No items found" 
}: {{ComponentName}}ListProps) {
  if (items.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        {emptyMessage}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {items.map((item) => (
        <{{ComponentName}}Card 
          key={item.id} 
          className="cursor-pointer hover:shadow-md transition-shadow"
          onClick={() => onItemClick?.(item)}
        >
          <div className="p-4">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <h3 className="font-semibold">{item.{{DisplayProperty}}}</h3>
                {item.{{DescriptionProperty}} && (
                  <p className="text-sm text-muted-foreground mt-1">
                    {item.{{DescriptionProperty}}}
                  </p>
                )}
              </div>
              
              {onItemDelete && (
                <{{ComponentName}}Button
                  variant="outline"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    onItemDelete(item);
                  }}
                >
                  Delete
                </{{ComponentName}}Button>
              )}
            </div>
          </div>
        </{{ComponentName}}Card>
      ))}
    </div>
  );
}''',
                "dependencies": ["react"]
            }
        }
        
        # Define component requirements for different app types
        app_requirements = {
            "todo": ["button", "card", "input", "page", "header", "footer", "form", "list", "hook"],
            "dashboard": ["card", "button", "page", "header", "footer", "layout", "hook"],
            "blog": ["card", "button", "input", "page", "header", "footer", "form", "list"],
            "ecommerce": ["card", "button", "input", "page", "header", "footer", "form", "list"],
            "landing": ["button", "card", "page", "header", "footer"],
            "admin": ["button", "card", "input", "page", "header", "footer", "layout", "form", "list", "hook"],
            "full": ["button", "card", "input", "page", "header", "footer", "layout", "form", "list", "hook", "context"]
        }
        
        # Get required component types for this app
        required_types = app_requirements.get(app_type.lower(), ["button", "card", "input"])
        
        # Generate React files for each component type (NO DUPLICATES!)
        generated_files = []
        dependencies_set = set()
        
        for comp_type in required_types:
            if comp_type not in curated_templates:
                logger.warning(f"No curated template found for component type: {comp_type}")
                continue
            
            template_data = curated_templates[comp_type]
            component_name = f"{app_type.title()}{comp_type.title()}"
            
            # Substitute template variables
            template = template_data["template"]
            generated_code = _substitute_app_template_variables(template, app_type, comp_type, component_name)
            
            # Collect dependencies
            if include_dependencies:
                dependencies_set.update(template_data.get("dependencies", []))
            
            # Determine file placement and extension
            file_extension = ".tsx" if comp_type in ["button", "card", "input", "page", "header", "footer", "layout", "form", "list"] else ".ts"
            
            # Create file entry
            file_entry = {
                "filename": f"{component_name}{file_extension}",
                "content": generated_code,
                "component_type": comp_type,
                "imports": [],
                "template_source": "curated"
            }
            
            generated_files.append(file_entry)
        
        # Add essential config files
        if include_dependencies:
            # Add package.json with dependencies
            package_json = {
                "filename": "package.json",
                "content": f'''{{
  "name": "{app_type.lower()}-app-components",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {{
    {', '.join([f'"{dep}": "latest"' for dep in sorted(dependencies_set)])}
  }}
}}''',
                "component_type": "config"
            }
            generated_files.append(package_json)
            
            # Add tsconfig.json
            tsconfig = {
                "filename": "tsconfig.json",
                "content": '''{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "paths": {
      "@/*": ["./"]
    }
  },
  "include": ["components", "lib", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}''',
                "component_type": "config"
            }
            generated_files.append(tsconfig)
            
            # Add lib/utils.ts - CRITICAL for @/lib/utils imports
            utils_file = {
                "filename": "lib/utils.ts",
                "content": '''import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}''',
                "component_type": "utility"
            }
            generated_files.append(utils_file)
            
            # Add README.md
            readme = {
                "filename": "README.md",
                "content": f'''# {app_type.title()} App Components

Generated React components using curated templates for consistent, high-quality output.

## Components Included

{chr(10).join([f"- {comp_type.title()}" for comp_type in required_types])}

## Usage

```typescript
import {{ {app_type.title()}Button }} from './components/{app_type.title()}Button';
import {{ {app_type.title()}Card }} from './components/{app_type.title()}Card';

// Use components in your app
<{app_type.title()}Button variant="default">Click me</{app_type.title()}Button>
```

## Dependencies

{chr(10).join([f"- {dep}" for dep in sorted(dependencies_set)])}

## Installation

```bash
npm install {' '.join(sorted(dependencies_set))}
```
''',
                "component_type": "docs"
            }
            generated_files.append(readme)
            
            # Add index.ts for easy imports
            index_exports = [f'export {{ {app_type.title()}{comp_type.title()} }} from "./{app_type.title()}{comp_type.title()}";' 
                           for comp_type in required_types]
            index_content = {
                "filename": "index.ts",
                "content": '\n'.join(index_exports),
                "component_type": "index"
            }
            generated_files.append(index_content)
        
        logger.info(f"Generated {len(generated_files)} curated components for {app_type} app")
        
        return {
            "success": True,
            "app_type": app_type,
            "generated_files": generated_files,
            "file_count": len(generated_files),
            "dependencies": list(dependencies_set) if include_dependencies else [],
            "template_source": "curated_high_quality",
            "message": f"Successfully generated {len(generated_files)} high-quality components for {app_type} app"
        }
        
    except Exception as e:
        logger.error(f"Failed to build app components: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to generate components for {app_type} app"
        }

@mcp.tool()
async def build_app_components(
    app_type: str,
    include_dependencies: bool = True
) -> Dict[str, Any]:
    """
    [INTERNAL] Generate React components in memory (returns JSON, no files created)
    Use bulk_create_component_files() instead to create actual files
    
    Args:
        app_type: Type of app to build (todo, dashboard, blog, ecommerce, etc.)
        include_dependencies: Whether to include import dependencies in output
    
    Returns:
        Generated React components as JSON data (not saved to disk)
    """
    return await _build_app_components_internal(app_type, include_dependencies)

@mcp.tool() 
async def generate_react_component(
    component_name: str,
    custom_props: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Generate a single React component from database template
    
    Args:
        component_name: Name of the Figma component to generate
        custom_props: Optional custom properties to inject into template
    
    Returns:
        Generated React component code with imports
    """
    try:
        logger.info(f"Generating React component: {component_name}")
        
        # Get component from database
        component = await db_client.get_component_by_name(component_name)
        
        if not component:
            return {
                "success": False,
                "error": f"Component '{component_name}' not found in database",
                "message": "Component not found"
            }
        
        # Extract React template
        react_template_data = component['props'].get('react_template', {})
        
        if not react_template_data:
            return {
                "success": False,
                "error": f"No React template available for '{component_name}'",
                "message": "Component has no executable React template"
            }
        
        # Get template
        template = react_template_data.get('template', '')
        shadcn_component = react_template_data.get('shadcn_component', 'Component')
        
        # Use custom props or generate defaults
        if custom_props:
            props = custom_props
        else:
            props = _get_default_props(shadcn_component, component_name)
        
        # Generate code
        generated_code = _substitute_template_variables(template, props)
        
        # Record usage
        await db_client.record_component_usage(component['id'], 'single_generated')
        
        return {
            "success": True,
            "component_name": component_name,
            "generated_code": generated_code,
            "filename": f"{props.get('componentName', component_name)}.tsx",
            "imports": react_template_data.get('imports', []),
            "dependencies": react_template_data.get('dependencies', []),
            "shadcn_component": shadcn_component,
            "message": f"Successfully generated React component for '{component_name}'"
        }
        
    except Exception as e:
        logger.error(f"Failed to generate React component: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to generate component '{component_name}'"
        }

def _substitute_app_template_variables(template: str, app_type: str, comp_type: str, component_name: str) -> str:
    """Substitute template variables with app-specific values"""
    
    # App-specific variables
    app_configs = {
        "todo": {
            "AppName": "Todo App",
            "AppDescription": "A simple and powerful task management application",
            "PageTitle": "My Tasks",
            "PageDescription": "Organize your tasks and boost your productivity",
            "CallToAction": "Add New Task",
            "SubmitButtonText": "Create Task",
            "DefaultTitle": "Create Task"
        },
        "dashboard": {
            "AppName": "Dashboard",
            "AppDescription": "Analytics and insights at your fingertips",
            "PageTitle": "Dashboard",
            "PageDescription": "Monitor your key metrics and performance",
            "CallToAction": "View Report",
            "SubmitButtonText": "Generate Report",
            "DefaultTitle": "New Report"
        },
        "blog": {
            "AppName": "Blog",
            "AppDescription": "Share your thoughts and stories with the world",
            "PageTitle": "Latest Posts",
            "PageDescription": "Discover amazing content from our community",
            "CallToAction": "Read More",
            "SubmitButtonText": "Publish Post",
            "DefaultTitle": "New Post"
        },
        "ecommerce": {
            "AppName": "Store",
            "AppDescription": "Premium products for modern lifestyle",
            "PageTitle": "Featured Products",
            "PageDescription": "Discover our latest collection",
            "CallToAction": "Shop Now",
            "SubmitButtonText": "Add to Cart",
            "DefaultTitle": "Product Details"
        },
        "landing": {
            "AppName": "Landing",
            "AppDescription": "Beautiful landing page for your business",
            "PageTitle": "Welcome",
            "PageDescription": "Transform your ideas into reality",
            "CallToAction": "Get Started",
            "SubmitButtonText": "Sign Up",
            "DefaultTitle": "Contact Us"
        },
        "admin": {
            "AppName": "Admin Panel",
            "AppDescription": "Manage your application with ease",
            "PageTitle": "Admin Dashboard",
            "PageDescription": "Control and monitor your system",
            "CallToAction": "View Details",
            "SubmitButtonText": "Save Changes",
            "DefaultTitle": "Admin Form"
        }
    }
    
    # Get app config or default
    app_config = app_configs.get(app_type.lower(), app_configs["todo"])
    
    # Component-specific variables
    component_vars = {
        "ComponentName": component_name,
        **app_config
    }
    
    # Add component-specific variables based on type
    if comp_type == "hook":
        component_vars.update({
            "HookOptions": "initialValue?: any",
            "StateVariable": "data",
            "InitialValue": "null",
            "ActionName": "updateData",
            "ActionParams": "newData: any",
            "ActionLogic": "Update the data state",
            "ActionImplementation": "setData(newData);",
            "EffectLogic": "Initialize hook",
            "EffectDependencies": ""
        })
    elif comp_type == "context":
        component_vars.update({
            "StateProperties": "items: any[];\n  loading: boolean;\n  error: string | null;",
            "ActionTypes": "| { type: 'SET_ITEMS'; payload: any[] }\n    | { type: 'SET_LOADING'; payload: boolean }\n    | { type: 'SET_ERROR'; payload: string | null }",
            "InitialStateValues": "items: [],\n  loading: false,\n  error: null",
            "ReducerCases": """case 'SET_ITEMS':
      return { ...state, items: action.payload };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };"""
        })
    elif comp_type == "form":
        component_vars.update({
            "FormFields": "title: string;\n  description: string;",
            "InitialFormValues": "title: '',\n    description: ''",
            "FormFieldComponents": f'''<{component_name}Input
            type="text"
            placeholder="Enter title"
            value={{{{formData.title}}}}
            onChange={{{{(e) => handleChange('title', e.target.value)}}}}
          />
          <{component_name}Input
            type="text"
            placeholder="Enter description"
            value={{{{formData.description}}}}
            onChange={{{{(e) => handleChange('description', e.target.value)}}}}
          />'''
        })
    elif comp_type == "list":
        component_vars.update({
            "ItemProperties": "id: string;\\n  title: string;\\n  description?: string;\\n  completed?: boolean;",
            "DisplayProperty": "title",
            "DescriptionProperty": "description"
        })
    elif comp_type == "page":
        component_vars.update({
            "PageContent": f'''<{component_name}Card>
              <{component_name}CardHeader>
                <{component_name}CardTitle>Getting Started</{component_name}CardTitle>
                <{component_name}CardDescription>
                  Welcome to your new {app_type} application
                </{component_name}CardDescription>
              </{component_name}CardHeader>
              <{component_name}CardContent>
                <p>Start building amazing features!</p>
              </{component_name}CardContent>
            </{component_name}Card>'''
        })
    
    # Substitute all variables in the template
    result = template
    for key, value in component_vars.items():
        placeholder = '{{' + key + '}}'
        result = result.replace(placeholder, str(value))
    
    return result

def _get_app_specific_props(app_type: str, component_type: str, component_name: str) -> Dict[str, str]:
    """Generate app-specific props for component templates"""
    
    base_props = {
        "componentName": component_name,
        "variant": "default",
        "size": "default",
        "disabled": ""
    }
    
    # App-specific customizations
    if app_type == "todo":
        if component_type == "button":
            base_props.update({
                "children": "Add Task",
                "variant": "default"
            })
        elif component_type == "card":
            base_props.update({
                "title": "Task Card",
                "description": "Task management component",
                "content": "<p>Task content goes here</p>",
                "footer": "<Button>Complete</Button>"
            })
        elif component_type == "input":
            base_props.update({
                "placeholder": "Enter new task...",
                "type": "text"
            })
    
    elif app_type == "dashboard":
        if component_type == "card":
            base_props.update({
                "title": "Dashboard Widget",
                "description": "Analytics component",
                "content": "<div>Dashboard content</div>",
                "footer": "<span>Updated now</span>"
            })
        elif component_type == "button":
            base_props.update({
                "children": "View Details",
                "variant": "outline"
            })
    
    elif app_type == "ecommerce":
        if component_type == "button":
            base_props.update({
                "children": "Add to Cart",
                "variant": "default"
            })
        elif component_type == "card":
            base_props.update({
                "title": "Product Card",
                "description": "$99.99",
                "content": "<img src='product.jpg' alt='Product' />",
                "footer": "<Button>Buy Now</Button>"
            })
    
    return base_props

def _get_default_props(shadcn_component: str, original_name: str) -> Dict[str, str]:
    """Generate default props for a component"""
    
    # Convert original name to PascalCase component name
    component_name = "".join(word.capitalize() for word in original_name.replace("-", " ").replace("_", " ").split())
    
    defaults = {
        "componentName": component_name,
        "variant": "default", 
        "size": "default",
        "disabled": "",
        "children": "Click me"
    }
    
    # Component-specific defaults
    if shadcn_component == "button":
        defaults["children"] = "Click me"
    elif shadcn_component == "card":
        defaults.update({
            "title": "Card Title",
            "description": "Card description",
            "content": "<p>Card content goes here</p>",
            "footer": "<Button>Action</Button>"
        })
    elif shadcn_component == "input":
        defaults.update({
            "placeholder": "Enter text...",
            "type": "text"
        })
    
    return defaults

def _substitute_template_variables(template: str, props: Dict[str, str]) -> str:
    """Substitute template variables with actual values"""
    
    generated_code = template
    
    for key, value in props.items():
        placeholder = '{{' + key + '}}'
        generated_code = generated_code.replace(placeholder, str(value))
    
    return generated_code

@mcp.tool()
async def create_app_blocks(
    app_type: str,
    output_directory: str,
    blocks: List[str],
    custom_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create production-ready application blocks using database components
    Similar to shadcn/ui pro blocks but using our component library
    
    Args:
        app_type: Type of application (dashboard, ecommerce, blog, saas, etc.)
        output_directory: Where to create the block files
        blocks: List of blocks to create (app-shell, auth, settings, etc.)
        custom_config: Custom configuration for blocks
    
    Available blocks:
        - app-shell: Complete application layout with nav, sidebar, header
        - auth: Sign in/up pages with forms
        - dashboard: Analytics dashboard with charts and stats
        - settings: User settings pages with forms
        - landing: Marketing landing page sections
        - pricing: Pricing tables and comparison
        - profile: User profile pages
        - empty-states: Empty data states
        - error-pages: 404, 500 error pages
        - onboarding: User onboarding flow
    
    Returns:
        Created block files and structure
    """
    try:
        import os
        from pathlib import Path
        
        # Create output directory
        Path(output_directory).mkdir(parents=True, exist_ok=True)
        
        created_files = []
        
        # Block definitions with component composition
        block_definitions = {
            "app-shell": {
                "files": ["AppShell.tsx", "Sidebar.tsx", "TopNav.tsx", "AppLayout.tsx"],
                "components": ["navigation", "header", "layout", "button"],
                "description": "Complete application shell with navigation"
            },
            "auth": {
                "files": ["SignIn.tsx", "SignUp.tsx", "ForgotPassword.tsx", "AuthLayout.tsx"],
                "components": ["form", "button", "card", "input"],
                "description": "Authentication pages and forms"
            },
            "dashboard": {
                "files": ["Dashboard.tsx", "StatsCards.tsx", "Charts.tsx", "RecentActivity.tsx"],
                "components": ["card", "chart", "table", "button"],
                "description": "Analytics dashboard with metrics"
            },
            "settings": {
                "files": ["Settings.tsx", "ProfileSettings.tsx", "AccountSettings.tsx", "NotificationSettings.tsx"],
                "components": ["form", "card", "button", "input", "switch"],
                "description": "User settings pages"
            },
            "landing": {
                "files": ["Hero.tsx", "Features.tsx", "Testimonials.tsx", "CTA.tsx"],
                "components": ["button", "card", "section", "header"],
                "description": "Marketing landing page sections"
            },
            "pricing": {
                "files": ["PricingTable.tsx", "PricingCard.tsx", "FeatureComparison.tsx"],
                "components": ["card", "button", "table", "badge"],
                "description": "Pricing and plan comparison"
            },
            "profile": {
                "files": ["UserProfile.tsx", "ProfileHeader.tsx", "ActivityFeed.tsx"],
                "components": ["card", "avatar", "button", "list"],
                "description": "User profile pages"
            },
            "empty-states": {
                "files": ["EmptyData.tsx", "NoResults.tsx", "FirstTimeUser.tsx"],
                "components": ["card", "button", "illustration"],
                "description": "Empty state components"
            },
            "error-pages": {
                "files": ["Error404.tsx", "Error500.tsx", "ErrorBoundary.tsx"],
                "components": ["page", "button", "illustration"],
                "description": "Error pages and boundaries"
            },
            "onboarding": {
                "files": ["OnboardingFlow.tsx", "WelcomeStep.tsx", "SetupStep.tsx", "CompleteStep.tsx"],
                "components": ["card", "form", "button", "progress"],
                "description": "User onboarding flow"
            }
        }
        
        # Process each requested block
        for block_name in blocks:
            if block_name not in block_definitions:
                logger.warning(f"Unknown block type: {block_name}")
                continue
                
            block_def = block_definitions[block_name]
            block_dir = os.path.join(output_directory, block_name)
            Path(block_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate each file in the block
            for file_name in block_def["files"]:
                # Generate block content using smart component selection
                block_content = await _generate_block_content(
                    app_type=app_type,
                    block_name=block_name,
                    file_name=file_name,
                    required_components=block_def["components"],
                    custom_config=custom_config
                )
                
                file_path = os.path.join(block_dir, file_name)
                with open(file_path, 'w') as f:
                    f.write(block_content)
                
                created_files.append({
                    "path": file_path,
                    "block": block_name,
                    "file": file_name
                })
                
                logger.info(f"Created block file: {file_path}")
        
        # Create index file for easy imports
        index_content = _generate_block_index(blocks, block_definitions)
        index_path = os.path.join(output_directory, "blocks.ts")
        with open(index_path, 'w') as f:
            f.write(index_content)
        created_files.append({"path": index_path, "file": "blocks.ts"})
        
        return {
            "success": True,
            "created_files": created_files,
            "blocks": blocks,
            "output_directory": output_directory,
            "message": f"Successfully created {len(created_files)} files for {len(blocks)} blocks"
        }
        
    except Exception as e:
        logger.error(f"Block creation failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create blocks"
        }

@mcp.tool()
async def create_application_blocks(
    app_type: str,
    output_directory: str,
    block_types: Optional[List[str]] = None,
    create_index: bool = True
) -> Dict[str, Any]:
    """
    Generate and SAVE application block files from database templates
    Creates complete application blocks as .tsx files in your project directory
    
    Args:
        app_type: Type of app to build (dashboard, marketing, blog, ecommerce, etc.)
        output_directory: Directory path where files should be created
        block_types: Specific block types to create (hero, features, pricing, etc.)
        create_index: Whether to create an index.ts file exporting all blocks
    
    Returns:
        List of created files and their paths
    
    Example:
        create_application_blocks("marketing", "./src/blocks", ["hero", "features", "pricing"])
        Creates: ./src/blocks/HeroSection.tsx, FeaturesSection.tsx, PricingSection.tsx
    """
    try:
        logger.info(f"Creating application blocks for {app_type} app in {output_directory}")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
        
        # Query application blocks from database
        query = db_client.supabase.table('application_blocks').select('*')
        
        # Filter by app_type if specific one requested
        if app_type != "all":
            query = query.or_(f"app_type.eq.{app_type},app_type.eq.marketing,app_type.eq.utility")
        
        # Filter by specific block types if requested
        if block_types:
            query = query.in_('block_type', block_types)
        
        result = query.execute()
        blocks = result.data if result.data else []
        
        if not blocks:
            return {
                "success": False,
                "error": f"No application blocks found for app_type='{app_type}' and block_types={block_types}",
                "message": "No blocks available"
            }
        
        created_files = []
        
        for block in blocks:
            # Generate filename from block name
            filename = block['name'].replace(' - ', '').replace(' ', '').replace('-', '') + '.tsx'
            file_path = os.path.join(output_directory, filename)
            
            # Get the React template from the block
            react_template = block.get('react_template', '')
            
            if not react_template:
                logger.warning(f"No React template found for block: {block['name']}")
                continue
            
            # Write the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(react_template)
            
            created_files.append({
                "path": file_path,
                "filename": filename,
                "block_name": block['name'],
                "block_type": block['block_type'],
                "app_type": block['app_type'],
                "size": len(react_template),
                "dependencies": block.get('dependencies', [])
            })
            
            logger.info(f"✅ Created {filename} ({len(react_template)} chars)")
        
        # Create index.ts file if requested
        if create_index and created_files:
            index_content = "// Auto-generated application blocks index\n\n"
            
            for file_info in created_files:
                component_name = file_info['filename'].replace('.tsx', '')
                index_content += f"export {{ default as {component_name} }} from './{component_name}';\n"
            
            index_path = os.path.join(output_directory, "index.ts")
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            created_files.append({
                "path": index_path,
                "filename": "index.ts",
                "block_name": "Index file",
                "block_type": "index",
                "app_type": "utility",
                "size": len(index_content)
            })
        
        # Create package.json for dependencies
        all_dependencies = set()
        for file_info in created_files:
            deps = file_info.get('dependencies', [])
            if isinstance(deps, list):
                all_dependencies.update(deps)
        
        if all_dependencies:
            package_json = {
                "name": f"{app_type}-blocks",
                "version": "1.0.0",
                "description": f"Application blocks for {app_type} app",
                "main": "index.ts",
                "dependencies": {
                    "react": "^18.0.0",
                    "@types/react": "^18.0.0",
                    "lucide-react": "^0.263.1"
                },
                "devDependencies": {
                    "typescript": "^5.0.0"
                }
            }
            
            package_path = os.path.join(output_directory, "package.json")
            with open(package_path, 'w', encoding='utf-8') as f:
                json.dump(package_json, f, indent=2)
            
            created_files.append({
                "path": package_path,
                "filename": "package.json",
                "block_name": "Package configuration",
                "block_type": "config",
                "app_type": "utility",
                "size": len(json.dumps(package_json))
            })
        
        return {
            "success": True,
            "files_created": created_files,
            "total_files": len(created_files),
            "total_blocks": len([f for f in created_files if f['block_type'] not in ['index', 'config']]),
            "output_directory": output_directory,
            "app_type": app_type,
            "message": f"Successfully created {len(created_files)} files with {len(blocks)} application blocks"
        }
        
    except Exception as e:
        logger.error(f"Application block creation failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create application blocks"
        }

@mcp.tool()
async def health_check() -> Dict[str, Any]:
    """
    Check health status of Figma MCP server and database connection
    
    Returns:
        Server and database health status
    """
    try:
        logger.info("Performing health check")
        
        # Test database connection
        db_status = await validate_database_access()
        
        # Check for React templates in database
        react_template_count = 0
        try:
            result = db_client.supabase.table('figma_components')\
                .select('id', count='exact')\
                .not_.is_('props->react_template', 'null')\
                .execute()
            react_template_count = result.count if hasattr(result, 'count') else 0
        except:
            react_template_count = 0
        
        return {
            "success": True,
            "server_status": "healthy",
            "database_status": "connected" if db_status["success"] else "disconnected",
            "component_count": db_status.get("component_count", 0),
            "react_templates_available": react_template_count,
            "categories_available": db_status.get("category_count", 0),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "database-powered-with-react-templates",
            "capabilities": [
                "component_search",
                "react_code_generation", 
                "app_type_intelligence",
                "template_substitution"
            ],
            "message": f"Figma MCP Server ready - {react_template_count} React templates available"
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "success": False,
            "server_status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

@mcp.tool()
async def store_app_context(
    session_id: str,
    app_description: str,
    requirements: Optional[List[str]] = None,
    ui_preferences: Optional[Dict[str, str]] = None,
    tech_stack: Optional[List[str]] = None,
    business_rules: Optional[List[str]] = None,
    user_stories: Optional[List[str]] = None,
    conversation_summary: Optional[str] = None
) -> Dict[str, Any]:
    """
    Store rich conversation context for later use by build_application_with_context
    
    This tool allows storing detailed context from the conversation that can be
    retrieved by the intelligent app generation tool.
    
    Args:
        session_id: Unique identifier for this conversation session
        app_description: Basic description of the app to build
        requirements: List of functional requirements
        ui_preferences: UI/UX preferences and styling choices
        tech_stack: Preferred technologies and frameworks
        business_rules: Business logic and rules
        user_stories: User stories and use cases
        conversation_summary: Summary of the conversation context
    
    Returns:
        Success status and context storage info
    """
    try:
        context = {
            "app_description": app_description,
            "requirements": requirements or [],
            "ui_preferences": ui_preferences or {},
            "tech_stack": tech_stack or [],
            "business_rules": business_rules or [],
            "user_stories": user_stories or [],
            "conversation_summary": conversation_summary or "",
            "stored_at": datetime.now(timezone.utc).isoformat()
        }
        
        store_conversation_context(session_id, context)
        
        return {
            "success": True,
            "session_id": session_id,
            "context_stored": True,
            "context_size": len(json.dumps(context)),
            "message": f"Context stored for session {session_id}"
        }
        
    except Exception as e:
        logger.error(f"Failed to store app context: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to store conversation context"
        }

@mcp.tool()
async def build_application_with_context(
    session_id: str,
    output_directory: str,
    include_ui_library: bool = True,
    include_auth: bool = True,
    include_data_layer: bool = True
) -> Dict[str, Any]:
    """
    Build application using stored conversation context for intelligent generation
    
    This tool retrieves rich conversation context and uses it for intelligent
    app generation with much better understanding of requirements.
    
    Args:
        session_id: Session ID to retrieve conversation context
        output_directory: Directory path where files should be created
        include_ui_library: Whether to include UI utility components
        include_auth: Whether to include authentication flows
        include_data_layer: Whether to include data management hooks and contexts
    
    Returns:
        Complete application structure with context-aware intelligent generation
    
    Example:
        # First store context:
        store_app_context("user123", "project management SaaS", 
                         requirements=["kanban boards", "team collaboration"],
                         ui_preferences={"style": "modern", "colors": "blue"})
        
        # Then build with context:
        build_application_with_context("user123", "./src")
    """
    try:
        logger.info(f"🔍 Retrieving context for session: {session_id}")
        
        # Get stored conversation context
        context = get_conversation_context(session_id)
        
        if not context:
            return {
                "success": False,
                "error": f"No context found for session {session_id}",
                "available_sessions": list(_conversation_contexts.keys()),
                "message": "Please use store_app_context first to provide conversation context"
            }
        
        logger.info(f"📊 Using rich context: {len(json.dumps(context))} chars")
        
        # Enhanced analysis using conversation context
        analysis = await _analyze_app_requirements_with_context(context)
        
        logger.info(f"🧠 Context-aware analysis: {analysis}")
        
        # Generate application structure with rich context
        result = await _generate_intelligent_app_structure(
            analysis=analysis,
            output_directory=output_directory,
            include_ui_library=include_ui_library,
            include_auth=include_auth,
            include_data_layer=include_data_layer
        )
        
        return {
            "success": True,
            "session_id": session_id,
            "context_used": True,
            "app_analysis": analysis,
            "files_created": result["files_created"],
            "total_files": result["total_files"],
            "total_blocks": result["total_blocks"],
            "estimated_dev_time": result["estimated_dev_time"],
            "next_steps": result["next_steps"],
            "customization_guide": result["customization_guide"],
            "message": f"✨ Context-aware app generation complete: {analysis['app_type']} with {result['total_blocks']} blocks"
        }
        
    except Exception as e:
        logger.error(f"Context-aware app generation failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to generate application with context"
        }

async def _analyze_app_requirements_with_context(context: Dict[str, Any]) -> Dict[str, Any]:
    """Enhanced analysis using rich conversation context"""
    
    app_description = context.get("app_description", "")
    requirements = context.get("requirements", [])
    ui_preferences = context.get("ui_preferences", {})
    tech_stack = context.get("tech_stack", [])
    business_rules = context.get("business_rules", [])
    user_stories = context.get("user_stories", [])
    
    # Start with basic analysis
    basic_analysis = await _analyze_app_requirements(app_description)
    
    # Enhance with context
    enhanced_analysis = basic_analysis.copy()
    
    # Override detected features with explicit requirements
    if requirements:
        additional_features = []
        for req in requirements:
            req_lower = req.lower()
            if any(auth_word in req_lower for auth_word in ["login", "signup", "user", "account"]):
                additional_features.append("auth")
            if any(payment_word in req_lower for payment_word in ["payment", "billing", "subscription"]):
                additional_features.append("payments")
            if any(search_word in req_lower for search_word in ["search", "filter", "find"]):
                additional_features.append("search")
            if any(upload_word in req_lower for upload_word in ["upload", "file", "image"]):
                additional_features.append("upload")
            if any(admin_word in req_lower for admin_word in ["admin", "manage", "control"]):
                additional_features.append("admin")
        
        enhanced_analysis["detected_features"].extend(additional_features)
        enhanced_analysis["detected_features"] = list(set(enhanced_analysis["detected_features"]))
    
    # Use UI preferences to adjust complexity
    if ui_preferences:
        style = ui_preferences.get("style", "").lower()
        if any(complex_word in style for complex_word in ["advanced", "rich", "complex", "enterprise"]):
            enhanced_analysis["complexity"] = "complex"
        elif any(simple_word in style for simple_word in ["simple", "minimal", "basic", "clean"]):
            enhanced_analysis["complexity"] = "simple"
    
    # Adjust based on tech stack
    if tech_stack:
        enhanced_analysis["tech_stack"] = tech_stack
        if any(complex_tech in tech_stack for complex_tech in ["Redux", "GraphQL", "Microservices", "Docker"]):
            if enhanced_analysis["complexity"] == "simple":
                enhanced_analysis["complexity"] = "medium"
    
    # Add context-specific information
    enhanced_analysis.update({
        "context_requirements": requirements,
        "ui_preferences": ui_preferences,
        "business_rules": business_rules,
        "user_stories": user_stories,
        "context_enhanced": True,
        "context_quality": "high" if len(requirements) > 3 else "medium" if len(requirements) > 1 else "basic"
    })
    
    # Re-determine blocks with enhanced context
    enhanced_analysis["required_blocks"] = _determine_required_blocks(
        enhanced_analysis["app_type"], 
        enhanced_analysis["detected_features"], 
        enhanced_analysis["complexity"]
    )
    
    return enhanced_analysis

@mcp.tool()
async def build_application(
    app_description: str,
    output_directory: str,
    include_ui_library: bool = True,
    include_auth: bool = True,
    include_data_layer: bool = True
) -> Dict[str, Any]:
    """
    Intelligently analyze a natural language app description and generate complete application structure
    
    This tool analyzes descriptions like "I want to build a project management SaaS" or "Create an e-commerce store"
    and automatically selects and generates appropriate blocks to create a complete application foundation.
    
    Args:
        app_description: Natural language description of the application (e.g., "project management SaaS", "blog platform", "e-commerce store")
        output_directory: Directory path where files should be created
        include_ui_library: Whether to include UI utility components
        include_auth: Whether to include authentication flows
        include_data_layer: Whether to include data management hooks and contexts
    
    Returns:
        Complete application structure with intelligent block selection
    
    Example:
        build_application("I want to build a task management app with teams", "./src")
    """
    try:
        logger.info(f"🧠 Analyzing app description: {app_description}")
        
        # Intelligent app analysis and categorization
        analysis = await _analyze_app_requirements(app_description)
        
        logger.info(f"📊 App analysis results: {analysis}")
        
        # Generate application structure based on analysis
        result = await _generate_intelligent_app_structure(
            analysis=analysis,
            output_directory=output_directory,
            include_ui_library=include_ui_library,
            include_auth=include_auth,
            include_data_layer=include_data_layer
        )
        
        return {
            "success": True,
            "app_analysis": analysis,
            "files_created": result["files_created"],
            "total_files": result["total_files"],
            "total_blocks": result["total_blocks"],
            "estimated_dev_time": result["estimated_dev_time"],
            "next_steps": result["next_steps"],
            "customization_guide": result["customization_guide"],
            "message": f"✨ Intelligent app generation complete: {analysis['app_type']} with {result['total_blocks']} blocks"
        }
        
    except Exception as e:
        import traceback
        logger.error(f"Intelligent app generation failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to analyze and generate application"
        }

async def _analyze_app_requirements(app_description: str) -> Dict[str, Any]:
    """Analyze natural language app description to determine requirements and block selection"""
    
    description_lower = app_description.lower()
    
    # App type detection patterns
    app_patterns = {
        "saas": ["saas", "software as a service", "subscription", "platform", "service", "tool", "dashboard", "management", "crm", "project management"],
        "e-commerce": ["store", "shop", "e-commerce", "ecommerce", "marketplace", "selling", "products", "cart", "checkout", "payment"],
        "blog": ["blog", "content", "articles", "posts", "writing", "cms", "publishing", "news", "magazine"],
        "portfolio": ["portfolio", "showcase", "personal", "resume", "cv", "work", "projects", "gallery"],
        "social": ["social", "community", "forum", "chat", "messaging", "feed", "users", "profiles", "friends"],
        "dashboard": ["dashboard", "analytics", "metrics", "reporting", "admin", "monitoring", "data"],
        "landing": ["landing", "marketing", "promotion", "company", "business", "agency", "services"],
        "utility": ["calculator", "converter", "tool", "utility", "generator", "checker", "validator"]
    }
    
    # Feature detection patterns
    feature_patterns = {
        "auth": ["login", "signup", "authentication", "users", "accounts", "profile", "registration"],
        "payments": ["payment", "billing", "subscription", "stripe", "paypal", "checkout", "pricing"],
        "real_time": ["real-time", "live", "chat", "notifications", "updates", "sync", "collaborative"],
        "search": ["search", "filter", "find", "query", "lookup", "discover"],
        "upload": ["upload", "files", "images", "documents", "media", "storage"],
        "api": ["api", "integration", "webhook", "external", "third-party", "connect"],
        "mobile": ["mobile", "responsive", "app", "ios", "android", "phone", "tablet"],
        "admin": ["admin", "management", "control", "moderate", "configure", "settings"]
    }
    
    # Complexity level detection
    complexity_indicators = {
        "simple": ["simple", "basic", "minimal", "quick", "easy", "starter"],
        "medium": ["medium", "standard", "typical", "regular", "normal"],
        "complex": ["complex", "advanced", "enterprise", "scalable", "robust", "comprehensive", "full-featured"]
    }
    
    # Detect primary app type
    detected_type = "utility"  # default
    type_confidence = 0
    for app_type, keywords in app_patterns.items():
        matches = sum(1 for keyword in keywords if keyword in description_lower)
        confidence = matches / len(keywords)
        if confidence > type_confidence:
            type_confidence = confidence
            detected_type = app_type
    
    # Detect required features
    detected_features = []
    for feature, keywords in feature_patterns.items():
        if any(keyword in description_lower for keyword in keywords):
            detected_features.append(feature)
    
    # Detect complexity
    complexity = "medium"  # default
    for level, keywords in complexity_indicators.items():
        if any(keyword in description_lower for keyword in keywords):
            complexity = level
            break
    
    # Determine required blocks based on app type and features
    required_blocks = _determine_required_blocks(detected_type, detected_features, complexity)
    
    return {
        "app_type": detected_type,
        "type_confidence": type_confidence,
        "detected_features": detected_features,
        "complexity": complexity,
        "required_blocks": required_blocks,
        "estimated_pages": len(required_blocks.get("pages", [])),
        "estimated_components": sum(len(blocks) for blocks in required_blocks.values()),
        "primary_use_case": _extract_primary_use_case(description_lower, detected_type)
    }

def _determine_required_blocks(app_type: str, features: List[str], complexity: str) -> Dict[str, List[str]]:
    """Determine which blocks are needed based on app analysis"""
    
    blocks = {
        "core": [],
        "pages": [],
        "sections": [],
        "features": [],
        "utilities": []
    }
    
    # Core blocks for all apps
    blocks["core"] = ["hero", "navigation", "footer"]
    
    # App type specific blocks
    if app_type == "saas":
        blocks["pages"] = ["dashboard", "settings", "billing"]
        blocks["sections"] = ["features", "pricing", "testimonials", "cta"]
        blocks["features"] = ["data-table", "stats-cards", "user-management"]
        
    elif app_type == "e-commerce":
        blocks["pages"] = ["product-listing", "product-detail", "cart", "checkout"]
        blocks["sections"] = ["product-grid", "categories", "reviews"]
        blocks["features"] = ["shopping-cart", "payment-form", "order-tracking"]
        
    elif app_type == "blog":
        blocks["pages"] = ["blog-home", "article", "about", "contact"]
        blocks["sections"] = ["blog-grid", "author-bio", "related-posts"]
        blocks["features"] = ["comment-system", "newsletter-signup", "search"]
        
    elif app_type == "portfolio":
        blocks["pages"] = ["home", "about", "work", "contact"]
        blocks["sections"] = ["hero", "skills", "projects", "experience"]
        blocks["features"] = ["project-gallery", "contact-form"]
        
    elif app_type == "social":
        blocks["pages"] = ["feed", "profile", "messages", "settings"]
        blocks["sections"] = ["user-feed", "friend-list", "activity"]
        blocks["features"] = ["post-creator", "messaging", "notifications"]
        
    elif app_type == "dashboard":
        blocks["pages"] = ["dashboard", "reports", "settings"]
        blocks["sections"] = ["stats-overview", "charts", "data-tables"]
        blocks["features"] = ["analytics", "export", "filtering"]
        
    elif app_type == "landing":
        blocks["pages"] = ["home", "about", "services", "contact"]
        blocks["sections"] = ["hero", "features", "testimonials", "cta", "team"]
        blocks["features"] = ["contact-form", "newsletter"]
    
    # Feature-specific additions
    if "auth" in features:
        blocks["pages"].extend(["login", "signup", "profile"])
        blocks["features"].append("authentication")
        
    if "payments" in features:
        blocks["pages"].extend(["pricing", "billing"])
        blocks["features"].extend(["payment-form", "subscription-management"])
        
    if "search" in features:
        blocks["features"].append("search-bar")
        blocks["utilities"].append("search-results")
        
    if "upload" in features:
        blocks["features"].append("file-upload")
        
    if "admin" in features:
        blocks["pages"].extend(["admin-dashboard", "user-management"])
        blocks["features"].append("admin-controls")
    
    # Complexity adjustments
    if complexity == "simple":
        # Reduce blocks for simple apps
        blocks["pages"] = blocks["pages"][:3]
        blocks["sections"] = blocks["sections"][:4]
    elif complexity == "complex":
        # Add advanced blocks for complex apps
        blocks["features"].extend(["advanced-search", "bulk-operations", "export-import"])
        blocks["utilities"].extend(["error-boundary", "loading-states", "empty-states"])
    
    # Always include essential utilities
    blocks["utilities"].extend(["error-404", "loading", "search-bar"])
    
    return blocks

def _extract_primary_use_case(description: str, app_type: str) -> str:
    """Extract the primary use case from the description"""
    
    use_case_patterns = {
        "task management": ["task", "todo", "project management", "productivity"],
        "team collaboration": ["team", "collaborate", "workspace", "sharing"],
        "customer management": ["customer", "client", "crm", "leads"],
        "content publishing": ["blog", "publish", "content", "articles"],
        "online selling": ["sell", "store", "products", "e-commerce"],
        "data visualization": ["dashboard", "analytics", "reports", "metrics"],
        "community building": ["community", "forum", "social", "discussion"]
    }
    
    for use_case, keywords in use_case_patterns.items():
        if any(keyword in description for keyword in keywords):
            return use_case
    
    return f"{app_type} application"

async def _generate_intelligent_app_structure(
    analysis: Dict[str, Any],
    output_directory: str,
    include_ui_library: bool,
    include_auth: bool,
    include_data_layer: bool
) -> Dict[str, Any]:
    """Generate complete app structure based on intelligent analysis"""
    
    files_created = []
    app_type = analysis["app_type"]
    required_blocks = analysis["required_blocks"]
    
    # Track blocks created for statistics
    total_blocks = 0
    
    # Create directory structure
    import os
    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(os.path.join(output_directory, "components"), exist_ok=True)
    os.makedirs(os.path.join(output_directory, "pages"), exist_ok=True)
    os.makedirs(os.path.join(output_directory, "hooks"), exist_ok=True)
    os.makedirs(os.path.join(output_directory, "lib"), exist_ok=True)
    
    # 1. Create application blocks from database
    try:
        # Get all relevant block types for this app
        block_types_needed = []
        for category in required_blocks.values():
            block_types_needed.extend(category)
        
        if block_types_needed:
            result = await create_application_blocks(
                app_type=app_type,
                output_directory=os.path.join(output_directory, "components"),
                block_types=list(set(block_types_needed))[:15],  # Limit to prevent overwhelming
                create_index=True
            )
            
            if result["success"]:
                files_created.extend(result["files_created"])
                total_blocks += result["total_blocks"]
                logger.info(f"✅ Created {result['total_blocks']} application blocks")
    
    except Exception as e:
        logger.warning(f"Failed to create application blocks: {e}")
    
    # 2. Generate intelligent component structure
    if include_ui_library:
        ui_components = await _generate_smart_ui_components(app_type, output_directory)
        files_created.extend(ui_components)
        total_blocks += len(ui_components)
    
    # 3. Create auth flows if needed
    if include_auth and ("auth" in analysis["detected_features"] or "auth" in required_blocks.get("features", [])):
        auth_components = await _generate_auth_components(app_type, output_directory)
        files_created.extend(auth_components)
        total_blocks += len(auth_components)
    
    # 4. Generate data layer if needed
    if include_data_layer:
        data_components = await _generate_data_layer(app_type, analysis, output_directory)
        files_created.extend(data_components)
        total_blocks += len(data_components)
    
    # 5. Generate pages that compose blocks into complete pages
    try:
        from page_generator import generate_pages
        
        # Get list of available blocks for page composition
        available_blocks = [file["filename"] for file in files_created if file.get("type") in ["block", "component"]]
        
        pages = await generate_pages(
            app_type=app_type,
            output_directory=output_directory,
            available_blocks=available_blocks
        )
        
        files_created.extend(pages)
        total_blocks += len(pages)
        logger.info(f"✅ Generated {len(pages)} complete pages")
        
    except Exception as e:
        logger.warning(f"Failed to generate pages: {e}")
        # Continue without pages - better to have components than nothing
    
    # 5. Create app configuration and utilities
    config_files = await _generate_app_config(analysis, output_directory)
    files_created.extend(config_files)
    
    # Generate next steps and customization guidance
    next_steps = _generate_next_steps(analysis, total_blocks)
    customization_guide = _generate_customization_guide(analysis, files_created)
    
    # Estimate development time
    estimated_dev_time = _estimate_development_time(analysis, total_blocks)
    
    return {
        "files_created": files_created,
        "total_files": len(files_created),
        "total_blocks": total_blocks,
        "estimated_dev_time": estimated_dev_time,
        "next_steps": next_steps,
        "customization_guide": customization_guide
    }

async def _generate_smart_ui_components(app_type: str, output_directory: str) -> List[Dict[str, Any]]:
    """Generate smart UI components based on app type"""
    
    components = []
    components_dir = os.path.join(output_directory, "components", "ui")
    os.makedirs(components_dir, exist_ok=True)
    
    # App-specific UI components
    ui_patterns = {
        "saas": ["Button", "Card", "Input", "Select", "Table", "Modal", "Tabs"],
        "e-commerce": ["Button", "Card", "Badge", "Rating", "Carousel", "Gallery"],
        "blog": ["Button", "Card", "Typography", "Tag", "ShareButtons"],
        "dashboard": ["Button", "Card", "Chart", "DataTable", "KPICard", "Filter"],
        "social": ["Button", "Card", "Avatar", "PostCard", "CommentBox"],
        "portfolio": ["Button", "Card", "Gallery", "ContactForm", "Timeline"]
    }
    
    needed_components = ui_patterns.get(app_type, ["Button", "Card", "Input"])
    
    for comp_name in needed_components:
        try:
            # Get best component from database for this type
            selected_components = await _smart_component_selection(app_type, comp_name.lower(), limit=1)
            
            if selected_components:
                component = selected_components[0]
                react_code = await _generate_react_from_database_component(component, comp_name)
                
                if react_code:
                    file_path = os.path.join(components_dir, f"{comp_name}.tsx")
                    
                    # Write component file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(react_code)
                    
                    components.append({
                        "filename": f"{comp_name}.tsx",
                        "path": file_path,
                        "type": "ui-component",
                        "size": len(react_code),
                        "component_name": comp_name
                    })
                    
        except Exception as e:
            logger.warning(f"Failed to create UI component {comp_name}: {e}")
    
    return components

async def _generate_auth_components(app_type: str, output_directory: str) -> List[Dict[str, Any]]:
    """Generate authentication components"""
    
    components = []
    auth_dir = os.path.join(output_directory, "components", "auth")
    os.makedirs(auth_dir, exist_ok=True)
    
    auth_templates = {
        "SignIn": '''import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';

export function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // Add authentication logic here
    console.log('Sign in:', { email, password });
    setLoading(false);
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Sign In</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}''',
        
        "SignUp": '''import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';

export function SignUp() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    setLoading(true);
    // Add registration logic here
    console.log('Sign up:', formData);
    setLoading(false);
  };

  const handleChange = (field: string) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, [field]: e.target.value }));
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Create Account</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            type="text"
            placeholder="Full Name"
            value={formData.name}
            onChange={handleChange('name')}
            required
          />
          <Input
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange('email')}
            required
          />
          <Input
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange('password')}
            required
          />
          <Input
            type="password"
            placeholder="Confirm Password"
            value={formData.confirmPassword}
            onChange={handleChange('confirmPassword')}
            required
          />
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Creating account...' : 'Create Account'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}'''
    }
    
    for comp_name, template in auth_templates.items():
        try:
            file_path = os.path.join(auth_dir, f"{comp_name}.tsx")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(template)
            
            components.append({
                "filename": f"{comp_name}.tsx",
                "path": file_path,
                "type": "auth-component",
                "size": len(template),
                "component_name": comp_name
            })
            
        except Exception as e:
            logger.warning(f"Failed to create auth component {comp_name}: {e}")
    
    return components

async def _generate_data_layer(app_type: str, analysis: Dict[str, Any], output_directory: str) -> List[Dict[str, Any]]:
    """Generate data management hooks and contexts"""
    
    components = []
    hooks_dir = os.path.join(output_directory, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    
    # Generate app-specific data hooks
    primary_entity = _get_primary_entity(app_type, analysis)
    
    hook_template = f'''import {{ useState, useEffect }} from 'react';

export interface {primary_entity} {{
  id: string;
  title: string;
  description?: string;
  status: string;
  createdAt: Date;
  updatedAt: Date;
}}

export function use{primary_entity}s() {{
  const [items, setItems] = useState<{primary_entity}[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load items from localStorage on mount
  useEffect(() => {{
    try {{
      const saved = localStorage.getItem('{primary_entity.lower()}s');
      if (saved) {{
        setItems(JSON.parse(saved));
      }}
    }} catch (err) {{
      console.error('Failed to load {primary_entity.lower()}s:', err);
    }}
  }}, []);

  // Save to localStorage when items change
  useEffect(() => {{
    try {{
      localStorage.setItem('{primary_entity.lower()}s', JSON.stringify(items));
    }} catch (err) {{
      console.error('Failed to save {primary_entity.lower()}s:', err);
    }}
  }}, [items]);

  const add{primary_entity} = async (data: Partial<{primary_entity}>) => {{
    setLoading(true);
    setError(null);
    
    try {{
      const new{primary_entity}: {primary_entity} = {{
        id: Date.now().toString(),
        title: data.title || '',
        description: data.description,
        status: data.status || 'active',
        createdAt: new Date(),
        updatedAt: new Date(),
        ...data
      }};
      
      setItems(prev => [...prev, new{primary_entity}]);
      return new{primary_entity};
    }} catch (err) {{
      const message = err instanceof Error ? err.message : 'Failed to add {primary_entity.lower()}';
      setError(message);
      throw new Error(message);
    }} finally {{
      setLoading(false);
    }}
  }};

  const update{primary_entity} = async (id: string, updates: Partial<{primary_entity}>) => {{
    setLoading(true);
    setError(null);
    
    try {{
      setItems(prev => prev.map(item => 
        item.id === id 
          ? {{ ...item, ...updates, updatedAt: new Date() }}
          : item
      ));
    }} catch (err) {{
      const message = err instanceof Error ? err.message : 'Failed to update {primary_entity.lower()}';
      setError(message);
      throw new Error(message);
    }} finally {{
      setLoading(false);
    }}
  }};

  const delete{primary_entity} = async (id: string) => {{
    setLoading(true);
    setError(null);
    
    try {{
      setItems(prev => prev.filter(item => item.id !== id));
    }} catch (err) {{
      const message = err instanceof Error ? err.message : 'Failed to delete {primary_entity.lower()}';
      setError(message);
      throw new Error(message);
    }} finally {{
      setLoading(false);
    }}
  }};

  return {{
    items,
    loading,
    error,
    add{primary_entity},
    update{primary_entity},
    delete{primary_entity}
  }};
}}'''
    
    try:
        file_path = os.path.join(hooks_dir, f"use{primary_entity}s.ts")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(hook_template)
        
        components.append({
            "filename": f"use{primary_entity}s.ts",
            "path": file_path,
            "type": "data-hook",
            "size": len(hook_template),
            "component_name": f"use{primary_entity}s"
        })
        
    except Exception as e:
        logger.warning(f"Failed to create data hook: {e}")
    
    return components

def _get_primary_entity(app_type: str, analysis: Dict[str, Any]) -> str:
    """Determine the primary entity for the app type"""
    
    entity_map = {
        "saas": "Project",
        "e-commerce": "Product", 
        "blog": "Post",
        "portfolio": "Project",
        "social": "Post",
        "dashboard": "Item",
        "landing": "Lead",
        "utility": "Item"
    }
    
    return entity_map.get(app_type, "Item")

async def _generate_app_config(analysis: Dict[str, Any], output_directory: str) -> List[Dict[str, Any]]:
    """Generate app configuration files"""
    
    files = []
    lib_dir = os.path.join(output_directory, "lib")
    os.makedirs(lib_dir, exist_ok=True)
    
    # Generate utils file
    utils_content = '''import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: Date | string) {
  return new Date(date).toLocaleDateString()
}

export function generateId() {
  return Math.random().toString(36).substr(2, 9)
}'''
    
    try:
        utils_path = os.path.join(lib_dir, "utils.ts")
        with open(utils_path, 'w', encoding='utf-8') as f:
            f.write(utils_content)
        
        files.append({
            "filename": "utils.ts",
            "path": utils_path,
            "type": "utility",
            "size": len(utils_content)
        })
    except Exception as e:
        logger.warning(f"Failed to create utils file: {e}")
    
    return files

def _generate_next_steps(analysis: Dict[str, Any], total_blocks: int) -> List[str]:
    """Generate next steps for the developer"""
    
    steps = [
        "1. Review generated components and customize styling as needed",
        "2. Connect data layer to your preferred backend/API",
        "3. Add proper TypeScript types for your data models",
        "4. Implement authentication with your auth provider",
        "5. Add error handling and loading states",
        "6. Configure routing between pages/components",
        "7. Add unit tests for critical components",
        "8. Optimize for performance and accessibility"
    ]
    
    # App-specific next steps
    app_type = analysis["app_type"]
    
    if app_type == "saas":
        steps.extend([
            "9. Set up subscription/billing integration",
            "10. Add user onboarding flow",
            "11. Implement role-based permissions"
        ])
    elif app_type == "e-commerce":
        steps.extend([
            "9. Connect to payment processor (Stripe, PayPal)",
            "10. Set up product inventory management",
            "11. Add order fulfillment workflow"
        ])
    elif app_type == "blog":
        steps.extend([
            "9. Set up content management system",
            "10. Add SEO optimization",
            "11. Implement commenting system"
        ])
    
    return steps

def _generate_customization_guide(analysis: Dict[str, Any], files_created: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate customization guidance"""
    
    return {
        "styling": {
            "theme_colors": "Modify CSS variables in your global styles or Tailwind config",
            "component_variants": "Add new variants to existing components using className props",
            "layout_adjustments": "Update grid layouts and spacing in layout components"
        },
        "functionality": {
            "data_integration": "Replace localStorage hooks with your API calls",
            "authentication": "Connect auth components to your auth provider (Supabase, Auth0, etc.)",
            "state_management": "Consider adding Redux/Zustand for complex state"
        },
        "performance": {
            "lazy_loading": "Add React.lazy() for route-based code splitting",
            "memoization": "Use React.memo() for expensive components",
            "optimization": "Implement virtual scrolling for large lists"
        },
        "files_to_customize": [f["filename"] for f in files_created if f.get("type") in ["ui-component", "auth-component"]]
    }

def _estimate_development_time(analysis: Dict[str, Any], total_blocks: int) -> str:
    """Estimate development time based on complexity"""
    
    complexity = analysis["complexity"]
    app_type = analysis["app_type"]
    
    base_hours = {
        "simple": 8,
        "medium": 20,
        "complex": 40
    }
    
    type_multiplier = {
        "utility": 0.5,
        "landing": 0.7,
        "blog": 1.0,
        "portfolio": 1.0,
        "social": 1.5,
        "dashboard": 1.3,
        "saas": 1.8,
        "e-commerce": 2.0
    }
    
    estimated_hours = base_hours[complexity] * type_multiplier.get(app_type, 1.0)
    
    # Add time for each block
    estimated_hours += total_blocks * 0.5
    
    if estimated_hours < 8:
        return "4-8 hours"
    elif estimated_hours < 20:
        return "1-2 days"
    elif estimated_hours < 40:
        return "3-5 days"
    elif estimated_hours < 80:
        return "1-2 weeks"
    else:
        return "2-4 weeks"

async def _generate_block_content(
    app_type: str,
    block_name: str,
    file_name: str,
    required_components: List[str],
    custom_config: Optional[Dict[str, Any]] = None
) -> str:
    """Generate content for a specific block file using database components"""
    
    # Get components for this block
    components = {}
    for comp_type in required_components:
        selected = await _smart_component_selection(app_type, comp_type, limit=2)
        if selected:
            components[comp_type] = selected[0]
    
    # Block-specific templates
    if block_name == "app-shell":
        if file_name == "AppShell.tsx":
            return _generate_app_shell_template(components, app_type, custom_config)
        elif file_name == "Sidebar.tsx":
            return _generate_sidebar_template(components, app_type, custom_config)
        elif file_name == "TopNav.tsx":
            return _generate_topnav_template(components, app_type, custom_config)
        elif file_name == "AppLayout.tsx":
            return _generate_app_layout_template(components, app_type, custom_config)
    
    elif block_name == "auth":
        if file_name == "SignIn.tsx":
            return _generate_signin_template(components, custom_config)
        elif file_name == "SignUp.tsx":
            return _generate_signup_template(components, custom_config)
        elif file_name == "ForgotPassword.tsx":
            return _generate_forgot_password_template(components, custom_config)
        elif file_name == "AuthLayout.tsx":
            return _generate_auth_layout_template(components, custom_config)
    
    elif block_name == "dashboard":
        if file_name == "Dashboard.tsx":
            return _generate_dashboard_template(components, app_type, custom_config)
        elif file_name == "StatsCards.tsx":
            return _generate_stats_cards_template(components, custom_config)
        elif file_name == "Charts.tsx":
            return _generate_charts_template(components, custom_config)
        elif file_name == "RecentActivity.tsx":
            return _generate_activity_template(components, custom_config)
    
    elif block_name == "settings":
        if file_name == "Settings.tsx":
            return _generate_settings_template(components, custom_config)
        elif file_name == "ProfileSettings.tsx":
            return _generate_profile_settings_template(components, custom_config)
        elif file_name == "AccountSettings.tsx":
            return _generate_account_settings_template(components, custom_config)
        elif file_name == "NotificationSettings.tsx":
            return _generate_notification_settings_template(components, custom_config)
    
    # Default template if specific one not found
    return _generate_default_block_template(block_name, file_name, components, custom_config)

def _generate_app_shell_template(components: Dict, app_type: str, config: Optional[Dict] = None) -> str:
    """Generate complete app shell template"""
    app_name = config.get("app_name", app_type.title()) if config else app_type.title()
    
    return f'''import React, {{ useState }} from 'react';
import {{ Sidebar }} from './Sidebar';
import {{ TopNav }} from './TopNav';
import {{ cn }} from '@/lib/utils';

interface AppShellProps {{
  children: React.ReactNode;
  className?: string;
}}

export function AppShell({{ children, className }}: AppShellProps) {{
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className={{cn("min-h-screen bg-background", className)}}>
      <TopNav 
        onMenuToggle={{() => setSidebarOpen(!sidebarOpen)}}
        onMobileMenuToggle={{() => setMobileMenuOpen(!mobileMenuOpen)}}
      />
      
      <div className="flex h-[calc(100vh-4rem)]">
        <Sidebar 
          open={{sidebarOpen}} 
          mobileOpen={{mobileMenuOpen}}
          onMobileClose={{() => setMobileMenuOpen(false)}}
        />
        
        <main className={{cn(
          "flex-1 overflow-y-auto transition-all duration-300",
          sidebarOpen ? "lg:ml-64" : "lg:ml-0"
        )}}>
          <div className="container mx-auto p-6">
            {{children}}
          </div>
        </main>
      </div>
    </div>
  );
}}
'''

def _generate_sidebar_template(components: Dict, app_type: str, config: Optional[Dict] = None) -> str:
    """Generate sidebar navigation template"""
    return '''import React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { 
  Home, Settings, Users, BarChart, Package, 
  ShoppingBag, FileText, HelpCircle 
} from 'lucide-react';

interface SidebarProps {
  open: boolean;
  mobileOpen: boolean;
  onMobileClose: () => void;
}

export function Sidebar({ open, mobileOpen, onMobileClose }: SidebarProps) {
  const menuItems = [
    { icon: Home, label: 'Dashboard', href: '/' },
    { icon: Package, label: 'Products', href: '/products' },
    { icon: Users, label: 'Customers', href: '/customers' },
    { icon: BarChart, label: 'Analytics', href: '/analytics' },
    { icon: FileText, label: 'Reports', href: '/reports' },
    { icon: Settings, label: 'Settings', href: '/settings' },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {mobileOpen && (
        <div 
          className="lg:hidden fixed inset-0 bg-black/50 z-40"
          onClick={onMobileClose}
        />
      )}
      
      {/* Sidebar */}
      <aside className={cn(
        "fixed lg:static inset-y-0 left-0 z-50 w-64 bg-card border-r transition-transform duration-300",
        open ? "translate-x-0" : "-translate-x-full lg:w-0",
        mobileOpen && "translate-x-0"
      )}>
        <div className="flex h-full flex-col gap-y-5 overflow-y-auto px-6 pb-4">
          <div className="flex h-16 shrink-0 items-center">
            <h2 className="text-lg font-semibold">Your App</h2>
          </div>
          
          <nav className="flex flex-1 flex-col">
            <ul role="list" className="flex flex-1 flex-col gap-y-7">
              <li>
                <ul role="list" className="-mx-2 space-y-1">
                  {menuItems.map((item) => (
                    <li key={item.label}>
                      <a
                        href={item.href}
                        className={cn(
                          "group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold",
                          "hover:text-primary hover:bg-muted"
                        )}
                      >
                        <item.icon className="h-5 w-5 shrink-0" />
                        {item.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </li>
            </ul>
          </nav>
        </div>
      </aside>
    </>
  );
}
'''

def _generate_topnav_template(components: Dict, app_type: str, config: Optional[Dict] = None) -> str:
    """Generate top navigation template"""
    return '''import React from 'react';
import { Button } from '@/components/ui/button';
import { Menu, Bell, User } from 'lucide-react';

interface TopNavProps {
  onMenuToggle: () => void;
  onMobileMenuToggle: () => void;
}

export function TopNav({ onMenuToggle, onMobileMenuToggle }: TopNavProps) {
  return (
    <header className="sticky top-0 z-40 border-b bg-background">
      <div className="flex h-16 items-center gap-x-4 px-4 sm:gap-x-6 sm:px-6 lg:px-8">
        <Button
          variant="ghost"
          size="icon"
          className="lg:hidden"
          onClick={onMobileMenuToggle}
        >
          <Menu className="h-5 w-5" />
        </Button>
        
        <Button
          variant="ghost"
          size="icon"
          className="hidden lg:flex"
          onClick={onMenuToggle}
        >
          <Menu className="h-5 w-5" />
        </Button>
        
        <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
          <div className="flex flex-1" />
          
          <div className="flex items-center gap-x-4 lg:gap-x-6">
            <Button variant="ghost" size="icon">
              <Bell className="h-5 w-5" />
            </Button>
            
            <Button variant="ghost" size="icon">
              <User className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}
'''

def _generate_signin_template(components: Dict, config: Optional[Dict] = None) -> str:
    """Generate sign in page template"""
    return '''import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

export function SignIn() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Add your authentication logic here
      console.log('Sign in:', { email, password });
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Redirect on success
      router.push('/dashboard');
    } catch (err) {
      setError('Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold">Sign in</CardTitle>
        <CardDescription>
          Enter your email and password to access your account
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="name@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <div className="flex items-center justify-between">
            <a href="/auth/forgot-password" className="text-sm text-primary hover:underline">
              Forgot password?
            </a>
          </div>
        </CardContent>
        
        <CardFooter className="flex flex-col space-y-4">
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign in'}
          </Button>
          
          <p className="text-sm text-center text-muted-foreground">
            Don't have an account?{' '}
            <a href="/auth/signup" className="text-primary hover:underline">
              Sign up
            </a>
          </p>
        </CardFooter>
      </form>
    </Card>
  );
}
'''

def _generate_dashboard_template(components: Dict, app_type: str, config: Optional[Dict] = None) -> str:
    """Generate dashboard page template"""
    return f'''import React from 'react';
import {{ StatsCards }} from './StatsCards';
import {{ Charts }} from './Charts';
import {{ RecentActivity }} from './RecentActivity';

export function Dashboard() {{
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome to your {app_type} dashboard
        </p>
      </div>
      
      <StatsCards />
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
        <div className="col-span-4">
          <Charts />
        </div>
        <div className="col-span-3">
          <RecentActivity />
        </div>
      </div>
    </div>
  );
}}
'''

def _generate_stats_cards_template(components: Dict, config: Optional[Dict] = None) -> str:
    """Generate stats cards template"""
    return '''import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp, TrendingDown, Users, DollarSign, Package, Activity } from 'lucide-react';

export function StatsCards() {
  const stats = [
    {
      title: 'Total Revenue',
      value: '$45,231.89',
      change: '+20.1%',
      trend: 'up',
      icon: DollarSign,
    },
    {
      title: 'New Customers',
      value: '+2,350',
      change: '+180.1%',
      trend: 'up',
      icon: Users,
    },
    {
      title: 'Active Orders',
      value: '12,234',
      change: '+19%',
      trend: 'up',
      icon: Package,
    },
    {
      title: 'Active Now',
      value: '573',
      change: '-4.3%',
      trend: 'down',
      icon: Activity,
    },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => (
        <Card key={stat.title}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
            <stat.icon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stat.value}</div>
            <p className="text-xs text-muted-foreground">
              {stat.trend === 'up' ? (
                <TrendingUp className="inline h-3 w-3 text-green-500" />
              ) : (
                <TrendingDown className="inline h-3 w-3 text-red-500" />
              )}
              <span className={stat.trend === 'up' ? 'text-green-500' : 'text-red-500'}>
                {' '}{stat.change}
              </span>
              {' '}from last month
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
'''

def _generate_block_index(blocks: List[str], definitions: Dict) -> str:
    """Generate index file for all blocks"""
    exports = []
    for block in blocks:
        if block in definitions:
            for file in definitions[block]["files"]:
                component_name = file.replace('.tsx', '')
                exports.append(f"export {{ {component_name} }} from './{block}/{file}';")
    
    return '\n'.join(exports)

def _generate_default_block_template(block_name: str, file_name: str, components: Dict, config: Optional[Dict] = None) -> str:
    """Generate a default template for any block"""
    component_name = file_name.replace('.tsx', '')
    
    return f'''import React from 'react';
import {{ cn }} from '@/lib/utils';

interface {component_name}Props {{
  className?: string;
}}

export function {component_name}({{ className }}: {component_name}Props) {{
  return (
    <div className={{cn("", className)}}>
      {{/* {block_name} - {component_name} content */}}
      <p>Generated {component_name} for {block_name} block</p>
    </div>
  );
}}
'''

def _generate_app_layout_template(components: Dict, app_type: str, config: Optional[Dict] = None) -> str:
    """Generate app layout template"""
    return '''import React from 'react';
import { AppShell } from './AppShell';

interface AppLayoutProps {
  children: React.ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
  return <AppShell>{children}</AppShell>;
}
'''

def _generate_signup_template(components: Dict, config: Optional[Dict] = None) -> str:
    """Generate sign up template"""
    return '''import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

export function SignUp() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    setLoading(true);

    try {
      // Add your registration logic here
      console.log('Sign up:', formData);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Redirect on success
      router.push('/dashboard');
    } catch (err) {
      setError('Failed to create account');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold">Create an account</CardTitle>
        <CardDescription>
          Enter your information to get started
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="confirmPassword">Confirm Password</Label>
            <Input
              id="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
              required
            />
          </div>
        </CardContent>
        
        <CardFooter className="flex flex-col space-y-4">
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Creating account...' : 'Sign up'}
          </Button>
          
          <p className="text-sm text-center text-muted-foreground">
            Already have an account?{' '}
            <a href="/auth/signin" className="text-primary hover:underline">
              Sign in
            </a>
          </p>
        </CardFooter>
      </form>
    </Card>
  );
}
'''

def _generate_forgot_password_template(components: Dict, config: Optional[Dict] = None) -> str:
    """Generate forgot password template"""
    return '''import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

export function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Add password reset logic here
      console.log('Reset password for:', email);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setSubmitted(true);
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Check your email</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            We've sent a password reset link to {email}
          </p>
        </CardContent>
        <CardFooter>
          <a href="/auth/signin" className="text-sm text-primary hover:underline">
            Back to sign in
          </a>
        </CardFooter>
      </Card>
    );
  }

  return (
    <Card className="w-full max-w-md">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold">Forgot password</CardTitle>
        <CardDescription>
          Enter your email and we'll send you a reset link
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="name@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
        </CardContent>
        
        <CardFooter className="flex flex-col space-y-4">
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Sending...' : 'Send reset link'}
          </Button>
          
          <a href="/auth/signin" className="text-sm text-center text-primary hover:underline">
            Back to sign in
          </a>
        </CardFooter>
      </form>
    </Card>
  );
}
'''

def _generate_auth_layout_template(components: Dict, config: Optional[Dict] = None) -> str:
    """Generate auth layout template"""
    return '''import React from 'react';

interface AuthLayoutProps {
  children: React.ReactNode;
}

export function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="w-full max-w-md px-4">
        {children}
      </div>
    </div>
  );
}
'''

def _generate_charts_template(components: Dict, config: Optional[Dict] = None) -> str:
    """Generate charts template"""
    return '''import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export function Charts() {
  return (
    <Card className="col-span-4">
      <CardHeader>
        <CardTitle>Revenue Overview</CardTitle>
        <CardDescription>Monthly revenue for the last 6 months</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[300px] flex items-center justify-center text-muted-foreground">
          Chart visualization would go here
        </div>
      </CardContent>
    </Card>
  );
}
'''

def _generate_activity_template(components: Dict, config: Optional[Dict] = None) -> str:
    """Generate recent activity template"""
    return '''import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export function RecentActivity() {
  const activities = [
    { id: 1, user: 'John Doe', action: 'Created new order #1234', time: '2 hours ago' },
    { id: 2, user: 'Jane Smith', action: 'Updated customer profile', time: '4 hours ago' },
    { id: 3, user: 'Mike Johnson', action: 'Processed refund for order #1233', time: '6 hours ago' },
    { id: 4, user: 'Sarah Wilson', action: 'Added new product to inventory', time: '8 hours ago' },
  ];

  return (
    <Card className="col-span-3">
      <CardHeader>
        <CardTitle>Recent Activity</CardTitle>
        <CardDescription>Latest actions in your system</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {activities.map((activity) => (
            <div key={activity.id} className="flex items-start space-x-4">
              <div className="w-2 h-2 bg-primary rounded-full mt-2" />
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium">{activity.user}</p>
                <p className="text-sm text-muted-foreground">{activity.action}</p>
                <p className="text-xs text-muted-foreground">{activity.time}</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
'''

def _generate_settings_template(components: Dict, config: Optional[Dict] = None) -> str:
    """Generate settings page template"""
    return '''import React from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ProfileSettings } from './ProfileSettings';
import { AccountSettings } from './AccountSettings';
import { NotificationSettings } from './NotificationSettings';

export function Settings() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground">
          Manage your account settings and preferences
        </p>
      </div>
      
      <Tabs defaultValue="profile" className="space-y-4">
        <TabsList>
          <TabsTrigger value="profile">Profile</TabsTrigger>
          <TabsTrigger value="account">Account</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
        </TabsList>
        
        <TabsContent value="profile">
          <ProfileSettings />
        </TabsContent>
        
        <TabsContent value="account">
          <AccountSettings />
        </TabsContent>
        
        <TabsContent value="notifications">
          <NotificationSettings />
        </TabsContent>
      </Tabs>
    </div>
  );
}
'''

def _generate_profile_settings_template(components: Dict, config: Optional[Dict] = None) -> str:
    """Generate profile settings template"""
    return '''import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';

export function ProfileSettings() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Profile</CardTitle>
        <CardDescription>Update your profile information</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="name">Name</Label>
          <Input id="name" placeholder="Your name" />
        </div>
        
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" placeholder="your@email.com" />
        </div>
        
        <div className="space-y-2">
          <Label htmlFor="bio">Bio</Label>
          <Textarea id="bio" placeholder="Tell us about yourself" />
        </div>
        
        <Button>Save changes</Button>
      </CardContent>
    </Card>
  );
}
'''

def _generate_account_settings_template(components: Dict, config: Optional[Dict] = None) -> str:
    """Generate account settings template"""
    return '''import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export function AccountSettings() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Password</CardTitle>
          <CardDescription>Change your password</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="current">Current password</Label>
            <Input id="current" type="password" />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="new">New password</Label>
            <Input id="new" type="password" />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="confirm">Confirm password</Label>
            <Input id="confirm" type="password" />
          </div>
          
          <Button>Update password</Button>
        </CardContent>
      </Card>
      
      <Card className="border-destructive">
        <CardHeader>
          <CardTitle className="text-destructive">Danger Zone</CardTitle>
          <CardDescription>Irreversible actions</CardDescription>
        </CardHeader>
        <CardContent>
          <Button variant="destructive">Delete account</Button>
        </CardContent>
      </Card>
    </div>
  );
}
'''

def _generate_notification_settings_template(components: Dict, config: Optional[Dict] = None) -> str:
    """Generate notification settings template"""
    return '''import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';

export function NotificationSettings() {
  const notifications = [
    { id: 'email', label: 'Email notifications', description: 'Receive updates via email' },
    { id: 'push', label: 'Push notifications', description: 'Receive push notifications' },
    { id: 'sms', label: 'SMS notifications', description: 'Receive SMS updates' },
    { id: 'marketing', label: 'Marketing emails', description: 'Receive marketing and promotional emails' },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Notifications</CardTitle>
        <CardDescription>Configure how you receive notifications</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {notifications.map((notification) => (
          <div key={notification.id} className="flex items-center justify-between space-x-2">
            <Label htmlFor={notification.id} className="flex flex-col space-y-1 cursor-pointer">
              <span>{notification.label}</span>
              <span className="text-sm font-normal text-muted-foreground">
                {notification.description}
              </span>
            </Label>
            <Switch id={notification.id} />
          </div>
        ))}
        
        <Button className="w-full">Save preferences</Button>
      </CardContent>
    </Card>
  );
}
'''

# ===================================================================
# PROMPTS AND RESOURCES
# ===================================================================

@mcp.prompt
def react_generation_guide(app_type: str) -> str:
    """Guide AI in using React template generation effectively"""
    return f"""
    You are building a {app_type} application using the Figma design system database.
    
    FIRST: If the user hasn't been specific about their requirements, ASK:
    - What specific features do you need in your {app_type}?
    - Are there any particular UI patterns you prefer?
    - Do you need forms, data tables, charts, or other specific components?
    
    THEN follow these steps:
    1. First, analyze what components are needed based on user requirements
    2. Query the database using preview_figma_components with relevant filters
    3. Select 10-15 most relevant components (not all 1054!)
    4. Use bulk_create_component_files to generate the React components
    
    Component selection criteria:
    - Core UI elements (buttons, inputs, cards)
    - App-specific components based on user needs
    - Layout components (headers, navigation)
    - Feedback components (alerts, toasts)
    
    IMPORTANT: Be selective! Quality over quantity. The examples in resources are just suggestions - adapt to user needs.
    """

@mcp.prompt
def template_customization_guide(component_type: str) -> str:
    """Guide AI in customizing templates appropriately"""
    return f"""
    When generating React components for {component_type}, customize templates as follows:
    
    1. Variable Substitution:
       - {{{{componentName}}}} - Use PascalCase (e.g., TodoItem, UserCard)
       - {{{{variant}}}} - Describe the variant clearly (e.g., "primary", "outlined")
       - {{{{propsInterface}}}} - Generate TypeScript interfaces based on Figma props
       - {{{{defaultProps}}}} - Set sensible defaults for the component type
    
    2. Component-Specific Customization:
       - Buttons: Include onClick, disabled, loading states
       - Forms: Add validation props, error states
       - Cards: Include content slots, actions
       - Lists: Add item rendering, selection
    
    3. Maintain Consistency:
       - Use the same prop naming conventions
       - Follow the design system's patterns
       - Include proper TypeScript types
    """

@mcp.prompt
def file_vs_memory_decision() -> str:
    """Help AI decide when to use bulk_create_component_files vs build_app_components"""
    return """
    Choose the right generation method:
    
    USE bulk_create_component_files WHEN:
    - User wants actual files created on disk
    - Building a real application
    - Need persistent output
    - Creating a starter template
    - User asks to "create", "generate", or "build" an app
    
    USE build_app_components WHEN:
    - User wants to preview components
    - Exploring design options
    - Need quick iteration
    - Testing component combinations
    - User asks to "show", "preview", or "demonstrate"
    
    DEFAULT: Use bulk_create_component_files for actual development work.
    """

@mcp.prompt
def component_selection_strategy(app_description: str) -> str:
    """Guide AI in selecting the right mix of components"""
    return f"""
    For the app: "{app_description}", select components strategically:
    
    1. Essential Components (5-7):
       - Layout structure (Header, Container, Grid)
       - Primary actions (Button, Link)
       - Data input (Input, Form, Select)
    
    2. App-Specific Components (3-5):
       - Based on app type (TodoItem for todo apps, ProductCard for e-commerce)
       - Domain-specific widgets
    
    3. Supporting Components (2-3):
       - Feedback (Alert, Toast, Loading)
       - Navigation (Tabs, Breadcrumb)
    
    Total: Aim for 10-15 components maximum.
    
    Query Strategy:
    1. Start with category filters (e.g., category='forms' for input-heavy apps)
    2. Use component_filter for specific searches
    3. Check popularity_score for commonly used components
    """

@mcp.resource("figma-db://best-practices/react-templates")
def react_template_best_practices() -> str:
    """Best practices for React template generation from database"""
    return """
    # React Template Generation Best Practices
    
    ## 1. Template Structure
    - Always generate TypeScript (.tsx) files
    - Include proper imports (React, types, styles)
    - Export as default for better tree-shaking
    - Use functional components with hooks
    
    ## 2. Props Interface
    - Generate from Figma component props
    - Include variant props (size, color, state)
    - Add event handlers (onClick, onChange)
    - Make appropriate props optional
    
    ## 3. Styling Approach
    - Use CSS modules or styled-components
    - Respect Figma's design tokens
    - Include responsive considerations
    - Support dark/light themes
    
    ## 4. Component Composition
    - Make components composable
    - Use children prop appropriately
    - Support ref forwarding
    - Include display name for debugging
    
    ## 5. File Organization
    components/
    ├── Button/
    │   ├── Button.tsx
    │   ├── Button.module.css
    │   └── index.ts
    ├── Card/
    │   ├── Card.tsx
    │   └── Card.module.css
    └── index.ts (barrel export)
    """

@mcp.resource("figma-db://workflow/app-types")
def app_type_component_mapping() -> str:
    """Component selection patterns for different app types"""
    return """
    # Component Selection by App Type
    
    **IMPORTANT**: These are EXAMPLES to guide component selection. Always:
    1. ASK THE USER what specific app they want to build
    2. ASK THE USER about specific features they need
    3. CUSTOMIZE component selection based on their requirements
    
    The user may say something like:
    - "Build me a task manager with categories"
    - "Create a simple blog"  
    - "I need a dashboard for analytics"
    - Or something completely different!
    
    ## Example: Todo App
    Common components might include:
    - TodoItem (with checkbox, delete)
    - TodoList (container)
    - AddTodoForm (input + button)
    - FilterTabs (all/active/completed)
    - Header (with title)
    - Button (primary/secondary)
    - Checkbox (for completion)
    
    ## Example: Dashboard
    Common components might include:
    - StatCard (metrics display)
    - Chart (placeholder)
    - DataTable (with sorting)
    - Sidebar (navigation)
    - Header (with user menu)
    - SearchBar
    - FilterDropdown
    
    ## Example: E-commerce
    Common components might include:
    - ProductCard (image, price, actions)
    - ProductGrid (responsive layout)
    - ShoppingCart (sidebar/modal)
    - CheckoutForm (multi-step)
    - PriceDisplay (with currency)
    - QuantitySelector
    - CategoryFilter
    
    ## Example: Blog
    Common components might include:
    - ArticleCard (preview)
    - ArticleLayout (full post)
    - CommentSection
    - AuthorBio
    - TagList
    - Pagination
    - SearchBar
    
    ## Example: Form-heavy App
    Common components might include:
    - Input (text, email, password)
    - Select (dropdown)
    - Checkbox/Radio groups
    - FormField (label + input + error)
    - MultiStepForm
    - ValidationMessage
    - SubmitButton (with loading)
    
    ## Custom Apps
    The user might want something unique:
    - Recipe app (RecipeCard, IngredientList, CookingTimer)
    - Social media (PostCard, CommentThread, UserProfile)
    - Project management (KanbanBoard, TaskCard, Timeline)
    - Or any other type!
    
    ALWAYS prioritize user requirements over these examples.
    """

@mcp.resource("figma-db://development/file-structure")
def generated_file_structure_guide() -> str:
    """Recommended file structure for generated components"""
    return """
    # Generated Project Structure
    
    my-app/
    ├── src/
    │   ├── components/           # All Figma components
    │   │   ├── Button/
    │   │   │   ├── Button.tsx
    │   │   │   ├── Button.module.css
    │   │   │   ├── Button.types.ts
    │   │   │   └── index.ts
    │   │   └── index.ts         # Barrel exports
    │   ├── hooks/               # Custom React hooks
    │   ├── utils/               # Helper functions
    │   ├── types/               # Shared TypeScript types
    │   └── styles/              # Global styles, variables
    ├── package.json             # Dependencies
    ├── tsconfig.json           # TypeScript config
    └── README.md               # Setup instructions
    
    ## Component File Template
    ```tsx
    // Button.tsx
    import React from 'react';
    import styles from './Button.module.css';
    import { ButtonProps } from './Button.types';
    
    export const Button: React.FC<ButtonProps> = ({
      children,
      variant = 'primary',
      size = 'medium',
      onClick,
      ...props
    }) => {
      return (
        <button
          className={`${styles.button} ${styles[variant]} ${styles[size]}`}
          onClick={onClick}
          {...props}
        >
          {children}
        </button>
      );
    };
    
    Button.displayName = 'Button';
    export default Button;
    ```
    """

@mcp.resource("figma-db://templates/starter-apps")
def starter_app_templates() -> str:
    """Complete starter app configurations"""
    return """
    # Starter App Templates
    
    ## Minimal Todo App
    ```json
    {
      "components": [
        "TodoItem",
        "TodoList", 
        "AddTodoForm",
        "Button",
        "Input",
        "Checkbox",
        "Container"
      ],
      "features": [
        "Add new todos",
        "Mark as complete",
        "Delete todos",
        "Filter by status"
      ]
    }
    ```
    
    ## Basic Dashboard
    ```json
    {
      "components": [
        "StatCard",
        "DataTable",
        "Header",
        "Sidebar",
        "Chart",
        "Button",
        "SearchBar"
      ],
      "layout": "sidebar-content"
    }
    ```
    
    ## Component Combinations
    - Form = Input + Button + Label + ErrorMessage
    - Card = CardHeader + CardBody + CardFooter
    - Table = TableHeader + TableRow + TableCell + Pagination
    - Modal = ModalOverlay + ModalContent + ModalActions
    """

# ===================================================================
# SERVER EXECUTION
# ===================================================================

if __name__ == "__main__":
    # Get port from environment or default to 8031
    port = int(os.getenv("FIGMA_MCP_PORT", 8031))
    
    logger.info(f"Starting Figma MCP server on port {port}")
    logger.info("Available tools:")
    try:
        # This might fail on some FastMCP versions, so wrap in try/catch
        tools = mcp.list_tools()
        for tool in tools:
            logger.info(f"  - {tool.name}")
    except Exception as e:
        logger.info("Could not list tools: %s", str(e))
        logger.info("Server starting anyway...")
    
    # Run with streamable-http transport for proper MCP compatibility  
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)