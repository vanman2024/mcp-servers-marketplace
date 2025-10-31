# V0 Enhanced Quick Reference

## 🚀 One-Line Summary
**V0 Enhanced creates complete UI components from natural language descriptions - talk to it like a designer, not a developer.**

## 🎯 When to Use
- Creating new UI components or pages
- Converting Figma designs to code
- Building dashboards and data visualizations  
- Rapid prototyping of features
- Implementing modern, polished interfaces

## ✅ Good Prompts
```
"Create a team member invite flow that feels like Slack's - clean modal with 
email input, role selector, and a personal message field. Show pending 
invites below with the ability to resend or revoke."
```

## ❌ Bad Prompts
```
"Create InviteModal.tsx with props: {isOpen, onClose, onSubmit} and use 
POST /api/invites endpoint with body: {email, role, message}"
```

## 🎨 Key Principles
1. **Describe the experience**, not the code
2. **Reference popular apps** for UI patterns
3. **Focus on what users do**, not how it works
4. **Include visual details** naturally
5. **Mention tech stack** conversationally

## 📝 Quick Templates

### Component
```
Build a [component] that [what it does]. It should look like [reference] 
with [key features]. Users can [actions]. Make it [requirements].
```

### Feature
```
Create a [feature name] where users can [main purpose]. Include [key elements].
The design should feel [aesthetic] similar to [app reference]. Add [specifics].
```

### Dashboard
```
Build a dashboard for [purpose] showing [metrics]. Use [visualizations] 
that [behavior]. Style it like [reference] but [differences].
```

## 🔧 MCP Tools

### Create Session
```python
mcp__vercel-v0-enhanced__create_v0_session(
    project_type="dashboard"  # Optional context
)
```

### Generate Code
```python
mcp__vercel-v0-enhanced__generate_with_v0(
    prompt="Your natural language description...",
    session_id="xxx",  # From create_v0_session
    create_files=True,
    target_directory="./components"
)
```

### Continue Session
```python
mcp__vercel-v0-enhanced__continue_v0_session(
    session_id="xxx",
    prompt="Now add dark mode support...",
    create_files=True
)
```

## 💡 Pro Tips
- Start simple, enhance iteratively
- Include error states and loading
- Mention responsive behavior
- Reference your design system
- Describe animations and transitions

## 🚨 Remember
**V0 is not ChatGPT** - it's specifically trained on Vercel's ecosystem and modern web patterns. It excels at Next.js, React, Tailwind, and creating production-ready components.