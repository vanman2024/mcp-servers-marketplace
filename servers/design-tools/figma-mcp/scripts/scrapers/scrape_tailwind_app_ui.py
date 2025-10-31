#!/usr/bin/env python3
"""
Tailwind UI Application UI Scraper
==================================
This scraper uses Puppeteer to extract Application UI components from Tailwind UI.
Requires authenticated session cookies from a paid Tailwind UI account.

IMPORTANT: This is for personal use only with a valid Tailwind UI license.
"""

import asyncio
import json
import os
from typing import List, Dict
from datetime import datetime

# Application UI sections we want to scrape
APP_UI_SECTIONS = {
    "application-shells": {
        "name": "Application Shells",
        "description": "Full application layouts with sidebars, headers, and content areas",
        "urls": [
            "https://tailwindui.com/components/application-ui/application-shells/stacked",
            "https://tailwindui.com/components/application-ui/application-shells/sidebar",
            "https://tailwindui.com/components/application-ui/application-shells/multi-column"
        ]
    },
    "data-display": {
        "name": "Data Display",
        "description": "Tables, lists, grids for displaying data",
        "urls": [
            "https://tailwindui.com/components/application-ui/data-display/description-lists",
            "https://tailwindui.com/components/application-ui/data-display/stats",
            "https://tailwindui.com/components/application-ui/data-display/calendars"
        ]
    },
    "forms": {
        "name": "Forms", 
        "description": "Form layouts and input groups for applications",
        "urls": [
            "https://tailwindui.com/components/application-ui/forms/form-layouts",
            "https://tailwindui.com/components/application-ui/forms/input-groups",
            "https://tailwindui.com/components/application-ui/forms/select-menus",
            "https://tailwindui.com/components/application-ui/forms/sign-in-forms",
            "https://tailwindui.com/components/application-ui/forms/textareas",
            "https://tailwindui.com/components/application-ui/forms/toggles",
            "https://tailwindui.com/components/application-ui/forms/action-panels"
        ]
    },
    "lists": {
        "name": "Lists",
        "description": "Various list layouts for applications",
        "urls": [
            "https://tailwindui.com/components/application-ui/lists/stacked-lists",
            "https://tailwindui.com/components/application-ui/lists/grid-lists",
            "https://tailwindui.com/components/application-ui/lists/feeds",
            "https://tailwindui.com/components/application-ui/lists/tables"
        ]
    },
    "navigation": {
        "name": "Navigation",
        "description": "Navigation patterns for applications",
        "urls": [
            "https://tailwindui.com/components/application-ui/navigation/navbars",
            "https://tailwindui.com/components/application-ui/navigation/pagination",
            "https://tailwindui.com/components/application-ui/navigation/tabs",
            "https://tailwindui.com/components/application-ui/navigation/vertical-navigation",
            "https://tailwindui.com/components/application-ui/navigation/sidebar-navigation",
            "https://tailwindui.com/components/application-ui/navigation/breadcrumbs",
            "https://tailwindui.com/components/application-ui/navigation/steps",
            "https://tailwindui.com/components/application-ui/navigation/command-palettes"
        ]
    },
    "overlays": {
        "name": "Overlays",
        "description": "Modals, slide-overs, and notifications",
        "urls": [
            "https://tailwindui.com/components/application-ui/overlays/dialogs",
            "https://tailwindui.com/components/application-ui/overlays/slide-overs",
            "https://tailwindui.com/components/application-ui/overlays/notifications"
        ]
    },
    "page-examples": {
        "name": "Page Examples",
        "description": "Complete page layouts for common app pages",
        "urls": [
            "https://tailwindui.com/components/application-ui/page-examples/home-screens",
            "https://tailwindui.com/components/application-ui/page-examples/detail-screens",
            "https://tailwindui.com/components/application-ui/page-examples/settings-screens"
        ]
    },
    "layout": {
        "name": "Layout",
        "description": "Layout patterns and containers",
        "urls": [
            "https://tailwindui.com/components/application-ui/layout/containers",
            "https://tailwindui.com/components/application-ui/layout/panels",
            "https://tailwindui.com/components/application-ui/layout/list-containers",
            "https://tailwindui.com/components/application-ui/layout/media-objects",
            "https://tailwindui.com/components/application-ui/layout/dividers"
        ]
    },
    "elements": {
        "name": "Elements",
        "description": "Small application UI elements",
        "urls": [
            "https://tailwindui.com/components/application-ui/elements/avatars",
            "https://tailwindui.com/components/application-ui/elements/badges",
            "https://tailwindui.com/components/application-ui/elements/buttons",
            "https://tailwindui.com/components/application-ui/elements/button-groups",
            "https://tailwindui.com/components/application-ui/elements/dropdowns"
        ]
    }
}

