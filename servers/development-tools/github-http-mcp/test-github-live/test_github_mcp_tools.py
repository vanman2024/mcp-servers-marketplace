#!/usr/bin/env python3
"""
Direct testing of GitHub MCP Server tools without needing Claude sessions
Tests the MCP tools by mocking the FastMCP decorator
"""

import asyncio
import os
import json
import sys
from datetime import datetime
from typing import Dict, Any, List

# Set environment variables BEFORE importing server
os.environ['GITHUB_TOKEN'] = os.getenv('GITHUB_TOKEN', '')
if not os.environ['GITHUB_TOKEN']:
    print("❌ GITHUB_TOKEN environment variable required")
    sys.exit(1)

# Mock the FastMCP decorator to get raw functions
import unittest.mock
with unittest.mock.patch('fastmcp.FastMCP.tool', lambda self: lambda f: f):
    with unittest.mock.patch('fastmcp.FastMCP.resource', lambda self, uri: lambda f: f):
        # Import after mocking AND after setting env vars
        sys.path.insert(0, 'src')
        import github_server as server

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
        print("📊 GITHUB MCP TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        if self.passed + self.failed > 0:
            print(f"📈 Success Rate: {self.passed / (self.passed + self.failed) * 100:.1f}%")
        
        print("\n📋 Failed Tests:")
        for result in self.results:
            if not result["passed"]:
                print(f"  ❌ {result['name']}: {result['details'][:100]}")

async def test_basic_repository_tools(results: TestResults):
    """Test basic repository operations"""
    print("\n🔧 TESTING BASIC REPOSITORY TOOLS")
    print("-" * 40)
    
    # Test search_repositories
    try:
        result = await server.search_repositories(query="mcp-kernel", page=1, per_page=5)
        results.add("search_repositories", result["success"], result.get("message", "Success"))
        if result["success"]:
            repos_count = len(result.get('repositories', result.get('items', [])))
            print(f"✅ search_repositories: {repos_count} repositories found")
    except Exception as e:
        results.add("search_repositories", False, str(e))
        print(f"❌ search_repositories: {e}")

async def test_issue_management(results: TestResults):
    """Test issue management tools"""
    print("\n🎫 TESTING ISSUE MANAGEMENT")
    print("-" * 40)
    
    # Test list_issues
    try:
        result = await server.list_issues(
            owner="vanman2024",
            repo="mcp-kernel-clean",
            state="open",
            per_page=5
        )
        results.add("list_issues", result["success"], result.get("message", "Success"))
        if result["success"]:
            print(f"✅ list_issues: {len(result['issues'])} issues found")
            
            # Store an issue number for sub-issue testing
            if result['issues']:
                issue_number = result['issues'][0]['number']
                print(f"   - Will use issue #{issue_number} for sub-issue test")
                return issue_number
    except Exception as e:
        results.add("list_issues", False, str(e))
        print(f"❌ list_issues: {e}")
    
    return None

async def test_create_sub_issue(results: TestResults, parent_issue_number: int = None):
    """Test the new create_sub_issue functionality"""
    print("\n🧵 TESTING CREATE SUB-ISSUE (NEW FEATURE)")
    print("-" * 40)
    
    if not parent_issue_number:
        print("⚠️  No parent issue available for sub-issue test")
        results.add("create_sub_issue", False, "No parent issue provided")
        return
    
    try:
        # Test create_sub_issue
        result = await server.create_sub_issue(
            owner="vanman2024",
            repo="mcp-kernel-clean",
            parent_issue_number=parent_issue_number,
            title="[TEST] Sub-issue for GitHub MCP Testing",
            body="This is a test sub-issue created by the GitHub MCP test script.",
            labels=["test", "mcp-server"]
        )
        
        results.add("create_sub_issue", result["success"], result.get("message", "Success"))
        if result["success"]:
            sub_issue_number = result['sub_issue']['number']
            print(f"✅ create_sub_issue: Created issue #{sub_issue_number}")
            print(f"   - Parent: #{result['parent_issue']['number']}")
            print(f"   - Labels: {result['sub_issue']['labels']}")
            print(f"   - Cross-reference added: {result['linkage']['cross_reference_comment_added']}")
            
            # Clean up - close the test issue
            try:
                close_result = await server.close_issue(
                    owner="vanman2024",
                    repo="mcp-kernel-clean", 
                    issue_number=sub_issue_number,
                    reason="Test completed - closing test sub-issue"
                )
                if close_result["success"]:
                    print(f"   - Cleaned up test issue #{sub_issue_number}")
            except Exception as cleanup_e:
                print(f"   - Could not clean up test issue: {cleanup_e}")
                
    except Exception as e:
        results.add("create_sub_issue", False, str(e))
        print(f"❌ create_sub_issue: {e}")

async def test_error_handling(results: TestResults):
    """Test error handling in sub-issue creation"""
    print("\n🚨 TESTING ERROR HANDLING")
    print("-" * 40)
    
    # Test with invalid parent issue number
    try:
        result = await server.create_sub_issue(
            owner="vanman2024",
            repo="mcp-kernel-clean",
            parent_issue_number=999999,  # Non-existent issue
            title="This should fail",
            body="Testing error handling"
        )
        # If we get here, the test failed because it should have thrown an error
        results.add("error_handling_invalid_parent", False, "Expected error but got success")
        print("❌ error_handling_invalid_parent: Expected error but got success")
    except Exception as e:
        # This is expected - the error should be caught
        if "not found" in str(e).lower():
            results.add("error_handling_invalid_parent", True, "Correctly handled invalid parent issue")
            print("✅ error_handling_invalid_parent: Correctly caught invalid parent issue")
        else:
            results.add("error_handling_invalid_parent", False, f"Unexpected error: {e}")
            print(f"❌ error_handling_invalid_parent: Unexpected error: {e}")

async def test_milestone_and_label_tools(results: TestResults):
    """Test milestone and label management"""
    print("\n🏷️ TESTING MILESTONE AND LABEL TOOLS")
    print("-" * 40)
    
    # Test list_milestones
    try:
        result = await server.list_milestones(
            owner="vanman2024",
            repo="mcp-kernel-clean",
            state="open"
        )
        results.add("list_milestones", result["success"], result.get("message", "Success"))
        if result["success"]:
            print(f"✅ list_milestones: {len(result['milestones'])} milestones found")
    except Exception as e:
        results.add("list_milestones", False, str(e))
        print(f"❌ list_milestones: {e}")
    
    # Test list_labels
    try:
        result = await server.list_labels(
            owner="vanman2024",
            repo="mcp-kernel-clean",
            per_page=10
        )
        results.add("list_labels", result["success"], result.get("message", "Success"))
        if result["success"]:
            print(f"✅ list_labels: {len(result['labels'])} labels found")
    except Exception as e:
        results.add("list_labels", False, str(e))
        print(f"❌ list_labels: {e}")

async def main():
    """Run all tests"""
    print("🚀 GITHUB MCP SERVER DIRECT TESTING")
    print(f"📅 Test run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔑 Using GitHub token: {os.environ['GITHUB_TOKEN'][:8]}...")
    print("=" * 60)
    
    results = TestResults()
    
    # Run test suites
    await test_basic_repository_tools(results)
    parent_issue = await test_issue_management(results)
    await test_create_sub_issue(results, parent_issue)
    await test_error_handling(results)
    await test_milestone_and_label_tools(results)
    
    # Print summary
    results.print_summary()
    
    print("\n✅ Testing complete! No Claude session required.")
    print("📝 This proves we can test MCP tools directly!")
    print(f"🧵 Sub-issue functionality {'✅ WORKING' if any(r['name'] == 'create_sub_issue' and r['passed'] for r in results.results) else '❌ FAILED'}")

if __name__ == "__main__":
    asyncio.run(main())