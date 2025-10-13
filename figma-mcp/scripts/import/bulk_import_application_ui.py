#!/usr/bin/env python3
"""
Bulk Import Application UI Components
====================================
System for importing Tailwind UI Application components with proper categorization
and metadata according to the official Tailwind UI taxonomy.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

class ApplicationUIImporter:
    """Handles bulk import of Application UI components into Supabase"""
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Missing Supabase credentials in environment variables")
            
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        
        # Load taxonomy
        taxonomy_path = Path(__file__).parent / 'tailwind_ui_taxonomy.json'
        with open(taxonomy_path, 'r') as f:
            self.taxonomy = json.load(f)
    
    def create_component_entry(self, 
                             name: str,
                             category: str,
                             subcategory: str = None,
                             code: str = "",
                             description: str = "",
                             tags: List[str] = None,
                             components_used: List[str] = None,
                             props: Dict = None,
                             variants: Dict = None) -> Dict:
        """Create a standardized component entry"""
        
        if tags is None:
            tags = []
        if components_used is None:
            components_used = []
        if props is None:
            props = {}
        if variants is None:
            variants = {}
        
        # Auto-generate tags based on category and subcategory
        auto_tags = [category.lower().replace(' ', '-')]
        if subcategory:
            auto_tags.append(subcategory.lower().replace(' ', '-'))
        
        # Combine auto-generated tags with custom tags
        all_tags = list(set(auto_tags + tags))
        
        component = {
            "name": name,
            "category": category,
            "subcategory": subcategory,
            "tags": all_tags,
            "source": "tailwind-ui-manual",
            "code": code,
            "description": description or f"{category} component from Tailwind UI",
            "components_used": components_used,
            "props": props,
            "variants": variants,
            "dependencies": ["react", "@headlessui/react", "tailwindcss"],
            "responsive": True,
            "accessibility": {
                "aria_labels": True,
                "keyboard_navigation": True,
                "screen_reader_support": True
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        return component
    
    def save_component_to_batch(self, component: Dict, batch_file: str = "application_ui_batch.json"):
        """Save component to a batch file for later bulk import"""
        batch_path = Path(__file__).parent / batch_file
        
        # Load existing batch or create new one
        if batch_path.exists():
            with open(batch_path, 'r') as f:
                batch_data = json.load(f)
        else:
            batch_data = {
                "created_at": datetime.now().isoformat(),
                "total_components": 0,
                "components": []
            }
        
        # Add component to batch
        batch_data["components"].append(component)
        batch_data["total_components"] = len(batch_data["components"])
        batch_data["updated_at"] = datetime.now().isoformat()
        
        # Save batch file
        with open(batch_path, 'w') as f:
            json.dump(batch_data, f, indent=2)
        
        print(f"✅ Added '{component['name']}' to batch file")
        print(f"   Category: {component['category']}")
        if component['subcategory']:
            print(f"   Subcategory: {component['subcategory']}")
        print(f"   Total components in batch: {batch_data['total_components']}")
        print(f"   Tags: {', '.join(component['tags'])}")
        print()
    
    def bulk_import_batch(self, batch_file: str = "application_ui_batch.json"):
        """Import all components from batch file to Supabase"""
        batch_path = Path(__file__).parent / batch_file
        
        if not batch_path.exists():
            print(f"❌ Batch file '{batch_file}' not found")
            return
        
        with open(batch_path, 'r') as f:
            batch_data = json.load(f)
        
        components = batch_data["components"]
        
        if not components:
            print("❌ No components to import")
            return
        
        print(f"🚀 Importing {len(components)} components to Supabase...")
        
        try:
            # Bulk insert all components
            result = self.supabase.table('sections').insert(components).execute()
            
            if result.data:
                print(f"✅ Successfully imported {len(result.data)} components!")
                
                # Archive the batch file
                archive_name = f"imported_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{batch_file}"
                archive_path = Path(__file__).parent / "imported_batches" / archive_name
                archive_path.parent.mkdir(exist_ok=True)
                batch_path.rename(archive_path)
                
                print(f"📁 Batch file archived as: {archive_name}")
                
                # Print summary
                categories = {}
                for component in components:
                    cat = component['category']
                    categories[cat] = categories.get(cat, 0) + 1
                
                print("\n📊 Import Summary:")
                for category, count in categories.items():
                    print(f"   {category}: {count} components")
                
            else:
                print("❌ No data returned from insert operation")
                
        except Exception as e:
            print(f"❌ Error importing components: {e}")
    
    def show_taxonomy(self):
        """Display the taxonomy structure for reference"""
        print("📋 Tailwind UI Application Components Taxonomy:")
        print("=" * 60)
        
        for category, details in self.taxonomy['taxonomy'].items():
            print(f"\n🏷️  {category}")
            print(f"   {details['description']}")
            
            if 'subcategories' in details:
                for subcat in details['subcategories']:
                    print(f"   └── {subcat}")
            print()

def main():
    """Main function for interactive component entry"""
    importer = ApplicationUIImporter()
    
    print("🚀 Tailwind UI Application Components Importer")
    print("=" * 50)
    print()
    
    # Show taxonomy
    importer.show_taxonomy()
    
    print("\n💡 Usage Instructions:")
    print("1. Copy a component from tailwindui.com")
    print("2. Run this script and follow the prompts")
    print("3. When you have a batch ready, run bulk_import_batch()")
    print("4. Components will be imported to Supabase with proper metadata")
    print()
    
    print("📝 Example workflow:")
    print("   python bulk_import_application_ui.py")
    print("   [Follow prompts to add components]")
    print("   [When ready] Call: importer.bulk_import_batch()")
    print()

if __name__ == "__main__":
    main()