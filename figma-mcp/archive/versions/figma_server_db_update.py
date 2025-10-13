"""
Updates to integrate theme and navigation systems into the main Figma server
This file contains the updated functions to be added/modified in figma_server_db.py
"""

# Add these imports to the top of figma_server_db.py:
# from theme_system import generate_project_theme
# from navigation_system import generate_navigation

# Update the _generate_intelligent_app_structure function:
async def _generate_intelligent_app_structure(
    analysis: Dict[str, Any],
    output_directory: str,
    include_ui_library: bool,
    include_auth: bool,
    include_data_layer: bool
) -> Dict[str, Any]:
    """Generate complete app structure based on intelligent analysis"""
    
    files_created = []
    app_type = analysis["app_type"]
    required_blocks = analysis["required_blocks"]
    
    # Track blocks created for statistics
    total_blocks = 0
    
    # Create directory structure
    import os
    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(os.path.join(output_directory, "components"), exist_ok=True)
    os.makedirs(os.path.join(output_directory, "pages"), exist_ok=True)
    os.makedirs(os.path.join(output_directory, "hooks"), exist_ok=True)
    os.makedirs(os.path.join(output_directory, "lib"), exist_ok=True)
    os.makedirs(os.path.join(output_directory, "app"), exist_ok=True)  # For globals.css
    
    # ===== NEW: 1. Generate Theme Configuration First =====
    try:
        from theme_system import generate_project_theme
        
        logger.info(f"🎨 Generating theme configuration for {app_type} app...")
        theme_result = generate_project_theme(
            project_type=app_type,
            output_directory=output_directory,
            base_color=None,  # Use default for app type
            custom_colors=None
        )
        
        if theme_result and "files_created" in theme_result:
            for theme_file in theme_result["files_created"]:
                files_created.append({
                    "filename": theme_file,
                    "path": os.path.join(output_directory, theme_file),
                    "type": "theme-config",
                    "component_name": theme_file
                })
            logger.info(f"✅ Created theme configuration: {', '.join(theme_result['files_created'])}")
            
    except Exception as e:
        logger.warning(f"Failed to generate theme configuration: {e}")
    
    # ===== NEW: 2. Generate Navigation Components =====
    try:
        from navigation_system import generate_navigation
        
        logger.info(f"🧭 Generating navigation components for {app_type} app...")
        nav_components = await generate_navigation(
            app_type=app_type,
            output_directory=output_directory
        )
        
        if nav_components:
            files_created.extend(nav_components)
            total_blocks += len(nav_components)
            logger.info(f"✅ Created {len(nav_components)} navigation components")
            
    except Exception as e:
        logger.warning(f"Failed to generate navigation components: {e}")
    
    # 3. Create application blocks from database (existing code)
    try:
        # Get all relevant block types for this app
        block_types_needed = []
        for category in required_blocks.values():
            block_types_needed.extend(category)
        
        if block_types_needed:
            result = await create_application_blocks(
                app_type=app_type,
                output_directory=os.path.join(output_directory, "components"),
                block_types=list(set(block_types_needed))[:15],  # Limit to prevent overwhelming
                create_index=True
            )
            
            if result["success"]:
                files_created.extend(result["files_created"])
                total_blocks += result["total_blocks"]
                logger.info(f"✅ Created {result['total_blocks']} application blocks")
    
    except Exception as e:
        logger.warning(f"Failed to create application blocks: {e}")
    
    # 4. Generate intelligent component structure
    if include_ui_library:
        ui_components = await _generate_smart_ui_components(app_type, output_directory)
        files_created.extend(ui_components)
        total_blocks += len(ui_components)
    
    # 5. Create auth flows if needed
    if include_auth and ("auth" in analysis["detected_features"] or "auth" in required_blocks.get("features", [])):
        auth_components = await _generate_auth_components(app_type, output_directory)
        files_created.extend(auth_components)
        total_blocks += len(auth_components)
    
    # 6. Generate data layer if needed
    if include_data_layer:
        data_components = await _generate_data_layer(app_type, analysis, output_directory)
        files_created.extend(data_components)
        total_blocks += len(data_components)
    
    # 7. Generate pages that compose blocks into complete pages
    try:
        from page_generator import generate_pages
        
        # Get list of available blocks for page composition
        available_blocks = [file["filename"] for file in files_created if file.get("type") in ["block", "component", "navigation"]]
        
        pages = await generate_pages(
            app_type=app_type,
            output_directory=output_directory,
            available_blocks=available_blocks
        )
        
        files_created.extend(pages)
        total_blocks += len(pages)
        logger.info(f"✅ Generated {len(pages)} complete pages")
        
    except Exception as e:
        logger.warning(f"Failed to generate pages: {e}")
        # Continue without pages - better to have components than nothing
    
    # 8. Create app configuration and utilities
    config_files = await _generate_app_config(analysis, output_directory)
    files_created.extend(config_files)
    
    # Generate next steps and customization guidance
    next_steps = _generate_next_steps(analysis, total_blocks)
    customization_guide = _generate_customization_guide(analysis, files_created)
    
    # Estimate development time
    estimated_dev_time = _estimate_development_time(analysis, total_blocks)
    
    return {
        "files_created": files_created,
        "total_files": len(files_created),
        "total_blocks": total_blocks,
        "estimated_dev_time": estimated_dev_time,
        "next_steps": next_steps,
        "customization_guide": customization_guide
    }


