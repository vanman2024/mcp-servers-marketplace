#!/usr/bin/env python3
"""
Insert extracted Figma components into Supabase database
Uses MCP tools for database operations
"""

import json
import sys
import os
from datetime import datetime, timezone

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Category mapping
CATEGORY_MAPPING = {
    "button": "67c515c4-87e1-44a6-997f-0773c9b82669",  # Buttons
    "form": "36ba3882-188b-4ee6-8cde-0e746f24331e",    # Forms
    "input": "36ba3882-188b-4ee6-8cde-0e746f24331e",   # Forms
    "navigation": "8a783d0c-d70f-4700-b649-ade1cfded25d",  # Navigation
    "layout": "0b25761c-856d-4306-8d4e-6888b09c286b",  # Layout
    "card": "372f1392-4989-42d7-81b1-8ce4b1c010a3",   # Cards
    "feedback": "62856418-308d-40fd-9734-652914399ff4", # Feedback
    "data-display": "d5d6e30f-01f6-4278-8228-624b6cd3572e", # Data Display
    "overlay": "39a395a4-fd92-4580-ab84-85ded91963e9",  # Overlays
    "media": "baf047c3-c1e5-4885-bab2-9c7e636f629b",   # Media
    "icon": "baf047c3-c1e5-4885-bab2-9c7e636f629b",    # Media (for icons)
    "modal": "39a395a4-fd92-4580-ab84-85ded91963e9",   # Overlays
    "badge": "d5d6e30f-01f6-4278-8228-624b6cd3572e",  # Data Display
    "component": "0b25761c-856d-4306-8d4e-6888b09c286b"  # Layout (default)
}

def load_components():
    """Load extracted components from JSON file"""
    try:
        with open('extracted_figma_components.json', 'r') as f:
            components = json.load(f)
        print(f"✅ Loaded {len(components)} components from file")
        return components
    except FileNotFoundError:
        print("❌ Error: extracted_figma_components.json not found")
        print("Run sync_figma_to_supabase.py first to extract components")
        return []
    except Exception as e:
        print(f"❌ Error loading components: {e}")
        return []

def transform_component_for_db(comp):
    """Transform extracted component for database insertion"""
    
    # Map component type to category ID
    category_id = CATEGORY_MAPPING.get(comp['component_type'], CATEGORY_MAPPING['component'])
    
    # Create database record
    db_component = {
        "figma_id": comp['figma_id'],
        "name": comp['name'],
        "description": comp.get('description', ''),
        "category_id": category_id,
        "figma_url": comp['figma_url'],
        "component_type": comp['component_type'],
        "tags": comp.get('tags', []),
        "complexity_score": comp.get('complexity_score', 1),
        "popularity_score": comp.get('popularity_score', 0),
        "props": comp.get('props', {}),
        "figma_node_type": comp.get('figma_node_type', 'COMPONENT'),
        "width": comp.get('width'),
        "height": comp.get('height'),
        "status": comp.get('status', 'active'),
        "last_synced": comp.get('last_synced', datetime.now(timezone.utc).isoformat())
    }
    
    return db_component

def main():
    """Main insertion function"""
    print("=== Inserting Figma Components to Database ===\n")
    
    # Load components
    components = load_components()
    if not components:
        return
    
    # Transform components for database
    print("🔄 Transforming components for database...")
    db_components = []
    
    for comp in components:
        try:
            db_comp = transform_component_for_db(comp)
            db_components.append(db_comp)
        except Exception as e:
            print(f"⚠️  Error transforming component {comp.get('name', 'unknown')}: {e}")
    
    print(f"✅ Transformed {len(db_components)} components")
    
    # Save sample for inspection
    sample_size = min(5, len(db_components))
    with open('sample_db_components.json', 'w') as f:
        json.dump(db_components[:sample_size], f, indent=2, default=str)
    
    print(f"📁 Sample of {sample_size} components saved to sample_db_components.json")
    
    # Show component type distribution
    type_counts = {}
    for comp in db_components:
        comp_type = comp['component_type']
        type_counts[comp_type] = type_counts.get(comp_type, 0) + 1
    
    print("\n📊 Component type distribution:")
    for comp_type, count in sorted(type_counts.items()):
        category_name = {v: k for k, v in CATEGORY_MAPPING.items()}.get(
            next((cat_id for cat_id in CATEGORY_MAPPING.values() 
                  if CATEGORY_MAPPING.get(comp_type) == cat_id), None), 
            "Unknown"
        )
        print(f"  {comp_type}: {count} components")
    
    print(f"\n✅ Ready to insert {len(db_components)} components into database")
    print("Use the MCP Supabase tools to perform the actual insertion in batches")
    
    # Save all components for batch insertion
    with open('db_ready_components.json', 'w') as f:
        json.dump(db_components, f, indent=2, default=str)
    
    print("📁 All components saved to db_ready_components.json")

if __name__ == "__main__":
    main()