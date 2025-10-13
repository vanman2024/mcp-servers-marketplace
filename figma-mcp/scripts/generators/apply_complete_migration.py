#!/usr/bin/env python3
"""
Apply Complete Phase 1 Migration: Insert all 15 e-commerce blocks into Supabase at once
"""

import sys
import os
import json
from datetime import datetime

# Import MCP functions
try:
    # Simulated Supabase execute_sql function - replace with actual MCP call
    def execute_sql(project_id, query):
        """Placeholder for MCP Supabase execution"""
        print(f"Executing SQL on project {project_id}:")
        print(f"Query length: {len(query)} characters")
        return {"status": "success"}
    
    # Import all block generation functions
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    
    from block_expansion_phase1 import generate_ecommerce_blocks
    from block_expansion_phase1_part2 import generate_remaining_ecommerce_blocks  
    from block_expansion_phase1_part3 import generate_final_ecommerce_blocks
    from block_expansion_phase1_part4 import generate_remaining_final_ecommerce_blocks
    
except ImportError as e:
    print(f"Error importing: {e}")
    sys.exit(1)

def escape_sql_string(text):
    """Properly escape strings for SQL"""
    if isinstance(text, str):
        return text.replace("'", "''").replace('\\', '\\\\')
    return text

def create_batch_insert_sql(all_blocks):
    """Create a single SQL statement with multiple INSERT VALUES"""
    
    sql_parts = []
    sql_parts.append("INSERT INTO application_blocks (")
    sql_parts.append("    id, name, description, block_type, app_type,")
    sql_parts.append("    react_template, dependencies, props_schema,")
    sql_parts.append("    example_props, tags, created_at, updated_at")
    sql_parts.append(") VALUES")
    
    value_parts = []
    for i, block in enumerate(all_blocks):
        value_part = f"""(
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
)"""
        value_parts.append(value_part)
    
    sql_parts.append(",\n".join(value_parts))
    sql_parts.append(";")
    
    return "\n".join(sql_parts)

def main():
    """Apply complete Phase 1 migration"""
    print("🚀 Applying Complete Phase 1 Migration")
    print("=" * 50)
    
    # Collect all blocks from all parts
    all_blocks = []
    
    try:
        # Part 1: Blocks 1-5 (Product grids, cards, detail gallery)
        part1_blocks = generate_ecommerce_blocks()
        all_blocks.extend(part1_blocks)
        print(f"✅ Part 1: {len(part1_blocks)} blocks collected")
        
        # Part 2: Blocks 6-8 (Product detail tabs, shopping cart sidebar & page)
        part2_blocks = generate_remaining_ecommerce_blocks()
        all_blocks.extend(part2_blocks)
        print(f"✅ Part 2: {len(part2_blocks)} blocks collected")
        
        # Part 3: Blocks 9-11 (Checkout, order summary, reviews)
        part3_blocks = generate_final_ecommerce_blocks()
        all_blocks.extend(part3_blocks)
        print(f"✅ Part 3: {len(part3_blocks)} blocks collected")
        
        # Part 4: Blocks 12-15 (Filter, banners, wishlist)
        part4_blocks = generate_remaining_final_ecommerce_blocks()
        all_blocks.extend(part4_blocks)
        print(f"✅ Part 4: {len(part4_blocks)} blocks collected")
        
    except Exception as e:
        print(f"❌ Error collecting blocks: {e}")
        sys.exit(1)
    
    print(f"\n📊 Total blocks to insert: {len(all_blocks)}")
    
    # Generate the complete batch INSERT SQL
    batch_sql = create_batch_insert_sql(all_blocks)
    
    # Save the SQL to a file for inspection
    with open("complete_phase1_batch_insert.sql", "w", encoding="utf-8") as f:
        f.write(f"-- Complete Phase 1 Migration: All {len(all_blocks)} E-commerce Blocks\n")
        f.write(f"-- Generated: {datetime.utcnow().isoformat()}\n\n")
        f.write(batch_sql)
    
    print(f"📝 SQL saved to: complete_phase1_batch_insert.sql")
    print(f"📏 SQL size: {len(batch_sql):,} characters")
    
    # Show block summary
    print(f"\n📋 Block Summary:")
    for i, block in enumerate(all_blocks, 1):
        print(f"  {i:2d}. {block['name']} ({block['block_type']})")
    
    print(f"\n🎯 Ready to execute batch INSERT for all {len(all_blocks)} blocks!")
    print("Next: Use MCP Supabase tool to execute complete_phase1_batch_insert.sql")

if __name__ == "__main__":
    main()