#!/usr/bin/env python3
"""
Simple test to check if cookies work
"""

import requests
from tailwind_cookies import TAILWIND_COOKIES

# Convert cookies to requests format
cookies = {}
for cookie in TAILWIND_COOKIES:
    cookies[cookie['name']] = cookie['value']

# Test authentication
url = "https://tailwindui.com/plus/ui-blocks/application-ui"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(url, cookies=cookies, headers=headers)

print(f"Status: {response.status_code}")
print(f"Response length: {len(response.text)}")

# Check if we're authenticated
if "Sign in" in response.text:
    print("✗ Not authenticated - cookies may be expired")
else:
    print("✓ Authenticated!")
    
# Save response for debugging
with open('test_response.html', 'w', encoding='utf-8') as f:
    f.write(response.text)