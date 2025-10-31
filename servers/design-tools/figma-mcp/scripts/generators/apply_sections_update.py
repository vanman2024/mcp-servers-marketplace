#!/usr/bin/env python3
"""
Apply Sections Architecture Update to Figma MCP Server
=====================================================
This script updates figma_server_db.py to use the new sections architecture.
"""

import re
import shutil
from datetime import datetime

def apply_sections_update():
    """Apply the sections architecture update to figma_server_db.py"""
    
    # Backup the original file
    original_file = 'src/figma_server_db.py'
    backup_file = f'src/figma_server_db_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.py'
    
    print(f"Creating backup: {backup_file}")
    shutil.copy(original_file, backup_file)
    
    # Read the original file
    with open(original_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply replacements
    replacements = [
        # Replace application_blocks table references
        (r"\.table\('application_blocks'\)", ".table('sections')"),
        (r'\.table\("application_blocks"\)', '.table("sections")'),
        
        # Update error messages
        (r"No application blocks found", "No sections found"),
        (r"Failed to create application blocks", "Failed to create sections"),
        
        # Update function descriptions
        (r"application block files", "section files"),
        (r"application blocks", "sections"),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Add new imports if not present
    if "from typing import Dict, Any, List, Optional, Union" not in content:
        # Update the import to include Union if needed
        content = content.replace(
            "from typing import Dict, Any, List, Optional",
            "from typing import Dict, Any, List, Optional, Union"
        )
    
    # Write the updated content
    with open(original_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {original_file}")
    print("✅ Created backup at", backup_file)
    
    # Create a summary of changes
    summary = """
    Applied Updates:
    ===============
    1. Replaced 'application_blocks' table references with 'sections'
    2. Updated error messages to use 'sections' terminology
    3. Updated function descriptions
    
    Next Steps:
    ==========
    1. Add the new functions from figma_server_db_sections_complete_update.py
    2. Test all endpoints with the new schema
    3. Execute the search_sections RPC function in the database
    """
    
    print(summary)
    
    # Create a new functions file to be manually added
    new_functions_file = 'src/new_sections_functions.py'
    
    new_functions_content = '''# =====================================================
# NEW FUNCTIONS TO ADD TO figma_server_db.py
# =====================================================

@mcp.tool()
async def get_sections_by_category(
    category: str,
    project_id: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Get sections filtered by category with optional project filtering
    
    Args:
        category: Category to filter by (marketing, e-commerce, forms, etc.)
        project_id: Optional project ID to get project-specific sections
        limit: Maximum number of sections to return
    
    Returns:
        List of sections with metadata
    """
    try:
        query = db_client.supabase.table('sections').select('*')
        query = query.eq('category', category)
        
        if project_id:
            # Get project-specific sections or template sections
            query = query.or_(f'project_id.eq.{project_id},is_template.eq.true')
        else:
            # Only get template sections
            query = query.eq('is_template', True)
        
        query = query.limit(limit)
        result = query.execute()
        
        return {
            "success": True,
            "sections": result.data,
            "count": len(result.data),
            "category": category
        }
        
    except Exception as e:
        logger.error(f"Failed to get sections by category: {e}")
        return {
            "success": False,
            "error": str(e),
            "sections": []
        }

@mcp.tool()
async def get_project_specification(project_id: str) -> Dict[str, Any]:
    """
    Get project-specific design tokens and style guide
    
    Args:
        project_id: The project UUID
    
    Returns:
        Project specifications including design tokens
    """
    try:
        result = db_client.supabase.table('project_specifications').select('*').eq('project_id', project_id).single().execute()
        
        if result.data:
            return {
                "success": True,
                "specification": result.data
            }
        else:
            return {
                "success": False,
                "error": "Project specification not found"
            }
            
    except Exception as e:
        logger.error(f"Failed to get project specification: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def create_custom_section(
    section_data: Dict[str, Any],
    project_id: str
) -> Dict[str, Any]:
    """
    Create a custom section for a specific project
    
    Args:
        section_data: Section data including name, code, etc.
        project_id: Project to associate the section with
    
    Returns:
        Created section details
    """
    try:
        # Add project_id and other defaults
        section_data['project_id'] = project_id
        section_data['source'] = 'custom'
        section_data['is_template'] = False
        section_data['published'] = True
        
        result = db_client.supabase.table('sections').insert(section_data).execute()
        
        return {
            "success": True,
            "section": result.data[0] if result.data else None,
            "message": "Custom section created successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to create custom section: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def search_sections(
    query: str,
    project_id: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Search sections using full-text search
    
    Args:
        query: Search query
        project_id: Optional project ID filter
        category: Optional category filter
        limit: Maximum results to return
    
    Returns:
        Matching sections
    """
    try:
        # Use RPC function for full-text search
        params = {
            'search_query': query,
            'limit_results': limit
        }
        
        if category:
            params['category_filter'] = category
            
        if project_id:
            params['project_filter'] = project_id
            
        result = db_client.supabase.rpc('search_sections', params).execute()
        
        return {
            "success": True,
            "sections": result.data,
            "count": len(result.data),
            "query": query
        }
        
    except Exception as e:
        logger.error(f"Failed to search sections: {e}")
        return {
            "success": False,
            "error": str(e),
            "sections": []
        }

@mcp.resource("figma-db://sections/templates/{source}")
def get_section_templates_resource(source: str) -> str:
    """MCP Resource: Get section templates by source (tailwind-ui, shadcn, custom)"""
    try:
        result = db_client.supabase.table('section_templates')\\
            .select('*')\\
            .eq('source', source)\\
            .execute()
        
        templates = result.data if result.data else []
        
        return json.dumps({
            "source": source,
            "count": len(templates),
            "templates": templates
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "source": source
        }, indent=2)
'''
    
    with open(new_functions_file, 'w', encoding='utf-8') as f:
        f.write(new_functions_content)
    
    print(f"✅ Created {new_functions_file} with new functions to add")

if __name__ == "__main__":
    apply_sections_update()