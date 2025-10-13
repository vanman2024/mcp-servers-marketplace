-- Figma MCP Server Database Schema
-- Version: 1.0.0
-- Description: Initial schema for storing Figma design components in Supabase

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Design Files Table
-- Stores registered Figma files
CREATE TABLE IF NOT EXISTS design_files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    file_key TEXT UNIQUE NOT NULL, -- Figma file key
    file_url TEXT NOT NULL,
    source TEXT NOT NULL DEFAULT 'figma',
    description TEXT,
    version INT DEFAULT 1,
    last_synced_at TIMESTAMP WITH TIME ZONE,
    figma_modified_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Design Components Table  
-- Stores individual components extracted from Figma files
CREATE TABLE IF NOT EXISTS design_components (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_id UUID NOT NULL REFERENCES design_files(id) ON DELETE CASCADE,
    name TEXT NOT NULL, -- e.g., "Button/Primary", "Card/Product"
    node_id TEXT NOT NULL, -- Figma node ID
    component_type TEXT NOT NULL, -- e.g., "button", "card", "input"
    shadcn_component TEXT, -- Mapped ShadCN component name
    json_layout JSONB NOT NULL, -- Normalized component data
    design_tokens JSONB DEFAULT '{}'::jsonb, -- Colors, spacing, typography
    tags TEXT[] DEFAULT '{}',
    theme TEXT DEFAULT 'light' CHECK (theme IN ('light', 'dark', 'both')),
    preview_url TEXT,
    thumbnail_url TEXT,
    figma_url TEXT, -- Direct link to component in Figma
    is_published BOOLEAN DEFAULT false,
    version INT DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_id, node_id)
);

-- Component Variants Table
-- Stores different states and variations of components
CREATE TABLE IF NOT EXISTS component_variants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    component_id UUID NOT NULL REFERENCES design_components(id) ON DELETE CASCADE,
    name TEXT NOT NULL, -- e.g., "hover", "disabled", "loading"
    variant_type TEXT NOT NULL, -- e.g., "state", "size", "color"
    properties JSONB NOT NULL, -- Variant-specific properties
    json_layout JSONB NOT NULL, -- Variant-specific layout data
    preview_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(component_id, name, variant_type)
);

-- Design Tokens Table
-- Global design tokens extracted from files
CREATE TABLE IF NOT EXISTS design_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_id UUID NOT NULL REFERENCES design_files(id) ON DELETE CASCADE,
    token_type TEXT NOT NULL, -- e.g., "color", "spacing", "typography", "shadow"
    name TEXT NOT NULL, -- e.g., "primary-500", "space-4", "heading-1"
    value TEXT NOT NULL, -- Token value
    css_variable TEXT, -- Generated CSS variable name
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_id, token_type, name)
);

-- Component Usage Analytics Table
-- Track component usage for insights
CREATE TABLE IF NOT EXISTS component_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    component_id UUID NOT NULL REFERENCES design_components(id) ON DELETE CASCADE,
    action TEXT NOT NULL, -- e.g., "fetched", "generated", "exported"
    user_id TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_design_files_file_key ON design_files(file_key);
CREATE INDEX idx_design_files_source ON design_files(source);
CREATE INDEX idx_design_files_last_synced ON design_files(last_synced_at);

CREATE INDEX idx_design_components_file_id ON design_components(file_id);
CREATE INDEX idx_design_components_name ON design_components(name);
CREATE INDEX idx_design_components_type ON design_components(component_type);
CREATE INDEX idx_design_components_shadcn ON design_components(shadcn_component);
CREATE INDEX idx_design_components_tags ON design_components USING GIN(tags);
CREATE INDEX idx_design_components_theme ON design_components(theme);
CREATE INDEX idx_design_components_published ON design_components(is_published);

CREATE INDEX idx_component_variants_component_id ON component_variants(component_id);
CREATE INDEX idx_component_variants_type ON component_variants(variant_type);

CREATE INDEX idx_design_tokens_file_id ON design_tokens(file_id);
CREATE INDEX idx_design_tokens_type ON design_tokens(token_type);

CREATE INDEX idx_component_usage_component_id ON component_usage(component_id);
CREATE INDEX idx_component_usage_action ON component_usage(action);
CREATE INDEX idx_component_usage_created ON component_usage(created_at);

-- Update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update trigger to tables
CREATE TRIGGER update_design_files_updated_at BEFORE UPDATE ON design_files
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_design_components_updated_at BEFORE UPDATE ON design_components
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_component_variants_updated_at BEFORE UPDATE ON component_variants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_design_tokens_updated_at BEFORE UPDATE ON design_tokens
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) Policies
-- Enable RLS on all tables
ALTER TABLE design_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE design_components ENABLE ROW LEVEL SECURITY;
ALTER TABLE component_variants ENABLE ROW LEVEL SECURITY;
ALTER TABLE design_tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE component_usage ENABLE ROW LEVEL SECURITY;

-- Public read access for published components
CREATE POLICY "Public read access for published components" ON design_components
    FOR SELECT USING (is_published = true);

-- Service role has full access (for MCP server)
CREATE POLICY "Service role full access" ON design_files
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role full access" ON design_components
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role full access" ON component_variants
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role full access" ON design_tokens
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role full access" ON component_usage
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

-- Comments for documentation
COMMENT ON TABLE design_files IS 'Stores registered Figma design files with metadata';
COMMENT ON TABLE design_components IS 'Individual components extracted from Figma files with normalized layouts';
COMMENT ON TABLE component_variants IS 'Different states and variations of design components';
COMMENT ON TABLE design_tokens IS 'Global design tokens (colors, spacing, typography) extracted from files';
COMMENT ON TABLE component_usage IS 'Analytics tracking for component usage and generation';

COMMENT ON COLUMN design_components.json_layout IS 'Normalized component structure compatible with code generation';
COMMENT ON COLUMN design_components.shadcn_component IS 'Mapped ShadCN UI component name for code generation';
COMMENT ON COLUMN design_components.design_tokens IS 'Component-specific design tokens override';