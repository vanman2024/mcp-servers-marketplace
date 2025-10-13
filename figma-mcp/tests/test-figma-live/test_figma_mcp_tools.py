#!/usr/bin/env python3
"""
Direct testing of Figma MCP Server tools without needing Claude sessions
Tests the MCP tools by mocking the FastMCP decorator
"""

import asyncio
import os
import json
import sys
from datetime import datetime
from typing import Dict, Any, List
import tempfile
import shutil

# Set environment variables BEFORE importing server
os.environ['SUPABASE_URL'] = 'https://wsmhiiharnhqupdniwgw.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndzbWhpaWhhcm5ocXVwZG5pd2d3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTIyNjk5OSwiZXhwIjoyMDY2ODAyOTk5fQ.R5DGQCoMhN9hj_P3Ri0Kkfl6VdaYGlKOOLmvnOmiJOA'

# Mock the FastMCP decorator to get raw functions
import unittest.mock
with unittest.mock.patch('fastmcp.FastMCP.tool', lambda self: lambda f: f):
    with unittest.mock.patch('fastmcp.FastMCP.resource', lambda self, uri: lambda f: f):
        # Import after mocking AND after setting env vars
        sys.path.insert(0, '../src')
        import figma_server_db as server

class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def add(self, name: str, passed: bool, details: str = ""):
        self.results.append({
            "name": name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print("\n" + "=" * 60)
        print("📊 FIGMA MCP TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        if self.passed + self.failed > 0:
            print(f"📈 Success Rate: {self.passed / (self.passed + self.failed) * 100:.1f}%")
        
        print("\n📋 Failed Tests:")
        for result in self.results:
            if not result["passed"]:
                print(f"  ❌ {result['name']}: {result['details'][:100]}")

async def test_basic_tools(results: TestResults):
    """Test basic component retrieval tools"""
    print("\n🔧 TESTING BASIC TOOLS")
    print("-" * 40)
    
    # Test preview_figma_components
    try:
        result = await server.preview_figma_components(limit=5)
        results.add("preview_figma_components", result["success"], result.get("error", "Success"))
        if result["success"]:
            print(f"✅ preview_figma_components: {len(result['components'])} components")
    except Exception as e:
        results.add("preview_figma_components", False, str(e))
        print(f"❌ preview_figma_components: {e}")
    
    # Test get_components_by_type
    try:
        result = await server.get_components_by_type(component_type="button", limit=3)
        results.add("get_components_by_type", result["success"], result.get("error", "Success"))
        if result["success"]:
            print(f"✅ get_components_by_type: {len(result['components'])} buttons")
    except Exception as e:
        results.add("get_components_by_type", False, str(e))
        print(f"❌ get_components_by_type: {e}")

async def test_application_blocks(results: TestResults):
    """Test application block creation"""
    print("\n📦 TESTING APPLICATION BLOCKS")
    print("-" * 40)
    
    # Create a temp directory for testing
    test_dir = tempfile.mkdtemp(prefix="figma_test_")
    
    try:
        # Test bulk_create_component_files
        result = await server.bulk_create_component_files(
            app_type="todo",
            output_directory=test_dir,
            create_index=True
        )
        results.add("bulk_create_component_files", result["success"], result.get("error", "Success"))
        if result["success"]:
            print(f"✅ bulk_create_component_files: {result['file_count']} files created")
            # List created files
            for file in result["created_files"][:3]:
                print(f"   - {file['filename']}")
    except Exception as e:
        results.add("bulk_create_component_files", False, str(e))
        print(f"❌ bulk_create_component_files: {e}")
    finally:
        # Clean up
        shutil.rmtree(test_dir)

async def test_build_application(results: TestResults):
    """Test the main build_application tool"""
    print("\n🏗️ TESTING BUILD APPLICATION")
    print("-" * 40)
    
    # Create test directories
    test_dirs = []
    
    try:
        # Test 1: Blog application
        blog_dir = tempfile.mkdtemp(prefix="blog_test_")
        test_dirs.append(blog_dir)
        
        result = await server.build_application(
            app_description="A simple blog website with articles",
            output_directory=blog_dir,
            include_ui_library=True,
            include_auth=False,
            include_data_layer=False
        )
        results.add("build_application (blog)", result["success"], result.get("error", "Success"))
        if result["success"]:
            print(f"✅ build_application (blog): {result['total_files']} files")
            print(f"   - App type: {result['app_analysis']['app_type']}")
            print(f"   - Blocks: {result['total_blocks']}")
        
        # Test 2: E-commerce application (expect partial success)
        ecom_dir = tempfile.mkdtemp(prefix="ecom_test_")
        test_dirs.append(ecom_dir)
        
        result2 = await server.build_application(
            app_description="An e-commerce store with shopping cart",
            output_directory=ecom_dir,
            include_ui_library=True,
            include_auth=True,
            include_data_layer=True
        )
        results.add("build_application (e-commerce)", result2["success"], result2.get("error", "Success"))
        if result2["success"]:
            print(f"✅ build_application (e-commerce): {result2['total_files']} files")
            print(f"   - Note: Some blocks may be missing for full e-commerce")
            
    except Exception as e:
        results.add("build_application", False, str(e))
        print(f"❌ build_application: {e}")
    finally:
        # Clean up test directories
        for dir in test_dirs:
            shutil.rmtree(dir)

async def test_database_operations(results: TestResults):
    """Test database health and component counts"""
    print("\n💾 TESTING DATABASE OPERATIONS")
    print("-" * 40)
    
    try:
        result = await server.validate_database_access()
        results.add("validate_database_access", result["success"], result.get("error", "Success"))
        if result["success"]:
            print(f"✅ validate_database_access: {result['component_count']} components")
            print(f"   - Status: {result['status']}")
    except Exception as e:
        results.add("validate_database_access", False, str(e))
        print(f"❌ validate_database_access: {e}")

async def main():
    """Run all tests"""
    print("🚀 FIGMA MCP SERVER DIRECT TESTING")
    print(f"📅 Test run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = TestResults()
    
    # Run test suites
    await test_database_operations(results)
    await test_basic_tools(results)
    await test_application_blocks(results)
    await test_build_application(results)
    
    # Print summary
    results.print_summary()
    
    print("\n✅ Testing complete! No Claude session required.")
    print("📝 This proves we can test MCP tools directly!")

if __name__ == "__main__":
    asyncio.run(main())