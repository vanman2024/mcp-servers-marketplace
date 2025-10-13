# Figma MCP Application Server - Complete Guide

## 🎯 Overview

The Figma MCP Application server provides access to a **comprehensive design system database** containing 2000+ pre-built, enterprise-grade components. Unlike traditional Figma extractors, this server uses a curated component library stored in Supabase - **no Figma file IDs or node IDs needed!**

## 🗄️ What's in the Database

### Component Categories
1. **Application Shells** (12 variants)
   - Dashboard layouts
   - Sidebar navigation
   - Multi-panel interfaces
   - Admin layouts

2. **Data Tables** (20 variants)
   - Sortable tables
   - Virtual scrolling
   - Bulk actions
   - Inline editing

3. **Form Systems** (25 variants)
   - Multi-step forms
   - Validation patterns
   - Auto-save forms
   - Complex inputs

4. **Navigation** (18 variants)
   - Breadcrumbs
   - Tab systems
   - Command palettes
   - Sidebars

5. **Overlays** (15 variants)
   - Modals
   - Slide-overs
   - Notifications
   - Progress indicators

6. **Data Visualization** (12 variants)
   - Charts
   - Stats cards
   - Activity feeds
   - Metrics displays

## 🚀 How to Use

### Getting Components by Category

```python
# Get dashboard components
result = mcp__figma-mcp-application__get_application_sections(
    category="dashboard",
    subcategory="analytics",
    include_code=True,
    create_files=True,
    output_directory="./components/dashboard"
)

# Search for specific components
result = mcp__figma-mcp-application__search_app_components(
    query="user profile",
    component_types=["cards", "forms"],
    limit=10
)
```

### Building Complete Features

#### 1. Analytics Dashboard
```python
dashboard = mcp__figma-mcp-application__build_dashboard(
    dashboard_type="analytics",
    widgets=[
        "stats_overview",
        "revenue_chart",
        "user_activity_feed",
        "conversion_funnel",
        "recent_transactions"
    ],
    layout="sidebar",
    theme="dark",
    data_refresh_interval=30,  # seconds
    responsive=True
)
```

#### 2. Data Management Table
```python
table = mcp__figma-mcp-application__create_data_table(
    table_id="user_management",
    columns=[
        {"key": "name", "label": "Name", "sortable": True},
        {"key": "email", "label": "Email", "sortable": True},
        {"key": "role", "label": "Role", "filterable": True},
        {"key": "status", "label": "Status", "badge": True}
    ],
    features={
        "search": True,
        "pagination": True,
        "bulk_select": True,
        "export": True,
        "column_resize": True
    },
    row_actions=["edit", "delete", "view_details"],
    bulk_actions=["export", "delete_selected", "change_status"]
)
```

#### 3. Multi-Step Form System
```python
form = mcp__figma-mcp-application__build_form_system(
    form_type="user_onboarding",
    submit_action="/api/users/create",
    layout="multi-step",
    validation_schema={
        "email": [
            {"rule": "required", "message": "Email is required"},
            {"rule": "email", "message": "Invalid email format"}
        ],
        "password": [
            {"rule": "required", "message": "Password is required"},
            {"rule": "min_length", "value": 8, "message": "Minimum 8 characters"}
        ]
    },
    include_social=True,
    theme={"primary_color": "#3B82F6", "border_radius": "8px"}
)
```

### Complete Application Examples

#### SaaS Admin Panel
```python
# 1. Create the main layout
layout = mcp__figma-mcp-application__create_sidebar_layout(
    sidebar_items=[
        {"label": "Dashboard", "icon": "home", "route": "/"},
        {"label": "Users", "icon": "users", "route": "/users"},
        {"label": "Analytics", "icon": "chart", "route": "/analytics"},
        {"label": "Settings", "icon": "settings", "route": "/settings"}
    ],
    header_config={
        "show_search": True,
        "show_notifications": True,
        "show_user_menu": True
    },
    theme="professional"
)

# 2. Add command palette
command_palette = mcp__figma-mcp-application__build_command_palette(
    placeholder="Search or jump to...",
    recent_items=["View Users", "Analytics Dashboard", "Account Settings"],
    shortcuts={
        "cmd+k": "open",
        "cmd+/": "search",
        "esc": "close"
    }
)

# 3. Create settings page
settings = mcp__figma-mcp-application__create_settings_page(
    sections=[
        "profile",
        "notifications",
        "security",
        "billing",
        "api_keys"
    ],
    layout="tabs",
    auto_save=True
)
```

## 🎨 Theme System

