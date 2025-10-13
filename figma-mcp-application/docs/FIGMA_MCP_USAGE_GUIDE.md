# Figma MCP Application Server - Usage Guide

## 🎨 Overview

The Figma MCP Application server provides access to a comprehensive design system database with 2000+ enterprise-grade components. All components are pre-built and categorized - NO Figma IDs needed!

## 🚀 Quick Start

### How It Works
- All components are stored in the Supabase design system database
- Components are organized by category (dashboards, forms, tables, etc.)
- Just specify what type of component you need
- The server handles all the complexity

### Basic Usage

```python
# Get application components by category
result = mcp__figma-mcp-application__get_application_sections(
    category="dashboard",
    subcategory="analytics",
    include_code=True,
    create_files=True
)

# Build a complete dashboard
result = mcp__figma-mcp-application__build_dashboard(
    dashboard_type="analytics",
    widgets=["stats_cards", "line_chart", "activity_feed"],
    layout="sidebar",
    theme="dark"
)
```

## 📋 Available Tools

### 1. Extract Single Component
```python
mcp__figma-mcp-application__extract_component_from_figma(
    file_id="abc123",           # Figma file ID
    node_id="2:43",            # Component node ID
    component_name="Button",    # Output component name
    output_dir="./components"   # Where to save
)
```

### 2. Batch Extract Components
```python
mcp__figma-mcp-application__batch_extract_components(
    file_id="abc123",
    components=[
        {"node_id": "2:43", "name": "Button"},
        {"node_id": "2:56", "name": "Card"},
        {"node_id": "2:89", "name": "Modal"}
    ],
    output_dir="./components"
)
```

### 3. Extract Design Tokens
```python
mcp__figma-mcp-application__extract_design_tokens(
    file_id="abc123",
    output_file="./styles/tokens.json"
)
```

### 4. Generate Complete UI Kit
```python
mcp__figma-mcp-application__generate_ui_kit_from_figma(
    file_id="abc123",
    output_dir="./components/ui-kit",
    include_tokens=True
)
```

## 🎯 Finding Figma IDs

### File ID
From Figma URL: `https://www.figma.com/file/wsmhiiharnhqupdniwgw/...`
The file ID is: `wsmhiiharnhqupdniwgw`

### Node IDs
1. Select component in Figma
2. Right-click → "Copy as" → "Copy link"
3. URL contains node ID: `...?node-id=2:43`

## 💡 Component Generation Examples

### Example 1: Button Component

**Figma Design**: Primary button with hover states

**Generated Code**:
```tsx
import React from 'react';
import { cn } from '@/lib/utils';

interface PrimaryButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
}

export const PrimaryButton: React.FC<PrimaryButtonProps> = ({
  children,
  onClick,
  disabled = false,
  variant = 'primary',
  size = 'md'
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={cn(
        'inline-flex items-center justify-center rounded-md font-medium transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
        'disabled:pointer-events-none disabled:opacity-50',
        {
          'bg-blue-600 text-white hover:bg-blue-700': variant === 'primary',
          'bg-gray-100 text-gray-900 hover:bg-gray-200': variant === 'secondary',
          'h-8 px-3 text-sm': size === 'sm',
          'h-10 px-4 text-base': size === 'md',
          'h-12 px-6 text-lg': size === 'lg'
        }
      )}
    >
      {children}
    </button>
  );
};
```

### Example 2: Card Component

**Generated from Figma**:
```tsx
export const ProductCard: React.FC<ProductCardProps> = ({
  image,
  title,
  price,
  description
}) => {
  return (
    <div className="group relative overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm transition-all hover:shadow-lg">
      <div className="aspect-square overflow-hidden bg-gray-100">
        <img
          src={image}
          alt={title}
          className="h-full w-full object-cover transition-transform group-hover:scale-105"
        />
      </div>
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <p className="mt-1 text-sm text-gray-600">{description}</p>
        <p className="mt-2 text-xl font-bold text-gray-900">${price}</p>
      </div>
    </div>
  );
};
```

## 🔧 Design Tokens

