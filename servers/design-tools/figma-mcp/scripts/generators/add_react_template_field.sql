-- Add react_template field to figma_components table for executable code generation
-- This field will store shadcn/ui React component templates with imports and dependencies

ALTER TABLE figma_components 
ADD COLUMN IF NOT EXISTS react_template JSONB DEFAULT '{}'::jsonb;

-- Add helpful comment
COMMENT ON COLUMN figma_components.react_template IS 'Executable React component template with imports, dependencies, and code for shadcn/ui components';

-- Create index for querying by component templates
CREATE INDEX IF NOT EXISTS idx_figma_components_react_template ON figma_components USING GIN(react_template);

-- Also add shadcn_component field for mapping if it doesn't exist
ALTER TABLE figma_components 
ADD COLUMN IF NOT EXISTS shadcn_component TEXT;

COMMENT ON COLUMN figma_components.shadcn_component IS 'Mapped shadcn/ui component name (button, card, input, etc.)';

-- Create index for shadcn component mapping
CREATE INDEX IF NOT EXISTS idx_figma_components_shadcn ON figma_components(shadcn_component);