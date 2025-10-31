#!/usr/bin/env python3
"""
Bulk insert all 15 Phase 1 blocks directly via Python using MCP calls
"""

import sys
import os
import json
from datetime import datetime

# Import block generation functions
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from block_expansion_phase1 import generate_ecommerce_blocks
    from block_expansion_phase1_part2 import generate_remaining_ecommerce_blocks  
    from block_expansion_phase1_part3 import generate_final_ecommerce_blocks
    from block_expansion_phase1_part4 import generate_remaining_final_ecommerce_blocks
except ImportError as e:
    print(f"Error importing: {e}")
    sys.exit(1)

def format_block_for_supabase(block):
    """Format block data for Supabase insert_data call"""
    return {
        "id": block["id"],
        "name": block["name"],
        "description": block["description"],
        "block_type": block["block_type"],
        "app_type": block["app_type"],
        "react_template": block["react_template"],
        "dependencies": block["dependencies"],
        "props_schema": block["props_schema"],
        "example_props": block["example_props"],
        "tags": block["tags"],
        "created_at": block["created_at"].isoformat(),
        "updated_at": block["updated_at"].isoformat()
    }

def main():
    """Generate and bulk insert all blocks"""
    print("🚀 Bulk Inserting All 15 Phase 1 Blocks")
    print("=" * 50)
    
    # Collect all blocks
    all_blocks = []
    
    try:
        # Part 1: Blocks 1-5
        part1_blocks = generate_ecommerce_blocks()
        all_blocks.extend(part1_blocks)
        print(f"✅ Part 1: {len(part1_blocks)} blocks")
        
        # Part 2: Blocks 6-8
        part2_blocks = generate_remaining_ecommerce_blocks()
        all_blocks.extend(part2_blocks)
        print(f"✅ Part 2: {len(part2_blocks)} blocks")
        
        # Part 3: Blocks 9-11
        part3_blocks = generate_final_ecommerce_blocks()
        all_blocks.extend(part3_blocks)
        print(f"✅ Part 3: {len(part3_blocks)} blocks")
        
        # Part 4: Blocks 12-15
        part4_blocks = generate_remaining_final_ecommerce_blocks()
        all_blocks.extend(part4_blocks)
        print(f"✅ Part 4: {len(part4_blocks)} blocks")
        
    except Exception as e:
        print(f"❌ Error collecting blocks: {e}")
        sys.exit(1)
    
    print(f"\n📊 Total blocks ready: {len(all_blocks)}")
    
    # Format all blocks for Supabase
    formatted_blocks = [format_block_for_supabase(block) for block in all_blocks]
    
    # Save as JSON for bulk insert
    with open("phase1_blocks_for_supabase.json", "w", encoding="utf-8") as f:
        json.dump(formatted_blocks, f, indent=2, default=str)
    
    print(f"📁 Blocks saved to: phase1_blocks_for_supabase.json")
    
    # Show summary
    print(f"\n📋 Block Summary:")
    for i, block in enumerate(all_blocks, 1):
        print(f"  {i:2d}. {block['name']}")
    
    print(f"\n🎯 Ready for MCP bulk insert!")
    print("Use: mcp__supabase-v4__insert_data with the JSON file")

if __name__ == "__main__":
    main()