### Available Themes
- **default**: Clean, minimal design
- **dark**: Dark mode interface
- **professional**: Enterprise look
- **modern**: Contemporary design
- **high-contrast**: Accessibility focused

### Applying Themes
```python
# Apply theme to any component
themed_component = mcp__figma-mcp-application__apply_theme_system(
    component_id="dashboard_main",
    theme_name="dark",
    custom_overrides={
        "primary_color": "#6366F1",
        "secondary_color": "#8B5CF6",
        "font_family": "Inter"
    }
)
```

## 🔍 Advanced Features

### 1. Accessibility Compliance
```python
# Validate component accessibility
validation = mcp__figma-mcp-application__validate_accessibility(
    component_ids=["form_system", "data_table"],
    standards="WCAG_2.1_AA"
)
```

### 2. Performance Optimization
```python
# Optimize components for performance
optimized = mcp__figma-mcp-application__optimize_performance(
    components=["large_data_table", "dashboard_widgets"],
    strategies=["virtual_scrolling", "lazy_loading", "memoization"]
)
```

### 3. Responsive Design
```python
# Manage responsive breakpoints
responsive = mcp__figma-mcp-application__manage_responsive_layout(
    component_id="admin_dashboard",
    breakpoints={
        "mobile": "640px",
        "tablet": "768px",
        "desktop": "1024px",
        "wide": "1280px"
    }
)
```

## 🏢 Enterprise Features

### Component Library Management
```python
# Get all available components
library = mcp__figma-mcp-application__get_component_library(
    include_metadata=True,
    include_usage_stats=True
)

# Track component usage
analytics = mcp__figma-mcp-application__track_component_usage(
    project_id="enterprise_app",
    components_used=["dashboard", "data_table", "forms"]
)
```

### Design System Compliance
```python
# Validate against design system
compliance = mcp__figma-mcp-application__validate_design_system(
    components=["new_feature"],
    design_system_rules="company_standards.json"
)
```

## 💡 Best Practices

### 1. Start with Categories
Instead of searching for specific components, browse by category first:
```python
# See what's available
categories = mcp__figma-mcp-application__get_categories()
# Returns: ["dashboard", "forms", "tables", "navigation", ...]
```

### 2. Use Pre-Built Dashboards
Don't build from scratch - use templates:
```python
# Analytics, CRM, E-commerce, Admin, etc.
dashboard = mcp__figma-mcp_application__build_dashboard(
    dashboard_type="crm",  # Pre-configured CRM dashboard
    widgets="default"      # Uses standard CRM widgets
)
```

### 3. Leverage Component Composition
Combine smaller components into larger features:
```python
# Combine form + modal + validation
user_editor = mcp__figma-mcp-application__compose_components([
    {"type": "modal", "size": "large"},
    {"type": "form", "variant": "user_profile"},
    {"type": "validation", "rules": "standard"}
])
```

## 🔄 Integration with V0 Enhanced

### Complementary Workflow
1. **V0 Enhanced**: Create the application structure
2. **Figma MCP Application**: Add enterprise components

```python
# V0 creates the app
v0_app = mcp__vercel-v0-enhanced__generate_with_v0(
    prompt="Create a CRM application with contact management"
)

# Figma MCP adds enterprise components
enterprise_table = mcp__figma-mcp-application__create_data_table(
    table_id="contacts",
    columns=crm_columns,
    features=enterprise_features
)
```

## 🚨 Common Patterns

### Admin Dashboard Pattern
```python
# 1. Layout
layout = create_sidebar_layout(...)
# 2. Dashboard
dashboard = build_dashboard(...)
# 3. Data tables
tables = create_data_table(...)
# 4. Settings
settings = create_settings_page(...)
```

### SaaS Application Pattern
```python
# 1. Onboarding
onboarding = build_form_system(form_type="onboarding")
# 2. User dashboard
dashboard = build_dashboard(dashboard_type="user")
# 3. Billing
billing = create_billing_interface(...)
# 4. Analytics
analytics = build_analytics_dashboard(...)
```

## 📝 Summary

The Figma MCP Application server provides:
- **No Figma IDs needed** - Everything is in the database
- **2000+ pre-built components** - Enterprise-grade quality
- **Complete features** - Not just individual components
- **Theme system** - Consistent styling across all components
- **Accessibility built-in** - WCAG 2.1 compliant
- **Performance optimized** - Virtual scrolling, lazy loading

Use it when you need:
- Enterprise-grade components
- Consistent design system
- Complex application features
- Accessibility compliance
- Professional polish