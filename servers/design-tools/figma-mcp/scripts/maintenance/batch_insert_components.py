#!/usr/bin/env python3
"""
Batch insert Figma components into Supabase database
Handles large datasets by processing in smaller batches
"""

import json
import sys
import os
from datetime import datetime

def load_components():
    """Load transformed components from JSON file"""
    try:
        with open('db_ready_components.json', 'r') as f:
            components = json.load(f)
        print(f"✅ Loaded {len(components)} components")
        return components
    except Exception as e:
        print(f"❌ Error loading components: {e}")
        return []

def create_batch_files(components, batch_size=50):
    """Split components into smaller batch files for MCP insertion"""
    batch_files = []
    
    for i in range(0, len(components), batch_size):
        batch = components[i:i + batch_size]
        batch_filename = f"batch_{i//batch_size + 1:03d}.json"
        
        with open(batch_filename, 'w') as f:
            json.dump(batch, f, indent=2, default=str)
        
        batch_files.append(batch_filename)
        print(f"📁 Created {batch_filename} with {len(batch)} components")
    
    return batch_files

def main():
    """Main batch processing function"""
    print("=== Batch Insert Figma Components ===\n")
    
    # Load all components
    components = load_components()
    if not components:
        return
    
    # Create batch files
    print(f"🔄 Creating batch files (50 components each)...")
    batch_files = create_batch_files(components, batch_size=50)
    
    print(f"\n✅ Created {len(batch_files)} batch files")
    print("📋 Sample batch files:")
    for batch_file in batch_files[:5]:
        print(f"  - {batch_file}")
    
    if len(batch_files) > 5:
        print(f"  ... and {len(batch_files) - 5} more")
    
    print(f"\n🎯 Ready to insert {len(components)} components using MCP tools")
    print("Use the Supabase MCP tools to insert each batch file into the figma_components table")
    
    # Create insertion script for MCP
    mcp_script = []
    mcp_script.append("# MCP Supabase insertion commands")
    mcp_script.append("# Run these one by one with the MCP tools\n")
    
    for i, batch_file in enumerate(batch_files, 1):
        mcp_script.append(f"# Batch {i} - {batch_file}")
        mcp_script.append(f"# mcp__supabase-v4__insert_data:")
        mcp_script.append(f"# - table: figma_components")
        mcp_script.append(f"# - data: {batch_file}")
        mcp_script.append(f"# - project_id: wsmhiiharnhqupdniwgw")
        mcp_script.append("")
    
    with open('mcp_insertion_commands.txt', 'w') as f:
        f.write('\n'.join(mcp_script))
    
    print("📄 MCP insertion commands saved to mcp_insertion_commands.txt")

if __name__ == "__main__":
    main()