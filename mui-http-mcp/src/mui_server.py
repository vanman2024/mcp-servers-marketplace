#!/usr/bin/env python3
import os
import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from fastmcp import FastMCP
from fastmcp.server.context import Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("MUI Component Generator")

# ===================================================================
# CONFIGURATION & TEMPLATES
# ===================================================================

# MUI Component Templates
MUI_TEMPLATES = {
    "button": {
        "component": "Button",
        "imports": ["Button"],
        "props": ["variant", "color", "size", "disabled", "startIcon", "endIcon", "onClick"],
        "variants": ["text", "outlined", "contained"],
        "colors": ["primary", "secondary", "error", "warning", "info", "success"],
        "sizes": ["small", "medium", "large"],
        "description": "Interactive button component with various styles and icons"
    },
    "card": {
        "component": "Card",
        "imports": ["Card", "CardContent", "CardActions", "CardHeader", "CardMedia"],
        "props": ["elevation", "variant", "sx"],
        "variants": ["elevation", "outlined"],
        "description": "Container component for displaying content in a card format"
    },
    "textfield": {
        "component": "TextField",
        "imports": ["TextField"],
        "props": ["variant", "size", "color", "disabled", "required", "error", "helperText", "label", "placeholder", "type"],
        "variants": ["outlined", "filled", "standard"],
        "sizes": ["small", "medium"],
        "description": "Input field component with various styles and validation"
    },
    "select": {
        "component": "Select",
        "imports": ["Select", "MenuItem", "FormControl", "InputLabel"],
        "props": ["variant", "size", "color", "disabled", "required", "error", "multiple"],
        "description": "Dropdown selection component with customizable options"
    },
    "dialog": {
        "component": "Dialog",
        "imports": ["Dialog", "DialogTitle", "DialogContent", "DialogActions", "DialogContentText"],
        "props": ["open", "onClose", "maxWidth", "fullWidth", "fullScreen", "scroll"],
        "maxWidths": ["xs", "sm", "md", "lg", "xl"],
        "description": "Modal dialog component for displaying content over the main interface"
    },
    "appbar": {
        "component": "AppBar",
        "imports": ["AppBar", "Toolbar", "Typography", "IconButton", "MenuIcon"],
        "props": ["position", "color", "elevation", "enableColorOnDark"],
        "positions": ["fixed", "absolute", "sticky", "static", "relative"],
        "description": "Top navigation bar component with toolbar and menu items"
    },
    "table": {
        "component": "Table",
        "imports": ["Table", "TableBody", "TableCell", "TableContainer", "TableHead", "TableRow", "Paper"],
        "props": ["size", "stickyHeader", "padding"],
        "sizes": ["small", "medium"],
        "description": "Data table component with sortable columns and pagination support"
    },
    "form": {
        "component": "Form",
        "imports": ["Box", "TextField", "Button", "FormControl", "FormLabel", "FormHelperText"],
        "props": ["spacing", "direction", "alignItems", "justifyContent"],
        "directions": ["row", "column"],
        "description": "Form container with validation and submission handling"
    },
    "chip": {
        "component": "Chip",
        "imports": ["Chip"],
        "props": ["label", "variant", "color", "size", "clickable", "deletable", "icon", "deleteIcon"],
        "variants": ["filled", "outlined"],
        "sizes": ["small", "medium"],
        "description": "Compact component for displaying tags, categories, or actions"
    },
    "avatar": {
        "component": "Avatar",
        "imports": ["Avatar"],
        "props": ["alt", "src", "variant", "sx"],
        "variants": ["circular", "rounded", "square"],
        "description": "User profile image or initials display component"
    }
}

# MUI Theme Presets
THEME_PRESETS = {
    "light": {
        "palette": {
            "mode": "light",
            "primary": {"main": "#1976d2"},
            "secondary": {"main": "#dc004e"},
            "background": {"default": "#ffffff", "paper": "#f5f5f5"}
        },
        "typography": {"fontFamily": "'Roboto', 'Helvetica', 'Arial', sans-serif"}
    },
    "dark": {
        "palette": {
            "mode": "dark",
            "primary": {"main": "#90caf9"},
            "secondary": {"main": "#f48fb1"},
            "background": {"default": "#121212", "paper": "#1e1e1e"}
        },
        "typography": {"fontFamily": "'Roboto', 'Helvetica', 'Arial', sans-serif"}
    },
    "corporate": {
        "palette": {
            "mode": "light",
            "primary": {"main": "#2e3440"},
            "secondary": {"main": "#5e81ac"},
            "background": {"default": "#ffffff", "paper": "#eceff4"}
        },
        "typography": {"fontFamily": "'Inter', 'Segoe UI', sans-serif"}
    },
    "modern": {
        "palette": {
            "mode": "light",
            "primary": {"main": "#6366f1"},
            "secondary": {"main": "#f59e0b"},
            "background": {"default": "#fafafa", "paper": "#ffffff"}
        },
        "typography": {"fontFamily": "'Poppins', 'system-ui', sans-serif"}
    },
    "minimal": {
        "palette": {
            "mode": "light",
            "primary": {"main": "#000000"},
            "secondary": {"main": "#666666"},
            "background": {"default": "#ffffff", "paper": "#f8f9fa"}
        },
        "typography": {"fontFamily": "'SF Pro Display', 'system-ui', sans-serif"}
    }
}

