#!/usr/bin/env python3
"""
Direct testing of Application UI MCP Server tools without needing Claude sessions
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
        import figma_application_server as server

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
        print("📊 APPLICATION UI MCP TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        if self.passed + self.failed > 0:
            print(f"📈 Success Rate: {self.passed / (self.passed + self.failed) * 100:.1f}%")
        
        print("\n📋 Failed Tests:")
        for result in self.results:
            if not result["passed"]:
                print(f"  ❌ {result['name']}: {result['details'][:100]}")

async def test_database_connection(results: TestResults):
    """Test database connection and validation"""
    print("\n💾 TESTING DATABASE CONNECTION")
    print("-" * 40)
    
    try:
        # Test if ConnectionManager can be instantiated
        conn_manager = server.ConnectionManager()
        await conn_manager.validate_connection()
        results.add("database_connection", True, "Connection successful")
        print("✅ Database connection: Success")
    except Exception as e:
        results.add("database_connection", False, str(e))
        print(f"❌ Database connection: {e}")

async def test_application_tools(results: TestResults):
    """Test application-specific tools with Tailwind UI components"""
    print("\n💻 TESTING APPLICATION TOOLS - TAILWIND UI ACCESS")
    print("-" * 40)
    
    # Test get_application_sections with Tailwind UI categories
    test_categories = ["Forms", "Navigation", "Layout", "Elements"]
    
    for category in test_categories:
        try:
            input_obj = server.GetApplicationSectionsInput(category=category, limit=5)
            result = await server.get_application_sections(input_obj)
            results.add(f"get_application_sections_{category}", result.get("success", False), result.get("error", "Success"))
            if result.get("success"):
                sections = result.get('sections', [])
                print(f"✅ get_application_sections({category}): {len(sections)} sections")
                if sections:
                    print(f"   Sample: {sections[0].get('name', 'Unknown')}")
            else:
                print(f"❌ get_application_sections({category}): {result.get('error', 'Unknown error')}")
        except Exception as e:
            results.add(f"get_application_sections_{category}", False, str(e))
            print(f"❌ get_application_sections({category}): {e}")
    
    # Test searching for specific Tailwind UI components
    try:
        input_obj = server.GetApplicationSectionsInput(search_query="Form", limit=3)
        result = await server.get_application_sections(input_obj)
        results.add("search_tailwind_components", result.get("success", False), result.get("error", "Success"))
        if result.get("success"):
            sections = result.get('sections', [])
            print(f"✅ Search 'Form': {len(sections)} sections found")
            for section in sections[:2]:
                print(f"   - {section.get('name', 'Unknown')}")
        else:
            print(f"❌ Search 'Form': {result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("search_tailwind_components", False, str(e))
        print(f"❌ Search 'Form': {e}")
    
    # Test if we can access component code
    try:
        input_obj = server.GetApplicationSectionsInput(category="Forms", limit=1, include_code=True)
        result = await server.get_application_sections(input_obj)
        results.add("get_component_code", result.get("success", False), result.get("error", "Success"))
        if result.get("success"):
            sections = result.get('sections', [])
            if sections and sections[0].get('react_template'):
                print(f"✅ Component code access: React template found ({len(sections[0]['react_template'])} chars)")
            else:
                print(f"⚠️ Component code access: No react_template field found")
        else:
            print(f"❌ Component code access: {result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("get_component_code", False, str(e))
        print(f"❌ Component code access: {e}")
    
    # Test create_data_table
    try:
        result = await server.create_data_table(
            columns=[
                {"key": "id", "label": "ID", "sortable": True},
                {"key": "name", "label": "Name", "filterable": True},
                {"key": "email", "label": "Email", "type": "email"}
            ],
            features=["pagination", "search", "export"],
            virtual_scrolling=True
        )
        results.add("create_data_table", result.get("success", False), result.get("error", "Success"))
        if result.get("success"):
            print("✅ create_data_table: Data table created")
        else:
            print(f"❌ create_data_table: {result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("create_data_table", False, str(e))
        print(f"❌ create_data_table: {e}")

async def test_dashboard_builder(results: TestResults):
    """Test dashboard generation"""
    print("\n📊 TESTING DASHBOARD BUILDER")
    print("-" * 40)
    
    # Create test directory
    test_dir = tempfile.mkdtemp(prefix="application_test_")
    
    try:
        result = await server.build_dashboard(
            layout="sidebar",
            widgets=["stats", "charts", "recent_activity", "notifications"],
            theme="dark",
            responsive=True,
            output_directory=test_dir
        )
        results.add("build_dashboard", result.get("success", False), result.get("error", "Success"))
        if result.get("success"):
            print(f"✅ build_dashboard: {result.get('file_count', 0)} files created")
            if result.get("created_files"):
                for file in result["created_files"][:3]:
                    print(f"   - {file}")
        else:
            print(f"❌ build_dashboard: {result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("build_dashboard", False, str(e))
        print(f"❌ build_dashboard: {e}")
    finally:
        # Clean up
        shutil.rmtree(test_dir)

async def test_form_system(results: TestResults):
    """Test form system generation"""
    print("\n📝 TESTING FORM SYSTEM")
    print("-" * 40)
    
    try:
        result = await server.build_form_system(
            form_type="multi-step",
            fields=[
                {"name": "email", "type": "email", "validation": "required|email"},
                {"name": "password", "type": "password", "validation": "required|min:8"},
                {"name": "preferences", "type": "checkbox-group", "options": ["notifications", "updates"]}
            ],
            auto_save=True,
            validation="real-time"
        )
        results.add("build_form_system", result.get("success", False), result.get("error", "Success"))
        if result.get("success"):
            print("✅ build_form_system: Form system created")
        else:
            print(f"❌ build_form_system: {result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("build_form_system", False, str(e))
        print(f"❌ build_form_system: {e}")

async def test_theme_system(results: TestResults):
    """Test theme system functionality"""
    print("\n🎨 TESTING THEME SYSTEM")
    print("-" * 40)
    
    try:
        # Test theme engine
        theme_engine = server.ThemeEngine()
        theme_result = await theme_engine.apply_theme(
            theme_name="custom",
            colors={"primary": "#3B82F6", "secondary": "#6B7280"},
            typography="modern",
            spacing="comfortable"
        )
        results.add("theme_system", theme_result.get("success", False), theme_result.get("error", "Success"))
        if theme_result.get("success"):
            print("✅ Theme system: Custom theme applied")
        else:
            print(f"❌ Theme system: {theme_result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("theme_system", False, str(e))
        print(f"❌ Theme system: {e}")

async def test_accessibility_manager(results: TestResults):
    """Test accessibility compliance checking"""
    print("\n♿ TESTING ACCESSIBILITY MANAGER")
    print("-" * 40)
    
    try:
        # Test accessibility manager
        accessibility = server.AccessibilityManager()
        audit_result = await accessibility.validate_accessibility(
            component_html="<button>Test Button</button>",
            standards=["WCAG_2_1_AA"]
        )
        results.add("accessibility_manager", audit_result.get("success", False), audit_result.get("error", "Success"))
        if audit_result.get("success"):
            print(f"✅ Accessibility manager: {len(audit_result.get('issues', []))} issues found")
        else:
            print(f"❌ Accessibility manager: {audit_result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("accessibility_manager", False, str(e))
        print(f"❌ Accessibility manager: {e}")

async def test_command_palette(results: TestResults):
    """Test command palette functionality"""
    print("\n⌘ TESTING COMMAND PALETTE")
    print("-" * 40)
    
    try:
        result = await server.build_command_palette(
            commands=[
                {"id": "new_project", "label": "New Project", "shortcut": "Ctrl+N"},
                {"id": "search", "label": "Search", "shortcut": "Ctrl+K"},
                {"id": "settings", "label": "Settings", "shortcut": "Ctrl+,"}
            ],
            fuzzy_search=True,
            keyboard_shortcuts=True
        )
        results.add("build_command_palette", result.get("success", False), result.get("error", "Success"))
        if result.get("success"):
            print("✅ build_command_palette: Command palette created")
        else:
            print(f"❌ build_command_palette: {result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("build_command_palette", False, str(e))
        print(f"❌ build_command_palette: {e}")

async def test_admin_panel_generator(results: TestResults):
    """Test admin panel generation"""
    print("\n🛠️ TESTING ADMIN PANEL GENERATOR")
    print("-" * 40)
    
    # Create test directory
    test_dir = tempfile.mkdtemp(prefix="admin_test_")
    
    try:
        result = await server.generate_admin_panel(
            panel_type="user_management",
            sections=["users", "roles", "permissions", "audit_log"],
            features=["crud", "bulk_actions", "export", "search"],
            output_directory=test_dir
        )
        results.add("generate_admin_panel", result.get("success", False), result.get("error", "Success"))
        if result.get("success"):
            print(f"✅ generate_admin_panel: {result.get('file_count', 0)} files created")
        else:
            print(f"❌ generate_admin_panel: {result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("generate_admin_panel", False, str(e))
        print(f"❌ generate_admin_panel: {e}")
    finally:
        # Clean up
        shutil.rmtree(test_dir)

async def main():
    """Run all tests"""
    print("🚀 APPLICATION UI MCP SERVER DIRECT TESTING")
    print(f"📅 Test run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = TestResults()
    
    # Run test suites
    await test_database_connection(results)
    await test_application_tools(results)
    await test_dashboard_builder(results)
    await test_form_system(results)
    await test_theme_system(results)
    await test_accessibility_manager(results)
    await test_command_palette(results)
    await test_admin_panel_generator(results)
    
    # Print summary
    results.print_summary()
    
    print("\n✅ Application UI server testing complete!")
    print("📝 Results show which application tools are working vs need component content")

if __name__ == "__main__":
    asyncio.run(main())