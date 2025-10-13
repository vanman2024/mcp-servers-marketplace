#!/usr/bin/env python3
"""
Direct database import without MCP
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from environment
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in environment")

# Read the SQL file
with open('bulk_marketing_import.sql', 'r') as f:
    sql_content = f.read()

# Direct Supabase REST API call
url = f"{SUPABASE_URL}/rest/v1/rpc/execute_sql"
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

print("Executing bulk import of ALL 76 marketing sections in ONE operation...")

response = requests.post(url, json={"query": sql_content}, headers=headers)

if response.status_code == 200:
    print("✓ Successfully executed bulk import!")
    # Check count
    count_url = "https://wsmhiiharnhqupdniwgw.supabase.co/rest/v1/sections?app_type=eq.marketing-site&select=count"
    count_response = requests.get(count_url, headers=headers)
    print(f"Total marketing sections in database: {count_response.json()}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)