# Layout Templates
LAYOUT_PATTERNS = {
    "dashboard": {
        "sections": ["header", "sidebar", "main", "footer"],
        "responsive_breakpoints": {"sidebar": "md", "grid": "sm"},
        "default_spacing": 3
    },
    "landing": {
        "sections": ["hero", "features", "about", "contact"],
        "responsive_breakpoints": {"grid": "md"},
        "default_spacing": 4
    },
    "form": {
        "sections": ["header", "form", "actions"],
        "responsive_breakpoints": {"container": "sm"},
        "default_spacing": 2
    },
    "table": {
        "sections": ["toolbar", "table", "pagination"],
        "responsive_breakpoints": {"table": "md"},
        "default_spacing": 2
    }
}

# ===================================================================
# TOOLS - COMPONENT GENERATION
# ===================================================================

@mcp.tool()
async def generate_mui_component(
    component_type: str,
    name: str,
    props: Optional[Dict[str, Any]] = None,
    children: Optional[str] = None,
    typescript: bool = True,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Generate a MUI component with specified properties
    
    Args:
        component_type: Type of MUI component (button, card, textfield, etc.)
        name: Name for the component
        props: Component properties and values
        children: Component children/content
        typescript: Generate TypeScript component
        ctx: Context for logging
    
    Returns:
        Generated component code and metadata
    """
    try:
        if ctx:
            await ctx.info(f"Generating MUI {component_type} component: {name}")
        
        if component_type not in MUI_TEMPLATES:
            available = ", ".join(MUI_TEMPLATES.keys())
            raise ValueError(f"Unknown component type '{component_type}'. Available: {available}")
        
        template = MUI_TEMPLATES[component_type]
        props = props or {}
        
        # Generate imports
        imports = template["imports"]
        import_line = f"import {{ {', '.join(imports)} }} from '@mui/material';"
        
        # Generate component props
        prop_strings = []
        for prop, value in props.items():
            if isinstance(value, str):
                prop_strings.append(f'{prop}="{value}"')
            elif isinstance(value, bool):
                prop_strings.append(f'{prop}={str(value).lower()}')
            else:
                prop_strings.append(f'{prop}={value}')
        
        props_string = " ".join(prop_strings)
        
        # Generate component code
        if typescript:
            file_ext = "tsx"
            interface_name = f"{name}Props"
            component_code = f"""import React from 'react';
{import_line}

interface {interface_name} {{
  // Add your props here
}}

const {name}: React.FC<{interface_name}> = (props) => {{
  return (
    <{template["component"]} {props_string}>
      {children or "// Add content here"}
    </{template["component"]}>
  );
}};

export default {name};"""
        else:
            file_ext = "jsx"
            component_code = f"""import React from 'react';
{import_line}

const {name} = (props) => {{
  return (
    <{template["component"]} {props_string}>
      {children or "// Add content here"}
    </{template["component"]}>
  );
}};

export default {name};"""
        
        result = {
            "success": True,
            "component_name": name,
            "component_type": component_type,
            "code": component_code,
            "file_name": f"{name}.{file_ext}",
            "imports": imports,
            "props": props,
            "template_info": template,
            "timestamp": datetime.now().isoformat()
        }
        
        if ctx:
            await ctx.info(f"Generated {name} component successfully")
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating MUI component: {e}")
        if ctx:
            await ctx.error(f"Component generation failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "component_type": component_type,
            "name": name
        }

@mcp.tool()
async def generate_mui_form(
    form_name: str,
    fields: List[Dict[str, Any]],
    validation: bool = True,
    submit_action: str = "handleSubmit",
    layout: str = "vertical",
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Generate a complete MUI form with validation
    
    Args:
        form_name: Name for the form component
        fields: List of field definitions with type, name, label, required
        validation: Include form validation
        submit_action: Name of submit handler function
        layout: Form layout (vertical, horizontal, grid)
        ctx: Context for logging
    
    Returns:
        Generated form component code
    """
    try:
        if ctx:
            await ctx.info(f"Generating MUI form: {form_name}")
        
        # Generate field components
        field_components = []
        for field in fields:
            field_type = field.get("type", "text")
            field_name = field.get("name", "field")
            label = field.get("label", field_name.title())
            required = field.get("required", False)
            
            if field_type == "select":
                options = field.get("options", [])
                field_components.append(f"""
          <FormControl fullWidth margin="normal" {'required' if required else ''}>
            <InputLabel>{label}</InputLabel>
            <Select
              name="{field_name}"
              label="{label}"
              value={{formData.{field_name}}}
              onChange={{handleChange}}
            >
              {chr(10).join([f'<MenuItem value="{opt}">{opt}</MenuItem>' for opt in options])}
            </Select>
          </FormControl>""")
            else:
                field_components.append(f"""
          <TextField
            fullWidth
            margin="normal"
            name="{field_name}"
            label="{label}"
            type="{field_type}"
            {'required' if required else ''}
            value={{formData.{field_name}}}
            onChange={{handleChange}}
          />""")
        
        # Generate form code
        imports = ["Box", "Button", "TextField", "Typography"]
        if any(field.get("type") == "select" for field in fields):
            imports.extend(["FormControl", "InputLabel", "Select", "MenuItem"])
        if layout == "grid":
            imports.append("Grid")
        
        form_code = f"""import React, {{ useState }} from 'react';
import {{ {', '.join(imports)} }} from '@mui/material';

interface {form_name}Data {{
{chr(10).join([f'  {field["name"]}: string;' for field in fields])}
}}

const {form_name} = () => {{
  const [formData, setFormData] = useState<{form_name}Data>({{{chr(10).join([f'    {field["name"]}: "",' for field in fields])}
  }});

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {{
    const {{ name, value }} = event.target;
    setFormData(prev => ({{
      ...prev,
      [name]: value
    }}));
  }};

  const {submit_action} = (event: React.FormEvent) => {{
    event.preventDefault();
    console.log('Form submitted:', formData);
    // Add your form submission logic here
  }};

  return (
    <Box component="form" onSubmit={{{submit_action}}} sx={{ maxWidth: 600, mx: 'auto', p: 3 }}>
      <Typography variant="h5" gutterBottom>
        {form_name.replace('Form', '')} Form
      </Typography>
      {''.join(field_components)}
      <Button
        type="submit"
        variant="contained"
        fullWidth
        sx={{ mt: 3 }}
      >
        Submit
      </Button>
    </Box>
  );
}};

export default {form_name};"""
        
        result = {
            "success": True,
            "form_name": form_name,
            "code": form_code,
            "file_name": f"{form_name}.tsx",
            "fields": fields,
            "validation": validation,
            "submit_action": submit_action,
            "layout": layout,
            "timestamp": datetime.now().isoformat()
        }
        
        if ctx:
            await ctx.info(f"Generated form {form_name} successfully")
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating MUI form: {e}")
        if ctx:
            await ctx.error(f"Form generation failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "form_name": form_name
        }

# ===================================================================
# TOOLS - THEMING & STYLING
# ===================================================================

@mcp.tool()
async def create_mui_theme(
    theme_name: str,
    preset: Optional[str] = None,
    custom_palette: Optional[Dict[str, Any]] = None,
    typography: Optional[Dict[str, Any]] = None,
    spacing: Optional[int] = None,
    breakpoints: Optional[Dict[str, Any]] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Create a custom MUI theme with advanced customization options
    
    Args:
        theme_name: Name for the theme
        preset: Use a preset theme (light, dark, corporate, modern, minimal)
        custom_palette: Custom palette colors
        typography: Typography settings
        spacing: Spacing unit (default 8)
        breakpoints: Custom breakpoint values
        ctx: Context for logging
    
    Returns:
        Generated theme configuration and code
    """
    try:
        if ctx:
            await ctx.info(f"Creating MUI theme: {theme_name}")
        
        # Start with preset or default
        if preset and preset in THEME_PRESETS:
            theme_config = THEME_PRESETS[preset].copy()
        else:
            theme_config = THEME_PRESETS["light"].copy()
        
        # Apply customizations
        if custom_palette:
            theme_config["palette"].update(custom_palette)
        
        if typography:
            theme_config["typography"] = typography
        
        if spacing:
            theme_config["spacing"] = spacing
        
        if breakpoints:
            theme_config["breakpoints"] = {"values": breakpoints}
        
        # Generate theme code
        theme_code = f"""import {{ createTheme }} from '@mui/material/styles';

const {theme_name} = createTheme({json.dumps(theme_config, indent=2)});

export default {theme_name};

// Usage example:
// import {{ ThemeProvider }} from '@mui/material/styles';
// 
// function App() {{
//   return (
//     <ThemeProvider theme={{{theme_name}}}>
//       {{/* Your app components */}}
//     </ThemeProvider>
//   );
// }}"""
        
        result = {
            "success": True,
            "theme_name": theme_name,
            "code": theme_code,
            "file_name": f"{theme_name}.ts",
            "config": theme_config,
            "preset_used": preset,
            "timestamp": datetime.now().isoformat()
        }
        
        if ctx:
            await ctx.info(f"Created theme {theme_name} successfully")
        
        return result
        
    except Exception as e:
        logger.error(f"Error creating MUI theme: {e}")
        if ctx:
            await ctx.error(f"Theme creation failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "theme_name": theme_name
        }

# ===================================================================
# TOOLS - LAYOUT & STRUCTURE
# ===================================================================

@mcp.tool()
async def generate_mui_layout(
    layout_type: str,
    name: str,
    sections: List[str],
    responsive: bool = True,
    sidebar: bool = False,
    navigation: bool = True,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Generate a complete MUI layout component with navigation and responsive design
    
    Args:
        layout_type: Type of layout (dashboard, landing, form, table)
        name: Name for the layout component
        sections: List of section names to include
        responsive: Make layout responsive
        sidebar: Include sidebar navigation
        navigation: Include top navigation
        ctx: Context for logging
    
    Returns:
        Generated layout component code
    """
    try:
        if ctx:
            await ctx.info(f"Generating MUI {layout_type} layout: {name}")
        
        # Base imports
        imports = ["Box", "Container", "Grid", "Paper", "Typography"]
        if sidebar:
            imports.extend(["Drawer", "List", "ListItem", "ListItemText", "ListItemIcon"])
        if navigation:
            imports.extend(["AppBar", "Toolbar", "IconButton", "MenuIcon"])
        
        # Generate layout pattern
        pattern = LAYOUT_PATTERNS.get(layout_type, LAYOUT_PATTERNS["dashboard"])
        
        # Generate sections
        section_components = []
        for section in sections:
            section_components.append(f"""
            <Grid item xs={12} md={6} lg={4}>
              <Paper sx={{ p: {pattern['default_spacing']}, minHeight: 200 }}>
                <Typography variant="h6" gutterBottom>
                  {section.replace('_', ' ').title()}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {section} content goes here. Add your components and functionality.
                </Typography>
              </Paper>
            </Grid>""")
        
        # Generate sidebar content
        sidebar_content = f"""
        <List>
          {chr(10).join([f'<ListItem button><ListItemText primary="{section}" /></ListItem>' for section in sections])}
        </List>""" if sidebar else ""
        
        # Generate layout code
        layout_code = f"""import React from 'react';
import {{ {', '.join(imports)} }} from '@mui/material';

const {name} = () => {{
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      {f'''<Drawer
        variant="permanent"
        sx={{
          width: 240,
          flexShrink: 0,
          display: {{ xs: 'none', md: 'block' }},
          '& .MuiDrawer-paper': {{
            width: 240,
            boxSizing: 'border-box',
          }},
        }}
      >
        {sidebar_content}
      </Drawer>''' if sidebar else ''}
      
      <Box component="main" sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        {f'''<AppBar position="sticky" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
          <Toolbar>
            <Typography variant="h6" noWrap component="div">
              {name.replace('Layout', '')} Dashboard
            </Typography>
          </Toolbar>
        </AppBar>''' if navigation else ''}
        
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
          <Grid container spacing={pattern['default_spacing']}>
            <Grid item xs={12}>
              <Typography variant="h4" gutterBottom>
                Welcome to {name.replace('Layout', '')}
              </Typography>
            </Grid>
            {''.join(section_components)}
          </Grid>
        </Container>
      </Box>
    </Box>
  );
}};

export default {name};"""
        
        result = {
            "success": True,
            "layout_name": name,
            "layout_type": layout_type,
            "code": layout_code,
            "file_name": f"{name}.tsx",
            "sections": sections,
            "responsive": responsive,
            "sidebar": sidebar,
            "navigation": navigation,
            "pattern": pattern,
            "imports": imports,
            "timestamp": datetime.now().isoformat()
        }
        
        if ctx:
            await ctx.info(f"Generated {layout_type} layout {name} successfully")
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating MUI layout: {e}")
        if ctx:
            await ctx.error(f"Layout generation failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "layout_name": name,
            "layout_type": layout_type
        }

# ===================================================================
# RESOURCES - TEMPLATES & DOCUMENTATION
# ===================================================================

@mcp.resource("mui://templates")
def get_mui_templates() -> Dict[str, Any]:
    """Get comprehensive MUI component templates with all properties and usage examples"""
    return {
        "templates": MUI_TEMPLATES,
        "total_components": len(MUI_TEMPLATES),
        "categories": {
            "input": ["textfield", "select", "form"],
            "display": ["card", "chip", "avatar", "table"],
            "navigation": ["appbar", "dialog"],
            "feedback": ["button"]
        },
        "description": "Complete MUI component templates with properties, variants, and implementation details"
    }

@mcp.resource("mui://themes")
def get_mui_themes() -> Dict[str, Any]:
    """Get comprehensive MUI theme presets and customization options"""
    return {
        "presets": THEME_PRESETS,
        "total_presets": len(THEME_PRESETS),
        "customization_options": [
            "palette", "typography", "spacing", "breakpoints", 
            "shadows", "transitions", "components"
        ],
        "usage_patterns": {
            "basic": "Use preset themes for quick setup",
            "custom": "Extend presets with custom palette and typography",
            "advanced": "Full theme customization with component overrides"
        },
        "description": "Available MUI theme presets and customization guide"
    }

@mcp.resource("mui://patterns")
def get_layout_patterns() -> Dict[str, Any]:
    """Get layout patterns and responsive design guidelines"""
    return {
        "patterns": LAYOUT_PATTERNS,
        "responsive_guidelines": {
            "mobile_first": "Start with mobile layout, enhance for larger screens",
            "breakpoints": "Use xs, sm, md, lg, xl breakpoints strategically",
            "grid_system": "Leverage 12-column grid for consistent layouts"
        },
        "best_practices": [
            "Use Container for consistent max-width",
            "Apply proper spacing with theme.spacing()",
            "Implement sidebar collapse on mobile",
            "Ensure touch-friendly navigation"
        ],
        "description": "Layout patterns and responsive design best practices"
    }

@mcp.resource("mui://examples/{component_type}")
def get_component_example(component_type: str) -> Dict[str, Any]:
    """
    Get comprehensive usage examples for specific MUI component type
    
    Args:
        component_type: Type of component to get examples for
    """
    if component_type not in MUI_TEMPLATES:
        return {
            "error": f"Unknown component type: {component_type}",
            "available": list(MUI_TEMPLATES.keys()),
            "suggestion": "Use mui://templates resource to see all available components"
        }
    
    template = MUI_TEMPLATES[component_type]
    
    comprehensive_examples = {
        "button": {
            "basic": '<Button variant="contained" color="primary">Click Me</Button>',
            "with_icon": '<Button startIcon={<SaveIcon />} variant="outlined">Save</Button>',
            "loading": '<Button loading disabled>Processing...</Button>',
            "sizes": {
                "small": '<Button size="small">Small</Button>',
                "medium": '<Button size="medium">Medium</Button>',
                "large": '<Button size="large">Large</Button>'
            }
        },
        "textfield": {
            "basic": '<TextField label="Name" variant="outlined" fullWidth />',
            "with_validation": '<TextField label="Email" type="email" required error={!!errors.email} helperText={errors.email} />',
            "multiline": '<TextField label="Description" multiline rows={4} />',
            "with_icon": '<TextField label="Search" InputProps={{ startAdornment: <SearchIcon /> }} />'
        },
        "card": {
            "basic": """<Card>
  <CardContent>
    <Typography variant="h5" component="div">Card Title</Typography>
    <Typography variant="body2" color="text.secondary">Card content goes here</Typography>
  </CardContent>
  <CardActions>
    <Button size="small">Learn More</Button>
  </CardActions>
</Card>""",
            "with_image": """<Card sx={{ maxWidth: 345 }}>
  <CardMedia component="img" height="140" image="/image.jpg" alt="description" />
  <CardContent>
    <Typography gutterBottom variant="h5">Title</Typography>
    <Typography variant="body2" color="text.secondary">Description</Typography>
  </CardContent>
</Card>"""
        },
        "form": {
            "login": """<Box component="form" sx={{ mt: 1 }}>
  <TextField margin="normal" required fullWidth label="Email" type="email" />
  <TextField margin="normal" required fullWidth label="Password" type="password" />
  <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
    Sign In
  </Button>
</Box>""",
            "contact": """<Grid container spacing={2}>
  <Grid item xs={12} sm={6}>
    <TextField required fullWidth label="First Name" />
  </Grid>
  <Grid item xs={12} sm={6}>
    <TextField required fullWidth label="Last Name" />
  </Grid>
  <Grid item xs={12}>
    <TextField required fullWidth label="Email" type="email" />
  </Grid>
  <Grid item xs={12}>
    <TextField fullWidth label="Message" multiline rows={4} />
  </Grid>
</Grid>"""
        }
    }
    
    return {
        "component_type": component_type,
        "template": template,
        "examples": comprehensive_examples.get(component_type, {
            "basic": f"<{template['component']} />",
            "with_props": f"<{template['component']} variant=\"outlined\" color=\"primary\" />"
        }),
        "props": template.get("props", []),
        "variants": template.get("variants", []),
        "colors": template.get("colors", []),
        "sizes": template.get("sizes", []),
        "description": template.get("description", f"MUI {component_type} component"),
        "accessibility": {
            "aria_labels": "Use aria-label for screen readers",
            "keyboard_navigation": "Ensure proper tab order and keyboard interactions",
            "color_contrast": "Maintain sufficient color contrast ratios"
        }
    }

@mcp.resource("mui://best-practices")
def get_best_practices() -> Dict[str, Any]:
    """Get MUI development best practices and guidelines"""
    return {
        "component_development": {
            "typescript": "Always use TypeScript for better type safety",
            "props_interface": "Define clear prop interfaces for components",
            "default_props": "Provide sensible default props",
            "forwarded_refs": "Use forwardRef for component composition"
        },
        "theming": {
            "consistent_spacing": "Use theme.spacing() for consistent spacing",
            "color_palette": "Stick to theme palette colors",
            "responsive_typography": "Use responsive typography variants",
            "dark_mode": "Support both light and dark themes"
        },
        "performance": {
            "lazy_loading": "Lazy load heavy components",
            "memoization": "Use React.memo for expensive components",
            "bundle_size": "Import only needed MUI components",
            "tree_shaking": "Configure webpack for proper tree shaking"
        },
        "accessibility": {
            "semantic_html": "Use semantic HTML elements",
            "aria_attributes": "Implement proper ARIA attributes",
            "keyboard_navigation": "Ensure full keyboard accessibility",
            "screen_readers": "Test with screen reader software"
        },
        "testing": {
            "unit_tests": "Write unit tests for component logic",
            "snapshot_tests": "Use snapshot testing for UI consistency",
            "accessibility_tests": "Include accessibility in test suite",
            "visual_regression": "Implement visual regression testing"
        }
    }

# ===================================================================
# PROMPTS - AI DEVELOPMENT ASSISTANCE
# ===================================================================

@mcp.prompt
def mui_component_prompt(component_type: str, requirements: str = "") -> str:
    """
    Generate a comprehensive prompt for creating MUI components with best practices
    
    Args:
        component_type: Type of MUI component to create
        requirements: Specific requirements or features needed
    """
    base_prompt = f"""Create a production-ready Material-UI {component_type} component with the following specifications:

Component Type: {component_type}
Requirements: {requirements if requirements else 'Standard component following MUI best practices'}

Implementation Requirements:
1. **TypeScript Integration**
   - Define clear prop interfaces with proper typing
   - Use generic types where appropriate
   - Include JSDoc comments for all props

2. **Responsive Design**
   - Mobile-first approach using MUI breakpoints
   - Proper grid system usage
   - Touch-friendly interactions

3. **Accessibility (WCAG 2.1 AA)**
   - Proper ARIA labels and roles
   - Keyboard navigation support
   - Screen reader compatibility
   - Color contrast compliance

4. **Material Design Principles**
   - Follow Material Design 3 guidelines
   - Consistent spacing using theme.spacing()
   - Proper elevation and shadows
   - Smooth animations and transitions

5. **Performance Optimization**
   - Minimize re-renders with React.memo if needed
   - Proper event handler memoization
   - Efficient prop passing

6. **Error Handling & Validation**
   - Input validation with helpful error messages
   - Graceful error states
   - Loading states where applicable

7. **Testing Considerations**
   - Component should be easily testable
   - Clear data-testid attributes
   - Predictable behavior"""

    if component_type in MUI_TEMPLATES:
        template = MUI_TEMPLATES[component_type]
        base_prompt += f"""

Component-Specific Guidelines:
- Available props: {', '.join(template.get('props', []))}
- Supported variants: {', '.join(template.get('variants', []))}
- Color options: {', '.join(template.get('colors', []))}
- Size variants: {', '.join(template.get('sizes', []))}
- Description: {template.get('description', 'Standard MUI component')}"""
    
    return base_prompt

@mcp.prompt
def mui_theme_prompt(theme_style: str, brand_requirements: str = "") -> str:
    """
    Generate a prompt for creating custom MUI themes with brand consistency
    
    Args:
        theme_style: Style of theme (corporate, modern, minimal, etc.)
        brand_requirements: Brand-specific color, typography, and style requirements
    """
    return f"""Create a comprehensive Material-UI theme that embodies a {theme_style} design aesthetic.

Theme Style: {theme_style}
Brand Requirements: {brand_requirements if brand_requirements else 'Modern, professional appearance with excellent usability'}

Theme Development Requirements:

1. **Color Palette Design**
   - Primary colors that convey the brand personality
   - Secondary colors for accents and emphasis
   - Error, warning, info, and success states
   - Background and surface colors
   - Text colors with proper contrast ratios

2. **Typography System**
   - Font family selection appropriate for {theme_style} style
   - Complete type scale (h1-h6, body1-body2, caption, etc.)
   - Font weights and letter spacing
   - Responsive typography that scales properly

3. **Spacing & Layout**
   - Consistent spacing scale using theme.spacing()
   - Component spacing guidelines
   - Container max-widths and breakpoints
   - Grid system customization

4. **Component Customization**
   - Button styles and variants
   - Input field appearances
   - Card and paper elevations
   - Navigation component styling

5. **Dark Mode Support**
   - Complete dark theme variant
   - Proper color adaptations
   - Smooth theme switching capability

6. **Accessibility Compliance**
   - WCAG 2.1 AA color contrast ratios
   - Focus indicators and states
   - High contrast mode support

Please include TypeScript definitions and usage examples showing how to apply the theme to a React application."""

@mcp.prompt
def mui_layout_prompt(layout_type: str, content_structure: str, user_needs: str = "") -> str:
    """
    Generate a prompt for creating responsive MUI layouts
    
    Args:
        layout_type: Type of layout (dashboard, landing, admin, etc.)
        content_structure: Description of content sections and hierarchy
        user_needs: Specific user interaction patterns and requirements
    """
    return f"""Design and implement a responsive Material-UI {layout_type} layout that provides excellent user experience across all devices.

Layout Type: {layout_type}
Content Structure: {content_structure}
User Needs: {user_needs if user_needs else 'Intuitive navigation and efficient content access'}

Layout Design Requirements:

1. **Responsive Architecture**
   - Mobile-first design approach
   - Breakpoint-specific layout adaptations
   - Flexible grid system implementation
   - Touch-friendly navigation on mobile

2. **Navigation Structure**
   - Clear information hierarchy
   - Consistent navigation patterns
   - Breadcrumb trails where appropriate
   - Search functionality integration

3. **Content Organization**
   - Logical content grouping
   - Progressive disclosure principles
   - Scannable content layout
   - Appropriate white space usage

4. **Performance Considerations**
   - Lazy loading for heavy content
   - Efficient component rendering
   - Minimal layout shifts
   - Fast loading times

5. **User Experience**
   - Intuitive interaction patterns
   - Clear call-to-action placement
   - Consistent feedback mechanisms
   - Error and loading states

6. **Accessibility Features**
   - Keyboard navigation support
   - Screen reader optimization
   - Skip navigation links
   - Focus management

Include implementation details for key components, responsive behavior specifications, and integration guidelines for dynamic content."""

@mcp.prompt
def mui_form_prompt(form_purpose: str, fields_description: str, validation_requirements: str = "") -> str:
    """
    Generate a prompt for creating comprehensive MUI forms with validation
    
    Args:
        form_purpose: Purpose and context of the form
        fields_description: Description of required form fields and types
        validation_requirements: Specific validation rules and requirements
    """
    return f"""Create a robust and user-friendly Material-UI form for {form_purpose} with comprehensive validation and excellent user experience.

Form Purpose: {form_purpose}
Fields Required: {fields_description}
Validation Requirements: {validation_requirements if validation_requirements else 'Standard field validation with helpful error messages'}

Form Development Requirements:

1. **Field Implementation**
   - Appropriate input types for each field
   - Clear labels and placeholder text
   - Helper text for complex fields
   - Proper field grouping and layout

2. **Validation System**
   - Real-time validation feedback
   - Field-level and form-level validation
   - Clear, actionable error messages
   - Success states and confirmation

3. **User Experience**
   - Progressive disclosure for complex forms
   - Save draft functionality if applicable
   - Clear progress indicators for multi-step forms
   - Keyboard navigation support

4. **Error Handling**
   - Network error handling
   - Graceful degradation
   - Retry mechanisms
   - Clear error recovery paths

5. **Accessibility Features**
   - Proper form labeling
   - Error announcement for screen readers
   - Logical tab order
   - Required field indicators

6. **Performance & Security**
   - Efficient form state management
   - Input sanitization
   - Secure data transmission
   - Minimal re-renders

Include TypeScript interfaces, validation schemas, and integration examples with popular form libraries like Formik or React Hook Form."""

@mcp.prompt
def mui_accessibility_prompt(component_focus: str, accessibility_level: str = "WCAG AA") -> str:
    """
    Generate a prompt for ensuring MUI components meet accessibility standards
    
    Args:
        component_focus: Specific component or feature to make accessible
        accessibility_level: Target accessibility compliance level
    """
    return f"""Implement comprehensive accessibility features for {component_focus} to meet {accessibility_level} compliance standards using Material-UI.

Accessibility Focus: {component_focus}
Compliance Target: {accessibility_level}

Accessibility Implementation Requirements:

1. **Semantic HTML Structure**
   - Proper heading hierarchy (h1-h6)
   - Semantic landmarks (nav, main, aside, footer)
   - List structures for grouped content
   - Form labels and fieldsets

2. **ARIA Implementation**
   - Appropriate ARIA roles
   - Descriptive ARIA labels
   - Live regions for dynamic content
   - State indicators (expanded, selected, etc.)

3. **Keyboard Navigation**
   - Full keyboard accessibility
   - Logical tab order
   - Custom keyboard shortcuts where appropriate
   - Focus trapping in modals

4. **Visual Accessibility**
   - Color contrast compliance
   - Focus indicators
   - Text scaling support (up to 200%)
   - Motion reduction preferences

5. **Screen Reader Support**
   - Descriptive text alternatives
   - Clear content structure
   - Meaningful link text
   - Form error announcements

6. **Testing & Validation**
   - Automated accessibility testing
   - Manual testing procedures
   - Screen reader testing
   - Keyboard-only navigation testing

Provide specific code examples, testing strategies, and common accessibility pitfalls to avoid when implementing {component_focus}."""

@mcp.prompt
def mui_performance_prompt(optimization_focus: str, performance_targets: str = "") -> str:
    """
    Generate a prompt for optimizing MUI application performance
    
    Args:
        optimization_focus: Specific area of performance optimization
        performance_targets: Target performance metrics and goals
    """
    return f"""Optimize the performance of Material-UI applications focusing on {optimization_focus} to achieve excellent user experience and performance metrics.

Optimization Focus: {optimization_focus}
Performance Targets: {performance_targets if performance_targets else 'Fast loading, smooth interactions, efficient resource usage'}

Performance Optimization Requirements:

1. **Bundle Optimization**
   - Tree shaking for MUI components
   - Code splitting strategies
   - Dynamic imports for large components
   - Webpack optimization configuration

2. **Rendering Performance**
   - Component memoization strategies
   - Virtual scrolling for large lists
   - Efficient state management
   - Debounced user interactions

3. **Loading Strategies**
   - Progressive loading techniques
   - Image optimization and lazy loading
   - Critical CSS extraction
   - Service worker implementation

4. **Memory Management**
   - Event listener cleanup
   - Component unmounting procedures
   - Memory leak prevention
   - Efficient data structures

5. **Network Optimization**
   - API request optimization
   - Caching strategies
   - Compression techniques
   - CDN utilization

6. **Measurement & Monitoring**
   - Performance metrics collection
   - Core Web Vitals optimization
   - Real User Monitoring (RUM)
   - Performance budgets

Include specific implementation examples, measurement tools, and monitoring strategies for maintaining optimal performance in production environments."""

@mcp.prompt
def mui_integration_prompt(integration_target: str, requirements: str = "") -> str:
    """
    Generate a prompt for integrating MUI with other technologies and frameworks
    
    Args:
        integration_target: Technology or framework to integrate with (Next.js, TypeScript, etc.)
        requirements: Specific integration requirements and constraints
    """
    return f"""Create a comprehensive integration guide for Material-UI with {integration_target}, ensuring seamless compatibility and optimal functionality.

Integration Target: {integration_target}
Specific Requirements: {requirements if requirements else 'Smooth integration with minimal configuration overhead'}

Integration Implementation Requirements:

1. **Configuration Setup**
   - Initial setup and configuration steps
   - Dependency management
   - Build tool configurations
   - Environment-specific settings

2. **Theme Integration**
   - Theme provider setup
   - Server-side rendering considerations
   - Dynamic theme switching
   - Custom theme overrides

3. **Component Integration**
   - Component library structure
   - Import/export patterns
   - Type definitions
   - Style injection methods

4. **Build Process**
   - Optimization configurations
   - Asset handling
   - Code splitting strategies
   - Production build setup

5. **Development Experience**
   - Hot reloading setup
   - Development tools integration
   - Debugging configurations
   - Testing environment setup

6. **Production Considerations**
   - Performance optimizations
   - Security configurations
   - Monitoring and analytics
   - Deployment strategies

Include step-by-step setup instructions, common troubleshooting scenarios, and best practices for maintaining the integration over time."""

# ===================================================================
# SERVER STARTUP
# ===================================================================

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv('MUI_MCP_PORT', '8040'))
    
    logger.info(f"Starting MUI HTTP MCP Server on port {port}")
    logger.info("=" * 60)
    logger.info("Available Tools:")
    logger.info("  • generate_mui_component - Create individual MUI components")
    logger.info("  • generate_mui_form - Build forms with validation")
    logger.info("  • create_mui_theme - Design custom themes")
    logger.info("  • generate_mui_layout - Create responsive layouts")
    logger.info("")
    logger.info("Available Resources:")
    logger.info("  • mui://templates - Component templates and properties")
    logger.info("  • mui://themes - Theme presets and customization")
    logger.info("  • mui://patterns - Layout patterns and guidelines")
    logger.info("  • mui://examples/{type} - Usage examples")
    logger.info("  • mui://best-practices - Development guidelines")
    logger.info("")
    logger.info("Available Prompts:")
    logger.info("  • mui_component_prompt - Component development guidance")
    logger.info("  • mui_theme_prompt - Theme creation assistance")
    logger.info("  • mui_layout_prompt - Layout design guidance")
    logger.info("  • mui_form_prompt - Form development assistance")
    logger.info("  • mui_accessibility_prompt - Accessibility implementation")
    logger.info("  • mui_performance_prompt - Performance optimization")
    logger.info("  • mui_integration_prompt - Technology integration")
    logger.info("=" * 60)
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")