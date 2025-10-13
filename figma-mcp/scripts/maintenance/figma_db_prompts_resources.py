# Prompts and Resources for figma_server_db.py
# Add these to figma_server_db.py after the tool definitions

# ============= PROMPTS =============

@mcp.prompt
def react_generation_guide(app_type: str) -> str:
    """Guide AI in using React template generation effectively"""
    return f"""
    You are building a {app_type} application using the Figma design system database.
    
    FIRST: If the user hasn't been specific about their requirements, ASK:
    - What specific features do you need in your {app_type}?
    - Are there any particular UI patterns you prefer?
    - Do you need forms, data tables, charts, or other specific components?
    
    THEN follow these steps:
    1. First, analyze what components are needed based on user requirements
    2. Query the database using preview_figma_components with relevant filters
    3. Select 10-15 most relevant components (not all 1054!)
    4. Use bulk_create_component_files to generate the React components
    
    Component selection criteria:
    - Core UI elements (buttons, inputs, cards)
    - App-specific components based on user needs
    - Layout components (headers, navigation)
    - Feedback components (alerts, toasts)
    
    IMPORTANT: Be selective! Quality over quantity. The examples in resources are just suggestions - adapt to user needs.
    """

@mcp.prompt
def template_customization_guide(component_type: str) -> str:
    """Guide AI in customizing templates appropriately"""
    return f"""
    When generating React components for {component_type}, customize templates as follows:
    
    1. Variable Substitution:
       - {{componentName}} - Use PascalCase (e.g., TodoItem, UserCard)
       - {{variant}} - Describe the variant clearly (e.g., "primary", "outlined")
       - {{propsInterface}} - Generate TypeScript interfaces based on Figma props
       - {{defaultProps}} - Set sensible defaults for the component type
    
    2. Component-Specific Customization:
       - Buttons: Include onClick, disabled, loading states
       - Forms: Add validation props, error states
       - Cards: Include content slots, actions
       - Lists: Add item rendering, selection
    
    3. Maintain Consistency:
       - Use the same prop naming conventions
       - Follow the design system's patterns
       - Include proper TypeScript types
    """

@mcp.prompt
def file_vs_memory_decision() -> str:
    """Help AI decide when to use bulk_create_component_files vs build_app_components"""
    return """
    Choose the right generation method:
    
    USE bulk_create_component_files WHEN:
    - User wants actual files created on disk
    - Building a real application
    - Need persistent output
    - Creating a starter template
    - User asks to "create", "generate", or "build" an app
    
    USE build_app_components WHEN:
    - User wants to preview components
    - Exploring design options
    - Need quick iteration
    - Testing component combinations
    - User asks to "show", "preview", or "demonstrate"
    
    DEFAULT: Use bulk_create_component_files for actual development work.
    """

@mcp.prompt
def component_selection_strategy(app_description: str) -> str:
    """Guide AI in selecting the right mix of components"""
    return f"""
    For the app: "{app_description}", select components strategically:
    
    1. Essential Components (5-7):
       - Layout structure (Header, Container, Grid)
       - Primary actions (Button, Link)
       - Data input (Input, Form, Select)
    
    2. App-Specific Components (3-5):
       - Based on app type (TodoItem for todo apps, ProductCard for e-commerce)
       - Domain-specific widgets
    
    3. Supporting Components (2-3):
       - Feedback (Alert, Toast, Loading)
       - Navigation (Tabs, Breadcrumb)
    
    Total: Aim for 10-15 components maximum.
    
    Query Strategy:
    1. Start with category filters (e.g., category='forms' for input-heavy apps)
    2. Use component_filter for specific searches
    3. Check popularity_score for commonly used components
    """

# ============= RESOURCES =============

@mcp.resource("figma-db://best-practices/react-templates")
def react_template_best_practices() -> str:
    """Best practices for React template generation from database"""
    return """
    # React Template Generation Best Practices
    
    ## 1. Template Structure
    - Always generate TypeScript (.tsx) files
    - Include proper imports (React, types, styles)
    - Export as default for better tree-shaking
    - Use functional components with hooks
    
    ## 2. Props Interface
    - Generate from Figma component props
    - Include variant props (size, color, state)
    - Add event handlers (onClick, onChange)
    - Make appropriate props optional
    
    ## 3. Styling Approach
    - Use CSS modules or styled-components
    - Respect Figma's design tokens
    - Include responsive considerations
    - Support dark/light themes
    
    ## 4. Component Composition
    - Make components composable
    - Use children prop appropriately
    - Support ref forwarding
    - Include display name for debugging
    
    ## 5. File Organization
    components/
    ├── Button/
    │   ├── Button.tsx
    │   ├── Button.module.css
    │   └── index.ts
    ├── Card/
    │   ├── Card.tsx
    │   └── Card.module.css
    └── index.ts (barrel export)
    """

