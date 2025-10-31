#!/usr/bin/env python3
"""
Section-Based Tools Update for Figma MCP Server
Adds new tools to work with the sections table for complete React templates
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

# New tool definitions to add to the server

async def preview_sections(
    section_filter: Optional[str] = None,
    category: Optional[str] = None,
    block_type: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Preview and search React sections from database with fast filtering
    
    Args:
        section_filter: Search term to filter sections (name, description, tags)
        category: Filter by category (marketing, e-commerce, etc.)
        block_type: Filter by block type (hero, pricing, testimonials, etc.)
        limit: Maximum number of sections to return (default: 20)
        
    Returns:
        List of matching sections with metadata
    """
    try:
        # Build query
        query = db_client.supabase.table('sections').select('*')
        
        # Apply filters
        if section_filter:
            # Use the search_vector for full-text search if available
            query = query.or_(
                f"name.ilike.%{section_filter}%,"
                f"description.ilike.%{section_filter}%,"
                f"tags.cs.{{{section_filter}}}"
            )
            
        if category:
            query = query.eq('category', category)
            
        if block_type:
            query = query.eq('block_type', block_type)
            
        # Execute query with limit
        result = query.limit(limit).execute()
        
        if not result.data:
            return {
                "sections": [],
                "total": 0,
                "message": "No sections found matching criteria"
            }
            
        # Format sections for output
        sections = []
        for section in result.data:
            sections.append({
                "id": section.get('id'),
                "name": section.get('name'),
                "description": section.get('description'),
                "category": section.get('category'),
                "block_type": section.get('block_type'),
                "tags": section.get('tags', []),
                "source": section.get('source'),
                "has_template": bool(section.get('react_template')),
                "preview_url": section.get('preview_image_url')
            })
            
        return {
            "sections": sections,
            "total": len(sections),
            "available_categories": list(set(s['category'] for s in sections if s['category'])),
            "available_block_types": list(set(s['block_type'] for s in sections if s['block_type']))
        }
        
    except Exception as e:
        logger.error(f"Error previewing sections: {str(e)}")
        return {
            "error": f"Failed to preview sections: {str(e)}",
            "sections": []
        }


