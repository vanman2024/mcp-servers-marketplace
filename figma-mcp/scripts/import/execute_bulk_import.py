#!/usr/bin/env python3
"""
Execute bulk SQL import directly without MCP server
"""

import os
from supabase import create_client, Client

# Supabase connection
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://wsmhiiharnhqupdniwgw.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndzbWhpaWhhcm5ocXVwZG5pd2d3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczMzE3MzgyMCwiZXhwIjoyMDQ4NzQ5ODIwfQ.DGO0DqCDX29z8x97xXbW0tZ-vH1x-XAgZGKCNJrZMLU')

def execute_bulk_import():
    """Execute the entire bulk import SQL file at once"""
    
    # Read the entire SQL file
    with open('bulk_marketing_import.sql', 'r') as f:
        bulk_sql = f.read()
    
    # Create Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    try:
        print("Executing bulk import of all 76 marketing sections...")
        
        # Execute the SQL directly using RPC
        result = supabase.rpc('execute_sql', {'query': bulk_sql}).execute()
        
        # Get count of imported sections
        count_result = supabase.table('sections').select('*', count='exact').eq('app_type', 'marketing-site').execute()
        count = count_result.count if hasattr(count_result, 'count') else len(count_result.data)
        
        print(f"\n✓ Successfully imported {count} marketing sections in one bulk operation!")
        
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    execute_bulk_import()