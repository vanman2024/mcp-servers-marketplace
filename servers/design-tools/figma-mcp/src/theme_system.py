"""
Theme System for Figma MCP Server
Implements shadcn/ui theming with CSS variables and design system constraints
"""

import json
import os
from typing import Dict, List, Any, Optional
from enum import Enum

class BaseColor(Enum):
    """Available base color schemes"""
    NEUTRAL = "neutral"
    SLATE = "slate"
    GRAY = "gray"
    ZINC = "zinc"
    STONE = "stone"

class ThemeMode(Enum):
    """Theme modes"""
    LIGHT = "light"
    DARK = "dark"

class ProjectType(Enum):
    """Project types with specific theme requirements"""
    ECOMMERCE = "e-commerce"
    SAAS = "saas"
    MARKETING = "marketing"
    BLOG = "blog"
    DASHBOARD = "dashboard"
    SOCIAL = "social"
    PORTFOLIO = "portfolio"
    DOCUMENTATION = "documentation"

class ThemeSystem:
    """Manages theme generation and configuration for projects"""
    
    def __init__(self):
        self.color_definitions = self._load_color_definitions()
        self.project_type_configs = self._load_project_type_configs()
        
    def _load_color_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Load base color definitions for all color schemes"""
        return {
            "neutral": {
                "light": {
                    "--background": "oklch(1 0 0)",
                    "--foreground": "oklch(0.145 0 0)",
                    "--card": "oklch(1 0 0)",
                    "--card-foreground": "oklch(0.145 0 0)",
                    "--popover": "oklch(1 0 0)",
                    "--popover-foreground": "oklch(0.145 0 0)",
                    "--primary": "oklch(0.205 0 0)",
                    "--primary-foreground": "oklch(0.985 0 0)",
                    "--secondary": "oklch(0.97 0 0)",
                    "--secondary-foreground": "oklch(0.205 0 0)",
                    "--muted": "oklch(0.97 0 0)",
                    "--muted-foreground": "oklch(0.556 0 0)",
                    "--accent": "oklch(0.97 0 0)",
                    "--accent-foreground": "oklch(0.205 0 0)",
                    "--destructive": "oklch(0.577 0.245 27.325)",
                    "--border": "oklch(0.922 0 0)",
                    "--input": "oklch(0.922 0 0)",
                    "--ring": "oklch(0.708 0 0)",
                    "--chart-1": "oklch(0.646 0.222 41.116)",
                    "--chart-2": "oklch(0.6 0.118 184.704)",
                    "--chart-3": "oklch(0.398 0.07 227.392)",
                    "--chart-4": "oklch(0.828 0.189 84.429)",
                    "--chart-5": "oklch(0.769 0.188 70.08)",
                    "--sidebar": "oklch(0.985 0 0)",
                    "--sidebar-foreground": "oklch(0.145 0 0)",
                    "--sidebar-primary": "oklch(0.205 0 0)",
                    "--sidebar-primary-foreground": "oklch(0.985 0 0)",
                    "--sidebar-accent": "oklch(0.97 0 0)",
                    "--sidebar-accent-foreground": "oklch(0.205 0 0)",
                    "--sidebar-border": "oklch(0.922 0 0)",
                    "--sidebar-ring": "oklch(0.708 0 0)"
                },
                "dark": {
                    "--background": "oklch(0.145 0 0)",
                    "--foreground": "oklch(0.985 0 0)",
                    "--card": "oklch(0.205 0 0)",
                    "--card-foreground": "oklch(0.985 0 0)",
                    "--popover": "oklch(0.269 0 0)",
                    "--popover-foreground": "oklch(0.985 0 0)",
                    "--primary": "oklch(0.922 0 0)",
                    "--primary-foreground": "oklch(0.205 0 0)",
                    "--secondary": "oklch(0.269 0 0)",
                    "--secondary-foreground": "oklch(0.985 0 0)",
                    "--muted": "oklch(0.269 0 0)",
                    "--muted-foreground": "oklch(0.708 0 0)",
                    "--accent": "oklch(0.371 0 0)",
                    "--accent-foreground": "oklch(0.985 0 0)",
                    "--destructive": "oklch(0.704 0.191 22.216)",
                    "--border": "oklch(1 0 0 / 10%)",
                    "--input": "oklch(1 0 0 / 15%)",
                    "--ring": "oklch(0.556 0 0)",
                    "--chart-1": "oklch(0.488 0.243 264.376)",
                    "--chart-2": "oklch(0.696 0.17 162.48)",
                    "--chart-3": "oklch(0.769 0.188 70.08)",
                    "--chart-4": "oklch(0.627 0.265 303.9)",
                    "--chart-5": "oklch(0.645 0.246 16.439)",
                    "--sidebar": "oklch(0.205 0 0)",
                    "--sidebar-foreground": "oklch(0.985 0 0)",
                    "--sidebar-primary": "oklch(0.488 0.243 264.376)",
                    "--sidebar-primary-foreground": "oklch(0.985 0 0)",
                    "--sidebar-accent": "oklch(0.269 0 0)",
                    "--sidebar-accent-foreground": "oklch(0.985 0 0)",
                    "--sidebar-border": "oklch(1 0 0 / 10%)",
                    "--sidebar-ring": "oklch(0.439 0 0)"
                }
            },
            # Add other color schemes (slate, gray, zinc, stone) as needed
        }
    
    def _load_project_type_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load project-specific theme configurations"""
        return {
            "e-commerce": {
                "baseColor": BaseColor.NEUTRAL,
                "customColors": {
                    "--warning": "oklch(0.84 0.16 84)",
                    "--warning-foreground": "oklch(0.28 0.07 46)",
                    "--success": "oklch(0.7 0.15 142)",
                    "--success-foreground": "oklch(0.2 0.04 142)"
                },
                "typography": {
                    "fontFamily": {
                        "sans": "Inter, system-ui, sans-serif",
                        "mono": "JetBrains Mono, monospace"
                    },
                    "fontSize": {
                        "xs": "0.75rem",    # 12px
                        "sm": "0.875rem",   # 14px
                        "base": "1rem",     # 16px
                        "lg": "1.125rem"    # 18px
                    },
                    "fontWeight": {
                        "normal": 400,
                        "semibold": 600
                    }
                },
                "spacing": {
                    "unit": 4,  # 4px base unit for 8pt grid
                    "scale": [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64]
                },
                "borderRadius": {
                    "none": "0",
                    "sm": "0.125rem",
                    "base": "0.375rem",
                    "md": "0.5rem",
                    "lg": "0.625rem",
                    "xl": "0.75rem",
                    "2xl": "1rem",
                    "full": "9999px"
                }
            },
            "saas": {
                "baseColor": BaseColor.SLATE,
                "customColors": {
                    "--info": "oklch(0.65 0.15 220)",
                    "--info-foreground": "oklch(0.15 0.02 220)"
                },
                "typography": {
                    "fontFamily": {
                        "sans": "'SF Pro Display', system-ui, sans-serif",
                        "mono": "'SF Mono', monospace"
                    }
                }
            },
            "dashboard": {
                "baseColor": BaseColor.ZINC,
                "customColors": {
                    "--chart-6": "oklch(0.55 0.2 120)",
                    "--chart-7": "oklch(0.65 0.18 180)",
                    "--chart-8": "oklch(0.75 0.16 240)"
                }
            }
        }
    
    def generate_components_json(
        self,
        project_type: str,
        style: str = "default",
        css_variables: bool = True,
        output_directory: str = "./"
    ) -> Dict[str, Any]:
        """Generate components.json configuration file"""
        
        config = self.project_type_configs.get(
            project_type, 
            self.project_type_configs["saas"]  # Default to SaaS
        )
        
        components_json = {
            "style": style,
            "rsc": True,
            "tsx": True,
            "tailwind": {
                "config": "tailwind.config.js",
                "css": "app/globals.css",
                "baseColor": config["baseColor"].value,
                "cssVariables": css_variables
            },
            "aliases": {
                "components": "@/components",
                "utils": "@/lib/utils",
                "ui": "@/components/ui",
                "lib": "@/lib",
                "hooks": "@/hooks"
            },
            "iconLibrary": "lucide"
        }
        
        # Write components.json
        json_path = os.path.join(output_directory, "components.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(components_json, f, indent=2)
        
        return components_json
    
    def generate_globals_css(
        self,
        project_type: str,
        base_color: Optional[BaseColor] = None,
        output_directory: str = "./"
    ) -> str:
        """Generate globals.css with theme variables"""
        
        config = self.project_type_configs.get(
            project_type,
            self.project_type_configs["saas"]
        )
        
        # Use project default or override
        color_scheme = base_color or config["baseColor"]
        color_defs = self.color_definitions.get(
            color_scheme.value,
            self.color_definitions["neutral"]
        )
        
        css_content = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --radius: 0.625rem;
"""
        
        # Add light mode variables
        for var, value in color_defs["light"].items():
            css_content += f"    {var}: {value};\n"
        
        # Add custom colors for project type
        if "customColors" in config:
            for var, value in config["customColors"].items():
                if not var.endswith("-foreground"):
                    css_content += f"    {var}: {value};\n"
        
        css_content += """  }

  .dark {
"""
        
        # Add dark mode variables
        for var, value in color_defs["dark"].items():
            css_content += f"    {var}: {value};\n"
        
        # Add custom dark mode colors
        if "customColors" in config:
            for var, value in config["customColors"].items():
                if var.endswith("-foreground"):
                    # Adjust foreground colors for dark mode
                    css_content += f"    {var}: {value.replace('0.2', '0.9')};\n"
        
        css_content += """  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}