async def get_section_template(
    section_id: Optional[str] = None,
    section_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get the full React template code for a section
    
    Args:
        section_id: The section's ID
        section_name: The section's name (alternative to ID)
        
    Returns:
        Section details with full React template code
    """
    try:
        if not section_id and not section_name:
            return {"error": "Either section_id or section_name must be provided"}
            
        # Query by ID or name
        if section_id:
            result = db_client.supabase.table('sections').select('*').eq('id', section_id).execute()
        else:
            result = db_client.supabase.table('sections').select('*').eq('name', section_name).execute()
            
        if not result.data:
            return {"error": f"Section not found"}
            
        section = result.data[0]
        
        return {
            "id": section.get('id'),
            "name": section.get('name'),
            "description": section.get('description'),
            "category": section.get('category'),
            "block_type": section.get('block_type'),
            "tags": section.get('tags', []),
            "react_template": section.get('react_template', ''),
            "dependencies": section.get('dependencies', {}),
            "props_schema": section.get('props_schema', {}),
            "example_props": section.get('example_props', {}),
            "source": section.get('source'),
            "preview_url": section.get('preview_image_url')
        }
        
    except Exception as e:
        logger.error(f"Error getting section template: {str(e)}")
        return {"error": f"Failed to get section template: {str(e)}"}


async def list_section_categories() -> Dict[str, Any]:
    """
    List all available section categories with counts
    
    Returns:
        Categories with section counts and descriptions
    """
    try:
        # Get unique categories with counts
        result = db_client.supabase.rpc('get_section_category_counts').execute()
        
        # If RPC doesn't exist, fall back to manual query
        if not result.data:
            result = db_client.supabase.table('sections').select('category').execute()
            
            if result.data:
                # Count categories manually
                category_counts = {}
                for item in result.data:
                    cat = item.get('category')
                    if cat:
                        category_counts[cat] = category_counts.get(cat, 0) + 1
                        
                categories = [
                    {"name": cat, "count": count} 
                    for cat, count in category_counts.items()
                ]
            else:
                categories = []
        else:
            categories = result.data
            
        # Add descriptions for known categories
        category_info = {
            "marketing": "Marketing and landing page sections",
            "marketing-landing": "Tailwind UI marketing templates",
            "e-commerce": "E-commerce and product sections",
            "navigation-layout": "Headers, footers, and navigation",
            "forms": "Contact forms, newsletters, and inputs",
            "content-display": "Blogs, galleries, and content sections",
            "analytics": "Stats and data visualization",
            "utility": "Banners, errors, and utility sections"
        }
        
        for cat in categories:
            cat['description'] = category_info.get(cat['name'], 'General purpose sections')
            
        return {
            "categories": categories,
            "total": len(categories)
        }
        
    except Exception as e:
        logger.error(f"Error listing categories: {str(e)}")
        return {"error": f"Failed to list categories: {str(e)}", "categories": []}


async def search_sections_by_use_case(
    use_case: str,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Search sections by use case (e.g., 'saas landing', 'blog', 'pricing')
    
    Args:
        use_case: The use case to search for
        limit: Maximum results to return
        
    Returns:
        Sections matching the use case
    """
    try:
        # Search in multiple fields for flexibility
        result = db_client.supabase.table('sections').select('*').or_(
            f"name.ilike.%{use_case}%,"
            f"description.ilike.%{use_case}%,"
            f"tags.cs.{{{use_case}}},"
            f"block_type.ilike.%{use_case}%"
        ).limit(limit).execute()
        
        if not result.data:
            return {
                "sections": [],
                "message": f"No sections found for use case: {use_case}"
            }
            
        sections = []
        for section in result.data:
            sections.append({
                "id": section.get('id'),
                "name": section.get('name'),
                "description": section.get('description'),
                "category": section.get('category'),
                "block_type": section.get('block_type'),
                "tags": section.get('tags', []),
                "relevance": "high" if use_case.lower() in section.get('name', '').lower() else "medium"
            })
            
        # Sort by relevance
        sections.sort(key=lambda x: x['relevance'], reverse=True)
        
        return {
            "use_case": use_case,
            "sections": sections,
            "total": len(sections)
        }
        
    except Exception as e:
        logger.error(f"Error searching by use case: {str(e)}")
        return {"error": f"Failed to search sections: {str(e)}", "sections": []}


# Update the build_app_components function to use sections
async def build_complete_page(
    page_type: str,
    sections_config: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Build a complete page using sections from the database
    
    Args:
        page_type: Type of page (landing, blog, ecommerce, dashboard)
        sections_config: Optional list of section configurations
        
    Returns:
        Complete page with all sections assembled
    """
    try:
        # Default section configurations for different page types
        default_configs = {
            "landing": [
                {"block_type": "navigation", "category": "marketing-landing"},
                {"block_type": "hero", "category": "marketing-landing"},
                {"block_type": "features", "category": "marketing-landing"},
                {"block_type": "testimonials", "category": "marketing-landing"},
                {"block_type": "pricing", "category": "marketing-landing"},
                {"block_type": "cta", "category": "marketing-landing"},
                {"block_type": "footer", "category": "marketing-landing"}
            ],
            "blog": [
                {"block_type": "navigation", "category": "navigation-layout"},
                {"block_type": "hero", "category": "navigation-layout"},
                {"block_type": "blog", "category": "marketing-landing"},
                {"block_type": "newsletter", "category": "forms"},
                {"block_type": "footer", "category": "navigation-layout"}
            ],
            "ecommerce": [
                {"block_type": "navigation", "category": "marketing-landing"},
                {"block_type": "hero", "category": "marketing-landing"},
                {"block_type": "ecommerce", "category": "marketing-landing"},
                {"block_type": "testimonials", "category": "marketing-landing"},
                {"block_type": "footer", "category": "marketing-landing"}
            ]
        }
        
        # Use provided config or default
        config = sections_config or default_configs.get(page_type, default_configs['landing'])
        
        # Fetch sections for each config
        page_sections = []
        imports = set()
        
        for section_config in config:
            # Query for matching section
            query = db_client.supabase.table('sections').select('*')
            
            if 'id' in section_config:
                query = query.eq('id', section_config['id'])
            else:
                if 'block_type' in section_config:
                    query = query.eq('block_type', section_config['block_type'])
                if 'category' in section_config:
                    query = query.eq('category', section_config['category'])
                    
            result = query.limit(1).execute()
            
            if result.data:
                section = result.data[0]
                page_sections.append({
                    "name": section['name'],
                    "component": f"{section['name'].replace(' ', '').replace('-', '')}",
                    "template": section.get('react_template', ''),
                    "props": section.get('example_props', {})
                })
                
                # Collect dependencies
                deps = section.get('dependencies', {})
                if isinstance(deps, dict):
                    for dep in deps.get('npm', []):
                        imports.add(dep)
                        
        # Generate complete page code
        page_code = f"""import React from 'react';
{chr(10).join(f"import {{ {imp} }} from '{imp}';" for imp in sorted(imports))}

// Section Components
{chr(10).join(s['template'] for s in page_sections if s['template'])}

// Main Page Component
export default function {page_type.title()}Page() {{
  return (
    <div className="min-h-screen bg-white">
      {chr(10).join(f"<{s['component']} />" for s in page_sections)}
    </div>
  );
}}
"""
        
        return {
            "page_type": page_type,
            "sections_used": [s['name'] for s in page_sections],
            "code": page_code,
            "dependencies": list(imports)
        }
        
    except Exception as e:
        logger.error(f"Error building page: {str(e)}")
        return {"error": f"Failed to build page: {str(e)}"}