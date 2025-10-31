"""
Enhanced Theme System with Static Color Palette and Design System Constraints
Implements the comprehensive design specifications from GitHub issue #44
"""

from typing import Dict, List, Optional, Any, Tuple
import os
import json
import re
from dataclasses import dataclass
from enum import Enum

# Complete Tailwind CSS v3 Color Palette (HSL format)
TAILWIND_COLOR_PALETTE = {
    "neutral": {
        "50": "0 0% 98%",
        "100": "0 0% 96%", 
        "200": "0 0% 90%",
        "300": "0 0% 83%",
        "400": "0 0% 64%",
        "500": "0 0% 45%",
        "600": "0 0% 32%",
        "700": "0 0% 25%",
        "800": "0 0% 15%",
        "900": "0 0% 9%",
        "950": "0 0% 4%"
    },
    "stone": {
        "50": "60 9% 98%",
        "100": "60 5% 96%",
        "200": "20 6% 90%",
        "300": "24 6% 83%",
        "400": "24 5% 64%",
        "500": "25 5% 45%",
        "600": "33 5% 32%",
        "700": "30 6% 25%",
        "800": "12 6% 15%",
        "900": "24 10% 10%",
        "950": "20 14% 4%"
    },
    "zinc": {
        "50": "0 0% 98%",
        "100": "240 5% 96%",
        "200": "240 6% 90%",
        "300": "240 5% 84%",
        "400": "240 5% 65%",
        "500": "240 4% 46%",
        "600": "240 5% 34%",
        "700": "240 5% 26%",
        "800": "240 4% 16%",
        "900": "240 6% 10%",
        "950": "240 10% 4%"
    },
    "slate": {
        "50": "210 40% 98%",
        "100": "210 40% 96%",
        "200": "214 32% 91%",
        "300": "213 27% 84%",
        "400": "215 20% 65%",
        "500": "215 16% 47%",
        "600": "215 19% 35%",
        "700": "215 25% 27%",
        "800": "217 33% 17%",
        "900": "222 47% 11%",
        "950": "229 84% 5%"
    },
    "gray": {
        "50": "210 20% 98%",
        "100": "220 14% 96%",
        "200": "220 13% 91%",
        "300": "216 12% 84%",
        "400": "218 11% 65%",
        "500": "220 9% 46%",
        "600": "215 14% 34%",
        "700": "217 19% 27%",
        "800": "215 28% 17%",
        "900": "221 39% 11%",
        "950": "224 71% 4%"
    },
    "red": {
        "50": "0 86% 97%",
        "100": "0 93% 94%",
        "200": "0 96% 89%",
        "300": "0 94% 82%",
        "400": "0 91% 71%",
        "500": "0 84% 60%",
        "600": "0 72% 51%",
        "700": "0 74% 42%",
        "800": "0 70% 35%",
        "900": "0 63% 31%",
        "950": "0 75% 15%"
    },
    "orange": {
        "50": "33 100% 96%",
        "100": "34 100% 92%",
        "200": "32 98% 83%",
        "300": "31 97% 72%",
        "400": "27 96% 61%",
        "500": "25 95% 53%",
        "600": "21 90% 48%",
        "700": "17 88% 40%",
        "800": "15 79% 34%",
        "900": "15 75% 28%",
        "950": "13 81% 15%"
    },
    "amber": {
        "50": "48 100% 96%",
        "100": "48 96% 89%",
        "200": "48 97% 77%",
        "300": "46 97% 65%",
        "400": "43 96% 56%",
        "500": "38 92% 50%",
        "600": "32 95% 44%",
        "700": "26 90% 37%",
        "800": "23 83% 31%",
        "900": "22 78% 26%",
        "950": "21 92% 14%"
    },
    "yellow": {
        "50": "55 92% 95%",
        "100": "55 97% 88%",
        "200": "53 98% 77%",
        "300": "50 98% 64%",
        "400": "48 96% 53%",
        "500": "45 93% 47%",
        "600": "41 96% 40%",
        "700": "35 92% 33%",
        "800": "32 81% 29%",
        "900": "28 73% 26%",
        "950": "26 83% 14%"
    },
    "lime": {
        "50": "78 92% 95%",
        "100": "80 89% 89%",
        "200": "81 88% 80%",
        "300": "82 85% 67%",
        "400": "83 78% 55%",
        "500": "84 81% 44%",
        "600": "85 85% 35%",
        "700": "86 78% 27%",
        "800": "86 69% 23%",
        "900": "88 61% 20%",
        "950": "89 80% 10%"
    },
    "green": {
        "50": "138 76% 97%",
        "100": "141 84% 93%",
        "200": "141 79% 85%",
        "300": "142 77% 73%",
        "400": "142 69% 58%",
        "500": "142 71% 45%",
        "600": "142 76% 36%",
        "700": "142 72% 29%",
        "800": "143 64% 24%",
        "900": "144 61% 20%",
        "950": "145 80% 10%"
    },
    "emerald": {
        "50": "152 81% 96%",
        "100": "149 80% 90%",
        "200": "152 76% 80%",
        "300": "156 72% 67%",
        "400": "158 64% 52%",
        "500": "160 84% 39%",
        "600": "161 94% 30%",
        "700": "163 94% 24%",
        "800": "163 88% 20%",
        "900": "164 86% 16%",
        "950": "166 91% 9%"
    },
    "teal": {
        "50": "166 76% 97%",
        "100": "167 85% 89%",
        "200": "168 84% 78%",
        "300": "171 77% 64%",
        "400": "172 66% 50%",
        "500": "173 80% 40%",
        "600": "175 84% 32%",
        "700": "175 77% 26%",
        "800": "176 69% 22%",
        "900": "176 61% 19%",
        "950": "177 87% 10%"
    },
    "cyan": {
        "50": "183 100% 96%",
        "100": "185 96% 90%",
        "200": "186 94% 82%",
        "300": "187 92% 69%",
        "400": "188 86% 53%",
        "500": "189 94% 43%",
        "600": "192 91% 36%",
        "700": "193 82% 31%",
        "800": "194 70% 27%",
        "900": "196 64% 24%",
        "950": "197 79% 15%"
    },
    "sky": {
        "50": "204 100% 97%",
        "100": "204 94% 94%",
        "200": "201 94% 86%",
        "300": "199 95% 74%",
        "400": "198 93% 60%",
        "500": "199 89% 48%",
        "600": "200 98% 39%",
        "700": "201 96% 32%",
        "800": "201 90% 27%",
        "900": "202 80% 24%",
        "950": "204 80% 16%"
    },
    "blue": {
        "50": "214 100% 97%",
        "100": "214 95% 93%",
        "200": "213 97% 87%",
        "300": "212 96% 78%",
        "400": "213 94% 68%",
        "500": "217 91% 60%",
        "600": "221 83% 53%",
        "700": "224 76% 48%",
        "800": "226 71% 40%",
        "900": "224 64% 33%",
        "950": "226 57% 21%"
    },
    "indigo": {
        "50": "226 100% 97%",
        "100": "226 100% 94%",
        "200": "228 96% 89%",
        "300": "230 94% 82%",
        "400": "234 89% 74%",
        "500": "239 84% 67%",
        "600": "243 75% 59%",
        "700": "245 58% 51%",
        "800": "244 55% 41%",
        "900": "242 47% 34%",
        "950": "244 47% 20%"
    },
    "violet": {
        "50": "250 100% 98%",
        "100": "251 91% 95%",
        "200": "251 95% 92%",
        "300": "252 95% 85%",
        "400": "255 92% 76%",
        "500": "258 90% 66%",
        "600": "262 83% 58%",
        "700": "263 70% 50%",
        "800": "263 69% 42%",
        "900": "264 67% 35%",
        "950": "265 68% 23%"
    },
    "purple": {
        "50": "270 100% 98%",
        "100": "269 100% 95%",
        "200": "269 100% 92%",
        "300": "269 97% 85%",
        "400": "270 95% 75%",
        "500": "271 91% 65%",
        "600": "271 81% 56%",
        "700": "272 72% 47%",
        "800": "273 67% 39%",
        "900": "274 66% 32%",
        "950": "274 87% 21%"
    },
    "fuchsia": {
        "50": "289 100% 98%",
        "100": "287 100% 95%",
        "200": "288 96% 91%",
        "300": "291 93% 83%",
        "400": "292 91% 73%",
        "500": "292 84% 61%",
        "600": "293 69% 49%",
        "700": "295 72% 40%",
        "800": "295 70% 33%",
        "900": "297 64% 28%",
        "950": "297 90% 16%"
    },
    "pink": {
        "50": "327 73% 97%",
        "100": "326 78% 95%",
        "200": "326 85% 90%",
        "300": "327 87% 82%",
        "400": "329 86% 70%",
        "500": "330 81% 60%",
        "600": "333 71% 51%",
        "700": "335 78% 42%",
        "800": "336 74% 35%",
        "900": "336 69% 30%",
        "950": "336 84% 17%"
    },
    "rose": {
        "50": "356 100% 97%",
        "100": "356 100% 95%",
        "200": "353 96% 90%",
        "300": "353 96% 82%",
        "400": "351 95% 71%",
        "500": "350 89% 60%",
        "600": "347 77% 50%",
        "700": "345 83% 41%",
        "800": "343 80% 35%",
        "900": "342 75% 30%",
        "950": "343 88% 16%"
    }
}

