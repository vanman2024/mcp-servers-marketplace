# V0 Enhanced MCP Server - DevLoop Integration

## Quick Reference for Claude Agents

### When to Use V0 Enhanced
- **Frontend Development**: Creating React/Next.js components and pages
- **UI/UX Implementation**: Converting design specs to working code
- **Rapid Prototyping**: Building MVPs and proof of concepts
- **Component Libraries**: Creating reusable UI components

### How to Prompt V0 Enhanced

#### ✅ DO: Use Natural Language
```python
# Good - Natural, descriptive language
prompt = """
Create a user profile page that shows avatar, name, bio, and recent activity. 
Include an edit mode where users can update their information inline. 
The design should be clean and modern, similar to GitHub's profile pages.
Add smooth transitions when switching between view and edit modes.
"""
```

#### ❌ DON'T: Use Technical Specifications
```python
# Bad - Too structured and technical
prompt = """
Requirements:
- UserProfile.tsx component
- Props: userId: string, editable: boolean
- State: isEditing, formData
- Methods: handleEdit(), handleSave(), handleCancel()
"""
```

### Integration with DevLoop Workflow

#### 1. Database → Backend → Frontend Flow
```python
# After database schema is created
prompt = f"""
Create a user interface for managing {entity_name}. Users should be able to:
- View all {entity_name} in a searchable, sortable table
- Add new {entity_name} with a form that includes {field_list}
- Edit existing {entity_name} inline
- Delete with confirmation
Make it feel professional like Airtable or Notion databases.
"""
```

#### 2. From Figma Design to Code
```python
# When implementing Figma designs
prompt = f"""
Build the {component_name} component based on this design:
- {design_description}
- The style should match our design system with {color_scheme}
- Include {interactions} with smooth animations
- Make it responsive, starting with mobile-first approach
Reference: {figma_url}
"""
```

#### 3. Creating Full Features
```python
# For complete feature implementation
prompt = f"""
Create a {feature_name} feature that allows users to {main_purpose}.
Key functionalities:
{functionality_list}

The interface should be intuitive like {reference_app}, with 
{specific_ui_elements}. Include proper error handling and loading states.
Make sure it works well with our existing {integration_points}.
"""
```

### Best Practices for Agents

1. **Context Awareness**
   - Include relevant context from previous work
   - Reference existing components/styles
   - Mention integration points

2. **Progressive Enhancement**
   ```python
   # First: Core functionality
   session = create_v0_session(project_type="feature")
   generate_with_v0(prompt="Basic implementation...", session_id=session_id)
   
   # Then: Add enhancements
   generate_with_v0(prompt="Add animations and polish...", session_id=session_id)
   ```

3. **Design System Alignment**
   - Always mention the project's design system
   - Reference color schemes and component patterns
   - Include accessibility requirements

### Example Agent Prompts

#### Task List Component
```
Create a task list component that integrates with our project management system.
Show tasks with title, status badge, assignee avatar, and due date. Include
filters for status and assignee. The design should match our existing dashboard
components - clean with subtle shadows and our blue accent color. Add keyboard
shortcuts for power users (j/k for navigation, enter to open, x to toggle).
```

#### Data Visualization
```
Build a chart component that displays project progress over time. Use a line
chart showing completed vs total tasks by week. Include a date range selector
and option to switch between different projects. Style it like Linear's 
insights - minimal with smooth animations. The chart should be responsive
and work well in both light and dark modes.
```

#### Form Builder
```
Create a dynamic form builder where users can drag and drop different field
types (text, number, select, date, file upload). Each field should have
configuration options in a sidebar. The interface should feel like Typeform's
builder but simpler. Include preview mode and the ability to save form
templates. Make sure the generated forms are accessible and mobile-friendly.
```

### Common Patterns

#### 1. CRUD Interfaces
```
Build a [resource] management interface where users can view all [resources]
in a table with search and filters. Include actions to add, edit, and delete.
The design should be clean and data-focused like Stripe's dashboard.
```

#### 2. Dashboards
```
Create a dashboard showing [metrics]. Include [chart types] that update in
real-time. The layout should be responsive with cards that users can 
rearrange. Style it like [reference] with our brand colors.
```

#### 3. Settings Pages
```
Build a settings page with sections for [setting categories]. Use a sidebar
navigation on desktop and accordion on mobile. Include immediate save with
success feedback. The design should be simple and clear like Notion's settings.
```

### Error Handling

Always include error handling in prompts:
```
Make sure to handle loading states, errors (show user-friendly messages),
and empty states (with helpful instructions). Include proper form validation
with inline error messages.
```

### Performance Considerations

Mention performance needs when relevant:
```
The list might contain thousands of items, so include virtualization for
performance. Add debounced search and pagination or infinite scroll.
```

### Testing Requirements

For test-driven development:
```
Include unit tests for the main functionality and integration tests for
user workflows. Make sure all interactive elements are keyboard accessible.
```

## Remember

V0 Enhanced works best when you:
1. Describe what users see and do
2. Reference well-known apps for patterns
3. Focus on outcomes, not implementation
4. Include context about the larger system
5. Mention technical requirements simply

The more natural and descriptive your prompt, the better the results!