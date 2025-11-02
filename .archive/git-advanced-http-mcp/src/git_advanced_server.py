#!/usr/bin/env python3
"""
Git Advanced FastMCP Server for Parallel Agent Development

This server provides advanced Git operations including worktree management
for parallel agent development. It enables multiple Claude instances to work
on different features simultaneously without conflicts.

Architecture:
- Standard Git operations (status, add, commit, push, etc.)
- Worktree management for isolated development environments
- Advanced operations (stash, cherry-pick, rebase, merge)
- Agent-aware context tracking
"""

import os
import logging
import asyncio
import json
import subprocess
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path

from fastmcp import FastMCP
from fastmcp.server.context import Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Git Advanced MCP Server")

# ===================================================================
# CONFIGURATION & INITIALIZATION
# ===================================================================

# Track active worktrees and their agents
ACTIVE_WORKTREES: Dict[str, Dict[str, Any]] = {}

# Base repository path (can be overridden by environment)
BASE_REPO_PATH = os.getenv('GIT_BASE_REPO_PATH', os.getcwd())

# Worktree storage directory
WORKTREE_BASE = os.getenv('GIT_WORKTREE_BASE', os.path.join(BASE_REPO_PATH, '.worktrees'))

async def run_git_command(
    cmd: List[str],
    cwd: Optional[str] = None,
    check: bool = True
) -> Tuple[bool, str, str]:
    """
    Run a git command and return success, stdout, stderr
    """
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd or BASE_REPO_PATH
        )
        stdout, stderr = await process.communicate()
        
        success = process.returncode == 0 if check else True
        return success, stdout.decode('utf-8').strip(), stderr.decode('utf-8').strip()
        
    except Exception as e:
        logger.error(f"Git command failed: {e}")
        return False, "", str(e)

def get_worktree_path(agent_id: str, branch: str) -> str:
    """Generate a consistent worktree path for an agent"""
    safe_branch = branch.replace('/', '-')
    return os.path.join(WORKTREE_BASE, f"{agent_id}-{safe_branch}")

# ===================================================================
# STANDALONE TOOLS (simple tools that don't call other tools)
# ===================================================================

