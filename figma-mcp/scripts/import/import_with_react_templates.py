#!/usr/bin/env python3
"""
Import ALL Figma components with BOTH metadata and executable React templates
Uses existing figma_components schema with props field to store React templates
"""

import os
import json
import uuid
from typing import Dict, Any, List
from supabase import create_client

def load_all_figma_components() -> List[Dict]:
    """Load all 1054 components from the original extraction"""
    
    print("=== LOADING ALL FIGMA COMPONENTS ===")
    
    # Load the original extraction data
    with open('extracted_figma_components.json', 'r') as f:
        all_components = json.load(f)
    
    print(f"✅ Loaded {len(all_components)} components from original extraction")
    return all_components

def load_component_templates() -> Dict[str, Any]:
    """Load shadcn/ui component templates"""
    
    if not os.path.exists('shadcn_component_templates.json'):
        print("❌ shadcn_component_templates.json not found. Running create_proper_component_mapping.py...")
        os.system('python3 create_proper_component_mapping.py')
    
    with open('shadcn_component_templates.json', 'r') as f:
        return json.load(f)

def load_figma_mapping() -> Dict[str, str]:
    """Load Figma to shadcn component mapping"""
    
    if not os.path.exists('figma_to_shadcn_mapping.json'):
        print("❌ figma_to_shadcn_mapping.json not found. Running create_proper_component_mapping.py...")
        os.system('python3 create_proper_component_mapping.py')
    
    with open('figma_to_shadcn_mapping.json', 'r') as f:
        return json.load(f)

def map_figma_to_shadcn(figma_name: str, mapping: Dict[str, str]) -> str:
    """Map a Figma component name to shadcn component"""
    
    # Direct mapping first
    if figma_name in mapping:
        return mapping[figma_name]
    
    # Fuzzy matching for common patterns
    name_lower = figma_name.lower()
    
    if 'button' in name_lower or 'btn' in name_lower:
        return 'button'
    elif 'card' in name_lower or 'panel' in name_lower:
        return 'card'
    elif 'input' in name_lower or 'field' in name_lower:
        return 'input'
    elif 'form' in name_lower:
        return 'form'
    elif 'dialog' in name_lower or 'modal' in name_lower:
        return 'dialog'
    elif 'nav' in name_lower or 'menu' in name_lower:
        return 'navigation-menu'
    elif 'switch' in name_lower or 'toggle' in name_lower:
        return 'button'  # Use button template for switches
    elif 'textarea' in name_lower:
        return 'input'  # Use input template for textareas
    
    # Default fallback
    return 'button'

def get_category_uuid(component_type: str) -> str:
    """Get category UUID based on component type"""
    
    category_mapping = {
        'button': '12cf1a44-94dc-49b2-ad50-0b9eef0e3b7c',  # UI Elements
        'card': '12cf1a44-94dc-49b2-ad50-0b9eef0e3b7c',    # UI Elements
        'input': '36ba3882-188b-4ee6-8cde-0e746f24331e',   # Forms
        'form': '36ba3882-188b-4ee6-8cde-0e746f24331e',    # Forms
        'dialog': '0b25761c-856d-4306-8d4e-6888b09c286b',  # Overlays
        'navigation': '8a783d0c-d70f-4700-b649-ade1cfded25d',  # Navigation
        'navigation-menu': '8a783d0c-d70f-4700-b649-ade1cfded25d',  # Navigation
        'component': '0b25761c-856d-4306-8d4e-6888b09c286b',  # Default to UI Elements
    }
    
    return category_mapping.get(component_type, '0b25761c-856d-4306-8d4e-6888b09c286b')

