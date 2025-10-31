-- MARKETING SECTIONS IMPORT
-- WARNING: These are marketing/landing page sections from Tailwind Plus templates
-- NOT for building applications - only for marketing websites!
-- Generated: 2025-07-17T20:18:19.443156

-- First ensure we have a default project
INSERT INTO project_specifications (name, description, design_tokens)
VALUES (
    'Default Project',
    'Default project for shared components',
    '{"colors": {}, "typography": {}}'::jsonb
) ON CONFLICT (name) DO NOTHING;


-- Forms - Signupform - Marketing
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
    'Forms - Signupform - Marketing',
    'Marketing/Landing page component from Tailwind Plus Commit template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { useId } from ''react''

import { Button } from ''@/components/Button''

