#!/usr/bin/env python3
"""
Updates to Figma MCP Server for Sections Architecture
=====================================================
This file contains the updates needed to support the new sections/components architecture.
"""

# Updated function to use sections table instead of application_blocks
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
    import os
    import json
    
    try:
        logger.info(f"Creating application blocks for {app_type} app in {output_directory}")
        
        # Initialize database client
        db_client = DatabaseClient()
        
        # Query sections table instead of application_blocks
        query = db_client.supabase.table('sections').select('*')
        
        # Filter by app_type
        if app_type and app_type != "all":
            query = query.eq('app_type', app_type)
        
        # Filter by block_types if specified
        if block_types:
            query = query.in_('block_type', block_types)
        
        # Execute query
        result = query.execute()
        
        if not result.data:
            return {
                "success": False,
                "error": f"No blocks found for app type: {app_type}",
                "created_files": []
            }
        
        # Create output directory
        os.makedirs(output_directory, exist_ok=True)
        
        created_files = []
        
        # Process each block
        for block in result.data:
            try:
                # Convert block name to filename
                filename = block['name'].replace(' - ', '').replace(' ', '')
                filename = filename[0].upper() + filename[1:] if filename else filename
                filename = f"{filename}.tsx"
                
                file_path = os.path.join(output_directory, filename)
                
                # Write the React template
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(block['react_template'])
                
                created_files.append({
                    "path": file_path,
                    "filename": filename,
                    "block_type": block['block_type'],
                    "app_type": block['app_type'],
                    "size": len(block['react_template'])
                })
                
                logger.info(f"Created: {file_path}")
                
            except Exception as e:
                logger.error(f"Failed to create block {block['name']}: {e}")
        
        # Create index file if requested
        if create_index and created_files:
            index_content = "// Auto-generated block exports\n\n"
            
            for file_info in created_files:
                component_name = file_info["filename"].replace(".tsx", "")
                index_content += f'export {{ default as {component_name} }} from "./{component_name}";\n'
            
            index_path = os.path.join(output_directory, "index.ts")
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            created_files.append({
                "path": index_path,
                "filename": "index.ts",
                "block_type": "index",
                "size": len(index_content)
            })
        
        return {
            "success": True,
            "created_files": created_files,
            "total_files": len(created_files),
            "output_directory": output_directory,
            "message": f"Successfully created {len(created_files)} block files"
        }
        
    except Exception as e:
        logger.error(f"Failed to create application blocks: {e}")
        return {
            "success": False,
            "error": str(e),
            "created_files": []
        }

# New function to get sections by category
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
        db_client = DatabaseClient()
        
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

# New function to get project specifications
async def get_project_specification(project_id: str) -> Dict[str, Any]:
    """
    Get project-specific design tokens and style guide
    
    Args:
        project_id: The project UUID
    
    Returns:
        Project specifications including design tokens
    """
    try:
        db_client = DatabaseClient()
        
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

# New function to create custom section
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
        db_client = DatabaseClient()
        
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

# New function to generate page from sections
async def generate_page_from_sections(
    section_ids: List[str],
    project_id: str,
    page_name: str = "GeneratedPage"
) -> Dict[str, Any]:
    """
    Generate a complete page by combining multiple sections
    
    Args:
        section_ids: List of section IDs to combine
        project_id: Project ID for styling
        page_name: Name for the generated page component
    
    Returns:
        Generated page code
    """
    try:
        db_client = DatabaseClient()
        
        # Get all sections
        sections_result = db_client.supabase.table('sections').select('*').in_('id', section_ids).execute()
        
        if not sections_result.data:
            return {
                "success": False,
                "error": "No sections found with provided IDs"
            }
        
        # Get project specifications
        spec_result = await get_project_specification(project_id)
        design_tokens = spec_result.get('specification', {}).get('design_tokens', {}) if spec_result.get('success') else {}
        
        # Sort sections by their order in section_ids
        sections = sorted(sections_result.data, key=lambda x: section_ids.index(x['id']))
        
        # Generate imports
        imports = set()
        imports.add("import React from 'react';")
        
        # Collect all dependencies
        for section in sections:
            if section.get('dependencies'):
                for dep in section['dependencies']:
                    if isinstance(dep, dict) and dep.get('npm'):
                        for npm_dep in dep['npm']:
                            imports.add(f"// npm install {npm_dep}")
        
        # Build page component
        page_code = f"""
{chr(10).join(sorted(imports))}

// Generated page combining multiple sections
// Project: {project_id}

export default function {page_name}() {{
  return (
    <div className="min-h-screen bg-background">
"""
        
        # Add each section
        for i, section in enumerate(sections):
            # Extract just the component JSX from the template
            template = section['react_template']
            
            # Simple extraction - find the return statement
            return_match = re.search(r'return\s*\(([\s\S]*?)\);', template)
            if return_match:
                jsx_content = return_match.group(1).strip()
                # Add section with comment
                page_code += f"""
      {{/* {section['name']} */}}
      <section id="section-{i}" className="w-full">
        {jsx_content}
      </section>
"""
        
        page_code += """
    </div>
  );
}
"""
        
        return {
            "success": True,
            "code": page_code,
            "page_name": page_name,
            "sections_used": len(sections),
            "message": f"Successfully generated page with {len(sections)} sections"
        }
        
    except Exception as e:
        logger.error(f"Failed to generate page from sections: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# Update the application context storage to use new schema
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
    Updated to work with new sections architecture
    """
    try:
        # Store context as before
        context = {
            "session_id": session_id,
            "app_description": app_description,
            "requirements": requirements or [],
            "ui_preferences": ui_preferences or {},
            "tech_stack": tech_stack or ["react", "typescript", "tailwindcss"],
            "business_rules": business_rules or [],
            "user_stories": user_stories or [],
            "conversation_summary": conversation_summary or "",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "2.0"  # Updated version for sections architecture
        }
        
        # Save to context directory
        _ensure_context_dir()
        context_file = os.path.join(CONTEXT_DIR, f"{session_id}_context.json")
        
        with open(context_file, 'w') as f:
            json.dump(context, f, indent=2)
        
        logger.info(f"Stored context for session {session_id}")
        
        return {
            "success": True,
            "session_id": session_id,
            "context_file": context_file,
            "message": "Context stored successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to store app context: {e}")
        return {
            "success": False,
            "error": str(e)
        }