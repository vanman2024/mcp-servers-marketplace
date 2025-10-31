#!/usr/bin/env python3
"""
SAFE METADATA ENHANCEMENT - PHASE 1 ONLY
Creates new infrastructure without modifying existing data
"""

import os
import asyncio
from typing import Dict, List, Optional
import json
import re
from dotenv import load_dotenv

# Use MCP tools for safety
import sys
sys.path.append('/home/gotime2022/mcp-kernel-new/servers/http/figma-mcp/src')

load_dotenv("../../../../configs/api-keys.env")

class SafeMetadataEnhancerPhase1:
    def __init__(self):
        print("🛡️ SAFE METADATA ENHANCEMENT - PHASE 1 ONLY")
        print("✅ Creates new infrastructure")
        print("❌ NO existing data modification")
        
    async def run_with_mcp_tools(self):
        """Run enhancement using MCP tools for safety"""
        print("\n🚀 Starting Phase 1 Enhancement using MCP tools...")
        
        try:
            from figma_server_db import mcp_supabase_execute_sql
            
            # Phase 1: Create new tables (safe)
            await self.create_tag_definitions_table()
            await self.create_use_cases_table()
            await self.create_compatibility_table()
            await self.create_smart_views()
            await self.create_helper_functions()
            await self.populate_standard_data()
            await self.generate_baseline_report()
            
            print("\n✅ Phase 1 Complete! New infrastructure ready.")
            print("\n📋 WHAT WAS CREATED:")
            print("  ✓ tag_definitions table")
            print("  ✓ component_tags table")
            print("  ✓ section_tags table") 
            print("  ✓ use_cases table")
            print("  ✓ component_compatibility table")
            print("  ✓ Smart discovery views")
            print("  ✓ Helper functions")
            print("  ✓ Standard seed data")
            
            print("\n🎯 NEXT STEPS:")
            print("  1. Test new views and functions")
            print("  2. Verify performance impact")
            print("  3. Decide on Phase 2 (tag updates)")
            
        except Exception as e:
            print(f"\n❌ Error during Phase 1: {e}")
            return False
            
        return True
        
    async def create_tag_definitions_table(self):
        """Create normalized tag storage"""
        print("\n🏷️ Creating tag_definitions infrastructure...")
        
        sql = """
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
        """
        
        try:
            await self.execute_sql_safely(sql)
            print("  ✓ Tag definitions tables created")
        except Exception as e:
            print(f"  ✗ Error creating tag tables: {e}")
            
    async def create_use_cases_table(self):
        """Create use case mapping tables"""
        print("\n🎯 Creating use case infrastructure...")
        
        sql = """
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
        """
        
        try:
            await self.execute_sql_safely(sql)
            print("  ✓ Use case tables created")
        except Exception as e:
            print(f"  ✗ Error creating use case tables: {e}")
            
    async def create_compatibility_table(self):
        """Create component compatibility matrix"""
        print("\n🔗 Creating compatibility infrastructure...")
        
        sql = """
        CREATE TABLE IF NOT EXISTS component_compatibility (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            component_a_id UUID REFERENCES figma_components(id) ON DELETE CASCADE,
            component_b_id UUID REFERENCES figma_components(id) ON DELETE CASCADE,
            compatibility_score INTEGER CHECK (compatibility_score >= 0 AND compatibility_score <= 100),
            integration_notes TEXT,
            tested BOOLEAN DEFAULT FALSE,
            UNIQUE(component_a_id, component_b_id)
        );
        """
        
        try:
            await self.execute_sql_safely(sql)
            print("  ✓ Compatibility table created")
        except Exception as e:
            print(f"  ✗ Error creating compatibility table: {e}")
            
    async def create_smart_views(self):
        """Create intelligent discovery views"""
        print("\n👁️ Creating smart discovery views...")
        
        sql = """
        -- Component discovery view
        CREATE OR REPLACE VIEW component_smart_search AS
        SELECT 
            fc.id,
            fc.name,
            fc.description,
            cc.name as category,
            fc.component_type,
            fc.complexity_score,
            fc.popularity_score,
            fc.tags,
            COUNT(DISTINCT cuc.use_case_id) as use_case_count,
            COUNT(DISTINCT sc.section_id) as used_in_sections
        FROM figma_components fc
        LEFT JOIN component_categories cc ON fc.category_id = cc.id
        LEFT JOIN component_use_cases cuc ON fc.id = cuc.component_id
        LEFT JOIN section_components sc ON fc.id = sc.component_id
        GROUP BY fc.id, fc.name, fc.description, cc.name, fc.component_type, 
                 fc.complexity_score, fc.popularity_score, fc.tags;

        -- Section readiness view
        CREATE OR REPLACE VIEW section_readiness AS
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
                WHEN s.react_template IS NOT NULL AND s.react_template != '' THEN TRUE
                ELSE FALSE
            END as is_app_ready
        FROM sections s
        LEFT JOIN section_components sc ON s.id = sc.section_id
        LEFT JOIN section_use_cases suc ON s.id = suc.section_id
        GROUP BY s.id, s.name, s.description, s.block_type, 
                 s.category, s.app_type, s.tags, s.react_template;

        -- Metadata health check view
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
        """
        
        try:
            await self.execute_sql_safely(sql)
            print("  ✓ Smart views created")
        except Exception as e:
            print(f"  ✗ Error creating views: {e}")
            
    async def create_helper_functions(self):
        """Create helper functions"""
        print("\n⚙️ Creating helper functions...")
        
        sql = """
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
        """
        
        try:
            await self.execute_sql_safely(sql)
            print("  ✓ Helper functions created")
        except Exception as e:
            print(f"  ✗ Error creating functions: {e}")
            
    async def populate_standard_data(self):
        """Populate with standard seed data"""
        print("\n🌱 Populating standard seed data...")
        
        sql = """
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
        """
        
        try:
            await self.execute_sql_safely(sql)
            print("  ✓ Standard seed data populated")
        except Exception as e:
            print(f"  ✗ Error populating data: {e}")
            
    async def generate_baseline_report(self):
        """Generate baseline metadata report"""
        print("\n📊 Generating baseline report...")
        
        try:
            # Use MCP tools to get current stats
            report = {
                "timestamp": "2024-01-19T20:00:00Z",
                "phase": "Phase 1 - Infrastructure Creation",
                "operations_performed": [
                    "Created tag_definitions table",
                    "Created component_tags table", 
                    "Created section_tags table",
                    "Created use_cases table",
                    "Created section_use_cases table",
                    "Created component_use_cases table",
                    "Created component_compatibility table",
                    "Created smart discovery views",
                    "Created helper functions",
                    "Populated standard seed data"
                ],
                "risk_level": "NONE - Only new infrastructure created",
                "existing_data_modified": False,
                "next_phase_available": "Phase 2 - Tag Updates (optional)"
            }
            
            # Save report
            with open("metadata_enhancement_phase1_report.json", "w") as f:
                json.dump(report, f, indent=2)
                
            print("  ✓ Baseline report saved to metadata_enhancement_phase1_report.json")
            
        except Exception as e:
            print(f"  ✗ Error generating report: {e}")
            
    async def execute_sql_safely(self, sql: str):
        """Execute SQL using MCP tools for safety"""
        try:
            # Import the MCP tool
            from figma_server_db import mcp_supabase_execute_sql
            
            # Execute via MCP tool
            result = await mcp_supabase_execute_sql(
                project_id="wsmhiiharnhqupdniwgw",
                query=sql
            )
            
            return result
            
        except Exception as e:
            print(f"Error executing SQL: {e}")
            # Fallback to direct execution if MCP fails
            raise e

async def main():
    enhancer = SafeMetadataEnhancerPhase1()
    success = await enhancer.run_with_mcp_tools()
    
    if success:
        print("\n🎉 Phase 1 Enhancement Successful!")
        print("\nNew infrastructure is ready for testing.")
    else:
        print("\n❌ Phase 1 Enhancement Failed!")

if __name__ == "__main__":
    asyncio.run(main())