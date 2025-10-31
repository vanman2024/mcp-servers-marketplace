#!/usr/bin/env python3
"""
Scrape Tailwind UI Application UI components using authenticated session
"""

import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright
from tailwind_cookies import TAILWIND_COOKIES

# Application UI sections to scrape
APP_UI_SECTIONS = {
    "application-shells": [
        "https://tailwindui.com/plus/ui-blocks/application-ui/application-shells/stacked",
        "https://tailwindui.com/plus/ui-blocks/application-ui/application-shells/sidebar", 
        "https://tailwindui.com/plus/ui-blocks/application-ui/application-shells/multi-column"
    ],
    "headings": [
        "https://tailwindui.com/plus/ui-blocks/application-ui/headings/page-headings",
        "https://tailwindui.com/plus/ui-blocks/application-ui/headings/card-headings",
        "https://tailwindui.com/plus/ui-blocks/application-ui/headings/section-headings"
    ],
    "data-display": [
        "https://tailwindui.com/plus/ui-blocks/application-ui/data-display/description-lists",
        "https://tailwindui.com/plus/ui-blocks/application-ui/data-display/stats",
        "https://tailwindui.com/plus/ui-blocks/application-ui/data-display/calendars"
    ],
    "lists": [
        "https://tailwindui.com/plus/ui-blocks/application-ui/lists/tables",
        "https://tailwindui.com/plus/ui-blocks/application-ui/lists/grid-lists", 
        "https://tailwindui.com/plus/ui-blocks/application-ui/lists/feeds",
        "https://tailwindui.com/plus/ui-blocks/application-ui/lists/stacked-lists"
    ],
    "forms": [
        "https://tailwindui.com/plus/ui-blocks/application-ui/forms/form-layouts",
        "https://tailwindui.com/plus/ui-blocks/application-ui/forms/input-groups",
        "https://tailwindui.com/plus/ui-blocks/application-ui/forms/select-menus",
        "https://tailwindui.com/plus/ui-blocks/application-ui/forms/sign-in-forms",
        "https://tailwindui.com/plus/ui-blocks/application-ui/forms/textareas",
        "https://tailwindui.com/plus/ui-blocks/application-ui/forms/toggles",
        "https://tailwindui.com/plus/ui-blocks/application-ui/forms/action-panels",
        "https://tailwindui.com/plus/ui-blocks/application-ui/forms/radio-groups",
        "https://tailwindui.com/plus/ui-blocks/application-ui/forms/checkboxes",
        "https://tailwindui.com/plus/ui-blocks/application-ui/forms/comboboxes"
    ],
    "feedback": [
        "https://tailwindui.com/plus/ui-blocks/application-ui/feedback/alerts",
        "https://tailwindui.com/plus/ui-blocks/application-ui/feedback/empty-states"
    ],
    "navigation": [
        "https://tailwindui.com/plus/ui-blocks/application-ui/navigation/navbars",
        "https://tailwindui.com/plus/ui-blocks/application-ui/navigation/pagination",
        "https://tailwindui.com/plus/ui-blocks/application-ui/navigation/tabs",
        "https://tailwindui.com/plus/ui-blocks/application-ui/navigation/vertical-navigation",
        "https://tailwindui.com/plus/ui-blocks/application-ui/navigation/sidebar-navigation",
        "https://tailwindui.com/plus/ui-blocks/application-ui/navigation/breadcrumbs",
        "https://tailwindui.com/plus/ui-blocks/application-ui/navigation/steps",
        "https://tailwindui.com/plus/ui-blocks/application-ui/navigation/command-palettes"
    ],
    "overlays": [
        "https://tailwindui.com/plus/ui-blocks/application-ui/overlays/dialogs",
        "https://tailwindui.com/plus/ui-blocks/application-ui/overlays/slide-overs",
        "https://tailwindui.com/plus/ui-blocks/application-ui/overlays/notifications"
    ],
    "elements": [
        "https://tailwindui.com/plus/ui-blocks/application-ui/elements/avatars",
        "https://tailwindui.com/plus/ui-blocks/application-ui/elements/badges",
        "https://tailwindui.com/plus/ui-blocks/application-ui/elements/buttons",
        "https://tailwindui.com/plus/ui-blocks/application-ui/elements/button-groups",
        "https://tailwindui.com/plus/ui-blocks/application-ui/elements/dropdowns"
    ],
    "layout": [
        "https://tailwindui.com/plus/ui-blocks/application-ui/layout/containers",
        "https://tailwindui.com/plus/ui-blocks/application-ui/layout/panels",
        "https://tailwindui.com/plus/ui-blocks/application-ui/layout/list-containers",
        "https://tailwindui.com/plus/ui-blocks/application-ui/layout/media-objects",
        "https://tailwindui.com/plus/ui-blocks/application-ui/layout/dividers"
    ]
}

