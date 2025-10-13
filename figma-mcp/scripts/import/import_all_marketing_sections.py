#!/usr/bin/env python3
"""
Import all marketing sections at once
"""

import json
import os

def import_all_sections():
    """Import all marketing sections in one go"""
    
    # Supabase project details
    project_id = "wsmhiiharnhqupdniwgw"
    
    # Load the marketing sections data
    with open('marketing_sections_to_import.json', 'r') as f:
        data = json.load(f)
    
    print(f"Importing {len(data['sections'])} marketing sections...")
    
    # Build one massive INSERT statement with all sections
    values_list = []
    
    for section in data['sections']:
        # Escape single quotes
        name = section['name'].replace("'", "''")
        description = section['description'].replace("'", "''")
        react_template = section['react_template'].replace("'", "''")
        
        # Map metadata
        metadata = section['metadata']
        component_type = metadata.get('component_type', 'component')
        
        # Build the VALUES clause for this section
        values = f"""(
    '{name}',
    '{description}',
    '{section['category']}',
    '{section['source']}',
    '{react_template}',
    '{component_type}',
    'marketing-site',
    {str(section['is_template']).lower()},
    {str(section['published']).lower()},
    ARRAY{section['tags']}::text[],
    '{json.dumps({"uses_components": metadata.get('uses_components', []), "dependencies": metadata.get('dependencies', [])})}'::jsonb,
    '{{}}'::jsonb,
    '{json.dumps(metadata)}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)"""
        values_list.append(values)
    
    # Build the complete SQL statement
    sql = f"""
-- Bulk import all marketing sections
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
) VALUES
{',\n'.join(values_list)}
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();
"""
    
    # Execute the SQL
    try:
        result = execute_sql(project_id, sql)
        print(f"Successfully imported all {len(data['sections'])} marketing sections!")
        return result
    except Exception as e:
        print(f"Error importing sections: {e}")
        # If bulk insert fails, try smaller batches
        print("Trying smaller batches...")
        batch_size = 10
        success_count = 0
        
        for i in range(0, len(values_list), batch_size):
            batch = values_list[i:i+batch_size]
            batch_sql = f"""
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
) VALUES
{',\n'.join(batch)}
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();
"""
            try:
                execute_sql(project_id, batch_sql)
                success_count += len(batch)
                print(f"Imported batch {i//batch_size + 1}: {len(batch)} sections")
            except Exception as batch_error:
                print(f"Error in batch {i//batch_size + 1}: {batch_error}")
        
        print(f"Total imported: {success_count} sections")
        return success_count

if __name__ == "__main__":
    import_all_sections()