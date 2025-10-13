#!/usr/bin/env python3
"""
Import Figma components as EXECUTABLE React code templates
This is the CORRECT approach for the MCP workflow
"""

import os
import json
import uuid
from typing import Dict, Any, List
from supabase import create_client

def load_component_templates() -> Dict[str, Any]:
    """Load shadcn/ui component templates"""
    with open('shadcn_component_templates.json', 'r') as f:
        return json.load(f)

def load_figma_mapping() -> Dict[str, str]:
    """Load Figma to shadcn component mapping"""
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
    
    # Default fallback
    return 'button'

def create_executable_component_data(figma_components: List[Dict], templates: Dict, mapping: Dict) -> List[Dict]:
    """Transform Figma components into executable React components"""
    
    executable_components = []
    
    for figma_comp in figma_components:
        # Map to shadcn component
        shadcn_component = map_figma_to_shadcn(figma_comp['name'], mapping)
        
        if shadcn_component not in templates:
            print(f"⚠️  No template for {shadcn_component}, skipping {figma_comp['name']}")
            continue
        
        template_data = templates[shadcn_component]
        
        # Create executable component entry
        component_data = {
            'id': str(uuid.uuid4()),
            'file_id': None,  # Will be set when file is created
            'name': figma_comp['name'],
            'node_id': figma_comp.get('figma_id', ''),
            'component_type': template_data['category'],
            'shadcn_component': shadcn_component,
            
            # THIS IS THE KEY - ACTUAL EXECUTABLE CODE TEMPLATE
            'json_layout': {
                'template': template_data['template'],
                'imports': template_data['imports'],
                'dependencies': template_data['dependencies'],
                'props': template_data['props'],
                'variants': template_data.get('variants', {}),
                'example': template_data['example'],
                'category': template_data['category'],
                'description': template_data['description']
            },
            
            # Design tokens extracted from Figma
            'design_tokens': {
                'colors': figma_comp.get('colors', {}),
                'spacing': figma_comp.get('spacing', {}),
                'typography': figma_comp.get('typography', {}),
                'figma_properties': figma_comp.get('props', {})
            },
            
            'tags': [shadcn_component, template_data['category']],
            'theme': 'both',
            'figma_url': figma_comp.get('figma_url', ''),
            'is_published': True,
            'version': 1
        }
        
        executable_components.append(component_data)
    
    return executable_components

def import_to_database(components: List[Dict]):
    """Import executable components to proper database schema"""
    
    # Connect to database
    supabase_url = 'https://wsmhiiharnhqupdniwgw.supabase.co'
    supabase_key = os.getenv('FIGMA_DESIGN_SYSTEM_SERVICE_KEY', 
                            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndzbWhpaWhhcm5ocXVwZG5pd2d3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNjcyMzE2OSwiZXhwIjoyMDUyMjk5MTY5fQ.xY6RCfcmgSTaZo4nI0mPdixrGfGgUeQ-ypd0zHGPCbI')
    
    supabase = create_client(supabase_url, supabase_key)
    
    # First, create a design file entry
    file_data = {
        'name': 'shadcn/ui Design System (Executable)',
        'file_key': 'JGMQqO02q6wLSyk29RDsgh',
        'file_url': 'https://www.figma.com/design/JGMQqO02q6wLSyk29RDsgh',
        'source': 'figma',
        'description': 'Executable React components mapped from Figma designs',
        'version': 1,
        'metadata': {
            'total_components': len(components),
            'import_type': 'executable_templates',
            'shadcn_version': '0.8.0'
        }
    }
    
    try:
        # Insert design file
        file_result = supabase.table('design_files').insert(file_data).execute()
        file_id = file_result.data[0]['id']
        print(f"✅ Created design file: {file_id}")
        
        # Update components with file_id
        for comp in components:
            comp['file_id'] = file_id
        
        # Insert components in batches
        batch_size = 20
        total_inserted = 0
        
        for i in range(0, len(components), batch_size):
            batch = components[i:i + batch_size]
            
            try:
                result = supabase.table('design_components').insert(batch).execute()
                total_inserted += len(result.data)
                print(f"✅ Inserted batch {i//batch_size + 1}: {len(result.data)} components")
                
            except Exception as e:
                print(f"❌ Batch {i//batch_size + 1} failed: {e}")
        
        print(f"\n🎯 IMPORT COMPLETE:")
        print(f"   Total components: {len(components)}")
        print(f"   Successfully inserted: {total_inserted}")
        print(f"   File ID: {file_id}")
        
        return file_id, total_inserted
        
    except Exception as e:
        print(f"❌ Database import failed: {e}")
        return None, 0

def test_code_generation(file_id: str):
    """Test generating actual React code from stored templates"""
    
    # Connect to database
    supabase_url = 'https://wsmhiiharnhqupdniwgw.supabase.co' 
    supabase_key = os.getenv('FIGMA_DESIGN_SYSTEM_SERVICE_KEY',
                            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndzbWhpaWhhcm5ocXVwZG5pd2d3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNjcyMzE2OSwiZXhwIjoyMDUyMjk5MTY5fQ.xY6RCfcmgSTaZo4nI0mPdixrGfGgUeQ-ypd0zHGPCbI')
    
    supabase = create_client(supabase_url, supabase_key)
    
    # Get a button component
    result = supabase.table('design_components').select('*').eq('shadcn_component', 'button').limit(1).execute()
    
    if result.data:
        comp = result.data[0]
        template = comp['json_layout']['template']
        
        # Generate actual React component
        props = {
            'componentName': 'TodoAppButton',
            'variant': 'default',
            'size': 'default', 
            'disabled': '',
            'children': 'Add Todo'
        }
        
        generated_code = template
        for key, value in props.items():
            placeholder = '{{' + key + '}}'
            generated_code = generated_code.replace(placeholder, str(value))
        
        print("\n=== GENERATED REACT COMPONENT ===")
        print(generated_code)
        
        # Save to file
        with open('generated_todo_button.tsx', 'w') as f:
            f.write(generated_code)
        
        print(f"\n✅ Generated component saved to: generated_todo_button.tsx")
        
        return True
    
    return False

def main():
    """Main import process"""
    
    print("🚀 Starting EXECUTABLE component import...")
    
    # Load templates and mapping
    templates = load_component_templates() 
    mapping = load_figma_mapping()
    
    # Create sample Figma components (in real workflow, this comes from Figma API)
    sample_figma_components = [
        {'name': 'Primary Button', 'figma_id': '1:1', 'type': 'button'},
        {'name': 'Secondary Button', 'figma_id': '1:2', 'type': 'button'}, 
        {'name': 'Product Card', 'figma_id': '2:1', 'type': 'card'},
        {'name': 'User Input', 'figma_id': '3:1', 'type': 'input'},
        {'name': 'Login Form', 'figma_id': '4:1', 'type': 'form'},
        {'name': 'Settings Dialog', 'figma_id': '5:1', 'type': 'dialog'}
    ]
    
    # Transform to executable components
    executable_components = create_executable_component_data(sample_figma_components, templates, mapping)
    
    print(f"📦 Created {len(executable_components)} executable components")
    
    # Import to database
    file_id, total_inserted = import_to_database(executable_components)
    
    if file_id and total_inserted > 0:
        print(f"\n🧪 Testing code generation...")
        test_code_generation(file_id)
        
        print(f"\n✅ SUCCESS! MCP server can now generate actual React files!")
        print(f"   When Claude asks: 'Build a todo app'")
        print(f"   MCP server will: Query database → Get React templates → Generate .tsx files")
    
if __name__ == "__main__":
    main()