async def scrape_tailwind_app_ui():
    """Scrape Application UI components with authentication"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set to True for production
        context = await browser.new_context()
        
        # Add cookies to context
        await context.add_cookies(TAILWIND_COOKIES)
        
        page = await context.new_page()
        
        # Test authentication by visiting a protected page
        print("Testing authentication...")
        await page.goto("https://tailwindui.com/plus")
        await page.wait_for_timeout(2000)
        
        # Check if we're logged in
        try:
            await page.wait_for_selector('text="Application UI"', timeout=5000)
            print("✓ Authentication successful!")
        except:
            print("✗ Authentication failed! Please update cookies.")
            await browser.close()
            return
        
        all_components = []
        
        # Scrape each section
        for section_key, urls in APP_UI_SECTIONS.items():
            print(f"\nScraping {section_key}...")
            
            for url in urls:
                print(f"  Visiting: {url}")
                await page.goto(url, wait_until='networkidle')
                await page.wait_for_timeout(2000)
                
                # Extract component code blocks
                # Tailwind UI uses specific selectors for code blocks
                components = await page.evaluate('''
                    () => {
                        const components = [];
                        
                        // Find all component containers
                        const componentContainers = document.querySelectorAll('[data-headlessui-state]');
                        
                        componentContainers.forEach(container => {
                            // Look for React/JSX code blocks
                            const codeBlocks = container.querySelectorAll('pre code');
                            const title = container.querySelector('h3')?.textContent || 'Untitled';
                            
                            codeBlocks.forEach(code => {
                                if (code.textContent.includes('export') || code.textContent.includes('function')) {
                                    components.push({
                                        title: title,
                                        code: code.textContent,
                                        section: window.location.pathname
                                    });
                                }
                            });
                        });
                        
                        return components;
                    }
                ''')
                
                # Add section metadata
                for component in components:
                    component['category'] = section_key
                    component['url'] = url
                    all_components.append(component)
                
                print(f"    Found {len(components)} components")
                
                # Be respectful - don't hammer the server
                await page.wait_for_timeout(1000)
        
        await browser.close()
        
        # Save scraped components
        output_dir = Path('scraped_app_ui')
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / 'app_ui_components.json', 'w') as f:
            json.dump({
                'total': len(all_components),
                'components': all_components
            }, f, indent=2)
        
        print(f"\n✓ Scraped {len(all_components)} Application UI components!")
        print(f"  Saved to: {output_dir / 'app_ui_components.json'}")
        
        # Generate import script
        generate_import_script(all_components)

def generate_import_script(components):
    """Generate SQL import script for scraped components"""
    
    print("\nGenerating import script...")
    
    sections_to_import = []
    
    for comp in components:
        section = {
            'name': f"App UI - {comp['category'].title()} - {comp['title']}",
            'description': f"Application UI component from Tailwind UI. Category: {comp['category']}",
            'block_type': comp['category'].replace('-', '_'),
            'app_type': 'application',
            'react_template': comp['code'],
            'category': 'application-ui',
            'source': 'tailwind-ui-scraped',
            'tags': ['application', 'ui', 'tailwind-ui', comp['category'], 'app-component'],
            'is_template': True,
            'published': True,
            'metadata': {
                'url': comp['url'],
                'section': comp['section'],
                'title': comp['title']
            }
        }
        sections_to_import.append(section)
    
    # Save for bulk import
    with open('app_ui_sections_to_import.json', 'w') as f:
        json.dump({
            'sections': sections_to_import
        }, f, indent=2)
    
    print(f"✓ Generated import data for {len(sections_to_import)} components")

if __name__ == "__main__":
    asyncio.run(scrape_tailwind_app_ui())