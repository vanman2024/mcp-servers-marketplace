#!/usr/bin/env python3
"""
Direct bulk import using psycopg2
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use the FIGMA DESIGN SYSTEM database - NOT DevLoop!
project_id = "wsmhiiharnhqupdniwgw"

# Standard Supabase database connection for Figma Design System
DATABASE_URL = f"postgresql://postgres.{project_id}:8yRKkfgqY!Gpd4E@aws-0-us-west-1.pooler.supabase.com:5432/postgres"

print(f"Connecting to project: {project_id}")

# Read SQL file
with open('bulk_marketing_import.sql', 'r') as f:
    sql_content = f.read()

# Connect and execute
try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    print("Executing bulk import of ALL 76 marketing sections in ONE operation...")
    
    # Execute the entire SQL file at once
    cur.execute(sql_content)
    conn.commit()
    
    # Verify import
    cur.execute("SELECT COUNT(*) FROM sections WHERE app_type = 'marketing-site'")
    count = cur.fetchone()[0]
    
    print(f"\n✓ SUCCESS! Imported {count} marketing sections in ONE bulk operation!")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
    if 'conn' in locals():
        conn.rollback()
        conn.close()