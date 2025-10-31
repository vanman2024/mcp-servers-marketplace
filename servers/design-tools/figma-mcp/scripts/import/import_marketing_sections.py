#!/usr/bin/env python3
"""
Import Tailwind Plus Marketing Templates into Sections Database
==============================================================
IMPORTANT: These are MARKETING/LANDING PAGE sections only!
NOT for building applications - just for company websites, landing pages, etc.
"""

import json
import os
import asyncio
from datetime import datetime
from typing import Dict, List, Set
import hashlib

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://wsmhiiharnhqupdniwgw.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
PROJECT_ID = 'wsmhiiharnhqupdniwgw'

async def import_marketing_sections():
    """Import extracted marketing sections into database"""
    
    # Load extracted sections
    with open('extracted_sections.json', 'r') as f:
        data = json.load(f)
    
    print(f"Found {data['total_sections']} marketing sections to import")
    
    # Deduplicate sections (many are duplicated between JS/TS versions)
    unique_sections = {}
    
    for section in data['sections']:
        # Create unique key based on template + component type + name pattern
        name_parts = section['name'].split(' - ')
        if len(name_parts) > 1:
            component_name = name_parts[1].split(' (')[0]
        else:
            component_name = name_parts[0].split(' (')[0]
        
        key = f"{section['template_name']}_{section['component_type']}_{component_name}"
        
        # Skip tiny utility components
        if len(section['code']) < 500 or section['component_type'] == 'forms' and 'date' in section['name'].lower():
            continue
            
        # Keep TypeScript version if we have both
        if key not in unique_sections or section['file_path'].endswith('.tsx'):
            unique_sections[key] = section
    
    print(f"After deduplication and filtering: {len(unique_sections)} unique sections")
    
    # Prepare sections for import
    sections_to_import = []
    
    for section_data in unique_sections.values():
        # Clean up the name
        clean_name = section_data['name'].split(' (')[0].strip()
        
        # Add clear marketing label
        if 'Hero' in clean_name:
            display_name = f"Marketing Hero - {section_data['template_name'].replace('tailwind-plus-', '').title()}"
        elif 'Pricing' in clean_name:
            display_name = f"Pricing Section - {section_data['template_name'].replace('tailwind-plus-', '').title()}"
        elif 'Features' in clean_name:
            display_name = f"Features Section - {section_data['template_name'].replace('tailwind-plus-', '').title()}"
        elif 'Testimonial' in clean_name:
            display_name = f"Testimonials - {section_data['template_name'].replace('tailwind-plus-', '').title()}"
        elif 'Footer' in clean_name:
            display_name = f"Site Footer - {section_data['template_name'].replace('tailwind-plus-', '').title()}"
        elif 'Navigation' in clean_name or 'Nav' in clean_name:
            display_name = f"Site Navigation - {section_data['template_name'].replace('tailwind-plus-', '').title()}"
        else:
            display_name = f"{clean_name} - Marketing"
        
        # Create description that makes it clear these are NOT for apps
        description = (
            f"Marketing/Landing page component from Tailwind Plus {section_data['template_name'].replace('tailwind-plus-', '').title()} template. "
            f"FOR MARKETING SITES ONLY - not for application UIs. "
            f"{section_data.get('description', '')}"
        )
        
        # Prepare section data
        section = {
            'name': display_name,
            'description': description,
            'category': 'marketing-landing',  # Override category to be clear
            'subcategory': section_data['category'],  # Original category as subcategory
            'source': 'tailwind-plus-marketing',  # Clear source
            'react_template': section_data['code'],
            'template_type': 'marketing-section',
            'preview_image': '',  # No preview images available
            'is_template': True,
            'published': True,
            'tags': [
                'marketing',
                'landing-page',
                'tailwind-plus',
                section_data['component_type'],
                section_data['template_name'].replace('tailwind-plus-', ''),
                'not-for-apps'  # Clear tag
            ],
            'metadata': {
                'template_name': section_data['template_name'],
                'component_type': section_data['component_type'],
                'file_path': section_data['file_path'],
                'uses_components': section_data.get('uses_components', []),
                'dependencies': section_data.get('dependencies', []),
                'is_page': section_data.get('is_page', False),
                'warning': 'This is a marketing/landing page component. For application UIs, use app-specific sections.'
            }
        }
        
        sections_to_import.append(section)
    
    print(f"\nPrepared {len(sections_to_import)} marketing sections for import")
    
    # Group by component type for summary
    by_type = {}
    for section in sections_to_import:
        comp_type = section['metadata']['component_type']
        if comp_type not in by_type:
            by_type[comp_type] = 0
        by_type[comp_type] += 1
    
    print("\nMarketing sections by type:")
    for comp_type, count in sorted(by_type.items()):
        print(f"  {comp_type}: {count}")
    
    # Save prepared data for review
    with open('marketing_sections_to_import.json', 'w') as f:
        json.dump({
            'total': len(sections_to_import),
            'sections': sections_to_import,
            'summary': by_type,
            'warning': 'These are MARKETING sections only - not for building applications!'
        }, f, indent=2)
    
    print(f"\nSaved {len(sections_to_import)} marketing sections to marketing_sections_to_import.json")
    print("\nThese sections are clearly labeled as marketing/landing page components.")
    print("They should NOT be used for building application UIs.")
    
    # Create SQL for bulk insert
    create_bulk_insert_sql(sections_to_import)

def create_bulk_insert_sql(sections: List[Dict]):
    """Create SQL file for bulk inserting marketing sections"""
    
    sql_statements = []
    
    # Add header warning
    sql_statements.append("""-- MARKETING SECTIONS IMPORT
-- WARNING: These are marketing/landing page sections from Tailwind Plus templates
-- NOT for building applications - only for marketing websites!
-- Generated: {}

""".format(datetime.now().isoformat()))
    
    for section in sections:
        # Escape single quotes in strings
        name = section['name'].replace("'", "''")
        description = section['description'].replace("'", "''")
        react_template = section['react_template'].replace("'", "''")
        
        sql = f"""
INSERT INTO sections (
    name,
    description,
    category,
    subcategory,
    source,
    react_template,
    template_type,
    is_template,
    published,
    tags,
    metadata,
    project_id
) VALUES (
    '{name}',
    '{description}',
    '{section['category']}',
    '{section['subcategory']}',
    '{section['source']}',
    '{react_template}',
    '{section['template_type']}',
    {section['is_template']},
    {section['published']},
    ARRAY{section['tags']}::text[],
    '{json.dumps(section['metadata'])}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    metadata = EXCLUDED.metadata,
    updated_at = NOW();
"""
        sql_statements.append(sql)
    
    # Write to file
    with open('import_marketing_sections.sql', 'w') as f:
        f.writelines(sql_statements)
    
    print(f"\nCreated import_marketing_sections.sql with {len(sections)} marketing sections")
    print("Run with: execute_sql on Supabase MCP")

if __name__ == "__main__":
    asyncio.run(import_marketing_sections())