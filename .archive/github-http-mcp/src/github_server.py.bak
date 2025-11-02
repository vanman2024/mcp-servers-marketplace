#!/usr/bin/env python3
"""
GitHub MCP Server - HTTP Implementation
Repository management, file operations, issues, PRs, and search via GitHub API

Converted from official MCP TypeScript stdio server to FastMCP HTTP server
"""

import os
import sys
import base64
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path for array_params_fix import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import and apply the array parameters fix
try:
    from array_params_fix import apply_array_params_fix
    apply_array_params_fix()
    logger.info("Array parameters fix applied successfully")
except ImportError:
    logger.warning("Could not import array_params_fix - array parameters may not work correctly")

# GitHub API client
from github import Github, GithubException
from github.GithubException import UnknownObjectException, BadCredentialsException

# FastMCP for HTTP serving
from fastmcp import FastMCP, Context


class GitHubClient:
    """Client for interacting with GitHub API"""
    
    def __init__(self, token: str):
        """Initialize with GitHub token"""
        self.github = Github(token)
        self.user = self.github.get_user()
        logger.info(f"GitHub client initialized for user: {self.user.login}")
    
    def _get_repo(self, owner: str, repo: str):
        """Get repository object"""
        try:
            return self.github.get_repo(f"{owner}/{repo}")
        except UnknownObjectException:
            raise ValueError(f"Repository {owner}/{repo} not found")
        except BadCredentialsException:
            raise ValueError("Invalid GitHub token")
    
    def _ensure_branch_exists(self, repo_obj, branch: str):
        """Ensure branch exists, create if it doesn't"""
        try:
            repo_obj.get_branch(branch)
            logger.info(f"Branch {branch} already exists")
        except UnknownObjectException:
            # Branch doesn't exist, create it from default branch
            default_branch = repo_obj.default_branch
            logger.info(f"Creating branch {branch} from {default_branch}")
            
            source = repo_obj.get_branch(default_branch)
            repo_obj.create_git_ref(f"refs/heads/{branch}", source.commit.sha)
            logger.info(f"Created branch {branch}")


# Initialize FastMCP server
mcp = FastMCP("github")

# Get token from environment
github_token = os.getenv('GITHUB_TOKEN')
if not github_token:
    raise ValueError("GITHUB_TOKEN environment variable required")

# Initialize GitHub client
github_client = GitHubClient(github_token)

# Repository Tools

