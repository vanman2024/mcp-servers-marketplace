# Git Advanced HTTP MCP Server

Advanced Git operations with worktree management for parallel agent development. This server enables multiple Claude instances to work on different features simultaneously without conflicts.

## Features

- Complete git operations (status, add, commit, branch, log)
- **Worktree management** for isolated agent workspaces
- Advanced operations (stash, cherry-pick, rebase, merge)
- Agent-aware context tracking
- Conflict resolution support
- Parallel-safe operations

## Server Organization

The server is organized into clear sections:

### 🛠️ Tools (13 main tools)
- **Basic Operations**: `git_status`, `git_add`, `git_commit`, `git_log`, `git_branch`
- **Worktree Management**: `worktree_add`, `worktree_list`, `worktree_remove`, `worktree_sync`
- **Advanced Operations**: `git_stash`, `git_push` (planned), `git_merge` (planned), `git_rebase` (planned)

### 📚 Resources (4 resource endpoints)
- **Usage Guide**: Comprehensive worktree workflow documentation
- **Worktree Examples**: Practical examples for parallel development
- **Git Commands**: Reference for all available commands
- **Agent Patterns**: Common patterns for agent git usage

### 💡 Prompts (5 specialized prompts)
- **Workflow Guide**: Git workflows for different task types
- **Commit Messages**: Conventional commit message templates
- **Conflict Resolution**: Step-by-step conflict resolution
- **Branch Strategy**: Project-specific branching strategies
- **Agent Checklist**: Pre-flight checklist for agents

## Setup

1. Install dependencies:
   ```bash
   cd servers/http/git-advanced-http-mcp
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export GIT_BASE_REPO_PATH=/path/to/your/repo  # Default: current directory
   export GIT_WORKTREE_BASE=/path/to/worktrees   # Default: .worktrees in repo
   export GIT_ADVANCED_MCP_PORT=8045              # Default: 8045
   ```

3. Run the server:
   ```bash
   python src/git_advanced_server.py
   ```

## Usage with Claude

1. Add to Claude:
   ```bash
   claude mcp add --transport http git-advanced http://localhost:8045
   ```

2. Use tools with worktree pattern:
   ```python
   # Agent requests isolated workspace
   worktree = await worktree_add(
       branch="feat/issue-123",
       agent_id="backend-agent-1",
       create_branch=True
   )
   
   # All operations use worktree path
   await git_add(files=["."], worktree_path=worktree["worktree_path"])
   await git_commit(message="feat: Add feature", worktree_path=worktree["worktree_path"])
   ```

3. Access resources:
   ```bash
   /mcp_resource git-advanced://usage_guide
   /mcp_resource git-advanced://worktree_examples
   ```

## Parallel Agent Workflow

### 1. Agent Initialization
Each agent gets its own worktree:
```python
# Backend agent
backend_wt = await worktree_add(
    branch="feat/api-endpoints",
    agent_id="backend-agent",
    create_branch=True
)

# Frontend agent
frontend_wt = await worktree_add(
    branch="feat/ui-components",
    agent_id="frontend-agent",
    create_branch=True
)
```

### 2. Isolated Development
Agents work without conflicts:
```python
# Backend agent commits
await git_commit(
    message="feat: Add user API",
    worktree_path=backend_wt["worktree_path"]
)

# Frontend agent commits simultaneously
await git_commit(
    message="feat: Add user dashboard",
    worktree_path=frontend_wt["worktree_path"]
)
```

### 3. Coordination
```python
# List all agent workspaces
worktrees = await worktree_list()

# Sync with main branch
await worktree_sync(agent_id="backend-agent", target_branch="main")
```

### 4. Cleanup
```python
# Remove worktree when done
await worktree_remove(agent_id="backend-agent")
```

## Best Practices

1. **One Worktree Per Agent**: Ensures complete isolation
2. **Descriptive Branch Names**: Include issue numbers
3. **Regular Syncing**: Keep worktrees updated with main
4. **Atomic Commits**: Clear, focused changes
5. **Clean Up**: Remove worktrees after merging

## Integration with MCP Manager

Add to `scripts/mcp-manager.sh`:
```bash
"git-advanced")
    PORT=8045
    cd "$MCP_ROOT/servers/http/git-advanced-http-mcp" || exit 1
    source venv/bin/activate 2>/dev/null || python -m venv venv && source venv/bin/activate
    pip install -q -r requirements.txt
    GIT_BASE_REPO_PATH="$PROJECT_ROOT" \
    GIT_ADVANCED_MCP_PORT=$PORT \
    python src/git_advanced_server.py &
    ;;
```

## Error Handling

The server handles common git scenarios:
- Uncommitted changes when removing worktrees
- Merge conflicts during sync operations
- Invalid branch names
- Non-existent worktrees
- Permission issues

## Security Considerations

- Operates only within configured repository
- No remote operations without explicit commands
- Validates all file paths
- Prevents operations outside repository

## Future Enhancements

- Push/pull operations for remote collaboration
- Advanced merge strategies
- Interactive rebase support
- Worktree templates
- Git hooks integration
- Performance metrics per agent

## Troubleshooting

### "No git repository found"
Set `GIT_BASE_REPO_PATH` to a valid git repository

### "Worktree already exists"
Each agent needs a unique ID

### "Permission denied"
Ensure write permissions in repository and worktree base

### Port conflicts
Change port with `GIT_ADVANCED_MCP_PORT` environment variable