def create_puppeteer_script():
    """Create the Puppeteer script for scraping"""
    
    script = '''
// Puppeteer script to scrape Tailwind UI Application components
// Requires authentication cookies from paid account

const puppeteer = require('puppeteer');
const fs = require('fs').promises;

// IMPORTANT: Add your Tailwind UI cookies here
// You can get these from Chrome DevTools > Application > Cookies
const TAILWIND_COOKIES = [
    // {
    //     name: '_tailwindui_session',
    //     value: 'YOUR_SESSION_COOKIE_VALUE',
    //     domain: '.tailwindui.com'
    // },
    // Add other necessary cookies
];

async function scrapeTailwindUI() {
    const browser = await puppeteer.launch({
        headless: false, // Set to true in production
        defaultViewport: { width: 1920, height: 1080 }
    });
    
    const page = await browser.newPage();
    
    // Set cookies
    await page.setCookie(...TAILWIND_COOKIES);
    
    const results = [];
    const sections = ''' + json.dumps(APP_UI_SECTIONS, indent=4) + ''';
    
    for (const [categoryKey, category] of Object.entries(sections)) {
        console.log(`\\nScraping ${category.name}...`);
        
        for (const url of category.urls) {
            console.log(`  Visiting: ${url}`);
            
            try {
                await page.goto(url, { waitUntil: 'networkidle0' });
                await page.waitForTimeout(2000); // Wait for dynamic content
                
                // Get all component examples on the page
                const components = await page.evaluate(() => {
                    const componentBlocks = [];
                    
                    // Find all component preview blocks
                    const blocks = document.querySelectorAll('[class*="component-preview"]');
                    
                    blocks.forEach(block => {
                        // Look for the "Show code" button
                        const codeButton = block.querySelector('button:contains("Show code"), button:contains("View code")');
                        
                        if (codeButton) {
                            // Get component name from heading
                            const heading = block.querySelector('h3, h4') || 
                                          block.previousElementSibling?.querySelector('h3, h4');
                            const name = heading?.textContent?.trim() || 'Unnamed Component';
                            
                            // Get description if available
                            const desc = block.querySelector('p') || 
                                        block.previousElementSibling?.querySelector('p');
                            const description = desc?.textContent?.trim() || '';
                            
                            componentBlocks.push({
                                name,
                                description,
                                element: block
                            });
                        }
                    });
                    
                    return componentBlocks;
                });
                
                // Click each "Show code" button and extract the code
                for (const component of components) {
                    const codeButton = await page.$('button:contains("Show code")');
                    if (codeButton) {
                        await codeButton.click();
                        await page.waitForTimeout(500);
                        
                        // Extract the code
                        const code = await page.evaluate(() => {
                            const codeBlock = document.querySelector('pre code');
                            return codeBlock?.textContent || '';
                        });
                        
                        if (code) {
                            results.push({
                                category: categoryKey,
                                categoryName: category.name,
                                url: url,
                                name: component.name,
                                description: component.description,
                                code: code,
                                timestamp: new Date().toISOString()
                            });
                            
                            console.log(`    ✓ Extracted: ${component.name}`);
                        }
                    }
                }
                
            } catch (error) {
                console.error(`  ✗ Error scraping ${url}:`, error.message);
            }
        }
    }
    
    // Save results
    await fs.writeFile(
        'tailwind_app_ui_components.json',
        JSON.stringify(results, null, 2)
    );
    
    console.log(`\\nScraped ${results.length} Application UI components`);
    await browser.close();
}

// Run the scraper
scrapeTailwindUI().catch(console.error);
'''
    
    with open('tailwind_ui_scraper.js', 'w') as f:
        f.write(script)
    
    print("Created tailwind_ui_scraper.js")
    print("\nTo use this scraper:")
    print("1. Install puppeteer: npm install puppeteer")
    print("2. Get your Tailwind UI session cookies from Chrome DevTools")
    print("3. Add the cookies to the TAILWIND_COOKIES array in the script")
    print("4. Run: node tailwind_ui_scraper.js")
    print("\nThis will extract all Application UI components for building real applications!")

def create_cookie_extractor():
    """Create a helper script to extract cookies from Chrome"""
    
    script = '''
// Helper to extract Tailwind UI cookies from Chrome DevTools
// 1. Log into Tailwind UI in Chrome
// 2. Open DevTools (F12)
// 3. Go to Console tab
// 4. Paste and run this code:

console.log("=== Tailwind UI Cookies ===");
const cookies = document.cookie.split('; ').map(c => {
    const [name, value] = c.split('=');
    return { 
        name, 
        value: decodeURIComponent(value),
        domain: '.tailwindui.com'
    };
});

console.log(JSON.stringify(cookies, null, 2));
console.log("\\nCopy the above and paste into TAILWIND_COOKIES in the scraper script");
'''
    
    with open('get_tailwind_cookies.js', 'w') as f:
        f.write(script)
    
    print("\nAlso created get_tailwind_cookies.js to help extract cookies")

if __name__ == "__main__":
    create_puppeteer_script()
    create_cookie_extractor()
    
    print("\n" + "="*60)
    print("IMPORTANT: Application UI Components")
    print("="*60)
    print("These are the REAL application building blocks we need:")
    print("- Application shells with sidebars")
    print("- Data tables with sorting/filtering")  
    print("- Form layouts for real apps")
    print("- Dashboard components")
    print("- Settings pages")
    print("- And much more!")
    print("\nUnlike the marketing templates, these are for building actual applications.")