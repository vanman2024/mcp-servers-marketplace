#!/usr/bin/env python3
"""
Complete Update for Figma MCP Server - Sections Architecture
============================================================
This file contains all the necessary updates to migrate from application_blocks
to the new sections architecture.

Apply these changes to figma_server_db.py:
1. Replace 'application_blocks' with 'sections' in all queries
2. Add new functions for project specifications
3. Update function signatures to support cross-project access
"""

# =====================================================
# UPDATED FUNCTIONS
# =====================================================

# 1. Update create_application_blocks function (line 2611)
@mcp.tool()
async def create_application_blocks(
    app_type: str,
    output_directory: str,
    block_types: Optional[List[str]] = None,
    create_index: bool = True,
    project_id: Optional[str] = None  # NEW: Add project_id parameter
) -> Dict[str, Any]:
    """
    Generate and SAVE application block files from database templates
    Creates complete application blocks as .tsx files in your project directory
    
    Args:
        app_type: Type of app to build (dashboard, marketing, blog, ecommerce, etc.)
        output_directory: Directory path where files should be created
        block_types: Specific block types to create (hero, features, pricing, etc.)
        create_index: Whether to create an index.ts file exporting all blocks
        project_id: Optional project ID to get project-specific sections
    
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
        
        # Query sections table instead of application_blocks
        query = db_client.supabase.table('sections').select('*')
        
        # Filter by app_type if specific one requested
        if app_type != "all":
            query = query.or_(f"app_type.eq.{app_type},app_type.eq.marketing,app_type.eq.utility")
        
        # Filter by specific block types if requested
        if block_types:
            query = query.in_('block_type', block_types)
        
        # Filter by project if specified
        if project_id:
            query = query.or_(f'project_id.eq.{project_id},is_template.eq.true')
        else:
            # Only get template sections if no project specified
            query = query.eq('is_template', True)
        
        result = query.execute()
        blocks = result.data if result.data else []
        
        if not blocks:
            return {
                "success": False,
                "error": f"No sections found for app_type='{app_type}' and block_types={block_types}",
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
                "category": block.get('category', 'general'),  # NEW: Include category
                "source": block.get('source', 'custom'),  # NEW: Include source
                "size": len(react_template),
                "dependencies": block.get('dependencies', [])
            })
            
            logger.info(f"✅ Created {filename} ({len(react_template)} chars)")
        
        # Create index.ts file if requested
        if create_index and created_files:
            index_content = "// Auto-generated application blocks index\n\n"
            
            for file_info in created_files:
                component_name = file_info['filename'].replace('.tsx', '')
                index_content += f"export { default as {component_name} } from './{component_name}';\n"
            
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
            "created_files": created_files,
            "total_files": len(created_files),
            "output_directory": output_directory,
            "project_id": project_id,
            "message": f"Successfully created {len(created_files)} files for {app_type} app"
        }
        
    except Exception as e:
        logger.error(f"Failed to create application blocks: {e}")
        return {
            "success": False,
            "error": str(e),
            "created_files": []
        }

# 2. Update the build_application function to use sections
# Search for any references to application_blocks in build_application function
# and replace with sections

# 3. Add new tool for getting sections by category
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

# 4. Add new tool for project specifications
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

# 5. Add new tool for creating custom sections
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

# 6. Add new tool for searching sections
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

# 7. Add resource for section templates
@mcp.resource("figma-db://sections/templates/{source}")
def get_section_templates_resource(source: str) -> str:
    """MCP Resource: Get section templates by source (tailwind-ui, shadcn, custom)"""
    try:
        result = db_client.supabase.table('section_templates')\
            .select('*')\
            .eq('source', source)\
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

# 8. Create the search_sections RPC function in database
SEARCH_SECTIONS_FUNCTION = """
CREATE OR REPLACE FUNCTION search_sections(
    search_query TEXT DEFAULT NULL,
    category_filter TEXT DEFAULT NULL,
    project_filter UUID DEFAULT NULL,
    limit_results INTEGER DEFAULT 20
)
RETURNS TABLE (
    id UUID,
    name VARCHAR(255),
    description TEXT,
    category VARCHAR(100),
    source VARCHAR(50),
    block_type VARCHAR(100),
    app_type VARCHAR(50),
    project_id UUID,
    is_template BOOLEAN,
    preview_url TEXT,
    created_at TIMESTAMPTZ,
    rank REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.id,
        s.name,
        s.description,
        s.category,
        s.source,
        s.block_type,
        s.app_type,
        s.project_id,
        s.is_template,
        s.preview_url,
        s.created_at,
        CASE 
            WHEN search_query IS NULL THEN 1.0
            ELSE ts_rank(s.search_vector, plainto_tsquery('english', search_query))
        END as rank
    FROM sections s
    WHERE 
        (search_query IS NULL OR s.search_vector @@ plainto_tsquery('english', search_query))
        AND (category_filter IS NULL OR s.category = category_filter)
        AND (project_filter IS NULL OR s.project_id = project_filter OR s.is_template = true)
        AND s.published = true
    ORDER BY rank DESC, s.created_at DESC
    LIMIT limit_results;
END;
$$ LANGUAGE plpgsql;
"""

# =====================================================
# MIGRATION CHECKLIST
# =====================================================

"""
To complete the migration in figma_server_db.py:

1. Replace all occurrences of 'application_blocks' with 'sections':
   - Line 2641: query = db_client.supabase.table('application_blocks').select('*')
   → query = db_client.supabase.table('sections').select('*')

2. Add the new functions from this file:
   - get_sections_by_category
   - get_project_specification
   - create_custom_section
   - search_sections
   - get_section_templates_resource

3. Update existing functions to include new parameters:
   - Add project_id parameter to create_application_blocks
   - Add category and source fields to returned data

4. Execute the search_sections RPC function in the database:
   - Use execute_sql to run the SEARCH_SECTIONS_FUNCTION SQL

5. Update any other references in:
   - build_application
   - build_application_with_context
   - create_app_blocks

6. Test all endpoints to ensure they work with the new schema
"""