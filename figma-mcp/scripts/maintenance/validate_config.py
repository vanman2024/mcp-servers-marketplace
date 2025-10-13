#!/usr/bin/env python3
"""
Figma MCP Server Configuration Validator

This script validates your environment configuration before starting the server.
It checks API keys, tests connections, and provides detailed feedback.

Usage:
    python validate_config.py
"""

import os
import sys
import asyncio
import aiohttp
from typing import Dict, Any, Tuple
from datetime import datetime

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_header(text: str):
    """Print a section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_info(text: str):
    """Print info message"""
    print(f"  {text}")

async def validate_figma_token(token: str) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validate Figma token by making an API call
    
    Returns:
        Tuple of (is_valid, error_message, user_info)
    """
    headers = {
        "X-FIGMA-TOKEN": token
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.figma.com/v1/me", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return True, "", data
                elif response.status == 401:
                    return False, "Invalid or expired token", {}
                elif response.status == 403:
                    return False, "Token lacks required permissions", {}
                else:
                    text = await response.text()
                    return False, f"API error (status {response.status}): {text}", {}
    except aiohttp.ClientError as e:
        return False, f"Network error: {str(e)}", {}
    except Exception as e:
        return False, f"Unexpected error: {str(e)}", {}

async def validate_supabase_connection(url: str, key: str) -> Tuple[bool, str]:
    """
    Validate Supabase connection
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}"
    }
    
    try:
        # Test with a simple query to check if tables exist
        async with aiohttp.ClientSession() as session:
            # Try to query the design_files table
            query_url = f"{url}/rest/v1/design_files?select=id&limit=1"
            async with session.get(query_url, headers=headers) as response:
                if response.status == 200:
                    return True, ""
                elif response.status == 401:
                    return False, "Invalid API key"
                elif response.status == 404:
                    return False, "Tables not found - please run database migrations"
                else:
                    text = await response.text()
                    return False, f"API error (status {response.status}): {text}"
    except aiohttp.ClientError as e:
        return False, f"Network error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def check_env_file():
    """Check if .env file exists and is readable"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        print_success(f"Found .env file at: {env_path}")
        return True
    else:
        print_warning("No .env file found")
        print_info("You can copy .env.example to .env and fill in your values")
        return False

async def main():
    """Main validation function"""
    print(f"{Colors.BOLD}Figma MCP Server Configuration Validator{Colors.RESET}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check for .env file
    print_header("Environment File Check")
    check_env_file()
    
    # Check Figma token
    print_header("Figma API Configuration")
    
    figma_pat = os.getenv('FIGMA_PAT')
    figma_access_token = os.getenv('FIGMA_ACCESS_TOKEN')
    figma_token = figma_pat or figma_access_token
    
    if figma_pat:
        print_success(f"FIGMA_PAT found (length: {len(figma_pat)})")
    else:
        print_warning("FIGMA_PAT not set")
    
    if figma_access_token:
        print_success(f"FIGMA_ACCESS_TOKEN found (length: {len(figma_access_token)})")
    else:
        print_warning("FIGMA_ACCESS_TOKEN not set")
    
    if not figma_token:
        print_error("No Figma token found!")
        print_info("Set either FIGMA_PAT or FIGMA_ACCESS_TOKEN environment variable")
        print_info("Get a token from: https://www.figma.com/developers/access-tokens")
    else:
        # Validate token format
        if figma_token.startswith(('figd_', 'figp_')):
            print_success("Token format looks correct")
        else:
            print_warning(f"Token has unusual format (starts with '{figma_token[:5]}')")
            print_info("Figma tokens typically start with 'figd_' or 'figp_'")
        
        # Test API connection
        print_info("Testing Figma API connection...")
        is_valid, error, user_info = await validate_figma_token(figma_token)
        
        if is_valid:
            print_success("Figma API connection successful!")
            print_info(f"Authenticated as: {user_info.get('email', 'Unknown')}")
            print_info(f"User handle: @{user_info.get('handle', 'Unknown')}")
        else:
            print_error(f"Figma API connection failed: {error}")
            if "401" in error or "Invalid" in error:
                print_info("→ Check that your token is correct and not expired")
                print_info("→ Tokens expire after 90 days of inactivity")
            elif "403" in error or "permissions" in error:
                print_info("→ Ensure your token has 'File content' read scope")
    
    # Check Supabase configuration
    print_header("Supabase Configuration")
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
    
    if supabase_url:
        print_success(f"SUPABASE_URL found: {supabase_url}")
        if not supabase_url.startswith('https://'):
            print_warning("URL should start with 'https://'")
    else:
        print_error("SUPABASE_URL not set")
        print_info("Get from: Supabase Dashboard → Settings → API → Project URL")
    
    if supabase_key:
        print_success(f"SUPABASE_SERVICE_KEY found (length: {len(supabase_key)})")
        if len(supabase_key) < 100:
            print_warning("Key seems short - service keys are typically 200+ characters")
            print_info("Make sure you're using the service_role key, not the anon key")
    else:
        print_error("SUPABASE_SERVICE_KEY not set")
        print_info("Get from: Supabase Dashboard → Settings → API → service_role secret")
    
    if supabase_url and supabase_key:
        print_info("Testing Supabase connection...")
        is_valid, error = await validate_supabase_connection(supabase_url, supabase_key)
        
        if is_valid:
            print_success("Supabase connection successful!")
        else:
            print_error(f"Supabase connection failed: {error}")
            if "Invalid API key" in error:
                print_info("→ Check that you're using the service_role key")
                print_info("→ The anon/public key will not work")
            elif "Tables not found" in error:
                print_info("→ Run the migration script in your Supabase dashboard")
                print_info("→ SQL file: migrations/001_initial_schema.sql")
    
    # Check optional configuration
    print_header("Optional Configuration")
    
    port = os.getenv('FIGMA_MCP_PORT', '8031')
    print_info(f"Server port: {port}")
    
    debug = os.getenv('FIGMA_DEBUG', 'false')
    if debug.lower() in ('true', '1', 'yes'):
        print_info("Debug mode: ENABLED")
    else:
        print_info("Debug mode: disabled (set FIGMA_DEBUG=true to enable)")
    
    # Summary
    print_header("Validation Summary")
    
    all_valid = True
    if not figma_token:
        print_error("Missing Figma authentication token")
        all_valid = False
    elif not figma_token.startswith(('figd_', 'figp_')):
        print_warning("Figma token format may be incorrect")
    
    if not supabase_url:
        print_error("Missing Supabase URL")
        all_valid = False
    
    if not supabase_key:
        print_error("Missing Supabase service key")
        all_valid = False
    
    if all_valid:
        print_success("All required configuration found!")
        print_info("\nTo start the server, run: ./start.sh")
    else:
        print_error("Configuration incomplete!")
        print_info("\n1. Copy .env.example to .env")
        print_info("2. Fill in the missing values")
        print_info("3. Run this validator again")
    
    return 0 if all_valid else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)