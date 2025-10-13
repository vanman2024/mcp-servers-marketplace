# V0 Enhanced MCP Server Test Plan

## Current Status
- ✅ V0 Enhanced server running on port 8015
- ✅ Real V0 API key loaded: `v1:VAbNhNzcXd53hVhUEJ5DffUp:rigbaHc9wa9HYhRqVoA6TodT`
- ❌ MCP tools not available until Claude Code restart

## How V0 Enhanced Handles Context

### 1. Session-Based Context Management
```python
# Create session with project context
mcp__vercel-v0-enhanced__create_v0_session(
    project_type="todo_application",
    tech_stack={
        "framework": "Next.js 14 App Router",
        "ui": "React 18 with TypeScript", 
        "styling": "Tailwind CSS",
        "components": "shadcn/ui",
        "state": "React hooks + localStorage",
        "testing": "Jest + React Testing Library"
    }
)
```

### 2. Design Specifications in Prompts
The full design specs can be included in the generation prompt:

```python
mcp__vercel-v0-enhanced__generate_with_v0(
    prompt="""
    Create a complete Todo application with these EXACT specifications:
    
    DESIGN SYSTEM:
    - Colors: 
      - Primary: blue-600 (#2563eb)
      - Secondary: gray-600 (#4b5563)
      - Success: green-600 (#16a34a)
      - Danger: red-600 (#dc2626)
    - Typography: Inter font family
    - Spacing: 4px base unit (Tailwind default)
    - Border radius: rounded-lg for cards, rounded-md for inputs
    
    FEATURES:
    1. Todo Management
       - Add new todos with Enter key
       - Edit inline by clicking todo text
       - Delete with confirmation
       - Mark complete/incomplete with checkbox
       - Drag and drop to reorder
    
    2. Filtering & Sorting
       - Filter: All, Active, Completed
       - Sort: Date created, Alphabetical, Priority
       - Search todos by text
    
    3. Persistence
       - LocalStorage for offline use
       - Export/Import JSON functionality
    
    4. UI/UX
       - Dark mode toggle in header
       - Smooth animations (Framer Motion)
       - Keyboard shortcuts overlay (? key)
       - Mobile responsive design
       - Empty state illustrations
    
    COMPONENT STRUCTURE:
    /app
      layout.tsx - Root layout with providers
      page.tsx - Main todo app page
      globals.css - Tailwind styles
    
    /components
      /ui - shadcn/ui components
      TodoApp.tsx - Main container
      TodoList.tsx - List container
      TodoItem.tsx - Individual todo
      TodoFilters.tsx - Filter controls
      TodoStats.tsx - Statistics bar
      ThemeToggle.tsx - Dark mode switch
    
    /lib
      /hooks
        useTodos.ts - Todo state management
        useLocalStorage.ts - Persistence hook
      /utils
        cn.ts - Class name utility
        todoHelpers.ts - Todo operations
    
    /types
      todo.ts - TypeScript interfaces
    
    CONFIG FILES:
    - package.json with all dependencies
    - tsconfig.json for TypeScript
    - tailwind.config.ts with custom theme
    - next.config.mjs for Next.js
    - .eslintrc.json for linting
    - .prettierrc for formatting
    """,
    session_id="[from-create-session]",
    create_files=True,
    target_directory="v0-todo-app-complete"
)
```

### 3. Project Context Analysis
V0 Enhanced includes a `ProjectContextAnalyzer` that:
- Detects project type from directory name
- Analyzes existing tech stack from package.json
- Scans project structure
- Identifies framework (Next.js app/pages router)

## Test Execution Steps

1. **Restart Claude Code** to refresh MCP connections
2. **Create V0 session** with project context
3. **Generate project** with detailed design specs
4. **Verify files created** in target directory
5. **Test the generated app** with npm install && npm run dev

## Expected Output

V0 Enhanced should create:
```
v0-todo-app-complete/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   ├── ui/
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   └── checkbox.tsx
│   ├── TodoApp.tsx
│   ├── TodoList.tsx
│   ├── TodoItem.tsx
│   ├── TodoFilters.tsx
│   ├── TodoStats.tsx
│   └── ThemeToggle.tsx
├── lib/
│   ├── hooks/
│   │   ├── useTodos.ts
│   │   └── useLocalStorage.ts
│   └── utils/
│       ├── cn.ts
│       └── todoHelpers.ts
├── types/
│   └── todo.ts
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.mjs
├── .eslintrc.json
└── .prettierrc
```

## Providing Additional Context

### Option 1: File-based Context
Create a `DESIGN_SPEC.md` file and reference it:
```
"Read the design specifications from ./DESIGN_SPEC.md and implement exactly as specified"
```

### Option 2: Multi-turn Conversation
Use `continue_v0_session` to build up context:
1. First prompt: Set up project structure
2. Second prompt: Add specific features
3. Third prompt: Implement design system

### Option 3: Template References
Reference existing UI patterns:
```
"Use the same design patterns as https://ui.shadcn.com/examples/tasks"
```

## Current Blockers
- Need to restart Claude Code for MCP tools to be available
- V0 API rate limits (unknown)
- File size limits for large projects

## Next Steps
1. Restart Claude Code session
2. Execute test with full design specifications
3. Validate generated code quality
4. Test build and runtime functionality