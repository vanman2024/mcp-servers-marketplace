#!/usr/bin/env python3
"""
Metadata Enhancement System for Figma MCP Database
Activates the underutilized metadata infrastructure
"""

import os
import asyncio
from typing import Dict, List, Optional
import asyncpg
from dotenv import load_dotenv
import json
import re

load_dotenv("../../../../configs/api-keys.env")

class MetadataEnhancer:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL", "https://wsmhiiharnhqupdniwgw.supabase.co")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        self.db_url = self.supabase_url.replace("https://", "postgresql://postgres:")
        self.db_url = f"{self.db_url.split('.')[0]}.pooler.supabase.com:6543/postgres"
        self.db_url = f"postgresql://postgres.wsmhiiharnhqupdniwgw:{self.supabase_key}@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
        
    async def connect(self):
        """Establish database connection"""
        self.conn = await asyncpg.connect(self.db_url)
        
    async def close(self):
        """Close database connection"""
        await self.conn.close()
        
    async def analyze_current_state(self):
        """Analyze current metadata state"""
        print("🔍 Analyzing Current Metadata State...")
        
        # Check table counts
        queries = [
            ("Components with categories", 
             "SELECT COUNT(*) FROM figma_components WHERE category_id IS NOT NULL"),
            ("Components with tags", 
             "SELECT COUNT(*) FROM figma_components WHERE array_length(tags, 1) > 0"),
            ("Sections with tags", 
             "SELECT COUNT(*) FROM sections WHERE array_length(tags, 1) > 0"),
            ("Section-component mappings", 
             "SELECT COUNT(*) FROM section_components"),
            ("Component relationships", 
             "SELECT COUNT(*) FROM component_relationships"),
        ]
        
        for label, query in queries:
            result = await self.conn.fetchval(query)
            print(f"  {label}: {result}")
            
    async def populate_section_components(self):
        """Analyze React templates and populate section_components table"""
        print("\n🔗 Linking Sections to Components...")
        
        sections = await self.conn.fetch("""
            SELECT id, name, react_template 
            FROM sections 
            WHERE react_template IS NOT NULL
            LIMIT 10  -- Start with a sample
        """)
        
        component_pattern = re.compile(r'<([A-Z][A-Za-z0-9]*)')
        links_created = 0
        
        for section in sections:
            # Extract component references from React template
            matches = component_pattern.findall(section['react_template'])
            component_names = set(matches) - {'React', 'Fragment', 'div', 'span', 'button'}
            
            for comp_name in component_names:
                # Try to find matching component
                component = await self.conn.fetchrow("""
                    SELECT id FROM figma_components 
                    WHERE name ILIKE $1 
                    LIMIT 1
                """, f"%{comp_name}%")
                
                if component:
                    try:
                        await self.conn.execute("""
                            INSERT INTO section_components 
                            (section_id, component_id, component_name, position)
                            VALUES ($1, $2, $3, $4)
                            ON CONFLICT DO NOTHING
                        """, section['id'], component['id'], comp_name, links_created)
                        links_created += 1
                    except Exception as e:
                        print(f"    Error linking {comp_name}: {e}")
                        
        print(f"  Created {links_created} section-component links")
        
    async def normalize_tags(self):
        """Extract and normalize tags from arrays into tag_definitions"""
        print("\n🏷️  Normalizing Tags...")
        
        # First create the tags table if it doesn't exist
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tag_definitions (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                category VARCHAR(50),
                description TEXT,
                usage_count INTEGER DEFAULT 0,
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        
        # Extract unique tags from both tables
        component_tags = await self.conn.fetch("""
            SELECT DISTINCT unnest(tags) as tag 
            FROM figma_components 
            WHERE tags IS NOT NULL
        """)
        
        section_tags = await self.conn.fetch("""
            SELECT DISTINCT unnest(tags) as tag 
            FROM sections 
            WHERE tags IS NOT NULL
        """)
        
        all_tags = set()
        for row in component_tags + section_tags:
            if row['tag']:
                all_tags.add(row['tag'])
                
        # Insert tags into normalized table
        tags_created = 0
        for tag in all_tags:
            category = self._categorize_tag(tag)
            try:
                await self.conn.execute("""
                    INSERT INTO tag_definitions (name, category)
                    VALUES ($1, $2)
                    ON CONFLICT (name) DO NOTHING
                """, tag, category)
                tags_created += 1
            except Exception as e:
                print(f"    Error inserting tag {tag}: {e}")
                
        print(f"  Created {tags_created} tag definitions")
        
    def _categorize_tag(self, tag: str) -> str:
        """Categorize a tag based on its content"""
        tag_lower = tag.lower()
        
        if any(word in tag_lower for word in ['responsive', 'animated', 'accessible', 'interactive']):
            return 'technical'
        elif any(word in tag_lower for word in ['hero', 'cta', 'nav', 'layout', 'header', 'footer']):
            return 'design'
        elif any(word in tag_lower for word in ['marketing', 'ecommerce', 'dashboard', 'auth']):
            return 'use-case'
        elif any(word in tag_lower for word in ['saas', 'retail', 'finance', 'healthcare']):
            return 'industry'
        else:
            return 'general'
            
    async def fix_not_for_apps_sections(self):
        """Fix sections incorrectly tagged as not-for-apps"""
        print("\n🔧 Fixing 'not-for-apps' Sections...")
        
        result = await self.conn.execute("""
            UPDATE sections 
            SET tags = array_remove(tags, 'not-for-apps') || ARRAY['marketing-ready', 'tailwindui']
            WHERE 'not-for-apps' = ANY(tags)
            RETURNING id
        """)
        
        count = len(result.split('\n')) - 1 if result else 0
        print(f"  Fixed {count} sections")
        
    async def create_smart_views(self):
        """Create intelligent views for component discovery"""
        print("\n👁️  Creating Smart Discovery Views...")
        
        views = [
            ("component_smart_search", """
                CREATE OR REPLACE VIEW component_smart_search AS
                SELECT 
                    fc.id,
                    fc.name,
                    fc.description,
                    cc.name as category,
                    fc.component_type,
                    fc.tags,
                    fc.complexity_score,
                    fc.popularity_score,
                    COUNT(DISTINCT sc.section_id) as used_in_sections
                FROM figma_components fc
                LEFT JOIN component_categories cc ON fc.category_id = cc.id
                LEFT JOIN section_components sc ON fc.id = sc.component_id
                GROUP BY fc.id, fc.name, fc.description, cc.name, 
                         fc.component_type, fc.tags, fc.complexity_score, fc.popularity_score
            """),
            
            ("section_readiness", """
                CREATE OR REPLACE VIEW section_readiness AS
                SELECT 
                    s.id,
                    s.name,
                    s.block_type,
                    s.category,
                    s.tags,
                    CASE 
                        WHEN s.react_template IS NOT NULL AND 
                             s.react_template != '' AND
                             NOT ('not-for-apps' = ANY(s.tags))
                        THEN 'ready'
                        WHEN s.react_template IS NULL OR s.react_template = ''
                        THEN 'needs-template'
                        ELSE 'needs-review'
                    END as status,
                    array_length(s.tags, 1) as tag_count
                FROM sections s
            """)
        ]
        
        for view_name, view_sql in views:
            try:
                await self.conn.execute(view_sql)
                print(f"  ✓ Created view: {view_name}")
            except Exception as e:
                print(f"  ✗ Error creating {view_name}: {e}")
                
    async def generate_metadata_report(self):
        """Generate a comprehensive metadata report"""
        print("\n📊 Generating Metadata Report...")
        
        report = {
            "timestamp": "2024-01-19T18:00:00Z",
            "database": "figma_design_system",
            "analysis": {}
        }
        
        # Component statistics
        comp_stats = await self.conn.fetchrow("""
            SELECT 
                COUNT(*) as total,
                COUNT(category_id) as with_category,
                COUNT(CASE WHEN array_length(tags, 1) > 0 THEN 1 END) as with_tags,
                AVG(array_length(tags, 1)) as avg_tags_per_component
            FROM figma_components
        """)
        
        report["analysis"]["components"] = {
            "total": comp_stats['total'],
            "with_category": comp_stats['with_category'],
            "with_tags": comp_stats['with_tags'],
            "avg_tags": float(comp_stats['avg_tags_per_component'] or 0)
        }
        
        # Section statistics
        section_stats = await self.conn.fetchrow("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN array_length(tags, 1) > 0 THEN 1 END) as with_tags,
                COUNT(DISTINCT block_type) as unique_block_types,
                COUNT(DISTINCT category) as unique_categories
            FROM sections
        """)
        
        report["analysis"]["sections"] = {
            "total": section_stats['total'],
            "with_tags": section_stats['with_tags'],
            "unique_block_types": section_stats['unique_block_types'],
            "unique_categories": section_stats['unique_categories']
        }
        
        # Save report
        with open("metadata_analysis_report.json", "w") as f:
            json.dump(report, f, indent=2)
            
        print("  Report saved to metadata_analysis_report.json")
        
    async def run_full_enhancement(self):
        """Run the complete metadata enhancement process"""
        print("🚀 Starting Metadata Enhancement Process...\n")
        
        try:
            await self.connect()
            
            # Run enhancement steps
            await self.analyze_current_state()
            await self.fix_not_for_apps_sections()
            await self.normalize_tags()
            await self.populate_section_components()
            await self.create_smart_views()
            await self.generate_metadata_report()
            
            print("\n✅ Metadata Enhancement Complete!")
            
        except Exception as e:
            print(f"\n❌ Error during enhancement: {e}")
            raise
        finally:
            await self.close()

async def main():
    enhancer = MetadataEnhancer()
    await enhancer.run_full_enhancement()

if __name__ == "__main__":
    asyncio.run(main())