### Extracted Token Structure
```json
{
  "colors": {
    "primary": {
      "50": "#eff6ff",
      "100": "#dbeafe",
      "500": "#3b82f6",
      "600": "#2563eb",
      "700": "#1d4ed8"
    },
    "gray": {
      "50": "#f9fafb",
      "100": "#f3f4f6",
      "900": "#111827"
    }
  },
  "spacing": {
    "xs": "0.5rem",
    "sm": "1rem",
    "md": "1.5rem",
    "lg": "2rem",
    "xl": "3rem"
  },
  "typography": {
    "fontFamily": {
      "sans": "Inter, system-ui, sans-serif",
      "mono": "JetBrains Mono, monospace"
    },
    "fontSize": {
      "xs": "0.75rem",
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem",
      "xl": "1.25rem"
    }
  },
  "borderRadius": {
    "sm": "0.25rem",
    "md": "0.375rem",
    "lg": "0.5rem",
    "full": "9999px"
  }
}
```

## 📁 Output Structure

```
components/
├── ui/
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── Input.tsx
│   └── Modal.tsx
├── icons/
│   ├── ChevronIcon.tsx
│   └── CloseIcon.tsx
└── tokens/
    ├── colors.ts
    ├── spacing.ts
    └── typography.ts
```

## 🎨 Working with Design Systems

### Step 1: Set Up Design System in Figma
- Create components with consistent naming
- Use Figma styles for colors and typography
- Set up component variants

### Step 2: Extract Base Components
```python
# Extract all base components
base_components = [
    {"node_id": "2:10", "name": "Button"},
    {"node_id": "2:20", "name": "Input"},
    {"node_id": "2:30", "name": "Select"},
    {"node_id": "2:40", "name": "Checkbox"},
    {"node_id": "2:50", "name": "Radio"}
]

mcp__figma-mcp-application__batch_extract_components(
    file_id="design-system-id",
    components=base_components,
    output_dir="./components/ui"
)
```

### Step 3: Extract Design Tokens
```python
mcp__figma-mcp-application__extract_design_tokens(
    file_id="design-system-id",
    output_file="./styles/design-tokens.json"
)
```

### Step 4: Generate Theme Configuration
```python
# Convert tokens to Tailwind config
mcp__figma-mcp-application__generate_tailwind_config(
    tokens_file="./styles/design-tokens.json",
    output_file="./tailwind.config.js"
)
```

## 🔄 Integration with V0 Enhanced

### Workflow Example
```python
# 1. V0 creates the application structure
v0_session = mcp__vercel-v0-enhanced__create_v0_session(
    project_type="dashboard"
)

mcp__vercel-v0-enhanced__generate_with_v0(
    prompt="Create a dashboard with sidebar, header, and content area",
    session_id=v0_session["session_id"]
)

# 2. Replace specific components with Figma designs
mcp__figma-mcp-application__extract_component_from_figma(
    file_id="brand-design-system",
    node_id="5:100",
    component_name="BrandedHeader",
    output_dir="./components/layout"
)

# 3. Update imports in V0-generated code
# The header component now uses the branded version
```

## ⚡ Best Practices

1. **Organize Figma Files**
   - Group related components
   - Use consistent naming
   - Create component variants

2. **Component Naming**
   - Match Figma names to code names
   - Use PascalCase for components
   - Be descriptive but concise

3. **Design Tokens**
   - Extract tokens first
   - Use tokens in components
   - Keep tokens in sync

4. **Version Control**
   - Track Figma file versions
   - Document component changes
   - Use git tags for releases

## 🚨 Common Issues

### Issue: Component not found
**Solution**: Verify node ID is correct and component is not in a hidden layer

### Issue: Styles not matching
**Solution**: Ensure Figma uses defined styles, not hardcoded values

### Issue: Missing responsive behavior
**Solution**: Create multiple Figma frames for different breakpoints

## 📚 Advanced Usage

### Custom Transformations
```python
# Extract with custom transformation rules
mcp__figma-mcp-application__extract_with_transform(
    file_id="abc123",
    node_id="2:43",
    transforms={
        "colors": "tailwind",  # Convert to Tailwind classes
        "spacing": "rem",      # Convert px to rem
        "icons": "lucide"      # Use Lucide icons
    }
)
```

### Component Documentation
```python
# Generate Storybook stories from Figma
mcp__figma-mcp-application__generate_stories(
    file_id="abc123",
    components=["Button", "Card", "Modal"],
    output_dir="./stories"
)
```

## 🎯 Summary

The Figma MCP Application server bridges the gap between design and development by:
- Converting Figma designs to production code
- Maintaining pixel-perfect accuracy
- Extracting reusable design tokens
- Generating consistent component libraries

Use it when you need exact design implementation, not when you need rapid prototyping (use V0 Enhanced for that).