#!/usr/bin/env python3
"""
Bulk insert all Figma components using SQL
"""

import json
import sys

def create_insert_sql(components, batch_num):
    """Create bulk insert SQL for a batch of components"""
    
    sql_values = []
    for comp in components:
        # Escape single quotes in strings
        name = comp['name'].replace("'", "''")
        description = comp.get('description', '').replace("'", "''")
        
        # Convert arrays to PostgreSQL format
        tags_str = "ARRAY[" + ",".join([f"'{tag}'" for tag in comp.get('tags', [])]) + "]"
        
        # Convert props to JSON string
        props_json = json.dumps(comp.get('props', {})).replace("'", "''")
        
        sql_value = f"""(
    '{comp['figma_id']}',
    '{name}',
    '{description}',
    '{comp['category_id']}',
    '{comp['figma_url']}',
    '{comp['component_type']}',
    {tags_str},
    {comp.get('complexity_score', 1)},
    {comp.get('popularity_score', 0)},
    '{props_json}'::jsonb,
    '{comp['figma_node_type']}',
    {comp.get('width', 'NULL')},
    {comp.get('height', 'NULL')},
    '{comp['status']}',
    '{comp['last_synced']}'::timestamptz
)"""
        sql_values.append(sql_value)
    
    insert_sql = f"""
INSERT INTO figma_components (
    figma_id, name, description, category_id, figma_url, component_type,
    tags, complexity_score, popularity_score, props, figma_node_type,
    width, height, status, last_synced
) VALUES 
{','.join(sql_values)}
ON CONFLICT (figma_id) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    last_synced = EXCLUDED.last_synced;
"""
    
    return insert_sql

def main():
    """Process all batch files and create SQL"""
    
    # Get all batch files
    import glob
    batch_files = sorted(glob.glob('batch_*.json'))
    
    print(f"Found {len(batch_files)} batch files")
    
    total_inserted = 0
    
    for i, batch_file in enumerate(batch_files, 1):
        print(f"Processing {batch_file}...")
        
        # Load batch data
        with open(batch_file, 'r') as f:
            components = json.load(f)
        
        print(f"  - {len(components)} components in this batch")
        
        # Create SQL
        sql = create_insert_sql(components, i)
        
        # Save SQL to file for review
        sql_file = f"insert_batch_{i:03d}.sql"
        with open(sql_file, 'w') as f:
            f.write(sql)
        
        print(f"  - SQL saved to {sql_file}")
        total_inserted += len(components)
    
    print(f"\nCreated SQL files for {total_inserted} total components")
    print("Review the SQL files and execute them using the Supabase MCP tool")

if __name__ == "__main__":
    main()