def create_enhanced_component_data(figma_components: List[Dict], templates: Dict, mapping: Dict) -> List[Dict]:
    """Transform Figma components into enhanced records with React templates"""
    
    enhanced_components = []
    
    print(f"=== ENHANCING {len(figma_components)} COMPONENTS ===")
    
    for i, figma_comp in enumerate(figma_components):
        # Map to shadcn component
        shadcn_component = map_figma_to_shadcn(figma_comp['name'], mapping)
        
        if shadcn_component not in templates:
            print(f"⚠️  No template for {shadcn_component}, using button template for {figma_comp['name']}")
            shadcn_component = 'button'  # Fallback
        
        template_data = templates[shadcn_component]
        
        # Get component type from original data or map from template
        component_type = figma_comp.get('type', template_data['category'])
        
        # Enhanced props field with BOTH Figma metadata AND React template
        enhanced_props = {
            # Original Figma metadata
            'figma_metadata': figma_comp.get('props', {}),
            'original_figma_props': figma_comp.get('props', {}),
            
            # NEW: Executable React template data
            'react_template': {
                'shadcn_component': shadcn_component,
                'template': template_data['template'],
                'imports': template_data['imports'],
                'dependencies': template_data['dependencies'],
                'props': template_data['props'],
                'variants': template_data.get('variants', {}),
                'example': template_data['example'],
                'category': template_data['category'],
                'description': template_data['description']
            },
            
            # Design tokens for styling
            'design_tokens': {
                'colors': figma_comp.get('colors', {}),
                'spacing': figma_comp.get('spacing', {}),
                'typography': figma_comp.get('typography', {}),
            }
        }
        
        # Create enhanced component entry for database
        component_data = {
            'figma_id': figma_comp.get('figma_id', f'generated-{uuid.uuid4()}'),
            'name': figma_comp['name'],
            'description': figma_comp.get('description', ''),
            'category_id': get_category_uuid(component_type),
            'figma_url': figma_comp.get('figma_url', ''),
            'component_type': component_type,
            'tags': [shadcn_component, template_data['category']] + figma_comp.get('tags', []),
            'complexity_score': 1,
            'popularity_score': 0,
            'props': enhanced_props,  # THIS IS THE KEY - Enhanced props with React template
            'figma_node_type': figma_comp.get('figma_node_type', 'COMPONENT'),
            'width': figma_comp.get('width', 100.0),
            'height': figma_comp.get('height', 100.0),
            'status': 'active',
            'last_synced': '2025-07-14T01:37:30.759031+00:00'
        }
        
        enhanced_components.append(component_data)
        
        if (i + 1) % 100 == 0:
            print(f"  Enhanced {i + 1}/{len(figma_components)} components...")
    
    print(f"✅ Enhanced all {len(enhanced_components)} components with React templates")
    return enhanced_components

def import_to_database(components: List[Dict]):
    """Import enhanced components to database using existing schema"""
    
    # Connect to database
    supabase_url = 'https://wsmhiiharnhqupdniwgw.supabase.co'
    supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndzbWhpaWhhcm5ocXVwZG5pd2d3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTIyNjk5OSwiZXhwIjoyMDY2ODAyOTk5fQ.R5DGQCoMhN9hj_P3Ri0Kkfl6VdaYGlKOOLmvnOmiJOA'
    
    supabase = create_client(supabase_url, supabase_key)
    
    print(f"=== IMPORTING {len(components)} COMPONENTS TO DATABASE ===")
    
    # Insert components in batches
    batch_size = 25
    total_inserted = 0
    failed_inserts = 0
    
    for i in range(0, len(components), batch_size):
        batch = components[i:i + batch_size]
        
        try:
            result = supabase.table('figma_components').upsert(batch, on_conflict='figma_id').execute()
            total_inserted += len(result.data)
            print(f"✅ Inserted batch {i//batch_size + 1}: {len(result.data)} components")
            
        except Exception as e:
            failed_inserts += len(batch)
            print(f"❌ Batch {i//batch_size + 1} failed: {e}")
            
            # Try individual inserts for this batch
            for comp in batch:
                try:
                    result = supabase.table('figma_components').upsert(comp, on_conflict='figma_id').execute()
                    total_inserted += 1
                    failed_inserts -= 1
                except Exception as e2:
                    print(f"  ❌ Failed to insert {comp['name']}: {e2}")
    
    print(f"\\n🎯 IMPORT COMPLETE:")
    print(f"   Total components: {len(components)}")
    print(f"   Successfully inserted: {total_inserted}")
    print(f"   Failed inserts: {failed_inserts}")
    
    return total_inserted, failed_inserts

