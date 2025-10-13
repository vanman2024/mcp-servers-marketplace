# V0 Platform API - Quick Reference

## Core Workflow

### 1. Project Setup
```python
# Create project
project = await create_v0_project(
    name="My App",
    description="Description here",
    environment_variables={"API_URL": "https://api.example.com"}
)

# Create session and link
session = await create_v0_session(project_type="web_app")
await assign_project_to_chat(session["session_id"], project["project_id"])
```

### 2. Context Loading
```python
# From GitHub repository
await initialize_chat_from_repo(
    session["session_id"],
    "https://github.com/user/repo"
)

# From local files
await initialize_chat_from_files(
    session["session_id"],
    ["src/App.tsx", "package.json", "tailwind.config.js"],
    base_path="/path/to/project"
)
```

### 3. Development
```python
# Generate with context
result = await generate_with_v0(
    prompt="Add a user dashboard with charts and data tables",
    session_id=session["session_id"],
    create_files=True,
    target_directory="./generated"
)

# Continue conversation
await continue_v0_session(
    session["session_id"],
    "Make it responsive and add dark mode"
)
```

### 4. Deployment
```python
# Deploy to Vercel
deployment = await create_v0_deployment(
    session["session_id"],
    deployment_name="dashboard-v1"
)

# Check status
status = await get_deployment_status(deployment["deployment_id"])
print(f"Status: {status['status']}, URL: {status['url']}")
```

## Session Management

### Forking & Experimentation
```python
# Fork for different approach
fork = await fork_v0_chat(
    session["session_id"],
    new_name="Alternative design"
)

# Work in fork
await generate_with_v0(
    prompt="Try a different layout approach",
    session_id=fork["forked_session_id"]
)
```

### Organization
```python
# Add metadata
await update_chat_metadata(
    session["session_id"],
    {"feature": "user-dashboard", "status": "in-progress"}
)

# Mark as favorite
await favorite_chat(session["session_id"], True)

# List all sessions
sessions = await list_v0_sessions()
for s in sessions["sessions"]:
    if s["is_favorite"]:
        print(f"⭐ {s['session_id']}: {s['metadata']}")
```

## Project Management

### List & Retrieve
```python
# List all projects
projects = await list_v0_projects()
for p in projects["projects"]:
    print(f"{p['name']}: {p['chat_count']} chats")

# Get specific project
project = await get_v0_project_by_id("project-id-here")
print(f"Environment vars: {project['environment_variables']}")
```

## Error Handling Pattern
```python
result = await create_v0_project(name="Test")
if not result["success"]:
    print(f"Error: {result['error']}")
else:
    print(f"Created: {result['project_id']}")
```

## New Tool Summary

| Category | Tool | Purpose |
|----------|------|---------|
| **Projects** | `create_v0_project` | Create new project |
| | `list_v0_projects` | List all projects |
| | `get_v0_project_by_id` | Get project details |
| | `assign_project_to_chat` | Link session to project |
| **Context** | `initialize_chat_from_repo` | Load GitHub repo |
| | `initialize_chat_from_files` | Load local files |
| **Deploy** | `create_v0_deployment` | Deploy to Vercel |
| | `get_deployment_status` | Check deploy status |
| | `get_deployment_logs` | Get deploy logs |
| **Sessions** | `fork_v0_chat` | Fork/branch session |
| | `update_chat_metadata` | Add metadata |
| | `favorite_chat` | Mark as favorite |

All tools return `{"success": boolean, ...}` format with comprehensive error handling.