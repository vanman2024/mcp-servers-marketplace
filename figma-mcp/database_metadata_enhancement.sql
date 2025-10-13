-- Database Metadata Enhancement Script
-- Purpose: Activate and enhance the existing metadata infrastructure for better component discovery

-- ============================================
-- 1. NORMALIZE TAGS
-- ============================================

-- Create normalized tag definitions table
CREATE TABLE IF NOT EXISTS tag_definitions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50), -- 'technical', 'design', 'use-case', 'industry'
    description TEXT,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create many-to-many relationships for tags
CREATE TABLE IF NOT EXISTS component_tags (
    component_id UUID REFERENCES figma_components(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tag_definitions(id) ON DELETE CASCADE,
    PRIMARY KEY (component_id, tag_id)
);

CREATE TABLE IF NOT EXISTS section_tags (
    section_id UUID REFERENCES sections(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tag_definitions(id) ON DELETE CASCADE,
    PRIMARY KEY (section_id, tag_id)
);

-- ============================================
-- 2. USE CASE MAPPING
-- ============================================

CREATE TABLE IF NOT EXISTS use_cases (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    industry VARCHAR(100),
    business_goal VARCHAR(200),
    user_persona VARCHAR(100),
    complexity_level VARCHAR(20), -- 'simple', 'intermediate', 'advanced'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Map sections to use cases
CREATE TABLE IF NOT EXISTS section_use_cases (
    section_id UUID REFERENCES sections(id) ON DELETE CASCADE,
    use_case_id UUID REFERENCES use_cases(id) ON DELETE CASCADE,
    relevance_score INTEGER DEFAULT 100, -- 0-100
    notes TEXT,
    PRIMARY KEY (section_id, use_case_id)
);

-- Map components to use cases
CREATE TABLE IF NOT EXISTS component_use_cases (
    component_id UUID REFERENCES figma_components(id) ON DELETE CASCADE,
    use_case_id UUID REFERENCES use_cases(id) ON DELETE CASCADE,
    relevance_score INTEGER DEFAULT 100,
    PRIMARY KEY (component_id, use_case_id)
);

-- ============================================
-- 3. COMPONENT COMPATIBILITY MATRIX
-- ============================================

CREATE TABLE IF NOT EXISTS component_compatibility (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    component_a_id UUID REFERENCES figma_components(id) ON DELETE CASCADE,
    component_b_id UUID REFERENCES figma_components(id) ON DELETE CASCADE,
    compatibility_score INTEGER CHECK (compatibility_score >= 0 AND compatibility_score <= 100),
    integration_notes TEXT,
    tested BOOLEAN DEFAULT FALSE,
    UNIQUE(component_a_id, component_b_id)
);

-- ============================================
-- 4. ENHANCED SEARCH CAPABILITIES
-- ============================================

-- Create search indices
CREATE INDEX IF NOT EXISTS idx_sections_search ON sections USING GIN(search_vector);
CREATE INDEX IF NOT EXISTS idx_components_search ON figma_components USING GIN(search_vector);

-- Update search vectors with better content
CREATE OR REPLACE FUNCTION update_section_search_vector() RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := to_tsvector('english',
        COALESCE(NEW.name, '') || ' ' ||
        COALESCE(NEW.description, '') || ' ' ||
        COALESCE(NEW.block_type, '') || ' ' ||
        COALESCE(NEW.category, '') || ' ' ||
        COALESCE(array_to_string(NEW.tags, ' '), '')
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_section_search 
    BEFORE INSERT OR UPDATE ON sections
    FOR EACH ROW
    EXECUTE FUNCTION update_section_search_vector();

-- ============================================
-- 5. POPULATE SECTION_COMPONENTS RELATIONSHIPS
-- ============================================

-- Function to extract component references from React templates
CREATE OR REPLACE FUNCTION extract_component_references(template TEXT)
RETURNS TEXT[] AS $$
DECLARE
    matches TEXT[];
BEGIN
    -- Extract component names from JSX (simplified regex)
    SELECT ARRAY_AGG(DISTINCT match[1])
    INTO matches
    FROM regexp_matches(template, '<([A-Z][A-Za-z0-9]*)', 'g') AS match
    WHERE match[1] NOT IN ('React', 'Fragment', 'HTML', 'SVG');
    
    RETURN COALESCE(matches, ARRAY[]::TEXT[]);
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 6. CREATE INTELLIGENT VIEWS
-- ============================================

-- Component discovery view
CREATE OR REPLACE VIEW component_discovery AS
SELECT 
    fc.id,
    fc.name,
    fc.description,
    cc.name as category,
    fc.component_type,
    fc.complexity_score,
    fc.popularity_score,
    fc.tags,
    COUNT(DISTINCT suc.use_case_id) as use_case_count,
    COUNT(DISTINCT sc.section_id) as used_in_sections,
    ts_rank(fc.search_vector, plainto_tsquery('english', '')) as search_relevance
FROM figma_components fc
LEFT JOIN component_categories cc ON fc.category_id = cc.id
LEFT JOIN component_use_cases suc ON fc.id = suc.component_id
LEFT JOIN section_components sc ON fc.id = sc.component_id
GROUP BY fc.id, fc.name, fc.description, cc.name, fc.component_type, 
         fc.complexity_score, fc.popularity_score, fc.tags, fc.search_vector;

-- Section discovery view
CREATE OR REPLACE VIEW section_discovery AS
SELECT 
    s.id,
    s.name,
    s.description,
    s.block_type,
    s.category,
    s.app_type,
    s.tags,
    COUNT(DISTINCT sc.component_id) as component_count,
    COUNT(DISTINCT suc.use_case_id) as use_case_count,
    CASE 
        WHEN 'not-for-apps' = ANY(s.tags) THEN FALSE
        ELSE TRUE
    END as is_app_ready,
    ts_rank(s.search_vector, plainto_tsquery('english', '')) as search_relevance
FROM sections s
LEFT JOIN section_components sc ON s.id = sc.section_id
LEFT JOIN section_use_cases suc ON s.id = suc.section_id
GROUP BY s.id, s.name, s.description, s.block_type, 
         s.category, s.app_type, s.tags, s.search_vector;

-- ============================================
-- 7. SEED INITIAL DATA
-- ============================================

-- Populate standard tags
INSERT INTO tag_definitions (name, category, description) VALUES
    -- Technical tags
    ('responsive', 'technical', 'Component adapts to different screen sizes'),
    ('accessible', 'technical', 'Follows WCAG accessibility guidelines'),
    ('animated', 'technical', 'Contains animations or transitions'),
    ('interactive', 'technical', 'Has user interaction capabilities'),
    ('form-element', 'technical', 'Part of form functionality'),
    
    -- Design tags
    ('hero', 'design', 'Hero section component'),
    ('cta', 'design', 'Call-to-action element'),
    ('navigation', 'design', 'Navigation component'),
    ('layout', 'design', 'Layout structure component'),
    ('content', 'design', 'Content display component'),
    
    -- Use case tags
    ('marketing', 'use-case', 'Marketing and landing pages'),
    ('ecommerce', 'use-case', 'E-commerce functionality'),
    ('dashboard', 'use-case', 'Admin and dashboard interfaces'),
    ('authentication', 'use-case', 'Login and authentication flows'),
    ('onboarding', 'use-case', 'User onboarding flows'),
    
    -- Industry tags
    ('saas', 'industry', 'Software as a Service'),
    ('retail', 'industry', 'Retail and shopping'),
    ('finance', 'industry', 'Financial services'),
    ('healthcare', 'industry', 'Healthcare applications'),
    ('education', 'industry', 'Educational platforms')
ON CONFLICT (name) DO NOTHING;

-- Populate standard use cases
INSERT INTO use_cases (name, description, industry, business_goal, complexity_level) VALUES
    ('SaaS Landing Page', 'Convert visitors to trial users', 'saas', 'Lead generation', 'intermediate'),
    ('E-commerce Product Catalog', 'Display and filter products', 'retail', 'Product discovery', 'advanced'),
    ('User Dashboard', 'Display user metrics and actions', 'saas', 'User engagement', 'advanced'),
    ('Marketing Campaign Page', 'Promote specific campaigns', 'marketing', 'Campaign conversion', 'simple'),
    ('Contact Form', 'Collect user inquiries', 'general', 'Lead capture', 'simple'),
    ('Pricing Page', 'Display pricing tiers', 'saas', 'Revenue conversion', 'intermediate'),
    ('Blog Layout', 'Display blog posts and articles', 'content', 'Content engagement', 'simple'),
    ('Team Page', 'Show team members', 'corporate', 'Trust building', 'simple')
ON CONFLICT DO NOTHING;

-- ============================================
-- 8. HELPER FUNCTIONS
-- ============================================

-- Function to find compatible components
CREATE OR REPLACE FUNCTION find_compatible_components(component_id UUID)
RETURNS TABLE(
    compatible_component_id UUID,
    component_name VARCHAR,
    compatibility_score INTEGER,
    category VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        CASE 
            WHEN cc.component_a_id = component_id THEN cc.component_b_id
            ELSE cc.component_a_id
        END as compatible_component_id,
        fc.name as component_name,
        cc.compatibility_score,
        cat.name as category
    FROM component_compatibility cc
    JOIN figma_components fc ON (
        (cc.component_a_id = component_id AND fc.id = cc.component_b_id) OR
        (cc.component_b_id = component_id AND fc.id = cc.component_a_id)
    )
    LEFT JOIN component_categories cat ON fc.category_id = cat.id
    WHERE cc.compatibility_score > 70
    ORDER BY cc.compatibility_score DESC;
END;
$$ LANGUAGE plpgsql;

-- Function to recommend sections for use case
CREATE OR REPLACE FUNCTION recommend_sections_for_use_case(use_case_name VARCHAR)
RETURNS TABLE(
    section_id UUID,
    section_name VARCHAR,
    block_type VARCHAR,
    relevance_score INTEGER,
    tags TEXT[]
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.id,
        s.name,
        s.block_type,
        COALESCE(suc.relevance_score, 50) as relevance_score,
        s.tags
    FROM sections s
    LEFT JOIN section_use_cases suc ON s.id = suc.section_id
    LEFT JOIN use_cases uc ON suc.use_case_id = uc.id
    WHERE 
        uc.name = use_case_name OR
        use_case_name = ANY(s.tags) OR
        s.description ILIKE '%' || use_case_name || '%'
    ORDER BY relevance_score DESC, s.name;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 9. FIX EXISTING DATA
-- ============================================

-- Update sections tagged as 'not-for-apps' to have proper categorization
UPDATE sections 
SET tags = array_remove(tags, 'not-for-apps') || ARRAY['marketing-landing']
WHERE 'not-for-apps' = ANY(tags) AND source = 'tailwindui';

-- Link figma_components to proper categories based on component_type
UPDATE figma_components fc
SET category_id = cc.id
FROM component_categories cc
WHERE fc.category_id IS NULL AND (
    (fc.component_type ILIKE '%button%' AND cc.name = 'Buttons') OR
    (fc.component_type ILIKE '%form%' AND cc.name = 'Forms') OR
    (fc.component_type ILIKE '%input%' AND cc.name = 'Forms') OR
    (fc.component_type ILIKE '%nav%' AND cc.name = 'Navigation') OR
    (fc.component_type ILIKE '%card%' AND cc.name = 'Cards') OR
    (fc.component_type ILIKE '%layout%' AND cc.name = 'Layout') OR
    (fc.component_type ILIKE '%alert%' AND cc.name = 'Feedback') OR
    (fc.component_type ILIKE '%modal%' AND cc.name = 'Overlays')
);

-- ============================================
-- 10. ANALYTICS AND REPORTING
-- ============================================

-- View to show metadata completeness
CREATE OR REPLACE VIEW metadata_health_check AS
SELECT 
    'figma_components' as table_name,
    COUNT(*) as total_records,
    COUNT(category_id) as has_category,
    COUNT(CASE WHEN array_length(tags, 1) > 0 THEN 1 END) as has_tags,
    COUNT(component_type) as has_type,
    ROUND(100.0 * COUNT(category_id) / COUNT(*), 2) as category_coverage_pct
FROM figma_components
UNION ALL
SELECT 
    'sections',
    COUNT(*),
    COUNT(category) as has_category,
    COUNT(CASE WHEN array_length(tags, 1) > 0 THEN 1 END) as has_tags,
    COUNT(block_type) as has_type,
    ROUND(100.0 * COUNT(category) / COUNT(*), 2) as category_coverage_pct
FROM sections;

COMMENT ON SCHEMA public IS 'Enhanced metadata schema for intelligent component discovery and application building';