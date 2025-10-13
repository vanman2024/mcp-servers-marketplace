#!/usr/bin/env python3
"""
Execute all SQL batch files using MCP Supabase tool
"""

import subprocess
import json
import time
import glob

def execute_sql_batch(batch_file, project_id="wsmhiiharnhqupdniwgw"):
    """Execute a single SQL batch file using MCP"""
    
    # Read the SQL content
    with open(batch_file, 'r') as f:
        sql_content = f.read()
    
    # Create MCP command
    mcp_command = [
        'python', '-c', f'''
import json
import subprocess
import sys

# MCP Supabase execute_sql call
cmd = [
    "mcp__supabase-v4__execute_sql",
    "--project_id", "{project_id}",
    "--query", {repr(sql_content)}
]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode == 0:
        print(f"✅ {batch_file} executed successfully")
    else:
        print(f"❌ {batch_file} failed: {{result.stderr}}")
except Exception as e:
    print(f"❌ {batch_file} error: {{e}}")
'''
    ]
    
    try:
        result = subprocess.run(mcp_command, capture_output=True, text=True, timeout=120)
        return result.returncode == 0
    except Exception as e:
        print(f"Error executing {batch_file}: {e}")
        return False

def main():
    """Execute all batch files"""
    
    # Get all SQL batch files
    batch_files = sorted(glob.glob('insert_batch_*.sql'))
    
    print(f"Found {len(batch_files)} batch files to execute")
    
    # Track progress
    completed = 0
    failed = 0
    
    # Start from batch 3 (assuming 1-2 are already done)
    start_batch = 3
    
    for batch_file in batch_files[start_batch-1:]:  # Skip first 2 batches
        batch_num = int(batch_file.split('_')[2].split('.')[0])
        
        print(f"\n=== Executing batch {batch_num} ({batch_file}) ===")
        
        success = execute_sql_batch(batch_file)
        
        if success:
            completed += 1
            print(f"✅ Batch {batch_num} completed")
        else:
            failed += 1
            print(f"❌ Batch {batch_num} failed")
        
        # Small delay between batches
        time.sleep(1)
    
    print(f"\n🎯 Execution Summary:")
    print(f"   Batches completed: {completed}")
    print(f"   Batches failed: {failed}")
    print(f"   Total processed: {completed + failed}")
    
    # Create completion report
    report = {
        'completed_batches': completed,
        'failed_batches': failed,
        'total_processed': completed + failed,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'completed' if failed == 0 else 'partially_completed'
    }
    
    with open('batch_execution_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to batch_execution_report.json")

if __name__ == "__main__":
    main()