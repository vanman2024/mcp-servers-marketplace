#!/usr/bin/env python3
"""
System for manually importing Tailwind UI Application components
with proper metadata and organization
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Create directories for organized storage
IMPORT_DIR = Path("manual_imports")
IMPORT_DIR.mkdir(exist_ok=True)

# Application UI Categories (from Tailwind UI structure)
APP_UI_CATEGORIES = {
    "application-shells": ["stacked", "sidebar", "multi-column"],
    "headings": ["page-headings", "card-headings", "section-headings"],
    "data-display": ["description-lists", "stats", "calendars"],
    "lists": ["stacked-lists", "tables", "grid-lists", "feeds"],
    "forms": ["form-layouts", "input-groups", "select-menus", "sign-in-forms", "textareas", "radio-groups", "checkboxes", "toggles", "action-panels", "comboboxes"],
    "feedback": ["alerts", "empty-states"],
    "navigation": ["navbars", "pagination", "tabs", "vertical-navigation", "sidebar-navigation", "breadcrumbs", "progress-bars", "command-palettes"],
    "overlays": ["modal-dialogs", "drawers", "notifications"],
    "elements": ["avatars", "badges", "dropdowns", "buttons", "button-groups"],
    "layout": ["containers", "cards", "list-containers", "media-objects", "dividers"],
    "page-examples": ["home-screens", "detail-screens", "settings-screens"]
}

def create_component_template(
    name: str,
    category: str,
    subcategory: str,
    component_code: str,
    variant_info: dict = None
):
    """
    Create a standardized component entry with rich metadata
    
    Args:
        name: Component name (e.g., "Simple form layout with labels on top")
        category: Main category (e.g., "forms")
        subcategory: Subcategory (e.g., "form-layouts")
        component_code: The actual React/JSX code
        variant_info: Info about dark mode, responsive variants, etc.
    """
    
    return {
        "id": f"app-ui-{category}-{subcategory}-{name.lower().replace(' ', '-')}",
        "name": f"App UI - {category.title()} - {subcategory.replace('-', ' ').title()} - {name}",
        "description": f"Application UI {subcategory.replace('-', ' ')} component from Tailwind UI",
        "category": category,
        "subcategory": subcategory,
        "app_type": "application",
        "block_type": f"app_{category}_{subcategory.replace('-', '_')}",
        "react_template": component_code,
        "tags": [
            "application-ui",
            "tailwind-ui",
            category,
            subcategory,
            "production-ready",
            "responsive"
        ],
        "metadata": {
            "source": "tailwind-ui-manual",
            "imported_at": datetime.now().isoformat(),
            "component_name": name,
            "variants": variant_info or {
                "has_dark_mode": False,
                "has_mobile_responsive": True,
                "has_typescript": True,
                "has_javascript": True
            },
            "dependencies": ["tailwindcss", "react"],
            "usage_notes": f"Use this {subcategory.replace('-', ' ')} component for {category} in your application"
        },
        "search_keywords": [
            name.lower(),
            category,
            subcategory,
            "application",
            "ui",
            "tailwind"
        ]
    }

def save_component_batch(components: list, batch_name: str):
    """Save a batch of components to JSON file"""
    
    filename = IMPORT_DIR / f"{batch_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w') as f:
        json.dump({
            "batch_name": batch_name,
            "total_components": len(components),
            "categories": list(set(c["category"] for c in components)),
            "imported_at": datetime.now().isoformat(),
            "components": components
        }, f, indent=2)
    
    print(f"✓ Saved {len(components)} components to {filename}")
    return filename

# Example usage template
example_component = create_component_template(
    name="Stacked form layout",
    category="forms",
    subcategory="form-layouts",
    component_code='''export default function Example() {
  return (
    <form className="space-y-6">
      <!-- Component code here -->
    </form>
  )
}''',
    variant_info={
        "has_dark_mode": True,
        "has_mobile_responsive": True,
        "has_typescript": True,
        "has_javascript": True
    }
)

print("Manual Import System Ready!")
print("\nCategories available:")
for category, subcategories in APP_UI_CATEGORIES.items():
    print(f"\n{category}:")
    for sub in subcategories:
        print(f"  - {sub}")

print("\n\nExample component structure:")
print(json.dumps(example_component, indent=2))

print("\n\nTo use this system:")
print("1. Copy component code from Tailwind UI")
print("2. Create component using create_component_template()")
print("3. Add to a list and save with save_component_batch()")
print("\nThe metadata will help with:")
print("- Clear identification of what each component is for")
print("- Easy searching and filtering")
print("- Proper categorization in the database")
print("- Usage documentation")