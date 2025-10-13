-- MARKETING SECTIONS IMPORT SETUP
-- First ensure we have a default project
INSERT INTO project_specifications (name, description, design_tokens)
VALUES (
    'Default Project',
    'Default project for shared components',
    '{"colors": {}, "typography": {}}'::jsonb
) ON CONFLICT (name) DO NOTHING;