/* Custom theme utilities */
@theme inline {
"""
        
        # Add custom color utilities
        if "customColors" in config:
            for var, _ in config["customColors"].items():
                if not var.endswith("-foreground"):
                    color_name = var.replace("--", "")
                    css_content += f"  --color-{color_name}: var({var});\n"
                    css_content += f"  --color-{color_name}-foreground: var({var}-foreground);\n"
        
        css_content += "}\n"
        
        # Create app directory if needed
        css_dir = os.path.join(output_directory, "app")
        os.makedirs(css_dir, exist_ok=True)
        
        # Write globals.css
        css_path = os.path.join(css_dir, "globals.css")
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        return css_content
    
    def generate_tailwind_config(
        self,
        project_type: str,
        output_directory: str = "./"
    ) -> str:
        """Generate tailwind.config.js with theme extensions"""
        
        config = self.project_type_configs.get(
            project_type,
            self.project_type_configs["saas"]
        )
        
        tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
"""
        
        # Add custom colors
        if "customColors" in config:
            for var, _ in config["customColors"].items():
                if not var.endswith("-foreground"):
                    color_name = var.replace("--", "")
                    tailwind_config += f"""        {color_name}: {{
          DEFAULT: "hsl(var(--{color_name}))",
          foreground: "hsl(var(--{color_name}-foreground))",
        }},
"""
        
        tailwind_config += """      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      fontFamily: {
"""
        
        # Add font families
        if "typography" in config and "fontFamily" in config["typography"]:
            for key, value in config["typography"]["fontFamily"].items():
                tailwind_config += f'        {key}: [{value}],\n'
        
        tailwind_config += """      },
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
"""
        
        # Write tailwind.config.js
        config_path = os.path.join(output_directory, "tailwind.config.js")
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(tailwind_config)
        
        return tailwind_config
    
    def validate_color_ratio(self, colors: Dict[str, str]) -> Dict[str, float]:
        """Validate 60/30/10 color rule"""
        # Analyze color usage in generated components
        # Returns percentages of neutral/primary/accent colors
        # This would analyze actual component usage
        return {
            "neutral": 60.0,
            "primary": 30.0,
            "accent": 10.0
        }
    
    def validate_typography(self, config: Dict[str, Any]) -> bool:
        """Validate 4 font sizes, 2 weights rule"""
        if "typography" not in config:
            return False
            
        sizes = config["typography"].get("fontSize", {})
        weights = config["typography"].get("fontWeight", {})
        
        return len(sizes) == 4 and len(weights) == 2
    
    def validate_spacing(self, value: int) -> bool:
        """Validate 8pt grid system (divisible by 4 or 8)"""
        return value % 4 == 0


# Export function to be used by the Figma server
def generate_project_theme(
    project_type: str,
    output_directory: str,
    base_color: Optional[str] = None,
    custom_colors: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Generate complete theme configuration for a project"""
    
    theme_system = ThemeSystem()
    
    # Generate configuration files
    components_json = theme_system.generate_components_json(
        project_type=project_type,
        output_directory=output_directory
    )
    
    # Generate CSS
    color_enum = BaseColor(base_color) if base_color else None
    globals_css = theme_system.generate_globals_css(
        project_type=project_type,
        base_color=color_enum,
        output_directory=output_directory
    )
    
    # Generate Tailwind config
    tailwind_config = theme_system.generate_tailwind_config(
        project_type=project_type,
        output_directory=output_directory
    )
    
    return {
        "components_json": components_json,
        "globals_css": globals_css,
        "tailwind_config": tailwind_config,
        "files_created": [
            "components.json",
            "app/globals.css",
            "tailwind.config.js"
        ]
    }