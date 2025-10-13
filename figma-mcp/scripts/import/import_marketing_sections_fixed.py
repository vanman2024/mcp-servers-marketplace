#!/usr/bin/env python3
"""
Import Tailwind Plus Marketing Templates into Sections Database
==============================================================
IMPORTANT: These are MARKETING/LANDING PAGE sections only!
NOT for building applications - just for company websites, landing pages, etc.
"""

import json
import os
from datetime import datetime
from typing import Dict, List

def create_import_sql():
    """Create SQL to import marketing sections"""
    
    # Load prepared sections
    with open('marketing_sections_to_import.json', 'r') as f:
        data = json.load(f)
    
    print(f"Creating SQL for {data['total']} marketing sections")
    print(f"WARNING: {data['warning']}")
    
    sql_statements = []
    
    # Add header
    sql_statements.append(f"""-- MARKETING SECTIONS IMPORT
-- WARNING: These are marketing/landing page sections from Tailwind Plus templates
-- NOT for building applications - only for marketing websites!
-- Generated: {datetime.now().isoformat()}

-- First ensure we have a default project
INSERT INTO project_specifications (name, description, design_tokens)
VALUES (
    'Default Project',
    'Default project for shared components',
    '{{"colors": {{}}, "typography": {{}}}}'::jsonb
) ON CONFLICT (name) DO NOTHING;

""")
    
    for section in data['sections']:
        # Escape single quotes
        name = section['name'].replace("'", "''")
        description = section['description'].replace("'", "''")
        react_template = section['react_template'].replace("'", "''")
        
        # Map our data to actual table columns
        sql = f"""
-- {name}
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    '{name}',
    '{description}',
    '{section['category']}',
    '{section['source']}',
    '{react_template}',
    '{section['metadata']['component_type']}',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    {section['is_template']},
    {section['published']},
    ARRAY{section['tags']}::text[],
    '{json.dumps({"uses_components": section['metadata'].get('uses_components', []), "dependencies": section['metadata'].get('dependencies', [])})}'::jsonb,
    '{{}}'::jsonb,  -- props_schema
    '{json.dumps(section['metadata'])}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();
"""
        sql_statements.append(sql)
    
    # Write to file
    with open('import_marketing_sections_fixed.sql', 'w') as f:
        f.writelines(sql_statements)
    
    print(f"\nCreated import_marketing_sections_fixed.sql")
    print("This includes {len(data['sections'])} marketing sections clearly labeled as NOT for applications")
    
    # Also create a smaller test file
    test_sql = sql_statements[0] + sql_statements[1]  # Header + first section
    with open('test_marketing_import.sql', 'w') as f:
        f.write(test_sql)
    
    print("\nAlso created test_marketing_import.sql with just 1 section for testing")

if __name__ == "__main__":
    create_import_sql()