@mcp.resource("figma-db://workflow/app-types")
def app_type_component_mapping() -> str:
    """Component selection patterns for different app types"""
    return """
    # Component Selection by App Type
    
    **IMPORTANT**: These are EXAMPLES to guide component selection. Always:
    1. ASK THE USER what specific app they want to build
    2. ASK THE USER about specific features they need
    3. CUSTOMIZE component selection based on their requirements
    
    The user may say something like:
    - "Build me a task manager with categories"
    - "Create a simple blog"  
    - "I need a dashboard for analytics"
    - Or something completely different!
    
    ## Example: Todo App
    Common components might include:
    - TodoItem (with checkbox, delete)
    - TodoList (container)
    - AddTodoForm (input + button)
    - FilterTabs (all/active/completed)
    - Header (with title)
    - Button (primary/secondary)
    - Checkbox (for completion)
    
    ## Example: Dashboard
    Common components might include:
    - StatCard (metrics display)
    - Chart (placeholder)
    - DataTable (with sorting)
    - Sidebar (navigation)
    - Header (with user menu)
    - SearchBar
    - FilterDropdown
    
    ## Example: E-commerce
    Common components might include:
    - ProductCard (image, price, actions)
    - ProductGrid (responsive layout)
    - ShoppingCart (sidebar/modal)
    - CheckoutForm (multi-step)
    - PriceDisplay (with currency)
    - QuantitySelector
    - CategoryFilter
    
    ## Example: Blog
    Common components might include:
    - ArticleCard (preview)
    - ArticleLayout (full post)
    - CommentSection
    - AuthorBio
    - TagList
    - Pagination
    - SearchBar
    
    ## Example: Form-heavy App
    Common components might include:
    - Input (text, email, password)
    - Select (dropdown)
    - Checkbox/Radio groups
    - FormField (label + input + error)
    - MultiStepForm
    - ValidationMessage
    - SubmitButton (with loading)
    
    ## Custom Apps
    The user might want something unique:
    - Recipe app (RecipeCard, IngredientList, CookingTimer)
    - Social media (PostCard, CommentThread, UserProfile)
    - Project management (KanbanBoard, TaskCard, Timeline)
    - Or any other type!
    
    ALWAYS prioritize user requirements over these examples.
    """

@mcp.resource("figma-db://development/file-structure")
def generated_file_structure_guide() -> str:
    """Recommended file structure for generated components"""
    return """
    # Generated Project Structure
    
    my-app/
    ├── src/
    │   ├── components/           # All Figma components
    │   │   ├── Button/
    │   │   │   ├── Button.tsx
    │   │   │   ├── Button.module.css
    │   │   │   ├── Button.types.ts
    │   │   │   └── index.ts
    │   │   └── index.ts         # Barrel exports
    │   ├── hooks/               # Custom React hooks
    │   ├── utils/               # Helper functions
    │   ├── types/               # Shared TypeScript types
    │   └── styles/              # Global styles, variables
    ├── package.json             # Dependencies
    ├── tsconfig.json           # TypeScript config
    └── README.md               # Setup instructions
    
    ## Component File Template
    ```tsx
    // Button.tsx
    import React from 'react';
    import styles from './Button.module.css';
    import { ButtonProps } from './Button.types';
    
    export const Button: React.FC<ButtonProps> = ({
      children,
      variant = 'primary',
      size = 'medium',
      onClick,
      ...props
    }) => {
      return (
        <button
          className={`${styles.button} ${styles[variant]} ${styles[size]}`}
          onClick={onClick}
          {...props}
        >
          {children}
        </button>
      );
    };
    
    Button.displayName = 'Button';
    export default Button;
    ```
    """

@mcp.resource("figma-db://templates/starter-apps")
def starter_app_templates() -> str:
    """Complete starter app configurations"""
    return """
    # Starter App Templates
    
    ## Minimal Todo App
    ```json
    {
      "components": [
        "TodoItem",
        "TodoList", 
        "AddTodoForm",
        "Button",
        "Input",
        "Checkbox",
        "Container"
      ],
      "features": [
        "Add new todos",
        "Mark as complete",
        "Delete todos",
        "Filter by status"
      ]
    }
    ```
    
    ## Basic Dashboard
    ```json
    {
      "components": [
        "StatCard",
        "DataTable",
        "Header",
        "Sidebar",
        "Chart",
        "Button",
        "SearchBar"
      ],
      "layout": "sidebar-content"
    }
    ```
    
    ## Component Combinations
    - Form = Input + Button + Label + ErrorMessage
    - Card = CardHeader + CardBody + CardFooter
    - Table = TableHeader + TableRow + TableCell + Pagination
    - Modal = ModalOverlay + ModalContent + ModalActions
    """