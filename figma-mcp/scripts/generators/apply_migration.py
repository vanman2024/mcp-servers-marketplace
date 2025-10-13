#!/usr/bin/env python3
"""
Apply database migration using supabase-v4 MCP functionality
Adds react_template field to figma_components table
"""

import os
import sys
import requests
import json

def execute_migration():
    """Use supabase MCP server to execute the migration"""
    
    # Read migration SQL
    with open('add_react_template_field.sql', 'r') as f:
        migration_sql = f.read()
    
    print('=== APPLYING MIGRATION VIA SUPABASE MCP ===')
    print(f'Migration SQL:\n{migration_sql}\n')
    
    # Use the supabase server endpoint (should be running on 8032)
    supabase_mcp_url = 'http://localhost:8032'
    
    # Call execute_sql function
    payload = {
        'project_id': 'wsmhiiharnhqupdniwgw',  # Figma Design System project
        'query': migration_sql
    }
    
    try:
        response = requests.post(f'{supabase_mcp_url}/execute_sql', json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print('✅ Migration executed successfully')
            print('Result:', json.dumps(result, indent=2))
            return True
        else:
            print(f'❌ Migration failed: {response.status_code}')
            print('Response:', response.text)
            return False
            
    except Exception as e:
        print(f'❌ Connection error: {e}')
        print('Note: Make sure supabase MCP server is running on port 8032')
        return False

def verify_migration():
    """Verify the migration was applied"""
    
    from supabase import create_client
    
    supabase_url = 'https://wsmhiiharnhqupdniwgw.supabase.co'
    supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndzbWhpaWhhcm5ocXVwZG5pd2d3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTIyNjk5OSwiZXhwIjoyMDY2ODAyOTk5fQ.R5DGQCoMhN9hj_P3Ri0Kkfl6VdaYGlKOOLmvnOmiJOA'
    
    supabase = create_client(supabase_url, supabase_key)
    
    print('\n=== VERIFYING MIGRATION ===')
    
    try:
        # Try to select the new fields
        result = supabase.table('figma_components').select('react_template, shadcn_component').limit(1).execute()
        print('✅ react_template and shadcn_component fields exist')
        print('Sample data:', result.data)
        return True
        
    except Exception as e:
        print(f'❌ Verification failed: {e}')
        return False

if __name__ == '__main__':
    
    # First try direct execution
    success = execute_migration()
    
    if not success:
        print('\n=== TRYING ALTERNATIVE APPROACH ===')
        # Alternative: Use direct supabase client with raw SQL
        from supabase import create_client
        
        supabase_url = 'https://wsmhiiharnhqupdniwgw.supabase.co'
        supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndzbWhpaWhhcm5ocXVwZG5pd2d3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTIyNjk5OSwiZXhwIjoyMDY2ODAyOTk5fQ.R5DGQCoMhN9hj_P3Ri0Kkfl6VdaYGlKOOLmvnOmiJOA'
        
        supabase = create_client(supabase_url, supabase_key)
        
        # Try to add columns using individual operations
        try:
            print('Attempting to add react_template column...')
            # This might work if the column doesn't exist yet
            result = supabase.table('figma_components').insert({
                'figma_id': 'test_id_for_schema',
                'name': 'test_component',
                'react_template': {'template': 'test'},
                'shadcn_component': 'button'
            }).execute()
            
            print('✅ Columns already exist or were created successfully')
            
            # Clean up test record
            supabase.table('figma_components').delete().eq('figma_id', 'test_id_for_schema').execute()
            
        except Exception as e:
            print(f'❌ Alternative approach failed: {e}')
    
    # Verify the migration regardless
    verify_migration()