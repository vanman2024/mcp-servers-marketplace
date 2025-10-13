#!/usr/bin/env python3
"""
Test script for theme and navigation system integration
Tests the complete flow of generating an app with theme and navigation
"""

import os
import sys
import json
import shutil
from datetime import datetime

# Add the src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the systems
from theme_system import ThemeSystem, generate_project_theme
from navigation_system import NavigationSystem
from page_generator import PageGenerator

def test_theme_generation():
    """Test theme generation for different app types"""
    print("\n🎨 Testing Theme Generation...")
    
    test_dir = "/tmp/test_theme_integration"
    os.makedirs(test_dir, exist_ok=True)
    
    app_types = ["e-commerce", "saas", "dashboard", "blog"]
    results = []
    
    for app_type in app_types:
        output_dir = os.path.join(test_dir, app_type)
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            result = generate_project_theme(
                project_type=app_type,
                output_directory=output_dir
            )
            
            # Verify files were created
            files_exist = all(
                os.path.exists(os.path.join(output_dir, file)) 
                for file in result["files_created"]
            )
            
            results.append({
                "app_type": app_type,
                "success": files_exist,
                "files": result["files_created"]
            })
            
            print(f"✅ {app_type}: Generated {len(result['files_created'])} files")
            
        except Exception as e:
            print(f"❌ {app_type}: Failed - {str(e)}")
            results.append({"app_type": app_type, "success": False, "error": str(e)})
    
    return results

def test_navigation_generation():
    """Test navigation component generation"""
    print("\n🧭 Testing Navigation Generation...")
    
    test_dir = "/tmp/test_nav_integration"
    os.makedirs(test_dir, exist_ok=True)
    
    nav_system = NavigationSystem()
    app_types = ["e-commerce", "dashboard", "saas", "blog", "social"]
    results = []
    
    for app_type in app_types:
        output_dir = os.path.join(test_dir, app_type)
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            components = nav_system.generate_navigation_components(
                app_type=app_type,
                output_directory=output_dir
            )
            
            results.append({
                "app_type": app_type,
                "success": True,
                "component_count": len(components),
                "components": [c["name"] for c in components]
            })
            
            print(f"✅ {app_type}: Generated {len(components)} navigation components")
            
        except Exception as e:
            print(f"❌ {app_type}: Failed - {str(e)}")
            results.append({"app_type": app_type, "success": False, "error": str(e)})
    
    return results

def test_full_integration():
    """Test full integration with page generation"""
    print("\n🚀 Testing Full Integration...")
    
    test_dir = "/tmp/test_full_integration"
    app_type = "e-commerce"
    
    # Clean and create directory
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir, exist_ok=True)
    
    try:
        # 1. Generate theme
        print("\n1️⃣ Generating theme configuration...")
        theme_result = generate_project_theme(
            project_type=app_type,
            output_directory=test_dir
        )
        print(f"   Created: {', '.join(theme_result['files_created'])}")
        
        # 2. Generate navigation
        print("\n2️⃣ Generating navigation components...")
        nav_system = NavigationSystem()
        nav_components = nav_system.generate_navigation_components(
            app_type=app_type,
            output_directory=test_dir
        )
        print(f"   Created {len(nav_components)} navigation components")
        
        # 3. Generate pages
        print("\n3️⃣ Generating pages...")
        page_gen = PageGenerator()
        pages = page_gen.generate_pages_for_app(
            app_type=app_type,
            output_directory=test_dir,
            available_blocks=["hero", "features", "testimonials", "product-grid"]
        )
        print(f"   Created {len(pages)} pages")
        
        # 4. Verify structure
        print("\n4️⃣ Verifying project structure...")
        expected_files = [
            "components.json",
            "tailwind.config.js",
            "app/globals.css",
            "components/navigation/index.ts",
            "pages/index.ts"
        ]
        
        missing_files = []
        for file in expected_files:
            path = os.path.join(test_dir, file)
            if not os.path.exists(path):
                missing_files.append(file)
            else:
                print(f"   ✅ {file}")
        
        if missing_files:
            print(f"\n   ❌ Missing files: {', '.join(missing_files)}")
        else:
            print("\n   ✅ All expected files created!")
        
        # 5. Sample file contents
        print("\n5️⃣ Sample file contents:")
        
        # Show components.json
        comp_json_path = os.path.join(test_dir, "components.json")
        if os.path.exists(comp_json_path):
            with open(comp_json_path, 'r') as f:
                comp_json = json.load(f)
            print(f"\n   📄 components.json:")
            print(f"      - Style: {comp_json.get('style')}")
            print(f"      - Base color: {comp_json.get('tailwind', {}).get('baseColor')}")
            print(f"      - CSS variables: {comp_json.get('tailwind', {}).get('cssVariables')}")
        
        # Count total files created
        total_files = 0
        for root, dirs, files in os.walk(test_dir):
            total_files += len(files)
        
        print(f"\n✨ Total files created: {total_files}")
        
        return {
            "success": True,
            "total_files": total_files,
            "missing_files": missing_files
        }
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def main():
    """Run all tests"""
    print("="*60)
    print("🧪 Figma MCP Theme & Navigation Integration Test")
    print("="*60)
    
    # Test individual systems
    theme_results = test_theme_generation()
    nav_results = test_navigation_generation()
    
    # Test full integration
    integration_result = test_full_integration()
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    theme_success = sum(1 for r in theme_results if r.get("success"))
    nav_success = sum(1 for r in nav_results if r.get("success"))
    
    print(f"\nTheme Generation: {theme_success}/{len(theme_results)} passed")
    print(f"Navigation Generation: {nav_success}/{len(nav_results)} passed")
    print(f"Full Integration: {'✅ Passed' if integration_result.get('success') else '❌ Failed'}")
    
    if integration_result.get("success"):
        print(f"\n🎉 All systems integrated successfully!")
        print(f"   Generated {integration_result['total_files']} files")
    else:
        print(f"\n⚠️ Integration needs attention")
        print(f"   Error: {integration_result.get('error', 'Unknown')}")

if __name__ == "__main__":
    main()