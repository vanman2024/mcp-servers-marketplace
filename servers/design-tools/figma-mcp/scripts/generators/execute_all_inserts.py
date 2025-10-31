#!/usr/bin/env python3
"""
Execute all SQL insert files sequentially
"""

import glob
import os
import time

def main():
    """Execute all SQL insert files"""
    
    # Get all SQL insert files
    sql_files = sorted(glob.glob('insert_batch_*.sql'))
    
    print(f"Found {len(sql_files)} SQL files to execute")
    
    for i, sql_file in enumerate(sql_files, 1):
        print(f"\nExecuting {sql_file} ({i}/{len(sql_files)})...")
        
        # Read SQL content
        with open(sql_file, 'r') as f:
            sql_content = f.read()
        
        # Create a temporary command file for the MCP tool
        cmd_file = f"mcp_cmd_{i:03d}.txt"
        with open(cmd_file, 'w') as f:
            f.write(f"Execute this SQL using mcp__supabase-v4__execute_sql:\n")
            f.write(f"project_id: wsmhiiharnhqupdniwgw\n")
            f.write(f"query: {sql_content}\n")
        
        print(f"  - Command prepared in {cmd_file}")
        
        # Note: The actual execution needs to be done via MCP tools
        # This script prepares the commands for manual execution
    
    print(f"\nPrepared {len(sql_files)} command files")
    print("Execute each command using the MCP Supabase tool")

if __name__ == "__main__":
    main()