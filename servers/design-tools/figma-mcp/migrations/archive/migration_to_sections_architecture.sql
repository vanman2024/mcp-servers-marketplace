-- =====================================================
-- Migration: Application Blocks to Sections Architecture
-- Date: 2025-01-18
-- Purpose: Transform application_blocks to hierarchical sections/components structure
-- =====================================================

-- Step 1: Create backup of existing data
CREATE TABLE IF NOT EXISTS application_blocks_backup AS 
SELECT * FROM application_blocks;

-- Step 2: Create new tables for the enhanced architecture
-- =====================================================

-- Project specifications table for cross-project support
CREATE TABLE IF NOT EXISTS project_specifications (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id UUID NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    design_tokens JSONB DEFAULT '{}' NOT NULL,
    style_guide JSONB DEFAULT '{}' NOT NULL,
    color_palette JSONB DEFAULT '{}',
    typography JSONB DEFAULT '{}',
    spacing JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for project specifications
CREATE INDEX idx_project_specifications_project_id ON project_specifications(project_id);

-- Step 3: Alter application_blocks to become sections table
-- =====================================================

-- Add new columns needed for sections architecture
ALTER TABLE application_blocks 
ADD COLUMN IF NOT EXISTS source VARCHAR(50) DEFAULT 'custom',
ADD COLUMN IF NOT EXISTS category VARCHAR(100),
ADD COLUMN IF NOT EXISTS project_id UUID,
ADD COLUMN IF NOT EXISTS design_spec_id UUID REFERENCES project_specifications(id),
ADD COLUMN IF NOT EXISTS parent_section_id UUID,
ADD COLUMN IF NOT EXISTS layout_config JSONB DEFAULT '{}',
ADD COLUMN IF NOT EXISTS style_overrides JSONB DEFAULT '{}',
ADD COLUMN IF NOT EXISTS visibility_rules JSONB DEFAULT '{}',
ADD COLUMN IF NOT EXISTS is_template BOOLEAN DEFAULT true,
ADD COLUMN IF NOT EXISTS version VARCHAR(20) DEFAULT '1.0.0',
ADD COLUMN IF NOT EXISTS published BOOLEAN DEFAULT true;

-- Update existing data to set proper categories based on block_type
UPDATE application_blocks SET category = 
  CASE 
    WHEN block_type IN ('hero', 'header', 'footer') THEN 'navigation-layout'
    WHEN block_type IN ('features', 'pricing', 'cta', 'testimonials') THEN 'marketing'
    WHEN block_type IN ('stats', 'stats-section', 'dashboard') THEN 'analytics'
    WHEN block_type IN ('blog-grid', 'gallery') THEN 'content-display'
    WHEN block_type IN ('contact', 'newsletter') THEN 'forms'
    WHEN block_type IN ('product-grid') THEN 'e-commerce'
    WHEN block_type IN ('error-404', 'cookie-consent', 'search-bar', 'banner') THEN 'utility'
    WHEN block_type IN ('team', 'timeline', 'comparison', 'integrations', 'logo-cloud', 'faq') THEN 'marketing'
    ELSE 'general'
  END
WHERE category IS NULL;

-- Step 4: Create section_components junction table
-- =====================================================

CREATE TABLE IF NOT EXISTS section_components (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    section_id UUID NOT NULL,
    component_id UUID REFERENCES figma_components(id),
    component_name VARCHAR(255), -- For components not in figma_components table
    position INTEGER NOT NULL DEFAULT 0,
    props JSONB DEFAULT '{}',
    style_overrides JSONB DEFAULT '{}',
    conditional_rendering JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_section_components_section 
        FOREIGN KEY (section_id) REFERENCES application_blocks(id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX idx_section_components_section_id ON section_components(section_id);
CREATE INDEX idx_section_components_component_id ON section_components(component_id);
CREATE INDEX idx_section_components_position ON section_components(section_id, position);

-- Step 5: Create section_templates for Tailwind UI imports
-- =====================================================

CREATE TABLE IF NOT EXISTS section_templates (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    source VARCHAR(50) NOT NULL, -- 'tailwind-ui', 'shadcn', 'custom'
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    original_path TEXT, -- Original file path from Tailwind UI
    code TEXT NOT NULL,
    preview_image_url TEXT,
    dependencies JSONB DEFAULT '[]',
    component_list TEXT[], -- List of components used
    responsive_variants JSONB DEFAULT '{}',
    accessibility_features TEXT[],
    browser_support TEXT[],
    tags TEXT[] DEFAULT '{}',
    search_vector tsvector,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create full-text search index
CREATE INDEX idx_section_templates_search ON section_templates USING gin(search_vector);
CREATE INDEX idx_section_templates_source ON section_templates(source);
CREATE INDEX idx_section_templates_category ON section_templates(category);
CREATE INDEX idx_section_templates_tags ON section_templates USING gin(tags);

-- Step 6: Create design_systems table for managing multiple design systems
-- =====================================================

CREATE TABLE IF NOT EXISTS design_systems (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(20) NOT NULL,
    source VARCHAR(50) NOT NULL, -- 'tailwind-ui', 'shadcn', 'material-ui', etc
    config JSONB NOT NULL,
    component_mappings JSONB DEFAULT '{}', -- Maps design system components to our components
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Step 7: Create usage_analytics table
-- =====================================================

CREATE TABLE IF NOT EXISTS section_usage_analytics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    section_id UUID NOT NULL,
    project_id UUID,
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMPTZ,
    performance_metrics JSONB DEFAULT '{}',
    user_ratings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_usage_section 
        FOREIGN KEY (section_id) REFERENCES application_blocks(id) ON DELETE CASCADE
);

CREATE INDEX idx_section_usage_analytics_section ON section_usage_analytics(section_id);
CREATE INDEX idx_section_usage_analytics_project ON section_usage_analytics(project_id);

-- Step 8: Rename application_blocks to sections
-- =====================================================

ALTER TABLE application_blocks RENAME TO sections;

-- Update foreign key constraint names to reflect new table name
ALTER TABLE section_components 
DROP CONSTRAINT IF EXISTS fk_section_components_section,
ADD CONSTRAINT fk_section_components_section 
    FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE;

ALTER TABLE section_usage_analytics 
DROP CONSTRAINT IF EXISTS fk_usage_section,
ADD CONSTRAINT fk_usage_section 
    FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE;

-- Step 9: Create views for easier querying
-- =====================================================

-- View for sections with their components
CREATE OR REPLACE VIEW sections_with_components AS
SELECT 
    s.*,
    array_agg(
        json_build_object(
            'component_id', sc.component_id,
            'component_name', COALESCE(fc.name, sc.component_name),
            'position', sc.position,
            'props', sc.props
        ) ORDER BY sc.position
    ) FILTER (WHERE sc.id IS NOT NULL) as components
FROM sections s
LEFT JOIN section_components sc ON s.id = sc.section_id
LEFT JOIN figma_components fc ON sc.component_id = fc.id
GROUP BY s.id;

-- View for project-specific sections
CREATE OR REPLACE VIEW project_sections AS
SELECT 
    s.*,
    ps.name as project_name,
    ps.design_tokens,
    ps.style_guide
FROM sections s
LEFT JOIN project_specifications ps ON s.project_id = ps.project_id;

-- Step 10: Create helper functions
-- =====================================================

-- Function to update search vectors
CREATE OR REPLACE FUNCTION update_section_search_vector() RETURNS trigger AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('english', COALESCE(NEW.name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.category, '')), 'C') ||
        setweight(to_tsvector('english', array_to_string(NEW.tags, ' ')), 'D');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add search vector column to sections
ALTER TABLE sections ADD COLUMN IF NOT EXISTS search_vector tsvector;

-- Create trigger for search vector updates
CREATE TRIGGER update_sections_search_vector 
BEFORE INSERT OR UPDATE ON sections
FOR EACH ROW EXECUTE FUNCTION update_section_search_vector();

-- Update existing records
UPDATE sections SET search_vector = 
    setweight(to_tsvector('english', COALESCE(name, '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(description, '')), 'B') ||
    setweight(to_tsvector('english', COALESCE(category, '')), 'C') ||
    setweight(to_tsvector('english', array_to_string(tags, ' ')), 'D');

-- Create search index
CREATE INDEX idx_sections_search ON sections USING gin(search_vector);

-- Step 11: Add RLS policies for security
-- =====================================================

-- Enable RLS
ALTER TABLE sections ENABLE ROW LEVEL SECURITY;
ALTER TABLE section_components ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_specifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE section_templates ENABLE ROW LEVEL SECURITY;

-- Create policies (adjust based on your auth setup)
CREATE POLICY "Public sections are viewable by everyone" 
ON sections FOR SELECT 
USING (project_id IS NULL OR published = true);

CREATE POLICY "Service role can manage all sections" 
ON sections FOR ALL 
USING (auth.jwt()->>'role' = 'service_role');

-- Step 12: Create initial project specification for existing blocks
-- =====================================================

INSERT INTO project_specifications (project_id, name, description, design_tokens, style_guide)
VALUES (
    '00000000-0000-0000-0000-000000000000'::uuid,
    'Default Project',
    'Default project for legacy blocks',
    '{
        "colors": {
            "primary": "#3B82F6",
            "secondary": "#8B5CF6",
            "accent": "#EC4899",
            "neutral": "#6B7280",
            "background": "#FFFFFF",
            "surface": "#F9FAFB",
            "error": "#EF4444",
            "warning": "#F59E0B",
            "info": "#3B82F6",
            "success": "#10B981"
        },
        "borderRadius": {
            "sm": "0.125rem",
            "md": "0.375rem",
            "lg": "0.5rem",
            "xl": "0.75rem",
            "2xl": "1rem",
            "3xl": "1.5rem",
            "full": "9999px"
        }
    }',
    '{
        "fontFamily": {
            "sans": "Inter, system-ui, sans-serif",
            "mono": "Fira Code, monospace"
        },
        "spacing": {
            "unit": 8,
            "scale": [0, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 56, 64]
        }
    }'
)
ON CONFLICT (project_id) DO NOTHING;

-- Update existing sections to use default project
UPDATE sections 
SET project_id = '00000000-0000-0000-0000-000000000000'::uuid
WHERE project_id IS NULL;

-- Step 13: Summary and verification
-- =====================================================

-- Create a summary view of the migration
CREATE OR REPLACE VIEW migration_summary AS
SELECT 
    'Sections' as table_name,
    COUNT(*) as record_count
FROM sections
UNION ALL
SELECT 
    'Section Components' as table_name,
    COUNT(*) as record_count
FROM section_components
UNION ALL
SELECT 
    'Project Specifications' as table_name,
    COUNT(*) as record_count
FROM project_specifications
UNION ALL
SELECT 
    'Section Templates' as table_name,
    COUNT(*) as record_count
FROM section_templates;

-- Final message
DO $$
BEGIN
    RAISE NOTICE 'Migration completed successfully!';
    RAISE NOTICE 'Tables created/modified:';
    RAISE NOTICE '  - application_blocks renamed to sections';
    RAISE NOTICE '  - section_components (junction table)';
    RAISE NOTICE '  - project_specifications';
    RAISE NOTICE '  - section_templates';
    RAISE NOTICE '  - design_systems';
    RAISE NOTICE '  - section_usage_analytics';
    RAISE NOTICE 'Original data backed up to: application_blocks_backup';
END $$;