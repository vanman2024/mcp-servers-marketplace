#!/usr/bin/env python3
"""
Find and remove duplicate marketing sections
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from collections import defaultdict

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('FIGMA_DESIGN_SYSTEM_URL', 'https://wsmhiiharnhqupdniwgw.supabase.co')
SUPABASE_KEY = os.getenv('FIGMA_DESIGN_SYSTEM_SERVICE_KEY')

# Create client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Analyzing duplicates in marketing sections...")

# Get all marketing sections
result = supabase.table('sections').select('*').eq('app_type', 'marketing-site').execute()
sections = result.data

print(f"Total marketing sections: {len(sections)}")

# Find duplicates by name
name_groups = defaultdict(list)
for section in sections:
    name_groups[section['name']].append(section)

# Find duplicates by react_template (exact code match)
template_groups = defaultdict(list)
for section in sections:
    template_groups[section['react_template']].append(section)

# Report duplicates
print("\n=== DUPLICATES BY NAME ===")
duplicate_count = 0
ids_to_delete = []

for name, group in name_groups.items():
    if len(group) > 1:
        print(f"\n'{name}': {len(group)} copies")
        # Keep the first one, mark others for deletion
        for i, section in enumerate(group[1:], 1):
            ids_to_delete.append(section['id'])
            duplicate_count += 1

print(f"\nTotal duplicates by name: {duplicate_count}")

# Check for same code but different names
print("\n=== DUPLICATES BY CODE (same code, maybe different names) ===")
code_duplicate_count = 0
for template, group in template_groups.items():
    if len(group) > 1:
        names = [s['name'] for s in group]
        if len(set(names)) > 1:  # Different names but same code
            print(f"\nSame code with different names: {names}")
        # Keep the first one regardless
        for section in group[1:]:
            if section['id'] not in ids_to_delete:
                ids_to_delete.append(section['id'])
                code_duplicate_count += 1

print(f"\nTotal additional duplicates by code: {code_duplicate_count}")
print(f"\nTOTAL IDs to delete: {len(ids_to_delete)}")
print(f"Will keep: {len(sections) - len(ids_to_delete)} unique sections")

# Delete duplicates
if ids_to_delete:
    print("\nDeleting duplicates...")
    # Delete in batches
    batch_size = 50
    for i in range(0, len(ids_to_delete), batch_size):
        batch = ids_to_delete[i:i+batch_size]
        result = supabase.table('sections').delete().in_('id', batch).execute()
        print(f"Deleted batch {i//batch_size + 1}: {len(batch)} records")
    
    # Verify final count
    final = supabase.table('sections').select('id', count='exact').eq('app_type', 'marketing-site').execute()
    print(f"\n✓ Cleanup complete! {final.count} unique marketing sections remain")
else:
    print("\nNo duplicates found!")