@mcp.tool()
async def create_repository(
    name: str,
    description: Optional[str] = None,
    private: Optional[bool] = False,
    auto_init: Optional[bool] = True,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Create a new GitHub repository in your account
    
    Args:
        name: Repository name
        description: Repository description
        private: Whether the repository should be private
        auto_init: Initialize with README.md
        ctx: Optional context for logging and progress
    
    Returns:
        Repository details including URL and clone URLs
    """
    if ctx:
        await ctx.info(f"Creating repository: {name} (private: {private})")
    
    try:
        user = github_client.user
        repo = user.create_repo(
            name=name,
            description=description or "",
            private=private,
            auto_init=auto_init
        )
        
        if ctx:
            await ctx.info(f"Successfully created repository: {repo.full_name}")
        
        return {
            "success": True,
            "repository": {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "private": repo.private,
                "html_url": repo.html_url,
                "clone_url": repo.clone_url,
                "ssh_url": repo.ssh_url,
                "default_branch": repo.default_branch
            }
        }
    except GithubException as e:
        logger.error(f"Failed to create repository: {e}")
        if ctx:
            await ctx.error(f"Failed to create repository: {e.data.get('message', str(e))}")
        raise ValueError(f"Failed to create repository: {e.data.get('message', str(e))}")

@mcp.tool()
async def search_repositories(
    query: str,
    page: Optional[int] = 1,
    per_page: Optional[int] = 30,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Search for GitHub repositories
    
    Args:
        query: Search query (see GitHub search syntax)
        page: Page number for pagination (default: 1)
        per_page: Number of results per page (default: 30, max: 100)
        ctx: Optional context for logging and progress
    
    Returns:
        Repository search results with metadata
    """
    if ctx:
        await ctx.info(f"Searching repositories for: {query}")
    
    try:
        per_page = min(per_page or 30, 100)
        repositories = github_client.github.search_repositories(
            query=query,
            sort="stars",
            order="desc"
        )
        
        # Get the specific page
        page_index = (page - 1) * per_page
        results = []
        
        for i, repo in enumerate(repositories):
            if i < page_index:
                continue
            if i >= page_index + per_page:
                break
                
            results.append({
                "name": repo.name,
                "full_name": repo.full_name,
                "owner": repo.owner.login,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language,
                "html_url": repo.html_url,
                "topics": repo.get_topics()
            })
        
        return {
            "success": True,
            "query": query,
            "total_count": repositories.totalCount,
            "page": page,
            "per_page": per_page,
            "results": results
        }
    except GithubException as e:
        logger.error(f"Search failed: {e}")
        raise ValueError(f"Search failed: {e.data.get('message', str(e))}")

@mcp.tool()
async def fork_repository(
    owner: str,
    repo: str,
    organization: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fork a GitHub repository to your account or specified organization
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        organization: Optional: organization to fork to (defaults to your personal account)
    
    Returns:
        Forked repository details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        if organization:
            org = github_client.github.get_organization(organization)
            fork = org.create_fork(repo_obj)
        else:
            fork = github_client.user.create_fork(repo_obj)
        
        return {
            "success": True,
            "repository": {
                "name": fork.name,
                "full_name": fork.full_name,
                "owner": fork.owner.login,
                "parent": f"{owner}/{repo}",
                "html_url": fork.html_url,
                "clone_url": fork.clone_url,
                "ssh_url": fork.ssh_url
            }
        }
    except GithubException as e:
        logger.error(f"Fork failed: {e}")
        raise ValueError(f"Fork failed: {e.data.get('message', str(e))}")

# File Operations

@mcp.tool()
async def get_file_contents(
    owner: str,
    repo: str,
    path: str,
    branch: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get the contents of a file or directory from a GitHub repository
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        path: Path to the file or directory
        branch: Branch to get contents from (defaults to default branch)
    
    Returns:
        File content (decoded) or directory listing
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        try:
            # Handle None branch by using default branch
            ref = branch if branch is not None else repo_obj.default_branch
            contents = repo_obj.get_contents(path, ref=ref)
            
            if isinstance(contents, list):
                # Directory
                return {
                    "success": True,
                    "type": "directory",
                    "path": path,
                    "entries": [
                        {
                            "name": item.name,
                            "path": item.path,
                            "type": item.type,
                            "size": item.size,
                            "sha": item.sha
                        }
                        for item in contents
                    ]
                }
            else:
                # File
                try:
                    # Try UTF-8 first
                    content = base64.b64decode(contents.content).decode('utf-8')
                except UnicodeDecodeError:
                    # If that fails, try latin-1 which accepts all bytes
                    try:
                        content = base64.b64decode(contents.content).decode('latin-1')
                    except:
                        # If all else fails, return raw base64
                        content = contents.content
                
                return {
                    "success": True,
                    "type": "file",
                    "path": contents.path,
                    "name": contents.name,
                    "size": contents.size,
                    "sha": contents.sha,
                    "content": content,
                    "encoding": contents.encoding
                }
        except UnknownObjectException:
            raise ValueError(f"Path '{path}' not found in repository")
            
    except GithubException as e:
        logger.error(f"Failed to get contents: {e}")
        raise ValueError(f"Failed to get contents: {e.data.get('message', str(e))}")

@mcp.tool()
async def create_or_update_file(
    owner: str,
    repo: str,
    path: str,
    content: str,
    message: str,
    branch: str,
    sha: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create or update a single file in a GitHub repository
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        path: Path where to create/update the file
        content: Content of the file
        message: Commit message
        branch: Branch to create/update the file in
        sha: SHA of the file being replaced (required when updating existing files)
    
    Returns:
        File and commit details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # Ensure branch exists
        github_client._ensure_branch_exists(repo_obj, branch)
        
        # Encode content
        content_bytes = content.encode('utf-8')
        
        # Try to get existing file
        existing_sha = sha
        if not existing_sha:
            try:
                # Use branch if provided, otherwise default branch
                ref = branch if branch is not None else repo_obj.default_branch
                existing_file = repo_obj.get_contents(path, ref=ref)
                if not isinstance(existing_file, list):
                    existing_sha = existing_file.sha
            except UnknownObjectException:
                # File doesn't exist, which is fine for create
                pass
        
        if existing_sha:
            # Update existing file
            result = repo_obj.update_file(
                path=path,
                message=message,
                content=content_bytes,
                sha=existing_sha,
                branch=branch
            )
        else:
            # Create new file
            result = repo_obj.create_file(
                path=path,
                message=message,
                content=content_bytes,
                branch=branch
            )
        
        return {
            "success": True,
            "commit": {
                "sha": result['commit'].sha if result.get('commit') else None,
                "message": result['commit'].commit.message if result.get('commit') and result['commit'].commit else None,
                "url": result['commit'].html_url if result.get('commit') else None
            },
            "content": {
                "path": result['content'].path if result.get('content') else path,
                "sha": result['content'].sha if result.get('content') else None,
                "size": result['content'].size if result.get('content') else len(content_bytes)
            }
        }
    except GithubException as e:
        logger.error(f"Failed to create/update file: {e}")
        raise ValueError(f"Failed to create/update file: {e.data.get('message', str(e))}")

@mcp.tool()
async def push_files(
    owner: str,
    repo: str,
    branch: str,
    files: List[Dict[str, str]],
    message: str
) -> Dict[str, Any]:
    """
    Push multiple files to a GitHub repository in a single commit
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        branch: Branch to push to (e.g., 'main' or 'master')
        files: Array of files to push, each with 'path' and 'content'
        message: Commit message
    
    Returns:
        Commit details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # Ensure branch exists
        github_client._ensure_branch_exists(repo_obj, branch)
        
        # Get the branch reference
        ref = repo_obj.get_git_ref(f"heads/{branch}")
        base_tree = repo_obj.get_git_tree(ref.object.sha)
        
        # Create tree elements
        tree_elements = []
        for file_info in files:
            path = file_info['path']
            content = file_info['content']
            
            # Create blob
            blob = repo_obj.create_git_blob(content, "utf-8")
            tree_elements.append({
                "path": path,
                "mode": "100644",  # Regular file
                "type": "blob",
                "sha": blob.sha
            })
        
        # Create tree
        tree = repo_obj.create_git_tree(tree_elements, base_tree)
        
        # Create commit
        parent = repo_obj.get_git_commit(ref.object.sha)
        commit = repo_obj.create_git_commit(
            message=message,
            tree=tree,
            parents=[parent]
        )
        
        # Update reference
        ref.edit(commit.sha)
        
        return {
            "success": True,
            "commit": {
                "sha": commit.sha,
                "message": message,
                "url": f"https://github.com/{owner}/{repo}/commit/{commit.sha}",
                "files_changed": len(files)
            },
            "branch": branch
        }
    except GithubException as e:
        logger.error(f"Failed to push files: {e}")
        raise ValueError(f"Failed to push files: {e.data.get('message', str(e))}")

# Branch Operations

@mcp.tool()
async def create_branch(
    owner: str,
    repo: str,
    branch: str,
    from_branch: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new branch in a GitHub repository
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        branch: Name for the new branch
        from_branch: Optional: source branch to create from (defaults to the repository's default branch)
    
    Returns:
        Branch details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # Get source branch
        source_branch = from_branch or repo_obj.default_branch
        source = repo_obj.get_branch(source_branch)
        
        # Create new branch
        ref = repo_obj.create_git_ref(
            ref=f"refs/heads/{branch}",
            sha=source.commit.sha
        )
        
        return {
            "success": True,
            "branch": {
                "name": branch,
                "ref": ref.ref,
                "sha": ref.object.sha,
                "created_from": source_branch,
                "url": f"https://github.com/{owner}/{repo}/tree/{branch}"
            }
        }
    except GithubException as e:
        logger.error(f"Failed to create branch: {e}")
        raise ValueError(f"Failed to create branch: {e.data.get('message', str(e))}")

# Issue Operations

@mcp.tool()
async def create_issue(
    owner: str,
    repo: str,
    title: str,
    body: Optional[str] = None,
    labels: Optional[List[str]] = None,
    assignees: Optional[List[str]] = None,
    milestone: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create a new issue in a GitHub repository
    
    Args:
        owner: Repository owner
        repo: Repository name
        title: Issue title
        body: Issue description
        labels: Array of label names
        assignees: Array of usernames to assign
        milestone: Milestone number
    
    Returns:
        Created issue details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # Create issue
        issue = repo_obj.create_issue(
            title=title,
            body=body or "",
            labels=labels or [],
            assignees=assignees or []
        )
        
        # Set milestone if provided
        if milestone:
            milestone_obj = repo_obj.get_milestone(milestone)
            issue.edit(milestone=milestone_obj)
        
        return {
            "success": True,
            "issue": {
                "number": issue.number,
                "title": issue.title,
                "body": issue.body,
                "state": issue.state,
                "html_url": issue.html_url,
                "labels": [label.name for label in issue.labels],
                "assignees": [user.login for user in issue.assignees],
                "created_at": issue.created_at.isoformat()
            }
        }
    except GithubException as e:
        logger.error(f"Failed to create issue: {e}")
        raise ValueError(f"Failed to create issue: {e.data.get('message', str(e))}")

@mcp.tool()
async def list_issues(
    owner: str,
    repo: str,
    state: Optional[str] = "open",
    labels: Optional[List[str]] = None,
    sort: Optional[str] = "created",
    direction: Optional[str] = "desc",
    page: Optional[int] = 1,
    per_page: Optional[int] = 30
) -> Dict[str, Any]:
    """
    List issues in a GitHub repository with filtering options
    
    Args:
        owner: Repository owner
        repo: Repository name
        state: State of issues to return (open, closed, all)
        labels: Filter by label names
        sort: What to sort results by (created, updated, comments)
        direction: Sort direction (asc, desc)
        page: Page number
        per_page: Results per page (max 100)
    
    Returns:
        List of issues with metadata
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # Get issues
        issues = repo_obj.get_issues(
            state=state,
            labels=labels or [],
            sort=sort,
            direction=direction
        )
        
        # Paginate
        per_page = min(per_page or 30, 100)
        page_index = (page - 1) * per_page
        results = []
        
        for i, issue in enumerate(issues):
            if i < page_index:
                continue
            if i >= page_index + per_page:
                break
                
            # Skip pull requests
            if issue.pull_request:
                continue
                
            results.append({
                "number": issue.number,
                "title": issue.title,
                "body": issue.body,
                "state": issue.state,
                "html_url": issue.html_url,
                "labels": [label.name for label in issue.labels],
                "assignees": [user.login for user in issue.assignees],
                "created_at": issue.created_at.isoformat(),
                "updated_at": issue.updated_at.isoformat(),
                "comments": issue.comments
            })
        
        return {
            "success": True,
            "page": page,
            "per_page": per_page,
            "total_count": issues.totalCount,
            "issues": results
        }
    except GithubException as e:
        logger.error(f"Failed to list issues: {e}")
        raise ValueError(f"Failed to list issues: {e.data.get('message', str(e))}")

@mcp.tool()
async def add_issue_comment(
    owner: str,
    repo: str,
    issue_number: int,
    body: str
) -> Dict[str, Any]:
    """
    Add a comment to an existing issue
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        issue_number: Issue number
        body: Comment body
        
    Returns:
        Created comment details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        issue = repo_obj.get_issue(issue_number)
        
        # Create comment
        comment = issue.create_comment(body)
        
        return {
            "success": True,
            "comment": {
                "id": comment.id,
                "body": comment.body,
                "html_url": comment.html_url,
                "user": comment.user.login,
                "created_at": comment.created_at.isoformat(),
                "updated_at": comment.updated_at.isoformat()
            }
        }
    except GithubException as e:
        logger.error(f"Failed to add comment: {e}")
        raise ValueError(f"Failed to add comment: {e.data.get('message', str(e))}")

@mcp.tool()
async def update_issue_comment(
    owner: str,
    repo: str,
    comment_id: int,
    body: str
) -> Dict[str, Any]:
    """
    Update an existing issue comment
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        comment_id: Comment ID
        body: New comment body
        
    Returns:
        Updated comment details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        # PyGithub doesn't have get_issue_comment on Repository
        # We need to use the GitHub API directly or get all comments
        # Using direct API call
        comment_url = f"{repo_obj.url}/issues/comments/{comment_id}"
        headers, data = repo_obj._requester.requestJsonAndCheck(
            "PATCH",
            comment_url,
            input={"body": body}
        )
        
        return {
            "success": True,
            "comment": {
                "id": data['id'],
                "body": data['body'],
                "html_url": data['html_url'],
                "user": data['user']['login'],
                "created_at": data['created_at'],
                "updated_at": data['updated_at']
            }
        }
    except GithubException as e:
        logger.error(f"Failed to update comment: {e}")
        raise ValueError(f"Failed to update comment: {e.data.get('message', str(e))}")

@mcp.tool()
async def delete_issue_comment(
    owner: str,
    repo: str,
    comment_id: int
) -> Dict[str, Any]:
    """
    Delete an issue comment
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        comment_id: Comment ID
        
    Returns:
        Success status
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        comment = repo_obj.get_issue_comment(comment_id)
        
        # Delete comment
        comment.delete()
        
        return {
            "success": True,
            "message": f"Comment {comment_id} deleted successfully"
        }
    except GithubException as e:
        logger.error(f"Failed to delete comment: {e}")
        raise ValueError(f"Failed to delete comment: {e.data.get('message', str(e))}")

@mcp.tool()
async def list_issue_comments(
    owner: str,
    repo: str,
    issue_number: int,
    since: Optional[str] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = 30
) -> Dict[str, Any]:
    """
    List comments on an issue
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        issue_number: Issue number
        since: Only show comments updated after this date (ISO 8601 format)
        page: Page number (default: 1)
        per_page: Results per page (default: 30, max: 100)
        
    Returns:
        List of comments
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        issue = repo_obj.get_issue(issue_number)
        
        # Get comments
        if since:
            from datetime import datetime
            since_date = datetime.fromisoformat(since.replace('Z', '+00:00'))
            comments = issue.get_comments(since=since_date)
        else:
            comments = issue.get_comments()
        
        # Paginate
        page_index = (page - 1) * per_page
        results = []
        
        for i, comment in enumerate(comments):
            if i < page_index:
                continue
            if i >= page_index + per_page:
                break
                
            results.append({
                "id": comment.id,
                "body": comment.body,
                "html_url": comment.html_url,
                "user": comment.user.login,
                "created_at": comment.created_at.isoformat(),
                "updated_at": comment.updated_at.isoformat()
            })
        
        return {
            "success": True,
            "issue_number": issue_number,
            "page": page,
            "per_page": per_page,
            "total_count": comments.totalCount,
            "comments": results
        }
    except GithubException as e:
        logger.error(f"Failed to list comments: {e}")
        raise ValueError(f"Failed to list comments: {e.data.get('message', str(e))}")

@mcp.tool()
async def close_issue(
    owner: str,
    repo: str,
    issue_number: int,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """
    Close an issue
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        issue_number: Issue number to close
        reason: Optional reason for closing (added as a comment)
        
    Returns:
        Updated issue details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        issue = repo_obj.get_issue(issue_number)
        
        # Add closing comment if reason provided
        if reason:
            issue.create_comment(reason)
        
        # Close the issue
        issue.edit(state="closed")
        
        return {
            "success": True,
            "issue": {
                "number": issue.number,
                "title": issue.title,
                "state": issue.state,
                "html_url": issue.html_url,
                "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
                "closed_by": issue.closed_by.login if issue.closed_by else None
            }
        }
    except GithubException as e:
        logger.error(f"Failed to close issue: {e}")
        raise ValueError(f"Failed to close issue: {e.data.get('message', str(e))}")

@mcp.tool()
async def update_issue(
    owner: str,
    repo: str,
    issue_number: int,
    title: Optional[str] = None,
    body: Optional[str] = None,
    labels: Optional[List[str]] = None,
    assignees: Optional[List[str]] = None,
    milestone: Optional[int] = None,
    state: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing issue
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        issue_number: Issue number to update
        title: New issue title
        body: New issue body/description
        labels: New list of label names (replaces existing)
        assignees: New list of assignee usernames (replaces existing)
        milestone: Milestone number (None to remove milestone)
        state: Issue state ('open' or 'closed')
    
    Returns:
        Updated issue details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        issue = repo_obj.get_issue(issue_number)
        
        # Prepare update data
        update_kwargs = {}
        if title is not None:
            update_kwargs['title'] = title
        if body is not None:
            update_kwargs['body'] = body
        if state is not None:
            update_kwargs['state'] = state
        if milestone is not None:
            milestone_obj = repo_obj.get_milestone(milestone)
            update_kwargs['milestone'] = milestone_obj
        elif milestone is None and 'milestone' in locals():
            # Explicitly remove milestone
            update_kwargs['milestone'] = None
            
        # Update the issue
        if update_kwargs:
            issue.edit(**update_kwargs)
        
        # Update labels if provided
        if labels is not None:
            issue.set_labels(*labels)
            
        # Update assignees if provided  
        if assignees is not None:
            issue.edit(assignees=assignees)
        
        # Refresh issue data
        issue = repo_obj.get_issue(issue_number)
        
        return {
            "success": True,
            "issue": {
                "number": issue.number,
                "title": issue.title,
                "body": issue.body,
                "state": issue.state,
                "labels": [label.name for label in issue.labels],
                "assignees": [assignee.login for assignee in issue.assignees],
                "milestone": {
                    "title": issue.milestone.title,
                    "number": issue.milestone.number
                } if issue.milestone else None,
                "created_at": issue.created_at.isoformat(),
                "updated_at": issue.updated_at.isoformat(),
                "html_url": issue.html_url
            }
        }
    except GithubException as e:
        logger.error(f"Failed to update issue: {e}")
        raise ValueError(f"Failed to update issue: {e.data.get('message', str(e))}")

@mcp.tool()
async def reopen_issue(
    owner: str,
    repo: str,
    issue_number: int,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """
    Reopen a closed issue
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        issue_number: Issue number to reopen
        reason: Optional reason for reopening (added as a comment)
        
    Returns:
        Updated issue details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        issue = repo_obj.get_issue(issue_number)
        
        # Add reopening comment if reason provided
        if reason:
            issue.create_comment(reason)
        
        # Reopen the issue
        issue.edit(state="open")
        
        return {
            "success": True,
            "issue": {
                "number": issue.number,
                "title": issue.title,
                "state": issue.state,
                "html_url": issue.html_url,
                "reopened_at": datetime.now().isoformat()
            }
        }
    except GithubException as e:
        logger.error(f"Failed to reopen issue: {e}")
        raise ValueError(f"Failed to reopen issue: {e.data.get('message', str(e))}")

# Pull Request Operations

@mcp.tool()
async def create_pull_request(
    owner: str,
    repo: str,
    title: str,
    head: str,
    base: str,
    body: Optional[str] = None,
    draft: Optional[bool] = False,
    maintainer_can_modify: Optional[bool] = True
) -> Dict[str, Any]:
    """
    Create a new pull request in a GitHub repository
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        title: Pull request title
        head: The name of the branch where your changes are implemented
        base: The name of the branch you want the changes pulled into
        body: Pull request body/description
        draft: Whether to create the pull request as a draft
        maintainer_can_modify: Whether maintainers can modify the pull request
    
    Returns:
        Created pull request details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # Create pull request
        pr = repo_obj.create_pull(
            title=title,
            body=body or "",
            head=head,
            base=base,
            draft=draft,
            maintainer_can_modify=maintainer_can_modify
        )
        
        return {
            "success": True,
            "pull_request": {
                "number": pr.number,
                "title": pr.title,
                "body": pr.body,
                "state": pr.state,
                "html_url": pr.html_url,
                "head": {
                    "ref": pr.head.ref,
                    "sha": pr.head.sha
                },
                "base": {
                    "ref": pr.base.ref,
                    "sha": pr.base.sha
                },
                "draft": pr.draft,
                "created_at": pr.created_at.isoformat()
            }
        }
    except GithubException as e:
        logger.error(f"Failed to create pull request: {e}")
        raise ValueError(f"Failed to create pull request: {e.data.get('message', str(e))}")

@mcp.tool()
async def list_pull_requests(
    owner: str,
    repo: str,
    state: Optional[str] = "open",
    head: Optional[str] = None,
    base: Optional[str] = None,
    sort: Optional[str] = "created",
    direction: Optional[str] = "desc",
    page: Optional[int] = 1,
    per_page: Optional[int] = 30
) -> Dict[str, Any]:
    """
    List and filter repository pull requests
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        state: State of the pull requests to return (open, closed, all)
        head: Filter by head user or head organization and branch name
        base: Filter by base branch name
        sort: What to sort results by (created, updated, popularity, long-running)
        direction: The direction of the sort (asc, desc)
        page: Page number of the results
        per_page: Results per page (max 100)
    
    Returns:
        List of pull requests with metadata
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # Get pull requests with proper None handling
        kwargs = {}
        if state is not None:
            kwargs['state'] = state
        if sort is not None:
            kwargs['sort'] = sort  
        if direction is not None:
            kwargs['direction'] = direction
        if base is not None:
            kwargs['base'] = base
        if head is not None:
            kwargs['head'] = head
            
        pulls = repo_obj.get_pulls(**kwargs)
        
        # Paginate
        per_page = min(per_page or 30, 100)
        page_index = (page - 1) * per_page
        results = []
        
        for i, pr in enumerate(pulls):
            if i < page_index:
                continue
            if i >= page_index + per_page:
                break
                
            results.append({
                "number": pr.number,
                "title": pr.title,
                "body": pr.body,
                "state": pr.state,
                "html_url": pr.html_url,
                "head": {
                    "ref": pr.head.ref,
                    "sha": pr.head.sha,
                    "user": pr.head.user.login if pr.head.user else None
                },
                "base": {
                    "ref": pr.base.ref,
                    "sha": pr.base.sha
                },
                "draft": pr.draft,
                "merged": pr.merged,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat()
            })
        
        return {
            "success": True,
            "page": page,
            "per_page": per_page,
            "total_count": pulls.totalCount,
            "pull_requests": results
        }
    except GithubException as e:
        logger.error(f"Failed to list pull requests: {e}")
        raise ValueError(f"Failed to list pull requests: {e.data.get('message', str(e))}")

@mcp.tool()
async def close_pull_request(
    owner: str,
    repo: str,
    pull_number: int,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """
    Close a pull request without merging
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        pull_number: Pull request number to close
        reason: Optional reason for closing (added as a comment)
        
    Returns:
        Updated pull request details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        pr = repo_obj.get_pull(pull_number)
        
        # Add closing comment if reason provided
        if reason:
            pr.create_issue_comment(reason)
        
        # Close the pull request
        pr.edit(state="closed")
        
        return {
            "success": True,
            "pull_request": {
                "number": pr.number,
                "title": pr.title,
                "state": pr.state,
                "html_url": pr.html_url,
                "closed_at": pr.closed_at.isoformat() if pr.closed_at else None
            }
        }
    except GithubException as e:
        logger.error(f"Failed to close pull request: {e}")
        raise ValueError(f"Failed to close pull request: {e.data.get('message', str(e))}")

@mcp.tool()
async def merge_pull_request(
    owner: str,
    repo: str,
    pull_number: int,
    commit_title: Optional[str] = None,
    commit_message: Optional[str] = None,
    merge_method: Optional[str] = "merge"
) -> Dict[str, Any]:
    """
    Merge a pull request
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        pull_number: Pull request number to merge
        commit_title: Title for the merge commit
        commit_message: Message for the merge commit
        merge_method: How to merge (merge, squash, rebase)
        
    Returns:
        Merge result details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        pr = repo_obj.get_pull(pull_number)
        
        # Check if PR is mergeable
        if not pr.mergeable:
            return {
                "success": False,
                "error": "Pull request is not mergeable. Check for conflicts or required status checks."
            }
        
        # Merge the pull request
        result = pr.merge(
            commit_title=commit_title,
            commit_message=commit_message,
            merge_method=merge_method
        )
        
        return {
            "success": result.merged,
            "message": result.message,
            "sha": result.sha,
            "pull_request": {
                "number": pr.number,
                "title": pr.title,
                "merged": True,
                "merged_at": datetime.now().isoformat(),
                "html_url": pr.html_url
            }
        }
    except GithubException as e:
        logger.error(f"Failed to merge pull request: {e}")
        raise ValueError(f"Failed to merge pull request: {e.data.get('message', str(e))}")

# Search Operations

@mcp.tool()
async def search_code(
    q: str,
    sort: Optional[str] = None,
    order: Optional[str] = "desc",
    page: Optional[int] = 1,
    per_page: Optional[int] = 30
) -> Dict[str, Any]:
    """
    Search for code across GitHub repositories
    
    Args:
        q: Search query (GitHub search syntax)
        sort: Sort field (indexed)
        order: Sort order (asc, desc)
        page: Page number (min 1)
        per_page: Results per page (max 100, min 1)
    
    Returns:
        Code search results with file content snippets
    """
    try:
        per_page = min(max(per_page or 30, 1), 100)
        
        # Build query parameters
        kwargs = {"query": q}
        if sort:
            kwargs["sort"] = sort
        if order:
            kwargs["order"] = order
            
        code_results = github_client.github.search_code(**kwargs)
        
        # Paginate
        page_index = (page - 1) * per_page
        results = []
        
        for i, code in enumerate(code_results):
            if i < page_index:
                continue
            if i >= page_index + per_page:
                break
                
            results.append({
                "name": code.name,
                "path": code.path,
                "sha": code.sha,
                "html_url": code.html_url,
                "repository": {
                    "name": code.repository.name,
                    "full_name": code.repository.full_name,
                    "owner": code.repository.owner.login
                }
            })
        
        return {
            "success": True,
            "query": q,
            "total_count": code_results.totalCount,
            "page": page,
            "per_page": per_page,
            "results": results
        }
    except GithubException as e:
        logger.error(f"Code search failed: {e}")
        raise ValueError(f"Code search failed: {e.data.get('message', str(e))}")

@mcp.tool()
async def search_issues(
    q: str,
    sort: Optional[str] = None,
    order: Optional[str] = "desc",
    page: Optional[int] = 1,
    per_page: Optional[int] = 30
) -> Dict[str, Any]:
    """
    Search for issues and pull requests across GitHub repositories
    
    Args:
        q: Search query (GitHub search syntax)
        sort: Sort field (comments, reactions, interactions, created, updated)
        order: Sort order (asc, desc)
        page: Page number (min 1)
        per_page: Results per page (max 100, min 1)
    
    Returns:
        Issue and PR search results
    """
    try:
        per_page = min(max(per_page or 30, 1), 100)
        
        # Build query parameters
        kwargs = {"query": q}
        if sort:
            kwargs["sort"] = sort
        if order:
            kwargs["order"] = order
            
        issue_results = github_client.github.search_issues(**kwargs)
        
        # Paginate
        page_index = (page - 1) * per_page
        results = []
        
        for i, issue in enumerate(issue_results):
            if i < page_index:
                continue
            if i >= page_index + per_page:
                break
                
            results.append({
                "number": issue.number,
                "title": issue.title,
                "body": issue.body[:200] + "..." if issue.body and len(issue.body) > 200 else issue.body,
                "state": issue.state,
                "html_url": issue.html_url,
                "repository": {
                    "name": issue.repository.name,
                    "full_name": issue.repository.full_name,
                    "owner": issue.repository.owner.login
                },
                "type": "pull_request" if issue.pull_request else "issue",
                "created_at": issue.created_at.isoformat(),
                "updated_at": issue.updated_at.isoformat()
            })
        
        return {
            "success": True,
            "query": q,
            "total_count": issue_results.totalCount,
            "page": page,
            "per_page": per_page,
            "results": results
        }
    except GithubException as e:
        logger.error(f"Issue search failed: {e}")
        raise ValueError(f"Issue search failed: {e.data.get('message', str(e))}")

# Milestone Operations

@mcp.tool()
async def list_milestones(
    owner: str,
    repo: str,
    state: Optional[str] = "open",
    sort: Optional[str] = "due_on",
    direction: Optional[str] = "asc",
    page: Optional[int] = 1,
    per_page: Optional[int] = 30
) -> Dict[str, Any]:
    """
    List all milestones for a repository
    
    Args:
        owner: Repository owner
        repo: Repository name
        state: State of milestones to return (open, closed, all)
        sort: Sort field (due_on or completeness)
        direction: Sort direction (asc or desc)
        page: Page number
        per_page: Results per page (max 100)
    
    Returns:
        List of milestones with details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # Get milestones
        milestones = repo_obj.get_milestones(state=state, sort=sort, direction=direction)
        
        # Paginate
        per_page = min(per_page or 30, 100)
        page_index = (page - 1) * per_page
        results = []
        
        for i, milestone in enumerate(milestones):
            if i < page_index:
                continue
            if i >= page_index + per_page:
                break
                
            results.append({
                "number": milestone.number,
                "title": milestone.title,
                "description": milestone.description,
                "state": milestone.state,
                "open_issues": milestone.open_issues,
                "closed_issues": milestone.closed_issues,
                "due_on": milestone.due_on.isoformat() if milestone.due_on else None,
                "created_at": milestone.created_at.isoformat(),
                "updated_at": milestone.updated_at.isoformat(),
                "html_url": milestone.html_url
            })
        
        return {
            "success": True,
            "page": page,
            "per_page": per_page,
            "milestones": results
        }
    except GithubException as e:
        logger.error(f"Failed to list milestones: {e}")
        raise ValueError(f"Failed to list milestones: {e.data.get('message', str(e))}")

@mcp.tool()
async def create_milestone(
    owner: str,
    repo: str,
    title: str,
    state: Optional[str] = "open",
    description: Optional[str] = None,
    due_on: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new milestone
    
    Args:
        owner: Repository owner
        repo: Repository name
        title: Milestone title
        state: State of the milestone (open or closed)
        description: Milestone description
        due_on: Due date in ISO format (YYYY-MM-DD)
    
    Returns:
        Created milestone details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # Parse due date if provided
        due_date = None
        if due_on:
            from datetime import datetime
            due_date = datetime.fromisoformat(due_on.replace('Z', '+00:00'))
        
        # Create milestone
        milestone = repo_obj.create_milestone(
            title=title,
            state=state,
            description=description,
            due_on=due_date
        )
        
        return {
            "success": True,
            "milestone": {
                "number": milestone.number,
                "title": milestone.title,
                "description": milestone.description,
                "state": milestone.state,
                "due_on": milestone.due_on.isoformat() if milestone.due_on else None,
                "html_url": milestone.html_url
            }
        }
    except GithubException as e:
        logger.error(f"Failed to create milestone: {e}")
        raise ValueError(f"Failed to create milestone: {e.data.get('message', str(e))}")

@mcp.tool()
async def update_milestone(
    owner: str,
    repo: str,
    milestone_number: int,
    title: Optional[str] = None,
    state: Optional[str] = None,
    description: Optional[str] = None,
    due_on: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing milestone
    
    Args:
        owner: Repository owner
        repo: Repository name
        milestone_number: Milestone number to update
        title: New title
        state: New state (open or closed)
        description: New description
        due_on: New due date in ISO format
    
    Returns:
        Updated milestone details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        milestone = repo_obj.get_milestone(milestone_number)
        
        # Parse due date if provided
        due_date = None
        if due_on:
            from datetime import datetime
            due_date = datetime.fromisoformat(due_on.replace('Z', '+00:00'))
        
        # Update only provided fields
        if title is not None:
            milestone.edit(title=title)
        if state is not None:
            milestone.edit(state=state)
        if description is not None:
            milestone.edit(description=description)
        if due_on is not None:
            milestone.edit(due_on=due_date)
        
        return {
            "success": True,
            "milestone": {
                "number": milestone.number,
                "title": milestone.title,
                "description": milestone.description,
                "state": milestone.state,
                "due_on": milestone.due_on.isoformat() if milestone.due_on else None
            }
        }
    except GithubException as e:
        logger.error(f"Failed to update milestone: {e}")
        raise ValueError(f"Failed to update milestone: {e.data.get('message', str(e))}")

# Label Operations

@mcp.tool()
async def list_labels(
    owner: str,
    repo: str,
    page: Optional[int] = 1,
    per_page: Optional[int] = 30
) -> Dict[str, Any]:
    """
    List all labels for a repository
    
    Args:
        owner: Repository owner
        repo: Repository name
        page: Page number
        per_page: Results per page (max 100)
    
    Returns:
        List of labels with details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # Get labels
        labels = repo_obj.get_labels()
        
        # Paginate
        per_page = min(per_page or 30, 100)
        page_index = (page - 1) * per_page
        results = []
        
        for i, label in enumerate(labels):
            if i < page_index:
                continue
            if i >= page_index + per_page:
                break
                
            results.append({
                "name": label.name,
                "color": label.color,
                "description": label.description,
                "url": label.url
            })
        
        return {
            "success": True,
            "page": page,
            "per_page": per_page,
            "labels": results
        }
    except GithubException as e:
        logger.error(f"Failed to list labels: {e}")
        raise ValueError(f"Failed to list labels: {e.data.get('message', str(e))}")

@mcp.tool()
async def create_label(
    owner: str,
    repo: str,
    name: str,
    color: str,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new label
    
    Args:
        owner: Repository owner
        repo: Repository name
        name: Label name
        color: Label color (6-character hex code without #)
        description: Label description
    
    Returns:
        Created label details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # Create label
        label = repo_obj.create_label(
            name=name,
            color=color,
            description=description or ""
        )
        
        return {
            "success": True,
            "label": {
                "name": label.name,
                "color": label.color,
                "description": label.description,
                "url": label.url
            }
        }
    except GithubException as e:
        logger.error(f"Failed to create label: {e}")
        raise ValueError(f"Failed to create label: {e.data.get('message', str(e))}")

# Issue Assignment Operations

@mcp.tool()
async def update_issue_assignees(
    owner: str,
    repo: str,
    issue_number: int,
    assignees: List[str]
) -> Dict[str, Any]:
    """
    Update assignees for an issue
    
    Args:
        owner: Repository owner
        repo: Repository name
        issue_number: Issue number
        assignees: List of GitHub usernames to assign
    
    Returns:
        Updated issue details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        issue = repo_obj.get_issue(issue_number)
        
        # Update assignees
        issue.edit(assignees=assignees)
        
        return {
            "success": True,
            "issue": {
                "number": issue.number,
                "title": issue.title,
                "assignees": [a.login for a in issue.assignees]
            }
        }
    except GithubException as e:
        logger.error(f"Failed to update assignees: {e}")
        raise ValueError(f"Failed to update assignees: {e.data.get('message', str(e))}")

# Relationship Operations

@mcp.tool()
async def get_issue_timeline(
    owner: str,
    repo: str,
    issue_number: int
) -> Dict[str, Any]:
    """
    Get timeline events for an issue showing all relationships and references
    
    Args:
        owner: Repository owner
        repo: Repository name
        issue_number: Issue number
    
    Returns:
        Timeline events including cross-references, mentions, and connections
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        issue = repo_obj.get_issue(issue_number)
        
        # Get timeline events
        timeline = issue.get_timeline()
        events = []
        
        for event in timeline:
            if event.event in ['cross-referenced', 'connected', 'disconnected']:
                events.append({
                    "id": event.id,
                    "event": event.event,
                    "created_at": event.created_at.isoformat() if event.created_at else None,
                    "actor": event.actor.login if event.actor else None,
                    "source": {
                        "type": "issue" if hasattr(event.source, 'number') else "pull_request",
                        "number": event.source.number if hasattr(event.source, 'number') else None,
                        "title": event.source.title if hasattr(event.source, 'title') else None
                    } if hasattr(event, 'source') and event.source else None
                })
        
        # Also get PRs that reference this issue
        referencing_prs = []
        
        # Search for PRs that mention this issue
        search_query = f"repo:{owner}/{repo} is:pr #{issue_number}"
        pr_results = github_client.github.search_issues(query=search_query)
        
        for pr in pr_results:
            if pr.pull_request:
                referencing_prs.append({
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "url": pr.html_url
                })
        
        return {
            "success": True,
            "issue_number": issue_number,
            "timeline_events": events,
            "referencing_pull_requests": referencing_prs
        }
    except GithubException as e:
        logger.error(f"Failed to get issue timeline: {e}")
        raise ValueError(f"Failed to get issue timeline: {e.data.get('message', str(e))}")

@mcp.tool()
async def get_pr_related_issues(
    owner: str,
    repo: str,
    pr_number: int
) -> Dict[str, Any]:
    """
    Get all issues related to a pull request (closes, fixes, resolves)
    
    Args:
        owner: Repository owner
        repo: Repository name
        pr_number: Pull request number
    
    Returns:
        Related issues that this PR closes/fixes
    """
    try:
        import re
        
        repo_obj = github_client._get_repo(owner, repo)
        pr = repo_obj.get_pull(pr_number)
        
        # Parse PR body for issue references
        body_text = (pr.body or "") + "\n" + (pr.title or "")
        
        # Common patterns for closing issues
        closing_patterns = [
            r'(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)',
            r'#(\d+)\s+(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)',
            r'(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+(?:https?://github\.com/[\w-]+/[\w-]+/issues/)?(\d+)'
        ]
        
        related_issues = set()
        
        for pattern in closing_patterns:
            matches = re.findall(pattern, body_text, re.IGNORECASE)
            for match in matches:
                issue_num = int(match) if match.isdigit() else int(match.split('/')[-1])
                related_issues.add(issue_num)
        
        # Get details for each related issue
        issues_data = []
        for issue_num in related_issues:
            try:
                issue = repo_obj.get_issue(issue_num)
                issues_data.append({
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "labels": [label.name for label in issue.labels],
                    "milestone": issue.milestone.title if issue.milestone else None,
                    "url": issue.html_url
                })
            except:
                # Issue might not exist or be inaccessible
                pass
        
        return {
            "success": True,
            "pull_request_number": pr_number,
            "closes_issues": issues_data,
            "pr_state": pr.state,
            "pr_merged": pr.merged
        }
    except GithubException as e:
        logger.error(f"Failed to get PR related issues: {e}")
        raise ValueError(f"Failed to get PR related issues: {e.data.get('message', str(e))}")

@mcp.tool()
async def create_issue_dependency(
    owner: str,
    repo: str,
    issue_number: int,
    depends_on: List[int],
    blocks: List[int],
    comment_template: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create dependency relationships between issues using comments
    
    Args:
        owner: Repository owner
        repo: Repository name
        issue_number: Issue number
        depends_on: List of issue numbers this issue depends on
        blocks: List of issue numbers this issue blocks
        comment_template: Custom comment template (uses default if not provided)
    
    Returns:
        Created comment with dependency information
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        issue = repo_obj.get_issue(issue_number)
        
        # Build dependency comment
        if not comment_template:
            comment_lines = ["## Dependencies\n"]
            
            if depends_on:
                comment_lines.append("**Depends on:**")
                for dep_num in depends_on:
                    comment_lines.append(f"- #{dep_num}")
                comment_lines.append("")
            
            if blocks:
                comment_lines.append("**Blocks:**")
                for block_num in blocks:
                    comment_lines.append(f"- #{block_num}")
            
            comment_template = "\n".join(comment_lines)
        
        # Create comment
        comment = issue.create_comment(comment_template)
        
        # Also add labels if they exist
        try:
            labels_to_add = []
            if depends_on:
                labels_to_add.append("has-dependencies")
            if blocks:
                labels_to_add.append("blocking")
            
            if labels_to_add:
                existing_labels = [label.name for label in issue.labels]
                issue.add_to_labels(*[label for label in labels_to_add if label not in existing_labels])
        except:
            # Labels might not exist, that's okay
            pass
        
        return {
            "success": True,
            "issue_number": issue_number,
            "comment_id": comment.id,
            "depends_on": depends_on,
            "blocks": blocks,
            "comment_url": comment.html_url
        }
    except GithubException as e:
        logger.error(f"Failed to create issue dependency: {e}")
        raise ValueError(f"Failed to create issue dependency: {e.data.get('message', str(e))}")

@mcp.tool()
async def sync_relationships_to_devloop(
    owner: str,
    repo: str,
    project_id: str,
    supabase_url: Optional[str] = None,
    supabase_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Sync GitHub issue/PR relationships to DevLoop task dependencies
    
    Args:
        owner: Repository owner
        repo: Repository name
        project_id: DevLoop project ID
        supabase_url: Supabase URL (optional)
        supabase_key: Supabase service key (optional)
    
    Returns:
        Sync results with created/updated relationships
    """
    try:
        from supabase import create_client
        import re
        
        # Initialize Supabase client
        url = supabase_url or os.getenv("SUPABASE_URL")
        key = supabase_key or os.getenv("SUPABASE_SERVICE_KEY")
        
        if not url or not key:
            raise ValueError("Supabase credentials not provided")
            
        supabase = create_client(url, key)
        
        # Get all tasks with GitHub issue numbers
        tasks_response = supabase.table("tasks").select("*").not_.is_("github_issue_number", "null").execute()
        
        if not tasks_response.data:
            return {"success": True, "message": "No tasks with GitHub issues found"}
        
        # Create mapping of issue number to task ID
        issue_to_task = {task["github_issue_number"]: task["id"] for task in tasks_response.data}
        
        synced_relationships = []
        
        # Get repository
        repo_obj = github_client._get_repo(owner, repo)
        
        # Process each task's GitHub issue
        for task in tasks_response.data:
            issue_num = task["github_issue_number"]
            
            try:
                issue = repo_obj.get_issue(issue_num)
                
                # Parse issue body for dependencies
                body_text = issue.body or ""
                
                # Look for dependency patterns
                depends_patterns = [
                    r'[Dd]epends on:?\s*#(\d+)',
                    r'[Bb]locked by:?\s*#(\d+)',
                    r'[Rr]equires:?\s*#(\d+)'
                ]
                
                blocks_patterns = [
                    r'[Bb]locks:?\s*#(\d+)',
                    r'[Bb]locking:?\s*#(\d+)'
                ]
                
                depends_on_issues = set()
                blocks_issues = set()
                
                for pattern in depends_patterns:
                    matches = re.findall(pattern, body_text)
                    depends_on_issues.update(int(m) for m in matches)
                
                for pattern in blocks_patterns:
                    matches = re.findall(pattern, body_text)
                    blocks_issues.update(int(m) for m in matches)
                
                # Also check comments for dependency information
                for comment in issue.get_comments():
                    comment_text = comment.body
                    
                    for pattern in depends_patterns:
                        matches = re.findall(pattern, comment_text)
                        depends_on_issues.update(int(m) for m in matches)
                    
                    for pattern in blocks_patterns:
                        matches = re.findall(pattern, comment_text)
                        blocks_issues.update(int(m) for m in matches)
                
                # Create task dependencies in database
                for dep_issue in depends_on_issues:
                    if dep_issue in issue_to_task:
                        dep_data = {
                            "task_id": task["id"],
                            "depends_on_task_id": issue_to_task[dep_issue],
                            "dependency_type": "depends_on",
                            "github_source": f"issue_{issue_num}_depends_on_{dep_issue}"
                        }
                        
                        # Check if dependency already exists
                        existing = supabase.table("task_dependencies").select("*").eq(
                            "task_id", task["id"]
                        ).eq("depends_on_task_id", issue_to_task[dep_issue]).execute()
                        
                        if not existing.data:
                            supabase.table("task_dependencies").insert(dep_data).execute()
                            synced_relationships.append({
                                "type": "depends_on",
                                "from_task": task["id"],
                                "to_task": issue_to_task[dep_issue],
                                "github_issues": f"#{issue_num} → #{dep_issue}"
                            })
                
                # Create blocking relationships
                for blocked_issue in blocks_issues:
                    if blocked_issue in issue_to_task:
                        dep_data = {
                            "task_id": issue_to_task[blocked_issue],
                            "depends_on_task_id": task["id"],
                            "dependency_type": "blocked_by",
                            "github_source": f"issue_{blocked_issue}_blocked_by_{issue_num}"
                        }
                        
                        # Check if dependency already exists
                        existing = supabase.table("task_dependencies").select("*").eq(
                            "task_id", issue_to_task[blocked_issue]
                        ).eq("depends_on_task_id", task["id"]).execute()
                        
                        if not existing.data:
                            supabase.table("task_dependencies").insert(dep_data).execute()
                            synced_relationships.append({
                                "type": "blocks",
                                "from_task": task["id"],
                                "to_task": issue_to_task[blocked_issue],
                                "github_issues": f"#{issue_num} → #{blocked_issue}"
                            })
                
            except Exception as e:
                logger.warning(f"Failed to process issue {issue_num}: {e}")
                continue
        
        return {
            "success": True,
            "synced_count": len(synced_relationships),
            "relationships": synced_relationships
        }
    except Exception as e:
        logger.error(f"Failed to sync relationships: {e}")
        raise ValueError(f"Failed to sync relationships: {str(e)}")

# DevLoop Sync Operations

@mcp.tool()
async def sync_milestones_from_github(
    owner: str,
    repo: str,
    project_id: str,
    supabase_url: Optional[str] = None,
    supabase_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Import GitHub milestones into DevLoop database as phases
    
    Args:
        owner: Repository owner
        repo: Repository name
        project_id: DevLoop project ID to sync milestones to
        supabase_url: Supabase URL (optional, uses env var if not provided)
        supabase_key: Supabase service key (optional, uses env var if not provided)
    
    Returns:
        Sync results with created/updated phases
    """
    try:
        from supabase import create_client
        
        # Initialize Supabase client
        url = supabase_url or os.getenv("SUPABASE_URL")
        key = supabase_key or os.getenv("SUPABASE_SERVICE_KEY")
        
        if not url or not key:
            raise ValueError("Supabase credentials not provided")
            
        supabase = create_client(url, key)
        
        # Get all milestones from GitHub
        repo_obj = github_client._get_repo(owner, repo)
        milestones = repo_obj.get_milestones(state="all")
        
        synced_phases = []
        
        for milestone in milestones:
            # Check if phase already exists with this GitHub milestone
            existing = supabase.table("phases").select("*").eq(
                "github_milestone_number", milestone.number
            ).eq("project_id", project_id).execute()
            
            phase_data = {
                "name": milestone.title,
                "description": milestone.description or "",
                "status": "active" if milestone.state == "open" else "completed",
                "project_id": project_id,
                "github_milestone_number": milestone.number,
                "due_date": milestone.due_on.isoformat() if milestone.due_on else None,
                "progress": (milestone.closed_issues / (milestone.open_issues + milestone.closed_issues) * 100) if (milestone.open_issues + milestone.closed_issues) > 0 else 0
            }
            
            if existing.data:
                # Update existing phase
                result = supabase.table("phases").update(phase_data).eq(
                    "id", existing.data[0]["id"]
                ).execute()
                synced_phases.append({
                    "action": "updated",
                    "phase_id": existing.data[0]["id"],
                    "milestone_number": milestone.number,
                    "title": milestone.title
                })
            else:
                # Create new phase
                result = supabase.table("phases").insert(phase_data).execute()
                synced_phases.append({
                    "action": "created",
                    "phase_id": result.data[0]["id"],
                    "milestone_number": milestone.number,
                    "title": milestone.title
                })
        
        return {
            "success": True,
            "synced_count": len(synced_phases),
            "phases": synced_phases
        }
    except Exception as e:
        logger.error(f"Failed to sync milestones: {e}")
        raise ValueError(f"Failed to sync milestones: {str(e)}")

@mcp.tool()
async def sync_issues_from_github(
    owner: str,
    repo: str,
    module_id: str,
    milestone_number: Optional[int] = None,
    labels: Optional[List[str]] = None,
    supabase_url: Optional[str] = None,
    supabase_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Import GitHub issues into DevLoop database as tasks
    
    Args:
        owner: Repository owner
        repo: Repository name
        module_id: DevLoop module ID to sync issues to
        milestone_number: Filter by milestone number
        labels: Filter by labels
        supabase_url: Supabase URL (optional)
        supabase_key: Supabase service key (optional)
    
    Returns:
        Sync results with created/updated tasks
    """
    try:
        from supabase import create_client
        import re
        
        # Initialize Supabase client
        url = supabase_url or os.getenv("SUPABASE_URL")
        key = supabase_key or os.getenv("SUPABASE_SERVICE_KEY")
        
        if not url or not key:
            raise ValueError("Supabase credentials not provided")
            
        supabase = create_client(url, key)
        
        # Get issues from GitHub
        repo_obj = github_client._get_repo(owner, repo)
        issues = repo_obj.get_issues(state="all")
        
        if milestone_number:
            milestone = repo_obj.get_milestone(milestone_number)
            issues = issues.filter(milestone=milestone)
        
        if labels:
            issues = issues.filter(labels=labels)
        
        synced_tasks = []
        
        for issue in issues:
            # Skip pull requests
            if issue.pull_request:
                continue
                
            # Extract task ID from issue body if present
            task_id_match = re.search(r'Task ID: ([a-f0-9-]+)', issue.body or "")
            existing_task_id = task_id_match.group(1) if task_id_match else None
            
            # Map GitHub issue state to task status
            status_map = {
                "open": "pending",
                "closed": "completed"
            }
            
            task_data = {
                "name": issue.title,
                "description": issue.body or "",
                "status": status_map.get(issue.state, "pending"),
                "module_id": module_id,
                "github_issue_number": issue.number,
                "priority": "high" if any(label.name.lower() == "priority-high" for label in issue.labels) else "medium",
                "assigned_to": issue.assignee.login if issue.assignee else None
            }
            
            if existing_task_id:
                # Update existing task
                result = supabase.table("tasks").update(task_data).eq(
                    "id", existing_task_id
                ).execute()
                synced_tasks.append({
                    "action": "updated",
                    "task_id": existing_task_id,
                    "issue_number": issue.number,
                    "title": issue.title
                })
            else:
                # Check if task already exists with this issue number
                existing = supabase.table("tasks").select("*").eq(
                    "github_issue_number", issue.number
                ).eq("module_id", module_id).execute()
                
                if existing.data:
                    # Update existing task
                    result = supabase.table("tasks").update(task_data).eq(
                        "id", existing.data[0]["id"]
                    ).execute()
                    synced_tasks.append({
                        "action": "updated",
                        "task_id": existing.data[0]["id"],
                        "issue_number": issue.number,
                        "title": issue.title
                    })
                else:
                    # Create new task
                    result = supabase.table("tasks").insert(task_data).execute()
                    synced_tasks.append({
                        "action": "created",
                        "task_id": result.data[0]["id"],
                        "issue_number": issue.number,
                        "title": issue.title
                    })
        
        return {
            "success": True,
            "synced_count": len(synced_tasks),
            "tasks": synced_tasks
        }
    except Exception as e:
        logger.error(f"Failed to sync issues: {e}")
        raise ValueError(f"Failed to sync issues: {str(e)}")

# Commit Operations

@mcp.tool()
async def list_commits(
    owner: str,
    repo: str,
    sha: Optional[str] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = 30
) -> Dict[str, Any]:
    """
    Get list of commits of a branch in a GitHub repository
    
    Args:
        owner: Repository owner
        repo: Repository name
        sha: SHA or branch to start listing commits from (defaults to default branch)
        page: Page number
        per_page: Results per page (max 100)
    
    Returns:
        List of commits with details
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # Get commits with proper None handling
        kwargs = {}
        if sha is not None:
            kwargs['sha'] = sha
        commits = repo_obj.get_commits(**kwargs)
        
        # Paginate
        per_page = min(per_page or 30, 100)
        page_index = (page - 1) * per_page
        results = []
        
        for i, commit in enumerate(commits):
            if i < page_index:
                continue
            if i >= page_index + per_page:
                break
                
            results.append({
                "sha": commit.sha,
                "message": commit.commit.message,
                "author": {
                    "name": commit.commit.author.name,
                    "email": commit.commit.author.email,
                    "date": commit.commit.author.date.isoformat()
                },
                "committer": {
                    "name": commit.commit.committer.name,
                    "email": commit.commit.committer.email,
                    "date": commit.commit.committer.date.isoformat()
                },
                "html_url": commit.html_url,
                "parents": [parent.sha for parent in commit.parents]
            })
        
        return {
            "success": True,
            "page": page,
            "per_page": per_page,
            "total_count": commits.totalCount,
            "commits": results
        }
    except GithubException as e:
        logger.error(f"Failed to list commits: {e}")
        raise ValueError(f"Failed to list commits: {e.data.get('message', str(e))}")

@mcp.tool()
async def create_sub_issue(
    owner: str,
    repo: str,
    parent_issue_number: int,
    title: str,
    body: Optional[str] = None,
    labels: Optional[List[str]] = None,
    assignees: Optional[List[str]] = None,
    milestone: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create a true GitHub sub-issue using GitHub's sub-issues API (2025)
    
    This function creates proper sub-issues using GitHub's REST API endpoints,
    not just regular issues with labels/comments.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        parent_issue_number: Parent issue number to link to
        title: Sub-issue title
        body: Sub-issue description
        labels: List of label names to add
        assignees: List of usernames to assign
        milestone: Milestone number
        
    Returns:
        Created sub-issue details with parent linkage information
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # Validate parent issue exists and is accessible
        try:
            parent_issue = repo_obj.get_issue(parent_issue_number)
            logger.info(f"Validated parent issue #{parent_issue_number}: {parent_issue.title}")
        except UnknownObjectException:
            raise ValueError(f"Parent issue #{parent_issue_number} not found")
        except GithubException as e:
            raise ValueError(f"Cannot access parent issue #{parent_issue_number}: {e.data.get('message', str(e))}")
        
        # Step 1: Create a regular child issue first
        logger.info(f"Creating child issue '{title}' for parent #{parent_issue_number}")
        issue_kwargs = {
            "title": title,
            "body": body or f"Sub-issue of #{parent_issue_number}"
        }
        
        if labels:
            issue_kwargs["labels"] = labels
        if assignees:
            issue_kwargs["assignees"] = assignees
        if milestone is not None:
            milestone_obj = repo_obj.get_milestone(milestone)
            issue_kwargs["milestone"] = milestone_obj
        
        child_issue = repo_obj.create_issue(**issue_kwargs)
        logger.info(f"Created child issue #{child_issue.number}")
        
        # Step 2: Use GitHub's sub-issues API to establish the relationship
        # This is the proper GitHub sub-issues API introduced in 2025
        try:
            logger.info(f"Creating sub-issue relationship: parent #{parent_issue_number} -> child #{child_issue.number} (ID: {child_issue.id})")
            
            # Use direct REST API with the existing GitHub client's requester
            # NOTE: sub_issue_id must be the issue ID (not number)
            sub_issues_url = f"/repos/{owner}/{repo}/issues/{parent_issue_number}/sub_issues"
            payload = {
                "sub_issue_id": child_issue.id  # Use ID, not number!
            }
            
            # Use the same pattern as other direct API calls in this file
            headers, data = repo_obj._requester.requestJsonAndCheck(
                "POST",
                sub_issues_url,
                input=payload
            )
            
            # Successfully created sub-issue relationship
            logger.info(f"✅ Sub-issue relationship created successfully via REST API")
            
            return {
                "success": True,
                "sub_issue": {
                    "number": child_issue.number,
                    "id": child_issue.id,
                    "title": child_issue.title,
                    "body": child_issue.body,
                    "state": child_issue.state,
                    "html_url": child_issue.html_url,
                    "labels": [label.name for label in child_issue.labels],
                    "assignees": [assignee.login for assignee in child_issue.assignees],
                    "created_at": child_issue.created_at.isoformat(),
                    "milestone": child_issue.milestone.title if child_issue.milestone else None,
                    "is_sub_issue": True
                },
                "parent_issue": {
                    "number": parent_issue.number,
                    "title": parent_issue.title,
                    "html_url": parent_issue.html_url
                },
                "linkage": {
                    "github_sub_issue_api_used": True,
                    "relationship_type": "true_sub_issue",
                    "method": "direct_rest_api",
                    "api_response": data
                }
            }
                
        except Exception as api_error:
            logger.warning(f"Failed to use GitHub sub-issues API: {api_error}")
            # Fall back to label-based approach
            fallback_result = await create_sub_issue_fallback(
                repo_obj, parent_issue, child_issue, title
            )
            fallback_result["linkage"]["api_fallback_reason"] = str(api_error)
            return fallback_result
            
    except GithubException as e:
        logger.error(f"Failed to create sub-issue: {e}")
        raise ValueError(f"Failed to create sub-issue: {e.data.get('message', str(e))}")


async def create_sub_issue_fallback(repo_obj, parent_issue, child_issue, title):
    """
    Fallback method using labels and comments when GitHub sub-issues API is not available
    """
    try:
        # Add sub-issue labels to the child issue
        sub_labels = ["sub-issue", f"child-of-{parent_issue.number}"]
        
        # Update the child issue with sub-issue labels
        current_labels = [label.name for label in child_issue.labels]
        all_labels = list(set(current_labels + sub_labels))
        child_issue.edit(labels=all_labels)
        
        # Add cross-reference comment to parent issue
        parent_comment = f"Sub-issue created: #{child_issue.number} - {title}"
        parent_issue.create_comment(parent_comment)
        logger.info(f"Added cross-reference comment to parent issue #{parent_issue.number}")
        
        # Update child issue body with parent reference
        enhanced_body = f"**Parent Issue:** #{parent_issue.number}\n\n{child_issue.body}"
        child_issue.edit(body=enhanced_body)
        
        return {
            "success": True,
            "sub_issue": {
                "number": child_issue.number,
                "title": child_issue.title,
                "body": child_issue.body,
                "state": child_issue.state,
                "html_url": child_issue.html_url,
                "labels": all_labels,
                "assignees": [assignee.login for assignee in child_issue.assignees],
                "created_at": child_issue.created_at.isoformat(),
                "milestone": child_issue.milestone.title if child_issue.milestone else None,
                "is_sub_issue": False  # Not a true sub-issue, just labeled
            },
            "parent_issue": {
                "number": parent_issue.number,
                "title": parent_issue.title,
                "html_url": parent_issue.html_url
            },
            "linkage": {
                "github_sub_issue_api_used": False,
                "relationship_type": "label_based_fallback",
                "parent_reference_added": True,
                "cross_reference_comment_added": True,
                "labels_added": sub_labels
            }
        }
    except Exception as e:
        logger.error(f"Fallback sub-issue creation failed: {e}")
        raise ValueError(f"Fallback sub-issue creation failed: {str(e)}")


@mcp.tool()
async def list_sub_issues(
    owner: str,
    repo: str,
    issue_number: int,
    per_page: Optional[int] = 30,
    page: Optional[int] = 1
) -> Dict[str, Any]:
    """
    List all sub-issues for a given parent issue
    
    Args:
        owner: Repository owner
        repo: Repository name  
        issue_number: Parent issue number
        per_page: Number of results per page (max 100)
        page: Page number for pagination
        
    Returns:
        List of sub-issues with metadata
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # List sub-issues using GitHub REST API
        sub_issues_url = f"/repos/{owner}/{repo}/issues/{issue_number}/sub_issues"
        
        params = {
            "per_page": per_page,
            "page": page
        }
        
        headers, data = repo_obj._requester.requestJsonAndCheck(
            "GET",
            sub_issues_url,
            parameters=params
        )
        
        return {
            "success": True,
            "sub_issues": data,
            "count": len(data),
            "pagination": {
                "page": page,
                "per_page": per_page
            }
        }
        
    except GithubException as e:
        logger.error(f"Failed to list sub-issues: {e}")
        raise ValueError(f"Failed to list sub-issues: {e.data.get('message', str(e))}")


@mcp.tool()
async def remove_sub_issue(
    owner: str,
    repo: str,
    parent_issue_number: int,
    sub_issue_id: int
) -> Dict[str, Any]:
    """
    Remove a sub-issue from a parent issue
    
    Args:
        owner: Repository owner
        repo: Repository name
        parent_issue_number: Parent issue number  
        sub_issue_id: Sub-issue ID to remove (issue ID, not number)
        
    Returns:
        Confirmation of removal
    """
    try:
        repo_obj = github_client._get_repo(owner, repo)
        
        # Remove sub-issue using GitHub REST API
        sub_issue_url = f"/repos/{owner}/{repo}/issues/{parent_issue_number}/sub_issue"
        
        payload = {
            "sub_issue_id": sub_issue_id
        }
        
        headers, data = repo_obj._requester.requestJsonAndCheck(
            "DELETE",
            sub_issue_url,
            input=payload
        )
        
        logger.info(f"✅ Removed sub-issue ID {sub_issue_id} from parent #{parent_issue_number}")
        
        return {
            "success": True,
            "message": f"Sub-issue {sub_issue_id} removed from parent issue #{parent_issue_number}",
            "parent_issue": data
        }
        
    except GithubException as e:
        logger.error(f"Failed to remove sub-issue: {e}")
        raise ValueError(f"Failed to remove sub-issue: {e.data.get('message', str(e))}")


@mcp.tool()
async def reprioritize_sub_issue(
    owner: str,
    repo: str,
    parent_issue_number: int,
    sub_issue_id: int,
    after_id: Optional[int] = None,
    before_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Reprioritize a sub-issue to a different position in the parent's sub-issue list
    
    Args:
        owner: Repository owner
        repo: Repository name
        parent_issue_number: Parent issue number
        sub_issue_id: Sub-issue ID to reprioritize
        after_id: Position after this sub-issue ID (either after_id OR before_id)
        before_id: Position before this sub-issue ID (either after_id OR before_id)
        
    Returns:
        Updated parent issue with new sub-issue order
    """
    try:
        if not after_id and not before_id:
            raise ValueError("Either after_id or before_id must be specified")
        if after_id and before_id:
            raise ValueError("Only one of after_id or before_id should be specified")
            
        repo_obj = github_client._get_repo(owner, repo)
        
        # Reprioritize sub-issue using GitHub REST API
        priority_url = f"/repos/{owner}/{repo}/issues/{parent_issue_number}/sub_issues/priority"
        
        payload = {
            "sub_issue_id": sub_issue_id
        }
        
        if after_id:
            payload["after_id"] = after_id
        if before_id:
            payload["before_id"] = before_id
        
        headers, data = repo_obj._requester.requestJsonAndCheck(
            "PATCH",
            priority_url,
            input=payload
        )
        
        position = f"after {after_id}" if after_id else f"before {before_id}"
        logger.info(f"✅ Reprioritized sub-issue {sub_issue_id} to position {position}")
        
        return {
            "success": True,
            "message": f"Sub-issue {sub_issue_id} reprioritized to position {position}",
            "new_position": {"after_id": after_id, "before_id": before_id},
            "parent_issue": data
        }
        
    except GithubException as e:
        logger.error(f"Failed to reprioritize sub-issue: {e}")
        raise ValueError(f"Failed to reprioritize sub-issue: {e.data.get('message', str(e))}")


if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv('GITHUB_MCP_PORT', '8011'))
    
    logger.info(f"Starting GitHub MCP Server on port {port}")
    logger.info(f"Authenticated as: {github_client.user.login}")
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")