@mcp.tool()
async def git_status(
    worktree_path: Optional[str] = None,
    verbose: bool = False,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Get git status for main repo or specific worktree
    
    Args:
        worktree_path: Path to worktree (uses main repo if not specified)
        verbose: Include untracked files and detailed info
        ctx: Context for logging
    """
    try:
        if ctx:
            await ctx.info(f"Getting git status for: {worktree_path or 'main repo'}")
        
        cwd = worktree_path or BASE_REPO_PATH
        cmd = ["git", "status", "--porcelain"]
        if verbose:
            cmd.append("-v")
        
        success, stdout, stderr = await run_git_command(cmd, cwd=cwd)
        
        if not success:
            return {"success": False, "error": stderr}
        
        # Parse status output
        changes = {
            "modified": [],
            "added": [],
            "deleted": [],
            "renamed": [],
            "untracked": []
        }
        
        for line in stdout.split('\n'):
            if not line:
                continue
            
            status = line[:2]
            file_path = line[3:]
            
            if status == "??":
                changes["untracked"].append(file_path)
            elif "M" in status:
                changes["modified"].append(file_path)
            elif "A" in status:
                changes["added"].append(file_path)
            elif "D" in status:
                changes["deleted"].append(file_path)
            elif "R" in status:
                changes["renamed"].append(file_path)
        
        # Get current branch
        success, branch, _ = await run_git_command(
            ["git", "branch", "--show-current"],
            cwd=cwd
        )
        
        result = {
            "success": True,
            "branch": branch,
            "changes": changes,
            "has_changes": any(changes.values()),
            "worktree": worktree_path is not None
        }
        
        if ctx:
            await ctx.info(f"Status complete: {len(changes['modified'])} modified, "
                          f"{len(changes['untracked'])} untracked files")
        
        return result
        
    except Exception as e:
        logger.error(f"Git status error: {e}")
        if ctx:
            await ctx.error(f"Git status failed: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def git_add(
    files: List[str],
    worktree_path: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Stage files for commit
    
    Args:
        files: List of file paths to stage (use ["."] for all)
        worktree_path: Path to worktree (uses main repo if not specified)
        ctx: Context for logging
    """
    try:
        if ctx:
            await ctx.info(f"Staging {len(files)} files")
        
        cwd = worktree_path or BASE_REPO_PATH
        cmd = ["git", "add"] + files
        
        success, stdout, stderr = await run_git_command(cmd, cwd=cwd)
        
        if not success:
            return {"success": False, "error": stderr}
        
        # Get updated status
        status_result = await git_status(worktree_path=worktree_path)
        
        return {
            "success": True,
            "files_staged": files,
            "current_status": status_result.get("changes", {})
        }
        
    except Exception as e:
        logger.error(f"Git add error: {e}")
        if ctx:
            await ctx.error(f"Git add failed: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def git_commit(
    message: str,
    worktree_path: Optional[str] = None,
    amend: bool = False,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Create a git commit
    
    Args:
        message: Commit message
        worktree_path: Path to worktree (uses main repo if not specified)
        amend: Amend the last commit instead of creating new one
        ctx: Context for logging
    """
    try:
        if ctx:
            await ctx.info(f"Creating commit: {message[:50]}...")
        
        cwd = worktree_path or BASE_REPO_PATH
        cmd = ["git", "commit", "-m", message]
        if amend:
            cmd.insert(2, "--amend")
        
        success, stdout, stderr = await run_git_command(cmd, cwd=cwd)
        
        if not success:
            return {"success": False, "error": stderr}
        
        # Get commit SHA
        success, commit_sha, _ = await run_git_command(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd
        )
        
        return {
            "success": True,
            "commit_sha": commit_sha[:7],
            "message": message,
            "amended": amend
        }
        
    except Exception as e:
        logger.error(f"Git commit error: {e}")
        if ctx:
            await ctx.error(f"Git commit failed: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def git_log(
    max_count: int = 10,
    oneline: bool = True,
    worktree_path: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    View git commit history
    
    Args:
        max_count: Maximum number of commits to show
        oneline: Use compact one-line format
        worktree_path: Path to worktree (uses main repo if not specified)
        ctx: Context for logging
    """
    try:
        if ctx:
            await ctx.info(f"Getting last {max_count} commits")
        
        cwd = worktree_path or BASE_REPO_PATH
        cmd = ["git", "log", f"-{max_count}"]
        if oneline:
            cmd.append("--oneline")
        else:
            cmd.extend(["--pretty=format:%H|%an|%ae|%at|%s"])
        
        success, stdout, stderr = await run_git_command(cmd, cwd=cwd)
        
        if not success:
            return {"success": False, "error": stderr}
        
        commits = []
        for line in stdout.split('\n'):
            if not line:
                continue
            
            if oneline:
                parts = line.split(' ', 1)
                commits.append({
                    "sha": parts[0],
                    "message": parts[1] if len(parts) > 1 else ""
                })
            else:
                parts = line.split('|')
                if len(parts) >= 5:
                    commits.append({
                        "sha": parts[0][:7],
                        "author": parts[1],
                        "email": parts[2],
                        "timestamp": parts[3],
                        "message": parts[4]
                    })
        
        return {
            "success": True,
            "commits": commits,
            "count": len(commits)
        }
        
    except Exception as e:
        logger.error(f"Git log error: {e}")
        if ctx:
            await ctx.error(f"Git log failed: {str(e)}")
        return {"success": False, "error": str(e)}

# ===================================================================
# CLASS-BASED TOOLS (complex tools that call other tools)
# ===================================================================

class GitWorktreeOperations:
    """
    Complex worktree operations that coordinate multiple git commands
    """
    
    async def worktree_add(
        self,
        branch: str,
        agent_id: str,
        create_branch: bool = False,
        base_branch: Optional[str] = None,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Create a new git worktree for an agent
        
        Args:
            branch: Branch name to checkout in worktree
            agent_id: Unique identifier for the agent
            create_branch: Create new branch if it doesn't exist
            base_branch: Base branch for new branch (default: current branch)
            ctx: Context for logging
        """
        try:
            if ctx:
                await ctx.info(f"Creating worktree for agent {agent_id} on branch {branch}")
            
            # Generate worktree path
            worktree_path = get_worktree_path(agent_id, branch)
            
            # Ensure worktree base directory exists
            os.makedirs(WORKTREE_BASE, exist_ok=True)
            
            # Build command
            cmd = ["git", "worktree", "add"]
            if create_branch:
                cmd.append("-b")
                cmd.append(branch)
                cmd.append(worktree_path)
                if base_branch:
                    cmd.append(base_branch)
            else:
                cmd.extend([worktree_path, branch])
            
            success, stdout, stderr = await run_git_command(cmd)
            
            if not success:
                return {"success": False, "error": stderr}
            
            # Track the worktree
            ACTIVE_WORKTREES[agent_id] = {
                "path": worktree_path,
                "branch": branch,
                "created_at": datetime.now().isoformat(),
                "agent_id": agent_id,
                "status": "active"
            }
            
            # Get initial status
            status = await git_status(worktree_path=worktree_path)
            
            result = {
                "success": True,
                "worktree_path": worktree_path,
                "branch": branch,
                "agent_id": agent_id,
                "created": True,
                "initial_status": status
            }
            
            if ctx:
                await ctx.info(f"✅ Worktree created at: {worktree_path}")
            
            return result
            
        except Exception as e:
            logger.error(f"Worktree add error: {e}")
            if ctx:
                await ctx.error(f"Worktree creation failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def worktree_list(
        self,
        include_details: bool = True,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        List all git worktrees with their status
        
        Args:
            include_details: Include detailed information about each worktree
            ctx: Context for logging
        """
        try:
            if ctx:
                await ctx.info("Listing all worktrees")
            
            cmd = ["git", "worktree", "list"]
            if include_details:
                cmd.append("--porcelain")
            
            success, stdout, stderr = await run_git_command(cmd)
            
            if not success:
                return {"success": False, "error": stderr}
            
            worktrees = []
            
            if include_details:
                # Parse porcelain output
                current = {}
                for line in stdout.split('\n'):
                    if not line:
                        if current:
                            # Match with tracked worktrees
                            for agent_id, info in ACTIVE_WORKTREES.items():
                                if info["path"] == current.get("worktree"):
                                    current["agent_id"] = agent_id
                                    current["tracked"] = True
                                    break
                            else:
                                current["tracked"] = False
                            
                            worktrees.append(current)
                            current = {}
                    elif line.startswith('worktree '):
                        current["worktree"] = line.split(' ', 1)[1]
                    elif line.startswith('HEAD '):
                        current["head"] = line.split(' ', 1)[1]
                    elif line.startswith('branch '):
                        current["branch"] = line.split(' ', 1)[1]
                    elif line.startswith('bare'):
                        current["bare"] = True
                
                if current:
                    worktrees.append(current)
            else:
                # Parse simple output
                for line in stdout.split('\n'):
                    if line:
                        parts = line.split()
                        if len(parts) >= 3:
                            worktrees.append({
                                "path": parts[0],
                                "commit": parts[1],
                                "branch": parts[2].strip('[]')
                            })
            
            # Add tracking info
            result = {
                "success": True,
                "worktrees": worktrees,
                "count": len(worktrees),
                "active_agents": list(ACTIVE_WORKTREES.keys())
            }
            
            if ctx:
                await ctx.info(f"Found {len(worktrees)} worktrees, "
                              f"{len(ACTIVE_WORKTREES)} tracked by agents")
            
            return result
            
        except Exception as e:
            logger.error(f"Worktree list error: {e}")
            if ctx:
                await ctx.error(f"Worktree list failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def worktree_remove(
        self,
        agent_id: str,
        force: bool = False,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Remove a git worktree for an agent
        
        Args:
            agent_id: Agent identifier whose worktree to remove
            force: Force removal even if there are uncommitted changes
            ctx: Context for logging
        """
        try:
            if agent_id not in ACTIVE_WORKTREES:
                return {
                    "success": False,
                    "error": f"No worktree found for agent {agent_id}"
                }
            
            worktree_info = ACTIVE_WORKTREES[agent_id]
            worktree_path = worktree_info["path"]
            
            if ctx:
                await ctx.info(f"Removing worktree for agent {agent_id}: {worktree_path}")
            
            # Check for uncommitted changes
            status = await git_status(worktree_path=worktree_path)
            if status.get("has_changes") and not force:
                return {
                    "success": False,
                    "error": "Worktree has uncommitted changes. Use force=True to remove anyway.",
                    "changes": status.get("changes", {})
                }
            
            # Remove the worktree
            cmd = ["git", "worktree", "remove", worktree_path]
            if force:
                cmd.insert(3, "--force")
            
            success, stdout, stderr = await run_git_command(cmd)
            
            if not success:
                return {"success": False, "error": stderr}
            
            # Remove from tracking
            del ACTIVE_WORKTREES[agent_id]
            
            result = {
                "success": True,
                "removed_path": worktree_path,
                "agent_id": agent_id,
                "forced": force
            }
            
            if ctx:
                await ctx.info(f"✅ Worktree removed for agent {agent_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Worktree remove error: {e}")
            if ctx:
                await ctx.error(f"Worktree removal failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def worktree_sync(
        self,
        agent_id: str,
        target_branch: str = "main",
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Sync worktree with target branch (merge or rebase)
        
        Args:
            agent_id: Agent identifier whose worktree to sync
            target_branch: Branch to sync with (default: main)
            ctx: Context for logging
        """
        try:
            if agent_id not in ACTIVE_WORKTREES:
                return {
                    "success": False,
                    "error": f"No worktree found for agent {agent_id}"
                }
            
            worktree_path = ACTIVE_WORKTREES[agent_id]["path"]
            
            if ctx:
                await ctx.info(f"Syncing worktree for agent {agent_id} with {target_branch}")
            
            # Fetch latest changes
            success, _, stderr = await run_git_command(
                ["git", "fetch", "origin", target_branch],
                cwd=worktree_path
            )
            
            if not success:
                return {"success": False, "error": f"Fetch failed: {stderr}"}
            
            # Try to merge
            success, stdout, stderr = await run_git_command(
                ["git", "merge", f"origin/{target_branch}", "--no-edit"],
                cwd=worktree_path
            )
            
            if not success:
                # Check if it's a merge conflict
                if "CONFLICT" in stderr or "CONFLICT" in stdout:
                    return {
                        "success": False,
                        "error": "Merge conflict detected",
                        "conflict": True,
                        "message": "Manual intervention required to resolve conflicts"
                    }
                return {"success": False, "error": stderr}
            
            # Get updated status
            status = await git_status(worktree_path=worktree_path)
            
            result = {
                "success": True,
                "synced_with": target_branch,
                "agent_id": agent_id,
                "current_status": status
            }
            
            if ctx:
                await ctx.info(f"✅ Worktree synced with {target_branch}")
            
            return result
            
        except Exception as e:
            logger.error(f"Worktree sync error: {e}")
            if ctx:
                await ctx.error(f"Worktree sync failed: {str(e)}")
            return {"success": False, "error": str(e)}

# Create instance and register class methods
worktree_ops = GitWorktreeOperations()
mcp.tool()(worktree_ops.worktree_add)
mcp.tool()(worktree_ops.worktree_list)
mcp.tool()(worktree_ops.worktree_remove)
mcp.tool()(worktree_ops.worktree_sync)

# ===================================================================
# ADVANCED GIT OPERATIONS
# ===================================================================

@mcp.tool()
async def git_stash(
    action: str = "push",
    message: Optional[str] = None,
    worktree_path: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Manage git stash
    
    Args:
        action: Stash action (push, pop, list, drop)
        message: Message for stash (when pushing)
        worktree_path: Path to worktree (uses main repo if not specified)
        ctx: Context for logging
    """
    try:
        if ctx:
            await ctx.info(f"Git stash {action}")
        
        cwd = worktree_path or BASE_REPO_PATH
        
        if action == "push":
            cmd = ["git", "stash", "push"]
            if message:
                cmd.extend(["-m", message])
        elif action == "pop":
            cmd = ["git", "stash", "pop"]
        elif action == "list":
            cmd = ["git", "stash", "list"]
        elif action == "drop":
            cmd = ["git", "stash", "drop"]
        else:
            return {"success": False, "error": f"Unknown stash action: {action}"}
        
        success, stdout, stderr = await run_git_command(cmd, cwd=cwd)
        
        if not success:
            return {"success": False, "error": stderr}
        
        result = {
            "success": True,
            "action": action,
            "output": stdout
        }
        
        if action == "list":
            stashes = []
            for line in stdout.split('\n'):
                if line:
                    parts = line.split(':', 2)
                    if len(parts) >= 3:
                        stashes.append({
                            "index": parts[0],
                            "branch": parts[1].strip(),
                            "message": parts[2].strip()
                        })
            result["stashes"] = stashes
        
        return result
        
    except Exception as e:
        logger.error(f"Git stash error: {e}")
        if ctx:
            await ctx.error(f"Git stash failed: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def git_branch(
    action: str = "list",
    branch_name: Optional[str] = None,
    worktree_path: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Manage git branches
    
    Args:
        action: Branch action (list, create, delete, checkout)
        branch_name: Name of branch (for create/delete/checkout)
        worktree_path: Path to worktree (uses main repo if not specified)
        ctx: Context for logging
    """
    try:
        if ctx:
            await ctx.info(f"Git branch {action}")
        
        cwd = worktree_path or BASE_REPO_PATH
        
        if action == "list":
            cmd = ["git", "branch", "-a"]
        elif action == "create" and branch_name:
            cmd = ["git", "branch", branch_name]
        elif action == "delete" and branch_name:
            cmd = ["git", "branch", "-d", branch_name]
        elif action == "checkout" and branch_name:
            cmd = ["git", "checkout", branch_name]
        else:
            return {"success": False, "error": f"Invalid branch action or missing branch_name"}
        
        success, stdout, stderr = await run_git_command(cmd, cwd=cwd)
        
        if not success:
            return {"success": False, "error": stderr}
        
        result = {
            "success": True,
            "action": action,
            "branch_name": branch_name
        }
        
        if action == "list":
            branches = []
            current_branch = None
            for line in stdout.split('\n'):
                if line:
                    is_current = line.startswith('*')
                    branch = line[2:].strip()
                    branches.append({
                        "name": branch,
                        "current": is_current
                    })
                    if is_current:
                        current_branch = branch
            
            result["branches"] = branches
            result["current_branch"] = current_branch
        
        return result
        
    except Exception as e:
        logger.error(f"Git branch error: {e}")
        if ctx:
            await ctx.error(f"Git branch failed: {str(e)}")
        return {"success": False, "error": str(e)}

# ===================================================================
# RESOURCES
# ===================================================================

@mcp.resource("resource://usage_guide")
def usage_guide() -> str:
    """
    Comprehensive guide for using Git Advanced MCP Server
    """
    return """
# Git Advanced MCP Server Usage Guide

## 🚨 CRITICAL: Worktree Management for Parallel Agents

This server is specifically designed for parallel agent development using Git worktrees.
Each agent gets its own isolated workspace to prevent conflicts.

## Workflow Pattern:

### 1. Agent Initialization
```python
# Each agent requests a worktree when starting work
worktree = await worktree_add(
    branch="feat/issue-123-authentication",
    agent_id="backend-agent-1",
    create_branch=True,
    base_branch="main"
)
# Returns: {"worktree_path": "/path/to/worktree", ...}
```

### 2. Agent Development
All git operations accept worktree_path parameter:
```python
# Agent works in isolated environment
await git_add(files=["."], worktree_path=worktree["worktree_path"])
await git_commit(message="feat: Add auth logic", worktree_path=worktree["worktree_path"])
```

### 3. Agent Coordination
```python
# List all active agent workspaces
worktrees = await worktree_list()

# Sync with main branch
await worktree_sync(agent_id="backend-agent-1", target_branch="main")
```

### 4. Cleanup
```python
# Remove worktree when agent completes
await worktree_remove(agent_id="backend-agent-1")
```

## Best Practices:

1. **One Worktree Per Agent**: Each agent should have its own worktree
2. **Clear Naming**: Use descriptive branch names with issue numbers
3. **Regular Syncing**: Keep worktrees up to date with main branch
4. **Clean Commits**: Make atomic commits with clear messages
5. **Proper Cleanup**: Remove worktrees when work is complete

## Error Handling:

- Check for conflicts when syncing
- Handle uncommitted changes before removing worktrees
- Verify branch existence before checkout
- Monitor worktree disk usage
"""

@mcp.resource("resource://worktree_examples")
def worktree_examples() -> str:
    """
    Practical examples of worktree usage
    """
    return """
# Worktree Usage Examples

## Example 1: Frontend Agent Working on UI
```python
# Frontend agent starts work
worktree = await worktree_add(
    branch="feat/issue-456-dashboard-ui",
    agent_id="frontend-agent-1",
    create_branch=True
)

# Make changes
await git_add(
    files=["src/components/Dashboard.tsx", "src/styles/dashboard.css"],
    worktree_path=worktree["worktree_path"]
)

await git_commit(
    message="feat: Implement dashboard layout",
    worktree_path=worktree["worktree_path"]
)
```

## Example 2: Multiple Agents on Same Feature
```python
# Backend agent
backend_wt = await worktree_add(
    branch="feat/auth-system",
    agent_id="backend-agent",
    create_branch=True
)

# Frontend agent on same feature
frontend_wt = await worktree_add(
    branch="feat/auth-system-ui",
    agent_id="frontend-agent",
    create_branch=True,
    base_branch="feat/auth-system"  # Branch from backend work
)
```

## Example 3: Conflict Resolution
```python
# Try to sync
sync_result = await worktree_sync(
    agent_id="backend-agent-1",
    target_branch="main"
)

if sync_result.get("conflict"):
    # Get status to see conflicts
    status = await git_status(worktree_path=worktree_path)
    
    # Agent resolves conflicts...
    
    # Mark resolved and commit
    await git_add(files=["."], worktree_path=worktree_path)
    await git_commit(
        message="resolve: Merge conflicts with main",
        worktree_path=worktree_path
    )
```

## Example 4: Stash Management
```python
# Agent needs to switch context temporarily
await git_stash(
    action="push",
    message="WIP: Auth middleware",
    worktree_path=worktree_path
)

# Do other work...

# Resume previous work
await git_stash(
    action="pop",
    worktree_path=worktree_path
)
```
"""

@mcp.resource("resource://git_commands")
def git_commands() -> str:
    """
    Reference for all available git commands
    """
    return """
# Git Commands Reference

## Basic Operations
- **git_status**: Check working directory status
- **git_add**: Stage files for commit
- **git_commit**: Create a commit
- **git_log**: View commit history
- **git_branch**: Manage branches

## Worktree Operations
- **worktree_add**: Create isolated workspace for agent
- **worktree_list**: List all active worktrees
- **worktree_remove**: Clean up worktree
- **worktree_sync**: Sync with target branch

## Advanced Operations
- **git_stash**: Save/restore work in progress
- **git_push**: Push commits to remote (coming soon)
- **git_pull**: Pull changes from remote (coming soon)
- **git_merge**: Merge branches (coming soon)
- **git_rebase**: Rebase branches (coming soon)

## Parameters Reference
Most commands accept:
- `worktree_path`: Specify which worktree to operate on
- `ctx`: Context for logging and progress reporting
"""

@mcp.resource("resource://agent_patterns")
def agent_patterns() -> str:
    """
    Common patterns for agent git usage
    """
    return """
# Agent Git Patterns

## Pattern 1: Issue-Based Development
```
1. Agent receives issue assignment
2. Creates worktree with issue-based branch name
3. Implements solution in isolated environment
4. Commits with conventional commit messages
5. Pushes branch for PR
6. Removes worktree after merge
```

## Pattern 2: Parallel Feature Development
```
1. Multiple agents work on related features
2. Each gets own worktree on feature branches
3. Regular syncing to avoid conflicts
4. Coordinate through shared base branches
5. Merge in dependency order
```

## Pattern 3: Hotfix Workflow
```
1. Urgent fix agent creates worktree from main
2. Implements fix quickly
3. Tests in isolation
4. Direct push to main (with permissions)
5. Other agents sync their worktrees
```

## Pattern 4: Code Review Agent
```
1. Review agent creates worktree from PR branch
2. Runs tests and analysis
3. Makes suggested changes
4. Commits improvements
5. Updates PR with fixes
```
"""

# ===================================================================
# PROMPTS
# ===================================================================

@mcp.prompt
def git_workflow_guide(task_type: str, complexity: str = "medium") -> str:
    """
    Generate git workflow guidance for specific task types
    """
    workflows = {
        "feature": f"""
Git Workflow for Feature Development ({complexity} complexity):

1. **Setup Phase**:
   - Create worktree with descriptive branch name
   - Base off main or develop branch
   - Verify clean working directory

2. **Development Phase**:
   - Make incremental commits
   - Write clear commit messages
   - {'Create multiple small PRs' if complexity == 'high' else 'Keep changes focused'}

3. **Integration Phase**:
   - Sync with base branch regularly
   - Resolve conflicts promptly
   - Run tests before pushing

4. **Completion Phase**:
   - Squash commits if needed
   - Update documentation
   - Clean up worktree
""",
        "bugfix": f"""
Git Workflow for Bug Fixes ({complexity} complexity):

1. **Investigation**:
   - Create worktree from affected branch
   - Reproduce the issue
   - {'Check related systems' if complexity == 'high' else 'Isolate the problem'}

2. **Implementation**:
   - Make minimal necessary changes
   - Add regression tests
   - Verify fix doesn't break other features

3. **Validation**:
   - Test in isolation
   - {'Full integration testing' if complexity == 'high' else 'Targeted testing'}
   - Document the fix

4. **Deployment**:
   - Fast-track if critical
   - Normal PR process otherwise
   - Monitor after deployment
""",
        "refactor": """
Git Workflow for Refactoring:

1. **Preparation**:
   - Create comprehensive test coverage first
   - Document current behavior
   - Create refactor branch

2. **Execution**:
   - Make incremental changes
   - Run tests after each change
   - Keep commits atomic

3. **Validation**:
   - Ensure no behavior changes
   - Performance testing
   - Code review focus on maintainability
"""
    }
    
    return workflows.get(task_type, f"Custom workflow for {task_type} with {complexity} complexity")

@mcp.prompt
def commit_message_template(change_type: str, scope: str, description: str) -> str:
    """
    Generate conventional commit message
    """
    # Conventional commit format
    type_emoji = {
        "feat": "✨",
        "fix": "🐛",
        "docs": "📚",
        "style": "💎",
        "refactor": "♻️",
        "test": "✅",
        "chore": "🔧"
    }
    
    emoji = type_emoji.get(change_type, "🔨")
    
    return f"""
{change_type}({scope}): {description}

[Detailed explanation of the changes]

- What was changed
- Why it was changed
- Any breaking changes

Resolves: #issue-number
"""

@mcp.prompt
def conflict_resolution_guide(conflict_type: str = "merge") -> str:
    """
    Guide for resolving git conflicts
    """
    return f"""
# Conflict Resolution Guide for {conflict_type}

## Understanding the Conflict:
1. Identify conflicting files with `git status`
2. Understand both versions of the code
3. Determine the correct resolution

## Resolution Steps:
1. **For code conflicts**:
   - Keep functionally correct version
   - Merge both changes if compatible
   - Consult with other agent if unclear

2. **For structural conflicts**:
   - Understand the architectural decision
   - Choose approach that maintains consistency
   - Document the decision

3. **Testing after resolution**:
   - Run all affected tests
   - Verify functionality
   - Check for regression

## Commands:
```bash
# See conflict markers
git diff

# After fixing conflicts
git add <resolved-files>
git commit

# Or abort the {conflict_type}
git {conflict_type} --abort
```
"""

@mcp.prompt
def branch_strategy_guide(project_type: str, team_size: str = "small") -> str:
    """
    Recommend git branching strategy
    """
    strategies = {
        "webapp": f"""
# Branching Strategy for Web Application ({team_size} team)

## Branch Structure:
- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent production fixes

## Workflow:
1. Feature branches from develop
2. {'Multiple staging branches' if team_size == 'large' else 'Direct to develop'}
3. Release branches for production prep
4. Hotfixes from main, merge back

## Agent Worktrees:
- Each agent gets feature branch worktree
- Shared develop worktree for integration
- Temporary hotfix worktrees as needed
""",
        "library": """
# Branching Strategy for Library

## Branch Structure:
- `main` - Latest stable release
- `develop` - Next version development
- `release/v*` - Release branches
- `feature/*` - New features

## Version Management:
- Semantic versioning (major.minor.patch)
- Tag releases on main
- Maintain multiple version branches
"""
    }
    
    return strategies.get(project_type, f"Custom branching strategy for {project_type}")

@mcp.prompt
def agent_git_checklist(agent_role: str) -> str:
    """
    Pre-flight checklist for agent git operations
    """
    return f"""
# Git Checklist for {agent_role} Agent

## Before Starting Work:
- [ ] Pull latest changes
- [ ] Create appropriate worktree
- [ ] Verify branch naming convention
- [ ] Check for existing related work

## During Development:
- [ ] Commit frequently with clear messages
- [ ] Keep commits atomic and focused
- [ ] Run tests before committing
- [ ] Sync with base branch regularly

## Before Completing:
- [ ] All tests passing
- [ ] Code review requirements met
- [ ] Documentation updated
- [ ] No sensitive data committed

## After Completion:
- [ ] Push branch to remote
- [ ] Create pull request
- [ ] Clean up local worktree
- [ ] Update issue status
"""

# ===================================================================
# SERVER EXECUTION
# ===================================================================

if __name__ == "__main__":
    # Get configuration from environment
    port = int(os.getenv('GIT_ADVANCED_MCP_PORT', '8045'))
    
    # Validate base repository
    if not os.path.exists(os.path.join(BASE_REPO_PATH, '.git')):
        logger.error(f"No git repository found at {BASE_REPO_PATH}")
        logger.error("Set GIT_BASE_REPO_PATH environment variable to a valid git repository")
        exit(1)
    
    logger.info(f"Starting Git Advanced MCP Server on port {port}")
    logger.info(f"Base repository: {BASE_REPO_PATH}")
    logger.info(f"Worktree storage: {WORKTREE_BASE}")
    
    # Ensure worktree directory exists
    os.makedirs(WORKTREE_BASE, exist_ok=True)
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")