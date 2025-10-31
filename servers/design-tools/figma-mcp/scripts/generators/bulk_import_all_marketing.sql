-- Bulk import all marketing sections at once
-- First, let's check what we already have
WITH existing AS (
    SELECT name FROM sections WHERE app_type = 'marketing-site'
)
SELECT COUNT(*) as already_imported FROM existing;

-- Now import all sections in one go
-- Using DO block to handle large insert
DO $$
BEGIN
    -- Import all sections that don't already exist
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
    )
    SELECT 
        s.name,
        s.description,
        s.category,
        s.source,
        s.react_template,
        s.block_type,
        s.app_type,
        s.is_template,
        s.published,
        s.tags,
        s.dependencies,
        s.props_schema,
        s.example_props,
        (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
    FROM (
        VALUES