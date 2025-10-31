#!/usr/bin/env python3
"""
Unzip all Tailwind UI template files
"""

import os
import zipfile
from pathlib import Path

# Update these paths as needed
DOWNLOADS_DIR = "/mnt/c/Users/angel/Downloads"
EXTRACT_TO = "/mnt/c/Users/angel/Downloads/tailwind-templates"

def unzip_all_templates():
    """Find and unzip all Tailwind UI template zip files"""
    
    # Create extraction directory
    os.makedirs(EXTRACT_TO, exist_ok=True)
    
    # Find all zip files that look like Tailwind templates
    template_patterns = [
        'catalyst', 'keynote', 'primer', 'transmit', 'spotlight',
        'protocol', 'syntax', 'commerce', 'commit', 'salient'
    ]
    
    downloads_path = Path(DOWNLOADS_DIR)
    zip_files = list(downloads_path.glob("*.zip"))
    
    print(f"Found {len(zip_files)} zip files in downloads")
    
    extracted_count = 0
    
    for zip_path in zip_files:
        # Check if it might be a Tailwind template
        if any(pattern in zip_path.name.lower() for pattern in template_patterns):
            print(f"\nExtracting: {zip_path.name}")
            
            # Create subdirectory for this template
            template_name = zip_path.stem
            extract_path = Path(EXTRACT_TO) / template_name
            
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                print(f"  ✓ Extracted to: {extract_path}")
                extracted_count += 1
            except Exception as e:
                print(f"  ✗ Error: {e}")
    
    print(f"\nExtracted {extracted_count} templates to {EXTRACT_TO}")
    print("\nNext: Run extract_tailwind_templates.py to parse the sections")

if __name__ == "__main__":
    unzip_all_templates()