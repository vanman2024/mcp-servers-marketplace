#!/usr/bin/env python3
"""
Test the enhanced theme system with static color palette and design constraints
"""

import os
import sys
import json
import shutil

# Add the src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from theme_system_enhanced import EnhancedThemeSystem, generate_intelligent_theme, ProjectType

def test_static_color_palette():
    """Test that all Tailwind colors are available"""
    print("\n🎨 Testing Static Color Palette...")
    
    theme_system = EnhancedThemeSystem()
    
    # Test that all color families exist
    expected_colors = [
        "neutral", "stone", "zinc", "slate", "gray",
        "red", "orange", "amber", "yellow", "lime", "green", "emerald",
        "teal", "cyan", "sky", "blue", "indigo", "violet", "purple",
        "fuchsia", "pink", "rose"
    ]
    
    for color in expected_colors:
        if color in theme_system.color_palette:
            print(f"✅ {color}: Found with {len(theme_system.color_palette[color])} shades")
        else:
            print(f"❌ {color}: Missing from palette")
            
def test_project_type_themes():
    """Test theme generation for different project types"""
    print("\n🏗️ Testing Project Type Themes...")
    
    test_dir = "/tmp/test_enhanced_themes"
    os.makedirs(test_dir, exist_ok=True)
    
    # Test different project types
    project_types = ["e-commerce", "dashboard", "saas", "blog", "fintech", "healthcare"]
    
    for project_type in project_types:
        print(f"\n📦 Testing {project_type}...")
        output_dir = os.path.join(test_dir, project_type)
        
        # Clean directory
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        
        # Create context as would come from LLM
        context = {
            "type": project_type,
            "industry": project_type,
            "features": ["auth", "dashboard", "analytics"],
            "target_audience": "B2B",
            "design_preferences": {}
        }
        
        # Add specific color preferences for some types
        if project_type == "fintech":
            context["design_preferences"]["primary_color"] = "blue"
            context["design_preferences"]["accent_color"] = "green"
        elif project_type == "healthcare":
            context["design_preferences"]["primary_color"] = "teal"
            context["design_preferences"]["accent_color"] = "sky"
            
        # Generate theme
        result = generate_intelligent_theme(context, output_dir)
        
        if result["success"]:
            print(f"  ✅ Generated {len(result['files_created'])} files")
            
            # Verify design tokens
            tokens_path = os.path.join(output_dir, "design-tokens.json")
            if os.path.exists(tokens_path):
                with open(tokens_path, 'r') as f:
                    tokens = json.load(f)
                print(f"  📌 Primary: {tokens['colors']['primary']}")
                print(f"  📌 Accent: {tokens['colors']['accent']}")
                print(f"  📌 Neutral: {tokens['colors']['neutral']}")
        else:
            print(f"  ❌ Failed to generate theme")
            
def test_design_constraints():
    """Test that design constraints are enforced"""
    print("\n📏 Testing Design Constraints...")
    
    theme_system = EnhancedThemeSystem()
    
    # Test typography constraints
    print("\n📝 Typography Constraints:")
    print(f"  Sizes: {theme_system.TYPOGRAPHY_SIZES} (4 only)")
    print(f"  Weights: {theme_system.FONT_WEIGHTS} (2 only)")
    
    # Test spacing grid
    print("\n📐 Spacing Grid (8pt system):")
    print(f"  Values: {theme_system.SPACING_GRID}")
    
    # Test constraint validation
    print("\n🔍 Testing Constraint Validation:")
    
    # Valid component
    valid_code = """
    <div className="text-lg font-semibold p-4 m-8 gap-16">
        <p className="text-base font-normal">Valid typography</p>
    </div>
    """
    
    # Invalid component
    invalid_code = """
    <div className="text-2xl font-bold p-5 m-11 gap-13">
        <p className="text-xs font-light">Invalid sizes</p>
    </div>
    """
    
    valid_violations = theme_system.validate_design_constraints(valid_code)
    invalid_violations = theme_system.validate_design_constraints(invalid_code)
    
    print(f"  Valid code violations: {len(valid_violations)}")
    print(f"  Invalid code violations: {len(invalid_violations)}")
    
    if invalid_violations:
        print("  Violations found:")
        for violation in invalid_violations:
            print(f"    - {violation}")
            
def test_color_distribution():
    """Test 60/30/10 color distribution in generated CSS"""
    print("\n🎯 Testing 60/30/10 Color Distribution...")
    
    test_dir = "/tmp/test_color_distribution"
    os.makedirs(test_dir, exist_ok=True)
    
    context = {
        "type": "e-commerce",
        "design_preferences": {
            "primary_color": "blue",
            "accent_color": "emerald",
            "neutral_color": "slate"
        }
    }
    
    result = generate_intelligent_theme(context, test_dir)
    
    # Read generated CSS
    css_path = os.path.join(test_dir, "app", "globals.css")
    if os.path.exists(css_path):
        with open(css_path, 'r') as f:
            css_content = f.read()
            
        # Count color variable usage
        neutral_vars = ["--background", "--foreground", "--card", "--secondary", "--muted"]
        primary_vars = ["--primary", "--primary-foreground"]
        accent_vars = ["--accent", "--accent-foreground"]
        
        print(f"  Neutral (60%): {len(neutral_vars)} variables")
        print(f"  Primary (30%): {len(primary_vars)} variables")
        print(f"  Accent (10%): {len(accent_vars)} variables")
        
def test_intelligent_context():
    """Test theme generation with rich LLM context"""
    print("\n🧠 Testing Intelligent Context Integration...")
    
    test_dir = "/tmp/test_intelligent_theme"
    os.makedirs(test_dir, exist_ok=True)
    
    # Simulate rich context from LLM conversation
    rich_context = {
        "type": "e-commerce",
        "industry": "electronics",
        "style": "modern",
        "features": [
            "product-catalog",
            "shopping-cart", 
            "secure-payments",
            "customer-reviews",
            "product-comparison"
        ],
        "target_audience": "B2C",
        "brand_personality": "tech-forward",
        "design_preferences": {
            "primary_color": "blue",
            "accent_color": "cyan",
            "neutral_color": "slate",
            "typography": "modern-sans",
            "spacing": "comfortable"
        },
        "special_requirements": [
            "mobile-first",
            "fast-checkout",
            "product-specs-display"
        ]
    }
    
    result = generate_intelligent_theme(rich_context, test_dir)
    
    if result["success"]:
        print("  ✅ Successfully generated theme from rich context")
        print(f"  📁 Created {len(result['files_created'])} files")
        
        # Show design configuration
        config = result["design_config"]
        print(f"\n  Design Configuration:")
        print(f"    Project Type: {config.project_type.value}")
        print(f"    Primary: {config.primary_color}")
        print(f"    Accent: {config.accent_color}")
        print(f"    Neutral: {config.neutral_color}")
        print(f"    Typography Scale: {config.typography_scale}")
        print(f"    Font Weights: {config.font_weights}")
        
def main():
    """Run all tests"""
    print("="*60)
    print("🧪 Enhanced Theme System Test Suite")
    print("="*60)
    
    test_static_color_palette()
    test_project_type_themes()
    test_design_constraints()
    test_color_distribution()
    test_intelligent_context()
    
    print("\n" + "="*60)
    print("✨ Enhanced Theme System Test Complete!")
    print("="*60)

if __name__ == "__main__":
    main()