#!/usr/bin/env python3
"""
Bulk import using Supabase client library
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Use FIGMA DESIGN SYSTEM credentials
SUPABASE_URL = os.getenv('FIGMA_DESIGN_SYSTEM_URL', 'https://wsmhiiharnhqupdniwgw.supabase.co')
SUPABASE_KEY = os.getenv('FIGMA_DESIGN_SYSTEM_SERVICE_KEY')

if not SUPABASE_KEY:
    raise ValueError("Missing FIGMA_DESIGN_SYSTEM_SERVICE_KEY")

print(f"Connecting to Figma Design System database...")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Read the entire SQL file
with open('bulk_marketing_import.sql', 'r') as f:
    sql_content = f.read()

try:
    print("Executing bulk import of ALL 76 marketing sections in ONE operation...")
    
    # Since Supabase doesn't have a direct SQL execute method in Python client,
    # we need to split and execute the statements
    
    # First ensure project exists
    project_sql = """
    INSERT INTO project_specifications (name, description, design_tokens)
    VALUES (
        'Default Project',
        'Default project for shared components',
        '{"colors": {}, "typography": {}}'::jsonb
    ) ON CONFLICT (name) DO NOTHING;
    """
    
    # Execute via postgrest (this won't work for raw SQL)
    # So let's use the data API instead
    
    # Check if default project exists
    result = supabase.table('project_specifications').select('*').eq('name', 'Default Project').execute()
    
    if not result.data:
        # Create default project
        supabase.table('project_specifications').insert({
            'name': 'Default Project',
            'description': 'Default project for shared components',
            'design_tokens': {"colors": {}, "typography": {}}
        }).execute()
    
    # Now import all sections at once using the data from marketing_sections_to_import.json
    import json
    with open('marketing_sections_to_import.json', 'r') as f:
        data = json.load(f)
    
    # Get project ID
    project = supabase.table('project_specifications').select('id').eq('name', 'Default Project').single().execute()
    project_id = project.data['id']
    
    # Prepare all sections for bulk insert
    sections_to_insert = []
    for section in data['sections']:
        sections_to_insert.append({
            'name': section['name'],
            'description': section['description'],
            'block_type': section['metadata'].get('component_type', 'component'),
            'app_type': 'marketing-site',
            'react_template': section['react_template'],
            'category': section['category'],
            'source': section['source'],
            'tags': section['tags'],
            'dependencies': {
                "uses_components": section['metadata'].get('uses_components', []),
                "dependencies": section['metadata'].get('dependencies', [])
            },
            'props_schema': {},
            'example_props': section['metadata'],
            'is_template': section['is_template'],
            'published': section['published'],
            'project_id': project_id
        })
    
    # Bulk insert all sections at once
    print(f"Inserting {len(sections_to_insert)} sections in ONE bulk operation...")
    result = supabase.table('sections').insert(sections_to_insert).execute()
    
    # Verify count
    count_result = supabase.table('sections').select('id', count='exact').eq('app_type', 'marketing-site').execute()
    
    print(f"\n✓ SUCCESS! {count_result.count} marketing sections now in database!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()