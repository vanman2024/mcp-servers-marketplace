# V0 Enhanced MCP Server - Prompting Guide

## 🎯 Key Principle: Natural Language > Code Specifications

V0 is designed to understand **conversational, descriptive prompts** - not structured code or technical specifications. Think of it as describing your app to a colleague, not writing requirements for a machine.

## ✅ GOOD Prompts (Natural Language)

### Example 1: Todo App
```
Build a modern todo application that feels like Linear or Notion. I want a clean, 
minimalist design with smooth animations. Users should be able to add, edit, and 
delete todos. Include filtering by all/active/completed, and save everything to 
localStorage so it persists. Make it responsive and add dark mode support. 
Use Next.js 14 with App Router, TypeScript, and Tailwind CSS.
```

### Example 2: Dashboard
```
Create a analytics dashboard for tracking website metrics. Show real-time visitor 
count, page views, and user engagement. Include interactive charts that update 
live. The design should be clean and professional, similar to Vercel's dashboard. 
Add date range filters and export functionality. Make it work well on mobile too.
```

### Example 3: E-commerce Product Page
```
Build a product detail page for an online clothing store. Include a large image 
gallery with zoom functionality, size selector, color options, and an add to cart 
button. Show customer reviews with ratings. The design should feel premium and 
minimal, inspired by high-end fashion sites. Include size guide and shipping info.
```

## ❌ BAD Prompts (Too Technical/Structured)

### Don't Do This:
```
Create the following files:
- /components/TodoItem.tsx with props: {id, text, completed, onToggle, onDelete}
- /hooks/useTodos.ts with methods: addTodo(), deleteTodo(), toggleTodo()
- /types/todo.ts with interface Todo { id: string; text: string; completed: boolean }
```

### Or This:
```
REQUIREMENTS:
1. Frontend: React 18.2.0
2. State Management: Zustand 4.5.0
3. Database Schema:
   - users table (id, email, password_hash)
   - todos table (id, user_id, text, completed)
4. API Endpoints:
   - POST /api/todos
   - GET /api/todos
   - PUT /api/todos/:id
```

## 🚀 Effective Prompting Strategies

### 1. **Start with the User Experience**
Describe what the user sees and does, not the technical implementation:
- ✅ "Users can drag and drop todos to reorder them"
- ❌ "Implement react-beautiful-dnd for drag functionality"

### 2. **Use Analogies to Popular Apps**
Reference well-known applications for design and functionality:
- ✅ "Like Notion's clean interface with Todoist's task management"
- ✅ "Similar to Linear's keyboard shortcuts and animations"
- ✅ "Inspired by Stripe's documentation design"

### 3. **Describe Visual Elements Naturally**
- ✅ "A soft shadow that appears on hover"
- ❌ "box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1)"

### 4. **Mention Technical Stack Conversationally**
- ✅ "Use Next.js with TypeScript and make it really fast"
- ❌ "Tech stack: Next.js 14.0.0, TypeScript 5.0.0, SWC compiler"

## 📝 Prompt Templates

### Basic Web App
```
Build a [type of app] that helps users [main purpose]. The interface should be 
[design style] with [key features]. Users can [list main actions]. Make it work 
great on mobile and desktop. Use modern web technologies like Next.js and Tailwind.
```

### Dashboard/Admin Panel
```
Create a dashboard for [who will use it] to manage [what they're managing]. 
Show [key metrics] with [visualization type]. Include [main features]. The design 
should feel [aesthetic description] similar to [reference app]. Add [specific 
functionality] and make sure it's [performance requirement].
```

### Landing Page
```
Design a landing page for [product/service] that [main goal]. Start with a 
[hero section description], then show [main sections]. The style should be 
[design aesthetic] that appeals to [target audience]. Include [specific elements] 
and make sure it [key requirement].
```

## 🔄 Iterative Development

### Start Simple, Then Enhance
1. **First prompt**: Basic functionality
   ```
   "Create a simple blog with a list of posts and individual post pages"
   ```

2. **Second prompt**: Add features
   ```
   "Add a comment system to the blog posts with nested replies"
   ```

3. **Third prompt**: Enhance design
   ```
   "Make the blog design more modern with better typography and spacing"
   ```

## 💡 Pro Tips

1. **Be Conversational**: Write like you're explaining to a friend
2. **Focus on Outcomes**: Describe what you want to achieve, not how
3. **Include Context**: Mention who will use it and why
4. **Reference Examples**: "Like X but with Y" is very effective
5. **Specify Preferences**: Mention if you prefer certain patterns or styles

## 🚨 Common Mistakes to Avoid

1. **Over-specifying Technical Details**
   - Let V0 choose the best implementation
   - Only mention tech if you have specific requirements

2. **Providing File Structures**
   - V0 will create an appropriate structure
   - Focus on functionality instead

3. **Writing Like Documentation**
   - Keep it conversational and descriptive
   - Avoid bullet points and rigid formatting

4. **Being Too Vague**
   - "Make a website" is too broad
   - Include specific features and purpose

## 📊 Measuring Success

A good V0 prompt should:
- ✅ Be readable by a non-developer
- ✅ Paint a clear picture of the final product
- ✅ Include user actions and experiences
- ✅ Reference design inspiration when relevant
- ✅ Mention technical requirements only when necessary

## 🎯 Example: Complete App Prompt

```
I need a recipe sharing platform where home cooks can share their favorite recipes. 
It should feel warm and inviting, like a modern cookbook but digital. Users can 
browse recipes by category (breakfast, lunch, dinner, desserts), search by 
ingredients, and save favorites. 

Each recipe should show a beautiful hero image, prep time, cooking time, 
difficulty level, and serving size. Include step-by-step instructions with 
optional photos for each step. Add a reviews section where people can rate 
recipes and leave comments about their experience.

The design should be clean and food-focused - think Bon Appétit meets Medium. 
Use a warm color palette with lots of white space. Make sure it looks amazing 
on phones since people often cook with their phone in the kitchen.

For logged-in users, let them create their own recipe collections and follow 
other cooks. Include a simple profile page showing their recipes and collections.

Build this with Next.js and whatever modern tools work best. I want it to be 
fast and work offline for viewing saved recipes.
```

This prompt works because it:
- Describes the user experience
- Paints a visual picture
- References known designs
- Mentions technical needs simply
- Focuses on outcomes, not implementation

## Summary

Remember: V0 Enhanced is like a skilled developer who understands context and can make smart technical decisions. Give it the vision and let it handle the implementation details!