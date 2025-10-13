#\!/usr/bin/env python3
import json

# Load the marketing sections data
with open('marketing_sections_to_import.json', 'r') as f:
    data = json.load(f)

# Get sections that aren't already imported
imported = [
    'Marketing Hero - Keynote Conference',
    'Marketing Hero - SaaS Product', 
    'Pricing Section - Three Tier'
]

remaining_sections = [s for s in data['sections'] if s['name'] not in imported]
print(f"Total sections: {len(data['sections'])}")
print(f"Already imported: {len(imported)}")
print(f"Remaining to import: {len(remaining_sections)}")

# Create batches of 10 sections each
batch_size = 10
for i in range(0, len(remaining_sections), batch_size):
    batch_num = (i // batch_size) + 1
    batch = remaining_sections[i:i+batch_size]
    
    with open(f'marketing_batch_{batch_num}.sql', 'w') as f:
        f.write(f"-- Marketing Sections Batch {batch_num}\n")
        f.write(f"-- {len(batch)} sections in this batch\n\n")
        
        for section in batch:
            # Escape single quotes properly
            name = section['name'].replace("'", "''")
            description = section['description'].replace("'", "''")
            react_template = section['react_template'].replace("'", "''")
            
            # Map metadata
            metadata = section['metadata']
            component_type = metadata.get('component_type', 'component')
            
            sql = f"""
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
    '{component_type}',
    'marketing-site',
    {str(section['is_template']).lower()},
    {str(section['published']).lower()},
    ARRAY{section['tags']}::text[],
    '{json.dumps({"uses_components": metadata.get('uses_components', []), "dependencies": metadata.get('dependencies', [])})}'::jsonb,
    '{{}}'::jsonb,
    '{json.dumps(metadata)}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
);

"""
            f.write(sql)
            
    print(f"Created marketing_batch_{batch_num}.sql")