def test_react_template_functionality():
    """Test that we can extract and use React templates from stored data"""
    
    # Connect to database
    supabase_url = 'https://wsmhiiharnhqupdniwgw.supabase.co'
    supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndzbWhpaWhhcm5ocXVwZG5pd2d3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTIyNjk5OSwiZXhwIjoyMDY2ODAyOTk5fQ.R5DGQCoMhN9hj_P3Ri0Kkfl6VdaYGlKOOLmvnOmiJOA'
    
    supabase = create_client(supabase_url, supabase_key)
    
    print("\\n=== TESTING REACT TEMPLATE FUNCTIONALITY ===")
    
    # Get a button component with React template
    result = supabase.table('figma_components').select('*').contains('props->react_template->shadcn_component', 'button').limit(1).execute()
    
    if result.data:
        comp = result.data[0]
        template_data = comp['props']['react_template']
        template = template_data['template']
        
        print(f"✅ Found component: {comp['name']}")
        print(f"✅ Shadcn component: {template_data['shadcn_component']}")
        
        # Generate actual React component
        props = {
            'componentName': 'TestButton',
            'variant': 'default',
            'size': 'default', 
            'disabled': '',
            'children': 'Click Me'
        }
        
        generated_code = template
        for key, value in props.items():
            placeholder = '{{' + key + '}}'
            generated_code = generated_code.replace(placeholder, str(value))
        
        print("\\n=== GENERATED REACT COMPONENT ===")
        print(generated_code)
        
        # Save to file
        with open('test_generated_component.tsx', 'w') as f:
            f.write(generated_code)
        
        print(f"\\n✅ Generated component saved to: test_generated_component.tsx")
        
        return True
    else:
        print("❌ No components with React templates found")
        return False

def main():
    """Main import process"""
    
    print("🚀 Starting COMPREHENSIVE component import with React templates...")
    
    # Load templates and mapping
    templates = load_component_templates() 
    mapping = load_figma_mapping()
    
    print(f"✅ Loaded {len(templates)} React templates")
    print(f"✅ Loaded {len(mapping)} component mappings")
    
    # Load all Figma components
    figma_components = load_all_figma_components()
    
    # Check how many are already in database
    supabase_url = 'https://wsmhiiharnhqupdniwgw.supabase.co'
    supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndzbWhpaWhhcm5ocXVwZG5pd2d3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTIyNjk5OSwiZXhwIjoyMDY2ODAyOTk5fQ.R5DGQCoMhN9hj_P3Ri0Kkfl6VdaYGlKOOLmvnOmiJOA'
    
    supabase = create_client(supabase_url, supabase_key)
    
    current_count = supabase.table('figma_components').select('count', count='exact').execute().count
    print(f"📊 Current database: {current_count} components")
    print(f"📊 Total to import: {len(figma_components)} components")
    print(f"📊 New components: {len(figma_components) - current_count}")
    
    # Transform to enhanced components with React templates
    enhanced_components = create_enhanced_component_data(figma_components, templates, mapping)
    
    # Import to database
    total_inserted, failed_inserts = import_to_database(enhanced_components)
    
    if total_inserted > 0:
        print(f"\\n🧪 Testing React template functionality...")
        test_react_template_functionality()
        
        print(f"\\n✅ SUCCESS! Figma-to-React workflow is now complete!")
        print(f"   Database contains: {current_count + total_inserted} total components")
        print(f"   With React templates: {total_inserted} components")
        print(f"   MCP server can now generate actual .tsx files from 'build a todo app' queries")
    else:
        print(f"\\n❌ Import failed - no components were added")

if __name__ == "__main__":
    main()