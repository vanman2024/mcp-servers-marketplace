# MUI HTTP MCP Server

Material-UI component generation server for Claude Code, providing tools to generate MUI components, themes, layouts, and forms with TypeScript support.

## Features

- **Component Generation**: Create MUI components (Button, Card, TextField, Select, Dialog, AppBar, Table, Form)
- **Theme Creation**: Generate custom MUI themes with presets (light, dark, corporate, modern)
- **Layout Generation**: Build complete layouts (dashboard, landing, form, table) with optional sidebar
- **Form Generation**: Create forms with validation and TypeScript interfaces
- **Resources**: Access component templates, theme presets, and usage examples  
- **Prompts**: Get AI prompts for component requirements and best practices

## Server Organization

The MUI server is organized into clear sections:

### 🛠️ Tools (4 main tools)
- **Component Generation**: Individual component creation
- **Form Generation**: Complete forms with validation  
- **Theme Creation**: Custom theme design
- **Layout Generation**: Responsive layout creation

### 📚 Resources (5 resource endpoints)
- **Templates**: Component specifications and properties
- **Themes**: Preset themes and customization options
- **Patterns**: Layout patterns and guidelines
- **Examples**: Usage examples with best practices
- **Best Practices**: Development guidelines and standards

### 💡 Prompts (7 specialized prompts)
- **Component Development**: Production-ready component creation
- **Theme Design**: Brand-consistent theme development
- **Layout Architecture**: Responsive layout design
- **Form Development**: Comprehensive form creation
- **Accessibility**: WCAG compliance implementation
- **Performance**: Optimization strategies
- **Integration**: Technology integration guidance

## Available Tools

### Component Generation Tools

#### `generate_mui_component`
Generate individual MUI components with props and TypeScript support.

**Parameters:**
- `component_type`: Type of component (button, card, textfield, select, dialog, appbar, table, form, chip, avatar)
- `name`: Component name
- `props`: Component properties (optional)
- `children`: Component content (optional)
- `typescript`: Generate TypeScript (default: true)

**Example:**
```python
await generate_mui_component(
    component_type="button",
    name="SubmitButton",
    props={"variant": "contained", "color": "primary"},
    children="Submit Form"
)
```

#### `generate_mui_form`
Generate complete MUI forms with validation and TypeScript interfaces.

**Parameters:**
- `form_name`: Form component name
- `fields`: List of field definitions with type, name, label, required
- `validation`: Include validation (default: true)
- `submit_action`: Submit handler name (default: "handleSubmit")
- `layout`: Form layout (vertical, horizontal, grid)

### Theming & Styling Tools

#### `create_mui_theme`
Create custom MUI themes with advanced customization options.

**Parameters:**
- `theme_name`: Name for the theme
- `preset`: Theme preset (light, dark, corporate, modern, minimal)
- `custom_palette`: Custom color palette (optional)
- `typography`: Typography settings (optional)
- `spacing`: Spacing unit (optional)
- `breakpoints`: Custom breakpoint values (optional)

### Layout & Structure Tools

#### `generate_mui_layout`
Generate complete layout components with navigation and responsive design.

**Parameters:**
- `layout_type`: Type of layout (dashboard, landing, form, table)
- `name`: Layout component name
- `sections`: List of section names
- `responsive`: Make responsive (default: true)
- `sidebar`: Include sidebar navigation (default: false)
- `navigation`: Include top navigation (default: true)

**Example:**
```python
await generate_mui_layout(
    layout_type="dashboard",
    name="AdminLayout",
    sections=["Overview", "Users", "Settings"],
    sidebar=True
)
```

### `generate_mui_form`
Create forms with validation and TypeScript interfaces.

**Parameters:**
- `form_name`: Form component name
- `fields`: List of field definitions
- `validation`: Include validation (default: true)
- `submit_action`: Submit handler name (default: "handleSubmit")

**Example:**
```python
await generate_mui_form(
    form_name="ContactForm",
    fields=[
        {"name": "name", "type": "text", "label": "Full Name", "required": True},
        {"name": "email", "type": "email", "label": "Email", "required": True},
        {"name": "message", "type": "textarea", "label": "Message"}
    ]
)
```

## Available Resources

### `mui://templates`
Get comprehensive MUI component templates with all properties, variants, and usage examples.

### `mui://themes`
Get available MUI theme presets (light, dark, corporate, modern, minimal) and customization options.

### `mui://patterns`
Get layout patterns and responsive design guidelines for different layout types.

### `mui://examples/{component_type}`
Get comprehensive usage examples for specific component types with accessibility and best practices.

### `mui://best-practices`
Get MUI development best practices covering component development, theming, performance, accessibility, and testing.

## Available Prompts

### `mui_component_prompt`
Generate comprehensive prompts for creating production-ready MUI components with best practices.

**Parameters:**
- `component_type`: Type of component to create
- `requirements`: Specific requirements (optional)

### `mui_theme_prompt`
Generate prompts for creating custom MUI themes with brand consistency.

