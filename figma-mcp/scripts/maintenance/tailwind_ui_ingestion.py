#!/usr/bin/env python3
"""
Tailwind UI Ingestion Script
============================
Parses downloaded Tailwind UI components and imports them into the Supabase database.

Expected directory structure:
- tailwind-ui/
  - marketing/
    - heroes/
      - simple-centered.tsx
      - with-app-screenshot.tsx
    - features/
      - grid-list.tsx
  - application-ui/
    - forms/
      - sign-in-forms/
        - simple.tsx
  - ecommerce/
    - components/
      - product-lists/
        - with-inline-price.tsx
"""

import os
import re
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import aiohttp
from dataclasses import dataclass, asdict

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://wsmhiiharnhqupdniwgw.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
TAILWIND_UI_PATH = os.getenv('TAILWIND_UI_PATH', './tailwind-ui')

@dataclass
class TailwindSection:
    """Represents a Tailwind UI section/component"""
    name: str
    description: str
    source: str = 'tailwind-ui'
    category: str = ''
    subcategory: str = ''
    original_path: str = ''
    code: str = ''
    preview_image_url: Optional[str] = None
    dependencies: List[str] = None
    component_list: List[str] = None
    responsive_variants: Dict = None
    accessibility_features: List[str] = None
    browser_support: List[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.component_list is None:
            self.component_list = []
        if self.responsive_variants is None:
            self.responsive_variants = {}
        if self.accessibility_features is None:
            self.accessibility_features = []
        if self.browser_support is None:
            self.browser_support = ['chrome', 'firefox', 'safari', 'edge']
        if self.tags is None:
            self.tags = []

class TailwindUIParser:
    """Parses Tailwind UI directory structure and extracts components"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.sections: List[TailwindSection] = []
        
    def parse_directory(self) -> List[TailwindSection]:
        """Walk directory tree and parse all component files"""
        print(f"Parsing Tailwind UI directory: {self.base_path}")
        
        for tsx_file in self.base_path.rglob("*.tsx"):
            section = self._parse_file(tsx_file)
            if section:
                self.sections.append(section)
                
        for jsx_file in self.base_path.rglob("*.jsx"):
            section = self._parse_file(jsx_file)
            if section:
                self.sections.append(section)
                
        for html_file in self.base_path.rglob("*.html"):
            section = self._parse_file(html_file)
            if section:
                self.sections.append(section)
                
        print(f"Found {len(self.sections)} sections")
        return self.sections
    
    def _parse_file(self, file_path: Path) -> Optional[TailwindSection]:
        """Parse individual component file"""
        try:
            relative_path = file_path.relative_to(self.base_path)
            path_parts = relative_path.parts
            
            # Extract category and subcategory from path
            category = path_parts[0] if len(path_parts) > 0 else "uncategorized"
            subcategory = path_parts[1] if len(path_parts) > 1 else ""
            
            # Generate name from filename
            name = self._generate_name(file_path.stem, category, subcategory)
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Extract metadata from code
            description = self._extract_description(code)
            dependencies = self._extract_dependencies(code)
            components = self._extract_components(code)
            tags = self._generate_tags(category, subcategory, name)
            accessibility = self._extract_accessibility_features(code)
            
            return TailwindSection(
                name=name,
                description=description,
                category=self._normalize_category(category),
                subcategory=subcategory,
                original_path=str(relative_path),
                code=code,
                dependencies=dependencies,
                component_list=components,
                tags=tags,
                accessibility_features=accessibility,
                responsive_variants=self._extract_responsive_variants(code)
            )
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
    
    def _generate_name(self, filename: str, category: str, subcategory: str) -> str:
        """Generate human-readable name from filename"""
        # Convert kebab-case to Title Case
        name = filename.replace('-', ' ').replace('_', ' ').title()
        
        # Add category context if not redundant
        if subcategory and subcategory.lower() not in name.lower():
            name = f"{subcategory.title()} - {name}"
            
        return name
    
    def _extract_description(self, code: str) -> str:
        """Extract description from code comments"""
        # Look for JSDoc style comments
        doc_match = re.search(r'/\*\*\s*\n\s*\*\s*(.+?)\n', code)
        if doc_match:
            return doc_match.group(1).strip()
        
        # Look for single line comments at top
        comment_match = re.search(r'^//\s*(.+?)$', code, re.MULTILINE)
        if comment_match:
            return comment_match.group(1).strip()
            
        return "Tailwind UI component"
    
    def _extract_dependencies(self, code: str) -> List[str]:
        """Extract npm dependencies from imports"""
        dependencies = []
        
        # Extract from import statements
        import_pattern = r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]"
        for match in re.finditer(import_pattern, code):
            dep = match.group(1)
            # Filter out relative imports and React
            if not dep.startswith('.') and dep not in ['react', 'react-dom']:
                dependencies.append(dep)
                
        # Extract from require statements
        require_pattern = r"require\(['\"]([^'\"]+)['\"]\)"
        for match in re.finditer(require_pattern, code):
            dep = match.group(1)
            if not dep.startswith('.') and dep not in ['react', 'react-dom']:
                dependencies.append(dep)
                
        return list(set(dependencies))
    
    def _extract_components(self, code: str) -> List[str]:
        """Extract list of components used"""
        components = []
        
        # Look for common UI component patterns
        component_patterns = [
            r'<(Button|Card|Input|Select|Modal|Dialog|Dropdown|Menu|Tab|Avatar|Badge|Icon|Form|Table|List|Grid|Flex|Box|Text|Heading|Link|Image|Video)',
            r'(Button|Card|Input|Select|Modal|Dialog|Dropdown|Menu|Tab|Avatar|Badge|Icon|Form|Table|List|Grid|Flex|Box|Text|Heading|Link|Image|Video)\.[\w]+',
        ]
        
        for pattern in component_patterns:
            for match in re.finditer(pattern, code):
                component = match.group(1)
                if component not in components:
                    components.append(component)
                    
        return components
    
    def _extract_accessibility_features(self, code: str) -> List[str]:
        """Extract accessibility features from code"""
        features = []
        
        # Check for ARIA attributes
        if re.search(r'aria-\w+', code):
            features.append('ARIA labels')
            
        # Check for role attributes
        if re.search(r'role=', code):
            features.append('ARIA roles')
            
        # Check for keyboard navigation
        if re.search(r'onKeyDown|onKeyPress|onKeyUp', code):
            features.append('Keyboard navigation')
            
        # Check for focus management
        if re.search(r'focus:|focus\(|tabIndex', code):
            features.append('Focus management')
            
        return features
    
    def _extract_responsive_variants(self, code: str) -> Dict:
        """Extract responsive breakpoint usage"""
        variants = {
            'mobile': False,
            'tablet': False,
            'desktop': False
        }
        
        # Check for Tailwind responsive prefixes
        if re.search(r'sm:', code):
            variants['mobile'] = True
        if re.search(r'md:|lg:', code):
            variants['tablet'] = True
        if re.search(r'xl:|2xl:', code):
            variants['desktop'] = True
            
        return variants
    
    def _normalize_category(self, category: str) -> str:
        """Normalize category names to match our schema"""
        category_map = {
            'marketing': 'marketing',
            'application-ui': 'application',
            'ecommerce': 'e-commerce',
            'e-commerce': 'e-commerce',
            'forms': 'forms',
            'navigation': 'navigation-layout',
            'layout': 'navigation-layout',
            'feedback': 'feedback',
            'overlays': 'overlays',
            'elements': 'elements',
            'data-display': 'content-display'
        }
        
        return category_map.get(category.lower(), category.lower())
    
    def _generate_tags(self, category: str, subcategory: str, name: str) -> List[str]:
        """Generate relevant tags for the section"""
        tags = [category.lower()]
        
        if subcategory:
            tags.append(subcategory.lower())
            
        # Add tags based on name
        name_lower = name.lower()
        if 'hero' in name_lower:
            tags.extend(['hero', 'header', 'landing'])
        if 'form' in name_lower:
            tags.extend(['form', 'input'])
        if 'nav' in name_lower:
            tags.extend(['navigation', 'menu'])
        if 'footer' in name_lower:
            tags.extend(['footer', 'links'])
        if 'card' in name_lower:
            tags.extend(['card', 'container'])
        if 'grid' in name_lower or 'list' in name_lower:
            tags.extend(['layout', 'grid'])
            
        # Add responsive tag
        tags.append('responsive')
        
        return list(set(tags))

class SupabaseIngester:
    """Handles insertion of parsed sections into Supabase"""
    
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key
        self.headers = {
            'apikey': key,
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }
        
    async def ingest_sections(self, sections: List[TailwindSection]):
        """Bulk insert sections into database"""
        async with aiohttp.ClientSession() as session:
            # Insert into section_templates table
            for batch in self._batch_sections(sections, batch_size=50):
                await self._insert_batch(session, batch)
                
    def _batch_sections(self, sections: List[TailwindSection], batch_size: int):
        """Split sections into batches"""
        for i in range(0, len(sections), batch_size):
            yield sections[i:i + batch_size]
            
    async def _insert_batch(self, session: aiohttp.ClientSession, batch: List[TailwindSection]):
        """Insert a batch of sections"""
        records = []
        for section in batch:
            record = {
                'name': section.name,
                'description': section.description,
                'source': section.source,
                'category': section.category,
                'subcategory': section.subcategory,
                'original_path': section.original_path,
                'code': section.code,
                'preview_image_url': section.preview_image_url,
                'dependencies': json.dumps(section.dependencies),
                'component_list': section.component_list,
                'responsive_variants': json.dumps(section.responsive_variants),
                'accessibility_features': section.accessibility_features,
                'browser_support': section.browser_support,
                'tags': section.tags
            }
            records.append(record)
            
        url = f"{self.url}/rest/v1/section_templates"
        
        try:
            async with session.post(url, json=records, headers=self.headers) as response:
                if response.status == 201:
                    print(f"Successfully inserted batch of {len(records)} sections")
                else:
                    error = await response.text()
                    print(f"Error inserting batch: {error}")
        except Exception as e:
            print(f"Exception during batch insert: {e}")

async def main():
    """Main ingestion workflow"""
    if not SUPABASE_KEY:
        print("Error: SUPABASE_SERVICE_KEY environment variable not set")
        return
        
    if not os.path.exists(TAILWIND_UI_PATH):
        print(f"Error: Tailwind UI directory not found at {TAILWIND_UI_PATH}")
        print("Please set TAILWIND_UI_PATH environment variable to the downloaded Tailwind UI directory")
        return
        
    # Parse Tailwind UI components
    parser = TailwindUIParser(TAILWIND_UI_PATH)
    sections = parser.parse_directory()
    
    if not sections:
        print("No sections found to import")
        return
        
    print(f"\nFound {len(sections)} sections to import:")
    
    # Show category breakdown
    categories = {}
    for section in sections:
        if section.category not in categories:
            categories[section.category] = 0
        categories[section.category] += 1
        
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count} sections")
        
    # Confirm before proceeding
    response = input("\nProceed with import? (y/n): ")
    if response.lower() != 'y':
        print("Import cancelled")
        return
        
    # Import to Supabase
    ingester = SupabaseIngester(SUPABASE_URL, SUPABASE_KEY)
    await ingester.ingest_sections(sections)
    
    print("\nImport complete!")

if __name__ == "__main__":
    asyncio.run(main())