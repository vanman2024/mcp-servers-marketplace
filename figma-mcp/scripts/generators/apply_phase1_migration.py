#!/usr/bin/env python3
"""
Apply Phase 1 Migration: Insert all 15 e-commerce blocks into Supabase
"""

import sys
import os
import json
from datetime import datetime

# Import all block generation functions
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from block_expansion_phase1 import generate_ecommerce_blocks
    from block_expansion_phase1_part2 import generate_remaining_ecommerce_blocks  
    from block_expansion_phase1_part3 import generate_final_ecommerce_blocks
    from block_expansion_phase1_part4 import generate_remaining_final_ecommerce_blocks
except ImportError as e:
    print(f"Error importing block functions: {e}")
    sys.exit(1)

def escape_sql_string(text):
    """Properly escape strings for SQL"""
    if isinstance(text, str):
        return text.replace("'", "''").replace('\\', '\\\\')
    return text

def create_insert_sql(block):
    """Create INSERT SQL statement for a single block"""
    sql = f"""INSERT INTO application_blocks (
    id, name, description, block_type, app_type, 
    react_template, dependencies, props_schema, 
    example_props, tags, created_at, updated_at
) VALUES (
    '{block['id']}',
    '{escape_sql_string(block['name'])}',
    '{escape_sql_string(block['description'])}',
    '{block['block_type']}',
    '{block['app_type']}',
    '{escape_sql_string(block['react_template'])}',
    '{json.dumps(block['dependencies']).replace("'", "''")}',
    '{json.dumps(block['props_schema']).replace("'", "''")}',
    '{json.dumps(block['example_props'], default=str).replace("'", "''")}',
    ARRAY{block['tags']}::text[],
    '{block['created_at'].isoformat()}',
    '{block['updated_at'].isoformat()}'
);"""
    return sql

def main():
    """Apply Phase 1 migration by generating INSERT statements"""
    print("Applying Phase 1 Migration: 15 E-commerce Blocks")
    print("=" * 50)
    
    # Collect all blocks
    all_blocks = []
    
    try:
        # Part 1: Blocks 1-5
        part1_blocks = generate_ecommerce_blocks()
        all_blocks.extend(part1_blocks)
        print(f"✅ Part 1: {len(part1_blocks)} blocks collected")
        
        # Part 2: Blocks 6-8
        part2_blocks = generate_remaining_ecommerce_blocks()
        all_blocks.extend(part2_blocks)
        print(f"✅ Part 2: {len(part2_blocks)} blocks collected")
        
        # Part 3: Blocks 9-11
        part3_blocks = generate_final_ecommerce_blocks()
        all_blocks.extend(part3_blocks)
        print(f"✅ Part 3: {len(part3_blocks)} blocks collected")
        
        # Part 4: Blocks 12-15
        part4_blocks = generate_remaining_final_ecommerce_blocks()
        all_blocks.extend(part4_blocks)
        print(f"✅ Part 4: {len(part4_blocks)} blocks collected")
        
    except Exception as e:
        print(f"❌ Error collecting blocks: {e}")
        sys.exit(1)
    
    print(f"\n📊 Total blocks to apply: {len(all_blocks)}")
    
    # Generate individual INSERT SQL files for manual execution
    for i, block in enumerate(all_blocks, 1):
        sql = create_insert_sql(block)
        filename = f"insert_block_{i:02d}_{block['name'].replace(' ', '_').replace('-', '_').lower()}.sql"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"-- Block {i}: {block['name']}\n")
            f.write(f"-- Description: {block['description']}\n")
            f.write(f"-- Generated: {datetime.utcnow().isoformat()}\n\n")
            f.write(sql)
            f.write("\n")
        
        print(f"  📝 {filename} - {block['name']}")
    
    print(f"\n🎯 Generated {len(all_blocks)} individual SQL files")
    print("\nNext steps:")
    print("1. Execute each SQL file manually via Supabase MCP server")
    print("2. Run verification queries to confirm migration")
    print("3. Begin Phase 2: Navigation & Forms blocks")

if __name__ == "__main__":
    main()