class ProjectType(Enum):
    """Supported project types with specific design needs"""
    ECOMMERCE = "e-commerce"
    DASHBOARD = "dashboard"
    SAAS = "saas"
    BLOG = "blog"
    MARKETING = "marketing"
    PORTFOLIO = "portfolio"
    SOCIAL = "social"
    FINTECH = "fintech"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"

@dataclass
class DesignSystemConfig:
    """Configuration for a project's design system"""
    project_type: ProjectType
    primary_color: str  # Tailwind color name (e.g., "blue")
    accent_color: str   # Tailwind color name (e.g., "emerald")
    neutral_color: str  # Tailwind color name (e.g., "slate")
    semantic_colors: Dict[str, str]  # success, warning, error colors
    typography_scale: List[str]  # 4 sizes only
    font_weights: List[str]  # 2 weights only
    spacing_scale: List[int]  # 8pt grid values
    border_radius: str  # rounded style preference
    shadow_style: str  # shadow intensity
    
class EnhancedThemeSystem:
    """
    Enhanced theme system with static color palette and design constraints
    Implements requirements from GitHub issue #44
    """
    
    # Design system constraints
    TYPOGRAPHY_SIZES = ["xs", "sm", "base", "lg"]  # 4 sizes only
    FONT_WEIGHTS = ["normal", "semibold"]  # 2 weights only
    SPACING_GRID = [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 72, 80, 96, 128]  # 8pt grid
    
    # Project-specific color recommendations
    PROJECT_COLOR_SCHEMES = {
        ProjectType.ECOMMERCE: {
            "primary": "blue",
            "accent": "emerald",
            "neutral": "slate",
            "semantic": {
                "success": "green",
                "warning": "amber",
                "error": "red",
                "info": "sky"
            }
        },
        ProjectType.DASHBOARD: {
            "primary": "indigo",
            "accent": "cyan",
            "neutral": "gray",
            "semantic": {
                "success": "emerald",
                "warning": "yellow",
                "error": "rose",
                "info": "blue"
            }
        },
        ProjectType.SAAS: {
            "primary": "violet",
            "accent": "teal",
            "neutral": "zinc",
            "semantic": {
                "success": "green",
                "warning": "orange",
                "error": "red",
                "info": "indigo"
            }
        },
        ProjectType.BLOG: {
            "primary": "stone",
            "accent": "amber",
            "neutral": "neutral",
            "semantic": {
                "success": "lime",
                "warning": "yellow",
                "error": "red",
                "info": "slate"
            }
        },
        ProjectType.MARKETING: {
            "primary": "purple",
            "accent": "pink",
            "neutral": "gray",
            "semantic": {
                "success": "teal",
                "warning": "amber",
                "error": "rose",
                "info": "violet"
            }
        },
        ProjectType.PORTFOLIO: {
            "primary": "neutral",
            "accent": "sky",
            "neutral": "stone",
            "semantic": {
                "success": "emerald",
                "warning": "amber",
                "error": "red",
                "info": "blue"
            }
        },
        ProjectType.SOCIAL: {
            "primary": "fuchsia",
            "accent": "cyan",
            "neutral": "slate",
            "semantic": {
                "success": "green",
                "warning": "yellow",
                "error": "pink",
                "info": "purple"
            }
        },
        ProjectType.FINTECH: {
            "primary": "blue",
            "accent": "green",
            "neutral": "gray",
            "semantic": {
                "success": "emerald",
                "warning": "amber",
                "error": "red",
                "info": "indigo"
            }
        },
        ProjectType.HEALTHCARE: {
            "primary": "teal",
            "accent": "sky",
            "neutral": "slate",
            "semantic": {
                "success": "green",
                "warning": "orange",
                "error": "rose",
                "info": "cyan"
            }
        },
        ProjectType.EDUCATION: {
            "primary": "indigo",
            "accent": "amber",
            "neutral": "stone",
            "semantic": {
                "success": "emerald",
                "warning": "yellow",
                "error": "red",
                "info": "blue"
            }
        }
    }
    
    def __init__(self):
        self.color_palette = TAILWIND_COLOR_PALETTE
        
    def get_design_system_config(
        self,
        project_type: str,
        custom_config: Optional[Dict[str, Any]] = None
    ) -> DesignSystemConfig:
        """
        Get design system configuration for a project type
        Can be overridden with custom configuration from LLM context
        """
        # Convert string to enum
        try:
            project_enum = ProjectType(project_type)
        except ValueError:
            project_enum = ProjectType.SAAS  # Default fallback
            
        # Get base configuration
        base_config = self.PROJECT_COLOR_SCHEMES.get(project_enum, self.PROJECT_COLOR_SCHEMES[ProjectType.SAAS])
        
        # Apply custom overrides if provided (from LLM context)
        if custom_config:
            if "primary_color" in custom_config:
                base_config["primary"] = custom_config["primary_color"]
            if "accent_color" in custom_config:
                base_config["accent"] = custom_config["accent_color"]
            if "neutral_color" in custom_config:
                base_config["neutral"] = custom_config["neutral_color"]
                
        return DesignSystemConfig(
            project_type=project_enum,
            primary_color=base_config["primary"],
            accent_color=base_config["accent"],
            neutral_color=base_config["neutral"],
            semantic_colors=base_config["semantic"],
            typography_scale=self.TYPOGRAPHY_SIZES,
            font_weights=self.FONT_WEIGHTS,
            spacing_scale=self.SPACING_GRID,
            border_radius="0.5rem",  # Default medium radius
            shadow_style="medium"
        )
        
    def generate_css_variables(self, config: DesignSystemConfig) -> str:
        """Generate CSS variables following shadcn/ui v4 patterns with OKLCH colors"""
        
        # Get color values from palette
        primary = self.color_palette[config.primary_color]
        accent = self.color_palette[config.accent_color]
        neutral = self.color_palette[config.neutral_color]
        
        # Convert HSL to OKLCH (simplified conversion for now)
        # In production, use proper color space conversion
        
        css_vars = f"""
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {{
  :root {{
    /* Border radius based on design system */
    --radius: {config.border_radius};
    
    /* Neutral colors (60% of design) */
    --background: {neutral["50"]};
    --foreground: {neutral["950"]};
    
    /* Card backgrounds */
    --card: {neutral["50"]};
    --card-foreground: {neutral["950"]};
    
    /* Popover */
    --popover: {neutral["50"]};
    --popover-foreground: {neutral["950"]};
    
    /* Primary colors (30% of design) */
    --primary: {primary["600"]};
    --primary-foreground: {primary["50"]};
    
    /* Secondary colors */
    --secondary: {neutral["100"]};
    --secondary-foreground: {neutral["900"]};
    
    /* Muted colors */
    --muted: {neutral["100"]};
    --muted-foreground: {neutral["500"]};
    
    /* Accent colors (10% of design) */
    --accent: {accent["500"]};
    --accent-foreground: {accent["50"]};
    
    /* Semantic colors */
    --destructive: {self.color_palette[config.semantic_colors["error"]]["500"]};
    --destructive-foreground: {self.color_palette[config.semantic_colors["error"]]["50"]};
    
    --success: {self.color_palette[config.semantic_colors["success"]]["500"]};
    --success-foreground: {self.color_palette[config.semantic_colors["success"]]["50"]};
    
    --warning: {self.color_palette[config.semantic_colors["warning"]]["500"]};
    --warning-foreground: {self.color_palette[config.semantic_colors["warning"]]["950"]};
    
    --info: {self.color_palette[config.semantic_colors["info"]]["500"]};
    --info-foreground: {self.color_palette[config.semantic_colors["info"]]["50"]};
    
    /* UI elements */
    --border: {neutral["200"]};
    --input: {neutral["200"]};
    --ring: {primary["500"]};
    
    /* Chart colors for data visualization */
    --chart-1: {primary["500"]};
    --chart-2: {accent["500"]};
    --chart-3: {self.color_palette[config.semantic_colors["info"]]["500"]};
    --chart-4: {self.color_palette[config.semantic_colors["warning"]]["500"]};
    --chart-5: {self.color_palette[config.semantic_colors["success"]]["500"]};
  }}
  
  .dark {{
    /* Dark mode with proper contrast ratios */
    --background: {neutral["950"]};
    --foreground: {neutral["50"]};
    
    --card: {neutral["900"]};
    --card-foreground: {neutral["50"]};
    
    --popover: {neutral["900"]};
    --popover-foreground: {neutral["50"]};
    
    --primary: {primary["500"]};
    --primary-foreground: {primary["950"]};
    
    --secondary: {neutral["800"]};
    --secondary-foreground: {neutral["50"]};
    
    --muted: {neutral["800"]};
    --muted-foreground: {neutral["400"]};
    
    --accent: {accent["600"]};
    --accent-foreground: {accent["50"]};
    
    --destructive: {self.color_palette[config.semantic_colors["error"]]["600"]};
    --destructive-foreground: {self.color_palette[config.semantic_colors["error"]]["50"]};
    
    --success: {self.color_palette[config.semantic_colors["success"]]["600"]};
    --success-foreground: {self.color_palette[config.semantic_colors["success"]]["50"]};
    
    --warning: {self.color_palette[config.semantic_colors["warning"]]["600"]};
    --warning-foreground: {self.color_palette[config.semantic_colors["warning"]]["50"]};
    
    --info: {self.color_palette[config.semantic_colors["info"]]["600"]};
    --info-foreground: {self.color_palette[config.semantic_colors["info"]]["50"]};
    
    --border: {neutral["800"]};
    --input: {neutral["800"]};
    --ring: {primary["400"]};
  }}
}}

@layer base {{
  * {{
    @apply border-border;
  }}
  body {{
    @apply bg-background text-foreground;
  }}
}}

/* Typography system - 4 sizes only */
.text-xs {{ @apply text-xs; }}    /* Small labels */
.text-sm {{ @apply text-sm; }}    /* Secondary text */
.text-base {{ @apply text-base; }} /* Body text */
.text-lg {{ @apply text-lg; }}    /* Headings */

/* Font weights - 2 only */
.font-normal {{ @apply font-normal; }}
.font-semibold {{ @apply font-semibold; }}

/* Spacing utilities following 8pt grid */
{self._generate_spacing_utilities(config.spacing_scale)}
"""
        return css_vars
        
    def _generate_spacing_utilities(self, spacing_scale: List[int]) -> str:
        """Generate spacing utilities that follow 8pt grid"""
        utilities = []
        for value in spacing_scale:
            px_value = value * 4  # Convert to pixels (assuming 1 unit = 4px)
            utilities.append(f".spacing-{value} {{ @apply p-{value}; }}")
        return "\n".join(utilities)
        
    def generate_tailwind_config(self, config: DesignSystemConfig) -> str:
        """Generate Tailwind configuration with theme constraints"""
        
        # Get font families based on project type
        font_sans = "Inter, system-ui, sans-serif"
        font_mono = "JetBrains Mono, monospace"
        
        if config.project_type in [ProjectType.BLOG, ProjectType.PORTFOLIO]:
            font_sans = "Georgia, serif"  # More editorial feel
        elif config.project_type == ProjectType.FINTECH:
            font_sans = "SF Pro Display, system-ui, sans-serif"  # More professional
            
        return f"""/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  darkMode: ["class"],
  content: [
    './pages/**/*.{{ts,tsx}}',
    './components/**/*.{{ts,tsx}}',
    './app/**/*.{{ts,tsx}}',
    './src/**/*.{{ts,tsx}}',
  ],
  theme: {{
    container: {{
      center: true,
      padding: "2rem",
      screens: {{
        "2xl": "1400px",
      }},
    }},
    extend: {{
      colors: {{
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {{
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        }},
        secondary: {{
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        }},
        destructive: {{
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        }},
        muted: {{
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        }},
        accent: {{
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        }},
        popover: {{
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        }},
        card: {{
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        }},
        success: {{
          DEFAULT: "hsl(var(--success))",
          foreground: "hsl(var(--success-foreground))",
        }},
        warning: {{
          DEFAULT: "hsl(var(--warning))",
          foreground: "hsl(var(--warning-foreground))",
        }},
        info: {{
          DEFAULT: "hsl(var(--info))",
          foreground: "hsl(var(--info-foreground))",
        }},
      }},
      borderRadius: {{
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      }},
      fontFamily: {{
        sans: ["{font_sans}"],
        mono: ["{font_mono}"],
      }},
      fontSize: {{
        xs: ['0.75rem', {{ lineHeight: '1rem' }}],
        sm: ['0.875rem', {{ lineHeight: '1.25rem' }}],
        base: ['1rem', {{ lineHeight: '1.5rem' }}],
        lg: ['1.125rem', {{ lineHeight: '1.75rem' }}],
      }},
      fontWeight: {{
        normal: '400',
        semibold: '600',
      }},
      spacing: {{
        {self._generate_spacing_config(config.spacing_scale)}
      }},
      keyframes: {{
        "accordion-down": {{
          from: {{ height: 0 }},
          to: {{ height: "var(--radix-accordion-content-height)" }},
        }},
        "accordion-up": {{
          from: {{ height: "var(--radix-accordion-content-height)" }},
          to: {{ height: 0 }},
        }},
      }},
      animation: {{
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      }},
    }},
  }},
  plugins: [require("tailwindcss-animate")],
}}
"""
        
    def _generate_spacing_config(self, spacing_scale: List[int]) -> str:
        """Generate Tailwind spacing configuration"""
        configs = []
        for value in spacing_scale:
            rem_value = value / 16  # Convert px to rem
            configs.append(f"'{value}': '{rem_value}rem'")
        return ",\n        ".join(configs)
        
    def generate_components_json(self, config: DesignSystemConfig) -> Dict[str, Any]:
        """Generate components.json for shadcn/ui CLI"""
        
        # Determine style based on project type
        style = "new-york"  # Default modern style
        if config.project_type in [ProjectType.PORTFOLIO, ProjectType.BLOG]:
            style = "default"  # More minimal style
            
        return {
            "$schema": "https://ui.shadcn.com/schema.json",
            "style": style,
            "rsc": True,
            "tsx": True,
            "tailwind": {
                "config": "tailwind.config.js",
                "css": "app/globals.css",
                "baseColor": config.neutral_color,
                "cssVariables": True
            },
            "aliases": {
                "components": "@/components",
                "utils": "@/lib/utils"
            }
        }
        
    def validate_design_constraints(self, component_code: str) -> List[str]:
        """
        Validate that generated code follows design system constraints
        Returns list of violations
        """
        violations = []
        
        # Check typography constraints
        font_sizes = ["text-xs", "text-sm", "text-base", "text-lg"]
        invalid_sizes = []
        for match in re.findall(r'text-\w+', component_code):
            if match.startswith("text-") and match not in font_sizes and not match.startswith("text-["):
                invalid_sizes.append(match)
        if invalid_sizes:
            violations.append(f"Invalid font sizes found: {', '.join(invalid_sizes)}. Use only: {', '.join(font_sizes)}")
            
        # Check font weight constraints
        font_weights = ["font-normal", "font-semibold"]
        invalid_weights = []
        for match in re.findall(r'font-\w+', component_code):
            if match not in font_weights and match != "font-sans" and match != "font-mono":
                invalid_weights.append(match)
        if invalid_weights:
            violations.append(f"Invalid font weights found: {', '.join(invalid_weights)}. Use only: {', '.join(font_weights)}")
            
        # Check spacing constraints (simplified check)
        spacing_pattern = r'(?:p|m|gap|space)-(\d+)'
        for match in re.findall(spacing_pattern, component_code):
            value = int(match)
            # Check if value follows 8pt grid (divisible by 2 for Tailwind units)
            if value > 0 and value % 2 != 0:
                violations.append(f"Spacing value {value} doesn't follow 8pt grid. Use multiples of 2.")
                
        return violations
        
    def generate_theme_from_context(
        self,
        project_context: Dict[str, Any],
        output_directory: str
    ) -> Dict[str, Any]:
        """
        Generate complete theme system from LLM-provided context
        This is the main entry point for intelligent theme generation
        """
        # Extract project type and preferences from context
        project_type = project_context.get("type", "saas")
        custom_config = {
            "primary_color": project_context.get("design_preferences", {}).get("primary_color"),
            "accent_color": project_context.get("design_preferences", {}).get("accent_color"),
            "neutral_color": project_context.get("design_preferences", {}).get("neutral_color")
        }
        
        # Remove None values
        custom_config = {k: v for k, v in custom_config.items() if v is not None}
        
        # Get design system configuration
        config = self.get_design_system_config(project_type, custom_config)
        
        # Generate all theme files
        files_created = []
        
        # 1. Generate globals.css
        css_content = self.generate_css_variables(config)
        css_path = os.path.join(output_directory, "app", "globals.css")
        os.makedirs(os.path.dirname(css_path), exist_ok=True)
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        files_created.append("app/globals.css")
        
        # 2. Generate tailwind.config.js
        tailwind_content = self.generate_tailwind_config(config)
        tailwind_path = os.path.join(output_directory, "tailwind.config.js")
        with open(tailwind_path, 'w', encoding='utf-8') as f:
            f.write(tailwind_content)
        files_created.append("tailwind.config.js")
        
        # 3. Generate components.json
        components_json = self.generate_components_json(config)
        components_path = os.path.join(output_directory, "components.json")
        with open(components_path, 'w', encoding='utf-8') as f:
            json.dump(components_json, f, indent=2)
        files_created.append("components.json")
        
        # 4. Generate design tokens file for reference
        design_tokens = {
            "project_type": project_type,
            "colors": {
                "primary": config.primary_color,
                "accent": config.accent_color,
                "neutral": config.neutral_color,
                "semantic": config.semantic_colors
            },
            "typography": {
                "sizes": config.typography_scale,
                "weights": config.font_weights
            },
            "spacing": {
                "scale": config.spacing_scale,
                "grid": "8pt"
            },
            "constraints": {
                "color_distribution": "60/30/10",
                "typography_rule": "4 sizes, 2 weights",
                "spacing_rule": "8pt grid system"
            }
        }
        
        tokens_path = os.path.join(output_directory, "design-tokens.json")
        with open(tokens_path, 'w', encoding='utf-8') as f:
            json.dump(design_tokens, f, indent=2)
        files_created.append("design-tokens.json")
        
        return {
            "success": True,
            "files_created": files_created,
            "design_config": config,
            "design_tokens": design_tokens
        }


# Export convenience function for direct use
def generate_intelligent_theme(
    project_context: Dict[str, Any],
    output_directory: str
) -> Dict[str, Any]:
    """
    Main entry point for generating theme from LLM context
    
    Args:
        project_context: Rich context from LLM conversation including:
            - type: Project type (e-commerce, dashboard, etc.)
            - industry: Specific industry context
            - design_preferences: Color and style preferences
            - features: List of features needed
            - target_audience: B2B, B2C, etc.
        output_directory: Where to create theme files
        
    Returns:
        Result with files created and design configuration
    """
    theme_system = EnhancedThemeSystem()
    return theme_system.generate_theme_from_context(project_context, output_directory)


# For backward compatibility with existing code
def generate_project_theme(
    project_type: str,
    output_directory: str,
    base_color: Optional[str] = None,
    custom_colors: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Legacy function for backward compatibility"""
    context = {
        "type": project_type,
        "design_preferences": {}
    }
    
    if base_color:
        context["design_preferences"]["primary_color"] = base_color
    if custom_colors:
        context["design_preferences"].update(custom_colors)
        
    return generate_intelligent_theme(context, output_directory)