# Add this new function to generate enhanced app config with theme support:
async def _generate_app_config(analysis: Dict[str, Any], output_directory: str) -> List[Dict[str, Any]]:
    """Generate app configuration files with theme support"""
    
    config_files = []
    app_type = analysis["app_type"]
    
    # 1. Package.json with all necessary dependencies
    package_json = {
        "name": f"{app_type}-app",
        "version": "0.1.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "lint": "next lint"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "next": "14.0.0",
            "@radix-ui/react-accordion": "^1.1.2",
            "@radix-ui/react-alert-dialog": "^1.0.5",
            "@radix-ui/react-dialog": "^1.0.5",
            "@radix-ui/react-dropdown-menu": "^2.0.6",
            "@radix-ui/react-label": "^2.0.2",
            "@radix-ui/react-popover": "^1.0.7",
            "@radix-ui/react-select": "^2.0.0",
            "@radix-ui/react-separator": "^1.0.3",
            "@radix-ui/react-slot": "^1.0.2",
            "@radix-ui/react-tabs": "^1.0.4",
            "@radix-ui/react-toast": "^1.1.5",
            "@radix-ui/react-tooltip": "^1.0.7",
            "class-variance-authority": "^0.7.0",
            "clsx": "^2.0.0",
            "lucide-react": "^0.292.0",
            "tailwind-merge": "^2.0.0",
            "tailwindcss-animate": "^1.0.7"
        },
        "devDependencies": {
            "@types/node": "^20.0.0",
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0",
            "autoprefixer": "^10.4.16",
            "eslint": "^8.0.0",
            "eslint-config-next": "14.0.0",
            "postcss": "^8.4.31",
            "tailwindcss": "^3.3.5",
            "typescript": "^5.0.0"
        }
    }
    
    # Add app-specific dependencies
    if app_type == "e-commerce":
        package_json["dependencies"]["@stripe/stripe-js"] = "^2.1.0"
        package_json["dependencies"]["swr"] = "^2.2.0"
    elif app_type == "dashboard":
        package_json["dependencies"]["recharts"] = "^2.9.0"
        package_json["dependencies"]["@tanstack/react-table"] = "^8.10.0"
    elif app_type == "blog":
        package_json["dependencies"]["@mdx-js/react"] = "^3.0.0"
        package_json["dependencies"]["gray-matter"] = "^4.0.3"
    
    # Write package.json
    package_path = os.path.join(output_directory, "package.json")
    with open(package_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(package_json, f, indent=2)
    
    config_files.append({
        "filename": "package.json",
        "path": package_path,
        "type": "config",
        "size": len(json.dumps(package_json, indent=2))
    })
    
    # 2. Next.js app directory structure
    app_dir = os.path.join(output_directory, "app")
    os.makedirs(app_dir, exist_ok=True)
    
    # Create layout.tsx with theme support
    layout_content = f'''import type {{ Metadata }} from 'next'
import {{ Inter }} from 'next/font/google'
import './globals.css'

const inter = Inter({{ subsets: ['latin'] }})

export const metadata: Metadata = {{
  title: '{analysis["app_title"]}',
  description: '{analysis["use_case"]}',
}}

export default function RootLayout({{
  children,
}}: {{
  children: React.ReactNode
}}) {{
  return (
    <html lang="en" className="h-full">
      <body className={{`${{inter.className}} min-h-full bg-background text-foreground`}}>
        {{children}}
      </body>
    </html>
  )
}}
'''
    
    layout_path = os.path.join(app_dir, "layout.tsx")
    with open(layout_path, 'w', encoding='utf-8') as f:
        f.write(layout_content)
    
    config_files.append({
        "filename": "app/layout.tsx",
        "path": layout_path,
        "type": "config",
        "size": len(layout_content)
    })
    
    # 3. PostCSS config
    postcss_config = """{
  "plugins": {
    "tailwindcss": {},
    "autoprefixer": {}
  }
}
"""
    postcss_path = os.path.join(output_directory, "postcss.config.json")
    with open(postcss_path, 'w', encoding='utf-8') as f:
        f.write(postcss_config)
    
    config_files.append({
        "filename": "postcss.config.json",
        "path": postcss_path,
        "type": "config",
        "size": len(postcss_config)
    })
    
    # 4. ESLint config
    eslint_config = """{
  "extends": ["next/core-web-vitals"]
}
"""
    eslint_path = os.path.join(output_directory, ".eslintrc.json")
    with open(eslint_path, 'w', encoding='utf-8') as f:
        f.write(eslint_config)
    
    config_files.append({
        "filename": ".eslintrc.json",
        "path": eslint_path,
        "type": "config",
        "size": len(eslint_config)
    })
    
    # 5. Next.js config
    next_config = """/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
}

module.exports = nextConfig
"""
    next_path = os.path.join(output_directory, "next.config.js")
    with open(next_path, 'w', encoding='utf-8') as f:
        f.write(next_config)
    
    config_files.append({
        "filename": "next.config.js",
        "path": next_path,
        "type": "config",
        "size": len(next_config)
    })
    
    # 6. README.md with theme instructions
    readme_content = f'''# {analysis["app_title"]}

{analysis["use_case"]}

## Generated with Figma MCP Server

This application was intelligently generated based on your description, including:

- ✅ Complete theme system with CSS variables
- ✅ Navigation components (sidebar, topbar, mobile navigation)
- ✅ {analysis["total_components"]} application-specific components
- ✅ {len(analysis["required_blocks"]["pages"])} pre-built pages
- ✅ Responsive design with mobile-first approach
- ✅ Tailwind CSS v4 with design system constraints

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) to see your app

## Theme Customization

The theme is configured in:
- `components.json` - shadcn/ui configuration
- `app/globals.css` - CSS variables for colors, spacing, etc.
- `tailwind.config.js` - Tailwind theme extensions

### Changing Colors

Edit the CSS variables in `app/globals.css`:

```css
:root {{
  --primary: oklch(0.205 0 0);  /* Change primary color */
  --secondary: oklch(0.97 0 0);  /* Change secondary color */
}}
```

### Design System Rules

This app follows strict design system constraints:
- **Typography**: 4 font sizes (xs, sm, base, lg), 2 weights (normal, semibold)
- **Spacing**: 8pt grid system (all spacing divisible by 4)
- **Colors**: 60/30/10 rule (60% neutral, 30% primary, 10% accent)

## Project Structure

```
{app_type}-app/
├── app/                    # Next.js app directory
│   ├── layout.tsx         # Root layout with theme
│   └── globals.css        # Global styles and CSS variables
├── components/            
│   ├── navigation/        # Navigation components
│   ├── ui/               # UI components
│   └── blocks/           # Application blocks
├── pages/                # Page components
├── lib/                  # Utilities and helpers
├── hooks/                # Custom React hooks
├── components.json       # shadcn/ui configuration
├── tailwind.config.js    # Tailwind configuration
└── package.json          # Project dependencies
```

## Next Steps

{chr(10).join(analysis.get("next_steps", ["Customize the theme", "Add your business logic", "Connect to your backend"]))}

## Development Time Estimate

Based on the complexity analysis: **{analysis.get("estimated_dev_time", "2-3 weeks")}**

---

Generated with ❤️ by Figma MCP Server
'''
    
    readme_path = os.path.join(output_directory, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    config_files.append({
        "filename": "README.md",
        "path": readme_path,
        "type": "docs",
        "size": len(readme_content)
    })
    
    return config_files


# Add this to the build_application_with_context function after retrieving context:
# (Around line where it calls _generate_intelligent_app_structure)

# In the section where analysis is enhanced with context:
if context:
    # ... existing context processing ...
    
    # Add theme preferences from context
    if context.get("ui_preferences"):
        ui_prefs = context["ui_preferences"]
        if isinstance(ui_prefs, dict):
            # Extract theme preferences
            if "style" in ui_prefs or "colors" in ui_prefs:
                analysis["theme_preferences"] = ui_prefs
                logger.info(f"📎 Applied theme preferences from context: {ui_prefs}")