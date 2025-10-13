#!/usr/bin/env python3
"""
Direct testing of Filesystem MCP Server tools without needing Claude sessions
Tests the MCP tools by mocking the FastMCP decorator
"""

import asyncio
import os
import json
import sys
import tempfile
import shutil
from datetime import datetime
from typing import Dict, Any, List

# Mock the FastMCP decorator to get raw functions
import unittest.mock
with unittest.mock.patch('fastmcp.FastMCP.tool', lambda self: lambda f: f):
    with unittest.mock.patch('fastmcp.FastMCP.resource', lambda self, uri: lambda f: f):
        # Import after mocking
        sys.path.insert(0, 'src')
        import filesystem_server as server

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
        print("📊 FILESYSTEM MCP TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        if self.passed + self.failed > 0:
            print(f"📈 Success Rate: {self.passed / (self.passed + self.failed) * 100:.1f}%")
        
        print("\n📋 Failed Tests:")
        for result in self.results:
            if not result["passed"]:
                print(f"  ❌ {result['name']}: {result['details'][:100]}")

async def test_file_operations(results: TestResults):
    """Test basic file operations"""
    print("\n📁 TESTING FILE OPERATIONS")
    print("-" * 40)
    
    # Create test directory
    test_dir = tempfile.mkdtemp(prefix="filesystem_test_")
    test_file = os.path.join(test_dir, "test.txt")
    
    try:
        # Test write_file
        try:
            result = await server.write_file(
                path=test_file,
                content="Hello, MCP filesystem test!"
            )
            results.add("write_file", result["success"], result.get("message", "Success"))
            if result["success"]:
                print(f"✅ write_file: File created successfully")
        except Exception as e:
            results.add("write_file", False, str(e))
            print(f"❌ write_file: {e}")
        
        # Test read_file
        try:
            result = await server.read_file(path=test_file)
            results.add("read_file", result["success"], result.get("message", "Success"))
            if result["success"]:
                print(f"✅ read_file: File read successfully ({len(result.get('content', ''))} chars)")
        except Exception as e:
            results.add("read_file", False, str(e))
            print(f"❌ read_file: {e}")
        
        # Test get_file_info
        try:
            result = await server.get_file_info(path=test_file)
            results.add("get_file_info", result["success"], result.get("message", "Success"))
            if result["success"]:
                print(f"✅ get_file_info: File info retrieved")
        except Exception as e:
            results.add("get_file_info", False, str(e))
            print(f"❌ get_file_info: {e}")
            
    finally:
        # Clean up
        shutil.rmtree(test_dir)

async def test_directory_operations(results: TestResults):
    """Test directory operations"""
    print("\n📂 TESTING DIRECTORY OPERATIONS")
    print("-" * 40)
    
    # Create test directory
    test_dir = tempfile.mkdtemp(prefix="filesystem_dir_test_")
    
    try:
        # Test create_directory
        new_dir = os.path.join(test_dir, "new_directory")
        try:
            result = await server.create_directory(path=new_dir)
            results.add("create_directory", result["success"], result.get("message", "Success"))
            if result["success"]:
                print(f"✅ create_directory: Directory created successfully")
        except Exception as e:
            results.add("create_directory", False, str(e))
            print(f"❌ create_directory: {e}")
        
        # Test list_directory
        try:
            result = await server.list_directory(path=test_dir)
            results.add("list_directory", result["success"], result.get("message", "Success"))
            if result["success"]:
                print(f"✅ list_directory: {len(result.get('items', []))} items found")
        except Exception as e:
            results.add("list_directory", False, str(e))
            print(f"❌ list_directory: {e}")
            
    finally:
        # Clean up
        shutil.rmtree(test_dir)

async def test_file_manipulation(results: TestResults):
    """Test file manipulation operations"""
    print("\n✏️ TESTING FILE MANIPULATION")
    print("-" * 40)
    
    # Create test directory
    test_dir = tempfile.mkdtemp(prefix="filesystem_manip_test_")
    source_file = os.path.join(test_dir, "source.txt")
    dest_file = os.path.join(test_dir, "destination.txt")
    
    try:
        # Create source file first
        await server.write_file(path=source_file, content="Test content for move")
        
        # Test move_file
        try:
            result = await server.move_file(source=source_file, destination=dest_file)
            results.add("move_file", result["success"], result.get("message", "Success"))
            if result["success"]:
                print(f"✅ move_file: File moved successfully")
        except Exception as e:
            results.add("move_file", False, str(e))
            print(f"❌ move_file: {e}")
        
        # Test edit_file
        try:
            edits = [{"oldText": "Test", "newText": "Modified"}]
            result = await server.edit_file(path=dest_file, edits=edits)
            results.add("edit_file", result["success"], result.get("message", "Success"))
            if result["success"]:
                print(f"✅ edit_file: File edited successfully")
        except Exception as e:
            results.add("edit_file", False, str(e))
            print(f"❌ edit_file: {e}")
            
    finally:
        # Clean up
        shutil.rmtree(test_dir)

async def test_search_operations(results: TestResults):
    """Test search operations"""
    print("\n🔍 TESTING SEARCH OPERATIONS")
    print("-" * 40)
    
    # Test search_files
    try:
        result = await server.search_files(path=".", pattern="*.py")
        results.add("search_files", result["success"], result.get("message", "Success"))
        if result["success"]:
            print(f"✅ search_files: {len(result.get('files', []))} Python files found")
    except Exception as e:
        results.add("search_files", False, str(e))
        print(f"❌ search_files: {e}")

async def main():
    """Run all tests"""
    print("🚀 FILESYSTEM MCP SERVER DIRECT TESTING")
    print(f"📅 Test run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = TestResults()
    
    # Run test suites
    await test_file_operations(results)
    await test_directory_operations(results)
    await test_file_manipulation(results)
    await test_search_operations(results)
    
    # Print summary
    results.print_summary()
    
    print("\n✅ Testing complete! No Claude session required.")
    print("📝 This proves we can test Filesystem MCP tools directly!")
    print(f"📁 File operations {'✅ WORKING' if any(r['name'] == 'write_file' and r['passed'] for r in results.results) else '❌ FAILED'}")

if __name__ == "__main__":
    asyncio.run(main())