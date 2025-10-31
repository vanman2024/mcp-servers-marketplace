# GitHub MCP Server (HTTP)

Comprehensive GitHub API access via FastMCP with HTTP transport.

Converted from the official MCP TypeScript stdio server to Python HTTP implementation using PyGithub.

## Features

- **Repository Management**: Create, fork, search repositories
- **File Operations**: Read, create, update files and directories
- **Multi-file Commits**: Push multiple files in a single commit
- **Branch Management**: Create and manage branches
- **Issues & PRs**: Create, list, and manage issues and pull requests
- **Advanced Search**: Search code, issues, and repositories
- **Automatic Branch Creation**: Branches created automatically when needed
- **HTTP Transport**: Using FastMCP with streamable-http

## Tools

### Repository Operations
- `create_repository(name, description?, private?, auto_init?)` - Create new repository
- `search_repositories(query, page?, per_page?)` - Search repositories
- `fork_repository(owner, repo, organization?)` - Fork a repository

### File Operations
- `get_file_contents(owner, repo, path, branch?)` - Get file or directory contents
- `create_or_update_file(owner, repo, path, content, message, branch, sha?)` - Create/update single file
- `push_files(owner, repo, branch, files, message)` - Push multiple files in one commit

### Branch Operations
- `create_branch(owner, repo, branch, from_branch?)` - Create new branch

### Issue Operations
- `create_issue(owner, repo, title, body?, labels?, assignees?, milestone?)` - Create issue
- `list_issues(owner, repo, state?, labels?, sort?, direction?, page?, per_page?)` - List issues

### Pull Request Operations
- `create_pull_request(owner, repo, title, head, base, body?, draft?, maintainer_can_modify?)` - Create PR
- `list_pull_requests(owner, repo, state?, head?, base?, sort?, direction?, page?, per_page?)` - List PRs

### Search Operations
- `search_code(q, sort?, order?, page?, per_page?)` - Search code across GitHub
- `search_issues(q, sort?, order?, page?, per_page?)` - Search issues and PRs

### Commit Operations
- `list_commits(owner, repo, sha?, page?, per_page?)` - List repository commits

## Configuration

### Environment Variables

```bash
# GitHub Personal Access Token (required)
GITHUB_TOKEN=your_github_token_here

# Server port
GITHUB_MCP_PORT=8004
```

### Default Settings
- **Default port**: 8004
- **Transport**: streamable-http
- **Authentication**: Personal Access Token

## Installation

```bash
# Install dependencies
pip install fastmcp python-dotenv uvicorn httpx PyGithub

# Run server
python src/github_server.py
```

## Usage Examples

### Create Repository
```python
{
    "name": "create_repository",
    "arguments": {
        "name": "my-new-repo",
        "description": "A test repository",
        "private": false,
        "auto_init": true
    }
}
```

### Search Repositories
```python
{
    "name": "search_repositories",
    "arguments": {
        "query": "language:python stars:>1000",
        "per_page": 10
    }
}
```

### Create or Update File
```python
{
    "name": "create_or_update_file",
    "arguments": {
        "owner": "myusername",
        "repo": "myrepo",
        "path": "README.md",
        "content": "# My Project\n\nThis is my project.",
        "message": "Update README",
        "branch": "main"
    }
}
```

### Push Multiple Files
```python
{
    "name": "push_files",
    "arguments": {
        "owner": "myusername",
        "repo": "myrepo",
        "branch": "feature-branch",
        "files": [
            {"path": "src/main.py", "content": "print('Hello, World!')"},
            {"path": "src/utils.py", "content": "def helper(): pass"}
        ],
        "message": "Add initial Python files"
    }
}
```

### Create Issue
```python
{
    "name": "create_issue",
    "arguments": {
        "owner": "myusername",
        "repo": "myrepo",
        "title": "Bug: Something is broken",
        "body": "## Description\n\nDetailed description here...",
        "labels": ["bug", "high-priority"]
    }
}
```

### Create Pull Request
```python
{
    "name": "create_pull_request",
    "arguments": {
        "owner": "myusername",
        "repo": "myrepo",
        "title": "Feature: Add new functionality",
        "head": "feature-branch",
        "base": "main",
        "body": "## Changes\n\n- Added new feature\n- Fixed bugs",
        "draft": false
    }
}
```

## HTTP Endpoints

The server runs on `http://localhost:8004` with MCP tools available at:
- `POST /tools/call` - Execute MCP tools
- `GET /tools/list` - List available tools
- `GET /health` - Health check

## Rate Limiting

GitHub API has rate limits:
- **Authenticated requests**: 5,000 per hour
- **Search requests**: 30 per minute

The server will return appropriate error messages when rate limits are exceeded.

## Error Handling

Common errors and their meanings:
- **401**: Invalid or missing GitHub token
- **403**: Insufficient permissions or rate limit exceeded
- **404**: Repository, file, or resource not found
- **422**: Validation error (e.g., invalid branch name)

## Getting a GitHub Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` (full control of private repositories)
   - `public_repo` (access to public repositories)
   - `read:org` (read org and team membership)
   - `user` (read user profile data)
4. Generate token and set as `GITHUB_TOKEN` environment variable

## Conversion Notes

This server maintains 100% feature parity with the original TypeScript stdio version while adding:

- **HTTP transport** for web integration
- **Async/await** throughout for performance
- **PyGithub** for robust GitHub API interaction
- **Better error messages** with specific causes
- **Automatic branch creation** when needed

## Testing

```bash
# Test repository search
curl -X POST http://localhost:8004/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "search_repositories",
    "arguments": {
        "query": "mcp servers",
        "per_page": 5
    }
  }'

# Test file reading
curl -X POST http://localhost:8004/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "get_file_contents",
    "arguments": {
        "owner": "modelcontextprotocol",
        "repo": "servers",
        "path": "README.md"
    }
  }'
```