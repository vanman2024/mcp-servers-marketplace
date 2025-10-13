#!/usr/bin/env python3
"""
Test Puppeteer authentication with Tailwind UI
"""

import asyncio
from playwright.async_api import async_playwright
from tailwind_cookies import TAILWIND_COOKIES

async def test_auth():
    """Test if we can authenticate with Tailwind UI"""
    
    async with async_playwright() as p:
        # Launch browser in non-headless mode to see what's happening
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        
        # Add cookies to context
        print("Adding cookies to browser context...")
        await context.add_cookies(TAILWIND_COOKIES)
        
        page = await context.new_page()
        
        # Try to visit the main plus page
        print("Navigating to Tailwind UI Plus...")
        await page.goto("https://tailwindui.com/plus", wait_until='domcontentloaded')
        
        # Wait a bit for the page to load
        await page.wait_for_timeout(3000)
        
        # Check if we're authenticated by looking for auth-specific elements
        print("\nChecking authentication status...")
        
        # Check for user menu or sign out button (typical indicators of being logged in)
        auth_indicators = [
            'text="Sign out"',
            'text="Account"',
            'text="My account"',
            'text="Dashboard"',
            '[data-auth="true"]'
        ]
        
        authenticated = False
        for indicator in auth_indicators:
            try:
                await page.wait_for_selector(indicator, timeout=1000)
                print(f"✓ Found auth indicator: {indicator}")
                authenticated = True
                break
            except:
                continue
        
        if not authenticated:
            print("✗ No authentication indicators found")
            
            # Check if we see "Sign in" button instead
            try:
                await page.wait_for_selector('text="Sign in"', timeout=1000)
                print("✗ Found 'Sign in' button - not authenticated")
            except:
                pass
        
        # Try to navigate to a protected page
        print("\nTrying to access Application UI components...")
        await page.goto("https://tailwindui.com/plus/ui-blocks/application-ui/forms/form-layouts", wait_until='domcontentloaded')
        await page.wait_for_timeout(3000)
        
        # Check if we can see component code
        try:
            # Look for code blocks which would only be visible when authenticated
            code_blocks = await page.query_selector_all('pre code')
            if code_blocks:
                print(f"✓ Found {len(code_blocks)} code blocks - likely authenticated!")
                
                # Try to get a sample of the code
                first_code = await code_blocks[0].inner_text() if code_blocks else ""
                if "export" in first_code or "function" in first_code:
                    print("✓ Code blocks contain actual component code!")
                    authenticated = True
            else:
                print("✗ No code blocks found")
        except Exception as e:
            print(f"Error checking for code blocks: {e}")
        
        # Take a screenshot for debugging
        await page.screenshot(path='auth_test_screenshot.png')
        print("\nScreenshot saved as auth_test_screenshot.png")
        
        # Keep browser open for manual inspection
        if not authenticated:
            print("\n⚠️  Authentication appears to have failed.")
            print("Browser will stay open for 30 seconds for manual inspection...")
            await page.wait_for_timeout(30000)
        
        await browser.close()
        
        return authenticated

if __name__ == "__main__":
    result = asyncio.run(test_auth())
    if result:
        print("\n✅ Authentication successful! Ready to scrape.")
    else:
        print("\n❌ Authentication failed. Please check cookies.")