**Parameters:**
- `theme_style`: Style of theme (corporate, modern, minimal, etc.)
- `brand_requirements`: Brand-specific requirements (optional)

### `mui_layout_prompt`
Generate prompts for creating responsive MUI layouts.

**Parameters:**
- `layout_type`: Type of layout (dashboard, landing, admin, etc.)
- `content_structure`: Description of content sections and hierarchy
- `user_needs`: Specific user interaction patterns (optional)

### `mui_form_prompt`
Generate prompts for creating comprehensive MUI forms with validation.

**Parameters:**
- `form_purpose`: Purpose and context of the form
- `fields_description`: Description of required form fields and types
- `validation_requirements`: Specific validation rules (optional)

### `mui_accessibility_prompt`
Generate prompts for ensuring MUI components meet accessibility standards.

**Parameters:**
- `component_focus`: Specific component or feature to make accessible
- `accessibility_level`: Target compliance level (default: "WCAG AA")

### `mui_performance_prompt`
Generate prompts for optimizing MUI application performance.

**Parameters:**
- `optimization_focus`: Specific area of performance optimization
- `performance_targets`: Target metrics and goals (optional)

### `mui_integration_prompt`
Generate prompts for integrating MUI with other technologies and frameworks.

**Parameters:**
- `integration_target`: Technology to integrate with (Next.js, TypeScript, etc.)
- `requirements`: Specific integration requirements (optional)

## Setup

1. **Install dependencies:**
   ```bash
   cd servers/http/mui-http-mcp
   pip install -r requirements.txt
   ```

2. **Set environment variables (optional):**
   ```bash
   export MUI_MCP_PORT=8040  # Default port
   ```

3. **Run the server:**
   ```bash
   python src/mui_server.py
   ```

## Usage with Claude

1. **Add to Claude Code:**
   ```bash
   claude mcp add --transport http mui-http http://localhost:8040
   ```

2. **List available tools:**
   ```bash
   /mcp
   ```

3. **Use tools:**
   ```bash
   # Generate a button component
   /mcp__mui_http__generate_mui_component "button" "SubmitButton" '{"variant": "contained", "color": "primary"}' "Submit Form"
   
   # Create a theme
   /mcp__mui_http__create_mui_theme "DarkTheme" "dark"
   
   # Generate a layout
   /mcp__mui_http__generate_mui_layout "dashboard" "AdminLayout" '["Users", "Analytics", "Settings"]' true true
   
   # Create a form
   /mcp__mui_http__generate_mui_form "ContactForm" '[{"name": "name", "type": "text", "label": "Name", "required": true}]'
   ```

4. **Access resources:**
   ```bash
   # Get component templates
   /mcp_resource mui://templates
   
   # Get theme presets
   /mcp_resource mui://themes
   
   # Get button examples
   /mcp_resource mui://examples/button
   ```

## Component Types Supported

- **button**: Various button variants with icons and states
- **card**: Cards with headers, content, actions, and media
- **textfield**: Input fields with validation and variants
- **select**: Dropdown selects with options and multi-select
- **dialog**: Modal dialogs with actions and content
- **appbar**: Navigation bars with toolbars and menus
- **table**: Data tables with sorting and pagination ready
- **form**: Complete forms with validation and layouts
- **chip**: Compact tags, categories, and action components
- **avatar**: User profile images and initials display

## Theme Presets

- **light**: Standard light theme with blue primary
- **dark**: Dark mode theme with light blue accents
- **corporate**: Professional theme with Nordic colors
- **modern**: Contemporary theme with purple and amber
- **minimal**: Clean black and white aesthetic

## Integration with Project Workflow

This MUI server integrates with the DevLoop workflow:

1. **Database Task Creation**: Create tasks for UI components
2. **MUI Component Generation**: Use this server to generate components
3. **File Creation**: Components are automatically created with proper structure
4. **GitHub Integration**: Commit generated components to feature branches
5. **Vercel Deployment**: Deploy with generated MUI components

## Best Practices

1. **TypeScript**: Always use TypeScript for better development experience
2. **Responsive Design**: Enable responsive layouts for mobile compatibility
3. **Accessibility**: Generated components include ARIA labels and keyboard navigation
4. **Material Design**: Follow Material Design principles for consistency
5. **Theme Consistency**: Use theme system for consistent styling across components

## Troubleshooting

### Server won't start
- Check if port 8040 is available
- Verify all dependencies are installed
- Check Python version (3.8+ required)

### Components not generating
- Verify component_type is supported
- Check prop names match MUI component props
- Ensure required parameters are provided

### Theme not applying
- Verify theme configuration syntax
- Check custom palette color format
- Ensure theme is properly imported in application

## Development

The server is built using FastMCP and provides:
- Async tool execution with context logging
- Resource-based template and example access
- Prompt generation for AI-assisted development
- Type-safe component generation
- Integration with modern React/TypeScript patterns

## Support

For issues or feature requests, check the MCP server logs and ensure proper integration with Claude Code's MCP transport system.