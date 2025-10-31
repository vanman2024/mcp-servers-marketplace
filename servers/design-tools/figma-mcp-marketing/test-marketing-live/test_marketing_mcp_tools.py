#!/usr/bin/env python3
"""
Direct testing of Marketing MCP Server tools without needing Claude sessions
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
        import figma_marketing_server as server

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
        print("📊 MARKETING MCP TEST SUMMARY")
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
        # Test if MarketingDatabaseManager can be instantiated
        db_manager = server.MarketingDatabaseManager()
        await db_manager.validate_connection()
        results.add("database_connection", True, "Connection successful")
        print("✅ Database connection: Success")
    except Exception as e:
        results.add("database_connection", False, str(e))
        print(f"❌ Database connection: {e}")

async def test_marketing_tools(results: TestResults):
    """Test marketing-specific tools"""
    print("\n🎪 TESTING MARKETING TOOLS")
    print("-" * 40)
    
    # Test get_marketing_sections
    try:
        result = await server.get_marketing_sections(category="hero", limit=3)
        results.add("get_marketing_sections", result.get("success", False), result.get("error", "Success"))
        if result.get("success"):
            print(f"✅ get_marketing_sections: {len(result.get('sections', []))} sections")
        else:
            print(f"❌ get_marketing_sections: {result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("get_marketing_sections", False, str(e))
        print(f"❌ get_marketing_sections: {e}")
    
    # Test create_hero_section
    try:
        result = await server.create_hero_section(
            style="split",
            headline="Test Headline",
            subtext="Test subtext for hero section",
            cta_text="Get Started",
            include_video=False
        )
        results.add("create_hero_section", result.get("success", False), result.get("error", "Success"))
        if result.get("success"):
            print("✅ create_hero_section: Hero section created")
        else:
            print(f"❌ create_hero_section: {result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("create_hero_section", False, str(e))
        print(f"❌ create_hero_section: {e}")

async def test_landing_page_builder(results: TestResults):
    """Test landing page generation"""
    print("\n🚀 TESTING LANDING PAGE BUILDER")
    print("-" * 40)
    
    # Create test directory
    test_dir = tempfile.mkdtemp(prefix="marketing_test_")
    
    try:
        result = await server.build_landing_page(
            template="saas",
            sections=["hero", "features", "testimonials", "cta"],
            brand_colors={"primary": "#3B82F6", "secondary": "#EF4444"},
            output_directory=test_dir
        )
        results.add("build_landing_page", result.get("success", False), result.get("error", "Success"))
        if result.get("success"):
            print(f"✅ build_landing_page: {result.get('file_count', 0)} files created")
            if result.get("created_files"):
                for file in result["created_files"][:3]:
                    print(f"   - {file}")
        else:
            print(f"❌ build_landing_page: {result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("build_landing_page", False, str(e))
        print(f"❌ build_landing_page: {e}")
    finally:
        # Clean up
        shutil.rmtree(test_dir)

async def test_ab_testing(results: TestResults):
    """Test A/B testing functionality"""
    print("\n📊 TESTING A/B TESTING ENGINE")
    print("-" * 40)
    
    try:
        # Test A/B testing engine
        engine = server.ABTestingEngine()
        variants = await engine.generate_variants(
            component_type="hero",
            base_config={"headline": "Original Headline", "style": "centered"},
            variant_count=2
        )
        results.add("ab_testing_variants", len(variants) > 0, f"Generated {len(variants)} variants")
        if len(variants) > 0:
            print(f"✅ A/B testing: Generated {len(variants)} variants")
        else:
            print("❌ A/B testing: No variants generated")
    except Exception as e:
        results.add("ab_testing_variants", False, str(e))
        print(f"❌ A/B testing: {e}")

async def test_analytics_engine(results: TestResults):
    """Test analytics and conversion tracking"""
    print("\n📈 TESTING ANALYTICS ENGINE")
    print("-" * 40)
    
    try:
        # Test analytics engine
        analytics = server.AnalyticsEngine()
        report = await analytics.generate_performance_report("test_campaign")
        results.add("analytics_engine", report.get("success", False), report.get("error", "Success"))
        if report.get("success"):
            print("✅ Analytics engine: Performance report generated")
        else:
            print(f"❌ Analytics engine: {report.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("analytics_engine", False, str(e))
        print(f"❌ Analytics engine: {e}")

async def main():
    """Run all tests"""
    print("🚀 MARKETING MCP SERVER DIRECT TESTING")
    print(f"📅 Test run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = TestResults()
    
    # Run test suites
    await test_database_connection(results)
    await test_marketing_tools(results)
    await test_landing_page_builder(results)
    await test_ab_testing(results)
    await test_analytics_engine(results)
    
    # Print summary
    results.print_summary()
    
    print("\n✅ Marketing server testing complete!")
    print("📝 Results show which marketing tools are working vs need component content")

if __name__ == "__main__":
    asyncio.run(main())