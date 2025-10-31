#!/usr/bin/env python3
"""
Interactive Component Paste Helper
==================================
Helper script for quickly adding components when copy/pasting from Tailwind UI
"""

import json
import os
from pathlib import Path
from bulk_import_application_ui import ApplicationUIImporter

def interactive_component_entry():
    """Interactive component entry with prompts"""
    
    importer = ApplicationUIImporter()
    
    print("🎯 Quick Component Entry")
    print("=" * 30)
    
    # Show available categories
    print("\n📂 Available Categories:")
    categories = list(importer.taxonomy['taxonomy'].keys())
    for i, cat in enumerate(categories, 1):
        print(f"{i:2d}. {cat}")
    
    # Get category
    while True:
        try:
            cat_choice = int(input(f"\nSelect category (1-{len(categories)}): "))
            if 1 <= cat_choice <= len(categories):
                category = categories[cat_choice - 1]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")
    
    # Get subcategory if available
    subcategory = None
    category_info = importer.taxonomy['taxonomy'][category]
    if 'subcategories' in category_info:
        subcategories = list(category_info['subcategories'].keys())
        print(f"\n📁 Available Subcategories for {category}:")
        for i, subcat in enumerate(subcategories, 1):
            print(f"{i:2d}. {subcat}")
        
        while True:
            try:
                subcat_choice = int(input(f"\nSelect subcategory (1-{len(subcategories)}): "))
                if 1 <= subcat_choice <= len(subcategories):
                    subcategory = subcategories[subcat_choice - 1]
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
    
    # Get component details
    print(f"\n📝 Component Details:")
    name = input("Component name: ").strip()
    description = input("Description (optional): ").strip()
    
    print(f"\n🏷️  Tags (comma-separated, optional): ")
    tags_input = input("Tags: ").strip()
    tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
    
    print(f"\n🧩 Components used (comma-separated, optional): ")
    components_input = input("Components: ").strip()
    components_used = [comp.strip() for comp in components_input.split(',') if comp.strip()]
    
    print(f"\n💻 Paste your TSX/JSX code below (press Enter, then Ctrl+D when done):")
    code_lines = []
    try:
        while True:
            line = input()
            code_lines.append(line)
    except EOFError:
        pass
    
    code = '\n'.join(code_lines)
    
    # Create component entry
    component = importer.create_component_entry(
        name=name,
        category=category,
        subcategory=subcategory,
        code=code,
        description=description,
        tags=tags,
        components_used=components_used
    )
    
    # Save to batch
    importer.save_component_to_batch(component)
    
    # Ask if user wants to continue
    continue_choice = input("\n❓ Add another component? (y/n): ").strip().lower()
    if continue_choice == 'y':
        interactive_component_entry()
    else:
        print("\n🎉 Done! Use bulk_import_batch() to import all components when ready.")
        
        # Show current batch status
        batch_path = Path(__file__).parent / "application_ui_batch.json"
        if batch_path.exists():
            with open(batch_path, 'r') as f:
                batch_data = json.load(f)
            print(f"📦 Current batch contains {batch_data['total_components']} components")

def quick_import_batch():
    """Quick function to import current batch"""
    importer = ApplicationUIImporter()
    importer.bulk_import_batch()

if __name__ == "__main__":
    interactive_component_entry()