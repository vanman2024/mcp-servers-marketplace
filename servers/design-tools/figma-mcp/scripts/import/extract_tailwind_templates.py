#!/usr/bin/env python3
"""
Tailwind UI Template Extractor
==============================
Extracts individual sections/components from Tailwind UI templates
and prepares them for import into the sections database.

This maintains clear separation:
- Sections (full page blocks) → sections table
- Individual components → figma_components table
"""

import os
import re
import json
import ast
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import asyncio

@dataclass
class ExtractedSection:
    """Represents an extracted section from a template"""
    name: str
    description: str
    category: str
    source: str = 'tailwind-ui-template'
    template_name: str = ''
    file_path: str = ''
    code: str = ''
    component_type: str = ''  # hero, features, pricing, etc.
    dependencies: List[str] = None
    uses_components: List[str] = None  # ShadCN/Catalyst components used
    props: Dict = None
    is_page: bool = False
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.uses_components is None:
            self.uses_components = []
        if self.props is None:
            self.props = {}

class TailwindTemplateExtractor:
    """Extracts sections from Tailwind UI templates"""
    
    # Common section patterns in Tailwind UI templates
    SECTION_PATTERNS = {
        'hero': ['hero', 'header', 'landing', 'banner'],
        'features': ['features', 'benefits', 'services'],
        'pricing': ['pricing', 'plans', 'tiers'],
        'testimonials': ['testimonials', 'reviews', 'quotes'],
        'cta': ['cta', 'call-to-action', 'contact'],
        'footer': ['footer'],
        'navigation': ['nav', 'navbar', 'header'],
        'stats': ['stats', 'numbers', 'metrics'],
        'team': ['team', 'about', 'people'],
        'faq': ['faq', 'questions'],
        'blog': ['blog', 'posts', 'articles'],
        'portfolio': ['portfolio', 'projects', 'work'],
        'forms': ['form', 'contact', 'subscribe', 'newsletter'],
        'ecommerce': ['product', 'cart', 'checkout', 'shop'],
        'dashboard': ['dashboard', 'analytics', 'admin'],
        'auth': ['login', 'register', 'signin', 'signup', 'auth'],
        'settings': ['settings', 'profile', 'account'],
        'empty': ['empty', 'no-data', 'placeholder'],
        'error': ['error', '404', '500'],
    }
    
    def __init__(self, templates_dir: str):
        self.templates_dir = Path(templates_dir)
        self.sections: List[ExtractedSection] = []
        
    def extract_all_templates(self) -> List[ExtractedSection]:
        """Extract sections from all templates in directory"""
        print(f"Scanning templates directory: {self.templates_dir}")
        
        # Find all template directories
        template_dirs = [d for d in self.templates_dir.iterdir() if d.is_dir()]
        
        for template_dir in template_dirs:
            template_name = template_dir.name
            print(f"\nProcessing template: {template_name}")
            self._extract_from_template(template_dir, template_name)
            
        print(f"\nTotal sections extracted: {len(self.sections)}")
        return self.sections
    
    def _extract_from_template(self, template_dir: Path, template_name: str):
        """Extract sections from a single template"""
        
        # Tailwind Plus templates have -js and -ts versions
        js_dir = template_dir / f"{template_name.replace('tailwind-plus-', '')}-js"
        ts_dir = template_dir / f"{template_name.replace('tailwind-plus-', '')}-ts"
        
        # Common locations for components in Tailwind Plus templates
        search_paths = [
            'src/components',
            'components',
            'src/pages',
            'pages',
            'src/app',
            'app',
            'src/sections',
            'sections',
            'src/views',
            'views',
        ]
        
        # Check both JS and TS versions
        for base_dir in [js_dir, ts_dir]:
            if base_dir.exists():
                for search_path in search_paths:
                    component_path = base_dir / search_path
                    if component_path.exists():
                        self._scan_directory(component_path, template_name)
    
    def _scan_directory(self, directory: Path, template_name: str):
        """Recursively scan directory for components"""
        
        for file_path in directory.rglob('*'):
            if file_path.suffix in ['.jsx', '.tsx', '.js', '.ts']:
                # Skip test files, stories, and configs
                if any(skip in str(file_path) for skip in ['test', 'spec', 'story', 'config', 'setup']):
                    continue
                    
                self._extract_from_file(file_path, template_name)
    
    def _extract_from_file(self, file_path: Path, template_name: str):
        """Extract section from a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if too small or likely a utility file
            if len(content) < 200:
                return
                
            # Determine section type
            section_type = self._identify_section_type(file_path, content)
            if not section_type:
                return
                
            # Extract component info
            name = self._generate_section_name(file_path, section_type, template_name)
            description = self._extract_description(content)
            dependencies = self._extract_dependencies(content)
            uses_components = self._identify_used_components(content)
            is_page = self._is_full_page(file_path, content)
            
            section = ExtractedSection(
                name=name,
                description=description,
                category=self._map_section_to_category(section_type),
                template_name=template_name,
                file_path=str(file_path.relative_to(self.templates_dir)),
                code=content,
                component_type=section_type,
                dependencies=dependencies,
                uses_components=uses_components,
                is_page=is_page
            )
            
            self.sections.append(section)
            print(f"  ✓ Extracted: {name} ({section_type})")
            
        except Exception as e:
            print(f"  ✗ Error processing {file_path}: {e}")
    
    def _identify_section_type(self, file_path: Path, content: str) -> Optional[str]:
        """Identify what type of section this is"""
        
        # Check filename and path
        path_str = str(file_path).lower()
        
        for section_type, patterns in self.SECTION_PATTERNS.items():
            if any(pattern in path_str for pattern in patterns):
                return section_type
        
        # Check content for common patterns
        content_lower = content.lower()
        for section_type, patterns in self.SECTION_PATTERNS.items():
            if any(f'"{pattern}' in content_lower or f"'{pattern}" in content_lower 
                   for pattern in patterns):
                return section_type
                
        # Check for specific class names or IDs
        if re.search(r'(className|class)=["\']\w*hero\w*["\']', content, re.I):
            return 'hero'
        if re.search(r'(className|class)=["\']\w*pricing\w*["\']', content, re.I):
            return 'pricing'
            
        return None
    
    def _generate_section_name(self, file_path: Path, section_type: str, template_name: str) -> str:
        """Generate a descriptive name for the section"""
        
        # Get filename without extension
        filename = file_path.stem
        
        # Clean up common patterns
        filename = filename.replace('-', ' ').replace('_', ' ')
        filename = re.sub(r'\b(component|section|page)\b', '', filename, flags=re.I)
        filename = filename.strip().title()
        
        # Add section type if not already in name
        if section_type not in filename.lower():
            filename = f"{section_type.title()} - {filename}"
            
        # Add template attribution
        return f"{filename} ({template_name})"
    
    def _extract_description(self, content: str) -> str:
        """Extract description from JSDoc or comments"""
        
        # Look for JSDoc comments
        doc_match = re.search(r'/\*\*\s*\n\s*\*\s*(.+?)\n', content)
        if doc_match:
            return doc_match.group(1).strip()
        
        # Look for single line comments at top
        comment_match = re.search(r'^//\s*(.+?)$', content, re.MULTILINE)
        if comment_match:
            desc = comment_match.group(1).strip()
            if len(desc) > 10 and len(desc) < 200:  # Reasonable description length
                return desc
                
        return f"Section extracted from {self.templates_dir.name} template"
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract npm dependencies from imports"""
        dependencies = []
        
        # Match import statements
        import_pattern = r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]"
        for match in re.finditer(import_pattern, content):
            dep = match.group(1)
            # Filter out relative imports and common React imports
            if not dep.startswith('.') and not dep.startswith('@/') and dep not in ['react', 'react-dom', 'next']:
                dependencies.append(dep)
                
        return list(set(dependencies))
    
    def _identify_used_components(self, content: str) -> List[str]:
        """Identify which base components are used (for mapping to ShadCN)"""
        components = []
        
        # Common component patterns
        component_patterns = [
            r'<(Button|Card|Input|Select|Dialog|Modal|Badge|Avatar|Table|Form|Grid|Flex)\b',
            r'(Button|Card|Input|Select|Dialog|Modal|Badge|Avatar|Table|Form|Grid|Flex)\.',
        ]
        
        for pattern in component_patterns:
            for match in re.finditer(pattern, content):
                component = match.group(1)
                if component not in components:
                    components.append(component)
                    
        return components
    
    def _is_full_page(self, file_path: Path, content: str) -> bool:
        """Determine if this is a full page vs a section"""
        
        # Check if in pages directory
        if 'pages' in str(file_path) or 'app' in str(file_path):
            return True
            
        # Check for page-like exports
        if 'getServerSideProps' in content or 'getStaticProps' in content:
            return True
            
        # Check for layout components
        if re.search(r'<(html|Html|body|Body|main|Main)\b', content):
            return True
            
        return False
    
    def _map_section_to_category(self, section_type: str) -> str:
        """Map section type to our database categories"""
        
        category_map = {
            'hero': 'marketing',
            'features': 'marketing',
            'pricing': 'marketing',
            'testimonials': 'marketing',
            'cta': 'marketing',
            'footer': 'navigation-layout',
            'navigation': 'navigation-layout',
            'stats': 'analytics',
            'team': 'marketing',
            'faq': 'marketing',
            'blog': 'content-display',
            'portfolio': 'content-display',
            'forms': 'forms',
            'ecommerce': 'e-commerce',
            'dashboard': 'analytics',
            'auth': 'forms',
            'settings': 'forms',
            'empty': 'utility',
            'error': 'utility',
        }
        
        return category_map.get(section_type, 'general')
    
    def save_extracted_sections(self, output_file: str = 'extracted_sections.json'):
        """Save extracted sections to JSON file"""
        
        output_data = {
            'total_sections': len(self.sections),
            'templates_processed': len(set(s.template_name for s in self.sections)),
            'sections': [asdict(s) for s in self.sections]
        }
        
        # Group by template for summary
        by_template = {}
        for section in self.sections:
            if section.template_name not in by_template:
                by_template[section.template_name] = []
            by_template[section.template_name].append(section.name)
        
        output_data['summary'] = by_template
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
            
        print(f"\nSaved extracted sections to {output_file}")
        
        # Print summary
        print("\nExtraction Summary:")
        for template, sections in by_template.items():
            print(f"  {template}: {len(sections)} sections")

def main():
    """Main extraction workflow"""
    
    # Set the templates directory
    # Update this path to where you extract the templates
    templates_dir = "/mnt/c/Users/angel/Downloads/Tailwind_Templates"
    
    if not os.path.exists(templates_dir):
        print(f"Templates directory not found: {templates_dir}")
        print("Please update the path to where you extract the Tailwind UI templates")
        return
    
    # Extract sections
    extractor = TailwindTemplateExtractor(templates_dir)
    sections = extractor.extract_all_templates()
    
    # Save results
    extractor.save_extracted_sections()
    
    print("\nNext steps:")
    print("1. Review extracted_sections.json")
    print("2. Run import script to add to database")
    print("3. Map base components to ShadCN equivalents")

if __name__ == "__main__":
    main()