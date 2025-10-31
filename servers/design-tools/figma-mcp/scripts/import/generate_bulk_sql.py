#!/usr/bin/env python3
"""
Generate a single bulk SQL insert for all marketing sections
"""

import json

# Load the marketing sections data
with open('marketing_sections_to_import.json', 'r') as f:
    data = json.load(f)

print(f"Generating SQL for {len(data['sections'])} marketing sections...")

# Start the SQL file
sql_statements = []

# Add header
sql_statements.append("""-- BULK MARKETING SECTIONS IMPORT
-- WARNING: These are marketing/landing page sections from Tailwind Plus templates
-- NOT for building applications - only for marketing websites!

-- Ensure default project exists
INSERT INTO project_specifications (name, description, design_tokens)
VALUES (
    'Default Project',
    'Default project for shared components',
    '{"colors": {}, "typography": {}}'::jsonb
) ON CONFLICT (name) DO NOTHING;

-- Bulk insert all marketing sections
WITH marketing_data AS (
    SELECT * FROM (VALUES""")

# Build the VALUES entries
values_entries = []
for i, section in enumerate(data['sections']):
    # Escape single quotes
    name = section['name'].replace("'", "''")
    description = section['description'].replace("'", "''")
    react_template = section['react_template'].replace("'", "''")
    
    # Map metadata
    metadata = section['metadata']
    component_type = metadata.get('component_type', 'component')
    
    # Build dependencies JSON
    deps = {
        "uses_components": metadata.get('uses_components', []),
        "dependencies": metadata.get('dependencies', [])
    }
    
    # Build the row
    row = f"""        (
            '{name}'::varchar,
            '{description}'::text,
            '{component_type}'::varchar,
            'marketing-site'::varchar,
            '{react_template}'::text,
            '{section['category']}'::varchar,
            '{section['source']}'::varchar,
            ARRAY{section['tags']}::text[],
            '{json.dumps(deps)}'::jsonb,
            '{{}}'::jsonb,
            '{json.dumps(metadata)}'::jsonb,
            {str(section['is_template']).lower()},
            {str(section['published']).lower()}
        )"""
    
    values_entries.append(row)

# Join all values
sql_statements.append(',\n'.join(values_entries))

# Add the column definitions
sql_statements.append("""    ) AS t(
        name, description, block_type, app_type, react_template,
        category, source, tags, dependencies, props_schema, 
        example_props, is_template, published
    )
)
INSERT INTO sections (
    name, description, block_type, app_type, react_template,
    category, source, tags, dependencies, props_schema,
    example_props, is_template, published, project_id
)
SELECT 
    md.name, md.description, md.block_type, md.app_type, md.react_template,
    md.category, md.source, md.tags, md.dependencies, md.props_schema,
    md.example_props, md.is_template, md.published,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
FROM marketing_data md
WHERE NOT EXISTS (
    SELECT 1 FROM sections s 
    WHERE s.name = md.name 
    AND s.project_id = (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
);

-- Return count of imported sections
SELECT COUNT(*) as imported_count FROM sections WHERE app_type = 'marketing-site';
""")

# Write to file
with open('bulk_marketing_import.sql', 'w') as f:
    f.write('\n'.join(sql_statements))

print("Created bulk_marketing_import.sql")
print(f"File contains {len(data['sections'])} marketing sections with proper tagging")