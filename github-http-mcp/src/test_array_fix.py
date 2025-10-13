import asyncio
import os
from github_server import mcp

async def test_github_array_fix():
    """Test that the GitHub MCP server array parameters fix is working"""
    print("🔧 Testing GitHub MCP Server Array Parameters Fix")
    print("=" * 50)
    
    # Check if we have a GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("⚠️ No GITHUB_TOKEN found - testing will be limited")
        return
    
    all_tools = await mcp.get_tools()
    
    # Test 1: Check if create_issue tool exists and accepts arrays
    print(f"\n✅ Testing create_issue with labels array")
    create_issue_tool = all_tools.get("create_issue")
    if create_issue_tool:
        print(f"   📋 create_issue tool found")
        
        # Test with labels array (should work now!)
        try:
            result = await create_issue_tool.fn(
                owner="vanman2024",
                repo="mcp-kernel-clean", 
                title="Array Fix Test Issue",
                body="Testing that labels array parameter works correctly",
                labels=["test", "array-fix", "automated"]  # This should work now!
            )
            
            if result.get('success'):
                print(f"   ✅ SUCCESS: Labels array parameter working!")
                print(f"   📋 Issue created: {result.get('issue', {}).get('html_url', 'Unknown URL')}")
            else:
                error = result.get('error', 'Unknown error')
                if 'validation error' in error and 'list_type' in error:
                    print(f"   ❌ FAILED: Array parameters still broken - {error}")
                else:
                    print(f"   ⚠️ Expected error (not array-related): {error}")
                    
        except Exception as e:
            if 'validation error' in str(e) and 'list_type' in str(e):
                print(f"   ❌ FAILED: Array parameters still broken - {e}")
            else:
                print(f"   ⚠️ Expected error (not array-related): {e}")
    else:
        print(f"   ❌ create_issue tool not found")
    
    # Test 2: Check list_issues (should work regardless)
    print(f"\n✅ Testing list_issues")
    list_issues_tool = all_tools.get("list_issues")
    if list_issues_tool:
        try:
            result = await list_issues_tool.fn(
                owner="vanman2024",
                repo="mcp-kernel-clean",
                state="open"
            )
            if result.get('success') or 'issues' in str(result):
                print(f"   ✅ list_issues working")
                issues = result.get('issues', [])
                print(f"   📊 Found {len(issues)} open issues")
            else:
                print(f"   ⚠️ list_issues error: {result}")
        except Exception as e:
            print(f"   ⚠️ list_issues error: {e}")
    
    # Test 3: Check that array_params_fix was imported
    print(f"\n🔧 Checking Array Parameters Fix Import")
    try:
        import sys
        if any("array_params_fix" in str(module) for module in sys.modules):
            print(f"   ✅ array_params_fix module imported successfully")
        else:
            print(f"   ⚠️ array_params_fix module not found in imports")
    except Exception as e:
        print(f"   ❌ Error checking imports: {e}")
    
    print(f"\n🎯 Array Fix Status:")
    print(f"   - If create_issue with labels worked: ✅ FIXED")
    print(f"   - If create_issue with labels failed with validation error: ❌ NOT FIXED")
    print(f"   - If create_issue failed for other reasons: ⚠️ NEEDS INVESTIGATION")

if __name__ == "__main__":
    asyncio.run(test_github_array_fix())