#!/usr/bin/env python3
"""
Direct testing of E-commerce MCP Server tools without needing Claude sessions
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
        import figma_ecommerce_server as server

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
        print("📊 E-COMMERCE MCP TEST SUMMARY")
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
        # Test if DatabaseConnectionPool can be instantiated
        db_manager = server.DatabaseConnectionPool()
        await db_manager.validate_connection()
        results.add("database_connection", True, "Connection successful")
        print("✅ Database connection: Success")
    except Exception as e:
        results.add("database_connection", False, str(e))
        print(f"❌ Database connection: {e}")

async def test_product_tools(results: TestResults):
    """Test product-specific tools"""
    print("\n🛒 TESTING PRODUCT TOOLS")
    print("-" * 40)
    
    # Test get_product_sections
    try:
        result = await server.get_product_sections(category="product_grid", limit=3)
        results.add("get_product_sections", result.get("success", False), result.get("error", "Success"))
        if result.get("success"):
            print(f"✅ get_product_sections: {len(result.get('sections', []))} sections")
        else:
            print(f"❌ get_product_sections: {result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("get_product_sections", False, str(e))
        print(f"❌ get_product_sections: {e}")
    
    # Test create_product_grid
    try:
        result = await server.create_product_grid(
            layout="4-column",
            show_price=True,
            show_rating=True,
            show_wishlist=True,
            product_count=12
        )
        results.add("create_product_grid", result.get("success", False), result.get("error", "Success"))
        if result.get("success"):
            print("✅ create_product_grid: Product grid created")
        else:
            print(f"❌ create_product_grid: {result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("create_product_grid", False, str(e))
        print(f"❌ create_product_grid: {e}")

async def test_shopping_cart(results: TestResults):
    """Test shopping cart functionality"""
    print("\n🛒 TESTING SHOPPING CART")
    print("-" * 40)
    
    try:
        result = await server.create_shopping_cart(
            style="sidebar",
            show_recommendations=True,
            enable_guest_checkout=True,
            payment_methods=["stripe", "paypal"]
        )
        results.add("create_shopping_cart", result.get("success", False), result.get("error", "Success"))
        if result.get("success"):
            print("✅ create_shopping_cart: Shopping cart created")
        else:
            print(f"❌ create_shopping_cart: {result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("create_shopping_cart", False, str(e))
        print(f"❌ create_shopping_cart: {e}")

async def test_ecommerce_store_builder(results: TestResults):
    """Test complete e-commerce store generation"""
    print("\n🏪 TESTING STORE BUILDER")
    print("-" * 40)
    
    # Create test directory
    test_dir = tempfile.mkdtemp(prefix="ecommerce_test_")
    
    try:
        result = await server.build_ecommerce_store(
            store_type="fashion",
            sections=["header", "hero", "featured_products", "categories", "footer"],
            payment_integration="stripe",
            output_directory=test_dir
        )
        results.add("build_ecommerce_store", result.get("success", False), result.get("error", "Success"))
        if result.get("success"):
            print(f"✅ build_ecommerce_store: {result.get('file_count', 0)} files created")
            if result.get("created_files"):
                for file in result["created_files"][:3]:
                    print(f"   - {file}")
        else:
            print(f"❌ build_ecommerce_store: {result.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("build_ecommerce_store", False, str(e))
        print(f"❌ build_ecommerce_store: {e}")
    finally:
        # Clean up
        shutil.rmtree(test_dir)

async def test_inventory_management(results: TestResults):
    """Test inventory management system"""
    print("\n📦 TESTING INVENTORY MANAGEMENT")
    print("-" * 40)
    
    try:
        # Test inventory manager
        inventory = server.InventoryManager()
        stock_data = await inventory.check_stock_levels("test_product_123")
        results.add("inventory_management", stock_data.get("success", False), stock_data.get("error", "Success"))
        if stock_data.get("success"):
            print("✅ Inventory management: Stock levels retrieved")
        else:
            print(f"❌ Inventory management: {stock_data.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("inventory_management", False, str(e))
        print(f"❌ Inventory management: {e}")

async def test_payment_processing(results: TestResults):
    """Test payment processing functionality"""
    print("\n💳 TESTING PAYMENT PROCESSING")
    print("-" * 40)
    
    try:
        # Test payment processor
        payment = server.PaymentProcessor()
        payment_options = await payment.get_payment_methods()
        results.add("payment_processing", payment_options.get("success", False), payment_options.get("error", "Success"))
        if payment_options.get("success"):
            print(f"✅ Payment processing: {len(payment_options.get('methods', []))} payment methods")
        else:
            print(f"❌ Payment processing: {payment_options.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("payment_processing", False, str(e))
        print(f"❌ Payment processing: {e}")

async def test_recommendation_engine(results: TestResults):
    """Test product recommendation system"""
    print("\n🎯 TESTING RECOMMENDATION ENGINE")
    print("-" * 40)
    
    try:
        # Test recommendation engine
        recommender = server.RecommendationEngine()
        recommendations = await recommender.get_product_recommendations(
            user_id="test_user",
            product_id="test_product",
            recommendation_type="similar"
        )
        results.add("recommendation_engine", recommendations.get("success", False), recommendations.get("error", "Success"))
        if recommendations.get("success"):
            print(f"✅ Recommendation engine: {len(recommendations.get('products', []))} recommendations")
        else:
            print(f"❌ Recommendation engine: {recommendations.get('error', 'Unknown error')}")
    except Exception as e:
        results.add("recommendation_engine", False, str(e))
        print(f"❌ Recommendation engine: {e}")

async def main():
    """Run all tests"""
    print("🚀 E-COMMERCE MCP SERVER DIRECT TESTING")
    print(f"📅 Test run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = TestResults()
    
    # Run test suites
    await test_database_connection(results)
    await test_product_tools(results)
    await test_shopping_cart(results)
    await test_ecommerce_store_builder(results)
    await test_inventory_management(results)
    await test_payment_processing(results)
    await test_recommendation_engine(results)
    
    # Print summary
    results.print_summary()
    
    print("\n✅ E-commerce server testing complete!")
    print("📝 Results show which e-commerce tools are working vs need component content")

if __name__ == "__main__":
    asyncio.run(main())