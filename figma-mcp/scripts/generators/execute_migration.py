#!/usr/bin/env python3
"""
Execute the complete Phase 1 migration by reading and applying the SQL file
"""

import os
import sys

def read_migration_file():
    """Read the complete migration SQL file"""
    try:
        with open("phase1_complete_ecommerce_migration.sql", "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print("❌ Migration file not found. Run phase1_complete_migration.py first.")
        return None

def main():
    """Execute the migration"""
    print("🚀 Executing Phase 1 Complete Migration")
    print("=" * 50)
    
    # Read migration file
    migration_sql = read_migration_file()
    if not migration_sql:
        sys.exit(1)
    
    print(f"📄 Migration file size: {len(migration_sql):,} characters")
    print(f"📄 Migration file lines: {len(migration_sql.splitlines()):,}")
    
    # Show first few lines
    lines = migration_sql.splitlines()
    print("\n📋 Migration Header:")
    for line in lines[:10]:
        print(f"  {line}")
    
    print("\n📋 Migration Footer:")
    for line in lines[-5:]:
        print(f"  {line}")
    
    print(f"\n🎯 Ready to execute complete migration!")
    print("⚠️  This will insert all 15 e-commerce blocks into Supabase")
    print("📁 File: phase1_complete_ecommerce_migration.sql")
    
    # The actual execution would be done via MCP Supabase tool
    # For now, just showing the file is ready
    return migration_sql

if __name__ == "__main__":
    sql = main()
    if sql:
        # Split by individual INSERT statements to show structure
        inserts = [part for part in sql.split("-- Block") if "INSERT INTO" in part]
        print(f"\n📊 Found {len(inserts)} individual INSERT statements")