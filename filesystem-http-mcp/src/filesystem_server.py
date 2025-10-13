#!/usr/bin/env python3
"""
Filesystem MCP Server - HTTP Implementation
Secure filesystem operations with path validation and safety checks

Converted from official MCP TypeScript stdio server to FastMCP HTTP server
Based on: https://github.com/modelcontextprotocol/servers/blob/main/src/filesystem/index.ts
"""

import os
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import shutil
import fnmatch
import re

# FastMCP for HTTP serving
from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecureFilesystem:
    """Secure filesystem operations with path validation"""
    
    def __init__(self, allowed_directories: List[str]):
        """Initialize with allowed directories"""
        self.allowed_directories = [Path(d).resolve() for d in allowed_directories]
        logger.info(f"Filesystem server initialized with allowed directories: {self.allowed_directories}")
    
    def _validate_path(self, path: str) -> Path:
        """Validate that path is within allowed directories"""
        try:
            requested_path = Path(path).resolve()
        except (OSError, ValueError) as e:
            raise ValueError(f"Invalid path: {path} - {e}")
        
        # Check if path is within any allowed directory
        for allowed_dir in self.allowed_directories:
            try:
                requested_path.relative_to(allowed_dir)
                return requested_path
            except ValueError:
                continue
        
        raise ValueError(f"Path {path} is outside allowed directories: {self.allowed_directories}")
    
    def _is_text_file(self, file_path: Path) -> bool:
        """Check if file appears to be text-based"""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(8192)
                # Check for null bytes (common in binary files)
                if b'\x00' in chunk:
                    return False
                # Try to decode as UTF-8
                chunk.decode('utf-8')
                return True
        except (UnicodeDecodeError, IOError):
            return False
    
    async def read_file(self, path: str) -> str:
        """Read complete file contents"""
        file_path = self._validate_path(path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {path}")
        
        if not self._is_text_file(file_path):
            raise ValueError(f"File appears to be binary: {path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"Read file: {path} ({len(content)} characters)")
            return content
            
        except UnicodeDecodeError:
            raise ValueError(f"File is not valid UTF-8: {path}")
        except Exception as e:
            raise IOError(f"Error reading file {path}: {e}")
    
    async def read_multiple_files(self, paths: List[str]) -> List[Dict[str, Any]]:
        """Read multiple files simultaneously"""
        results = []
        
        for path in paths:
            try:
                content = await self.read_file(path)
                results.append({
                    "path": path,
                    "content": content,
                    "success": True
                })
            except Exception as e:
                results.append({
                    "path": path,
                    "error": str(e),
                    "success": False
                })
        
        return results
    
    async def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """Create or overwrite a file with new content"""
        file_path = self._validate_path(path)
        
        try:
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Wrote file: {path} ({len(content)} characters)")
            return {
                "success": True,
                "path": str(file_path),
                "size": len(content)
            }
            
        except Exception as e:
            error_msg = f"Error writing file {path}: {e}"
            logger.error(error_msg)
            raise IOError(error_msg)
    
    async def edit_file(self, path: str, edits: List[Dict[str, str]], dry_run: bool = False) -> Dict[str, Any]:
        """Make line-based edits to a text file"""
        file_path = self._validate_path(path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        # Read current content
        current_content = await self.read_file(path)
        lines = current_content.splitlines(keepends=True)
        
        # Apply edits
        modified_lines = lines.copy()
        changes_made = []
        
        for edit in edits:
            old_text = edit.get("oldText", "")
            new_text = edit.get("newText", "")
            
            # Find and replace old_text with new_text
            content_str = ''.join(modified_lines)
            if old_text in content_str:
                modified_content = content_str.replace(old_text, new_text)
                modified_lines = modified_content.splitlines(keepends=True)
                changes_made.append({
                    "old": old_text,
                    "new": new_text,
                    "applied": True
                })
            else:
                changes_made.append({
                    "old": old_text,
                    "new": new_text,
                    "applied": False,
                    "error": "Text not found"
                })
        
        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "changes": changes_made,
                "preview": ''.join(modified_lines)
            }
        
        # Write modified content
        if changes_made and any(c["applied"] for c in changes_made):
            modified_content = ''.join(modified_lines)
            await self.write_file(path, modified_content)
        
        return {
            "success": True,
            "changes": changes_made,
            "file_size": len(''.join(modified_lines))
        }
    
    async def create_directory(self, path: str) -> Dict[str, Any]:
        """Create a new directory"""
        dir_path = self._validate_path(path)
        
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {path}")
            return {
                "success": True,
                "path": str(dir_path)
            }
        except Exception as e:
            error_msg = f"Error creating directory {path}: {e}"
            logger.error(error_msg)
            raise IOError(error_msg)
    
    async def list_directory(self, path: str) -> List[Dict[str, Any]]:
        """Get detailed listing of directory contents"""
        dir_path = self._validate_path(path)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")
        
        if not dir_path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")
        
        items = []
        try:
            for item in sorted(dir_path.iterdir()):
                try:
                    stat = item.stat()
                    items.append({
                        "name": item.name,
                        "type": "directory" if item.is_dir() else "file",
                        "size": stat.st_size if item.is_file() else None,
                        "modified": stat.st_mtime,
                        "permissions": oct(stat.st_mode)[-3:],
                        "path": str(item)
                    })
                except (OSError, PermissionError) as e:
                    items.append({
                        "name": item.name,
                        "type": "unknown",
                        "error": str(e),
                        "path": str(item)
                    })
            
            logger.info(f"Listed directory: {path} ({len(items)} items)")
            return items
            
        except Exception as e:
            raise IOError(f"Error listing directory {path}: {e}")
    
    async def move_file(self, source: str, destination: str) -> Dict[str, Any]:
        """Move or rename files and directories"""
        source_path = self._validate_path(source)
        dest_path = self._validate_path(destination)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source not found: {source}")
        
        try:
            # Create destination directory if needed
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(source_path), str(dest_path))
            
            logger.info(f"Moved: {source} → {destination}")
            return {
                "success": True,
                "source": source,
                "destination": str(dest_path)
            }
            
        except Exception as e:
            error_msg = f"Error moving {source} to {destination}: {e}"
            logger.error(error_msg)
            raise IOError(error_msg)
    
    async def search_files(self, path: str, pattern: str, exclude_patterns: List[str] = None) -> List[Dict[str, Any]]:
        """Recursively search for files and directories matching a pattern"""
        search_path = self._validate_path(path)
        
        if not search_path.exists():
            raise FileNotFoundError(f"Search path not found: {path}")
        
        if not search_path.is_dir():
            raise ValueError(f"Search path is not a directory: {path}")
        
        exclude_patterns = exclude_patterns or []
        results = []
        
        try:
            for item in search_path.rglob("*"):
                # Skip if matches exclude pattern
                if any(fnmatch.fnmatch(item.name, excl) for excl in exclude_patterns):
                    continue
                
                # Check if matches search pattern
                if fnmatch.fnmatch(item.name.lower(), pattern.lower()):
                    try:
                        stat = item.stat()
                        results.append({
                            "name": item.name,
                            "path": str(item),
                            "type": "directory" if item.is_dir() else "file",
                            "size": stat.st_size if item.is_file() else None,
                            "modified": stat.st_mtime
                        })
                    except (OSError, PermissionError):
                        # Skip items we can't access
                        continue
            
            logger.info(f"Search completed: {path} with pattern '{pattern}' ({len(results)} results)")
            return results
            
        except Exception as e:
            raise IOError(f"Error searching in {path}: {e}")
    
    async def get_file_info(self, path: str) -> Dict[str, Any]:
        """Retrieve detailed metadata about a file or directory"""
        file_path = self._validate_path(path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        
        try:
            stat = file_path.stat()
            
            info = {
                "name": file_path.name,
                "path": str(file_path),
                "type": "directory" if file_path.is_dir() else "file",
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "accessed": stat.st_atime,
                "permissions": oct(stat.st_mode)[-3:],
                "owner_readable": bool(stat.st_mode & 0o400),
                "owner_writable": bool(stat.st_mode & 0o200),
                "owner_executable": bool(stat.st_mode & 0o100)
            }
            
            if file_path.is_file():
                info["is_text"] = self._is_text_file(file_path)
            
            logger.info(f"Retrieved file info: {path}")
            return info
            
        except Exception as e:
            raise IOError(f"Error getting file info for {path}: {e}")


# Initialize FastMCP server
mcp = FastMCP("filesystem")

# Get allowed directories from environment or default to current directory
allowed_dirs = os.getenv('FILESYSTEM_ALLOWED_DIRS', '.').split(':')

# Remote workspace configuration
WORKSPACE_BASE = os.getenv('WORKSPACE_BASE', '/workspace')
WORKTREE_BASE = os.getenv('WORKTREE_BASE', '/workspace/worktrees')

filesystem = SecureFilesystem(allowed_dirs)

# Agent workspace management
def get_agent_workspace_path(agent_id: str, workspace_type: str = "worktree") -> Path:
    """Get the workspace path for a specific agent"""
    if workspace_type == "worktree":
        return Path(WORKTREE_BASE) / agent_id
    elif workspace_type == "shared":
        return Path(WORKSPACE_BASE) / "shared"
    else:
        raise ValueError(f"Unknown workspace type: {workspace_type}")

def validate_agent_path(agent_id: str, path: str, workspace_type: str = "worktree") -> str:
    """Validate and resolve path within agent's workspace"""
    workspace = get_agent_workspace_path(agent_id, workspace_type)
    workspace.mkdir(parents=True, exist_ok=True)
    
    # If path is absolute, make it relative to workspace
    if os.path.isabs(path):
        # Remove leading slash and resolve within workspace
        path = path.lstrip('/')
    
    # Resolve full path within workspace
    full_path = workspace / path
    return str(full_path)

# Register tools
@mcp.tool()
async def read_file(path: str, ctx: Optional[Context] = None) -> str:
    """
    Read the complete contents of a file from the filesystem.
    
    Args:
        path: The path to the file to read
        ctx: Optional context for logging and progress
        
    Returns:
        The contents of the file as a string
    """
    if ctx:
        await ctx.info(f"Reading file: {path}")
    
    try:
        content = await filesystem.read_file(path)
        if ctx:
            await ctx.debug(f"Successfully read {len(content)} characters from {path}")
        return content
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to read file {path}: {str(e)}")
        raise

@mcp.tool()
async def read_multiple_files(paths: List[str], ctx: Optional[Context] = None) -> List[Dict[str, Any]]:
    """
    Read the contents of multiple files simultaneously.
    
    Args:
        paths: List of file paths to read
        ctx: Optional context for logging and progress
        
    Returns:
        List of results, each containing path, content (if successful), or error
    """
    if ctx:
        await ctx.info(f"Reading {len(paths)} files")
    
    try:
        results = []
        for idx, path in enumerate(paths):
            if ctx and len(paths) > 3:
                await ctx.report_progress(progress=idx, total=len(paths))
            
            try:
                result = await filesystem.read_file(path)
                results.append({"path": path, "content": result})
            except Exception as e:
                results.append({"path": path, "error": str(e)})
                if ctx:
                    await ctx.warning(f"Failed to read {path}: {str(e)}")
        
        if ctx:
            successful = sum(1 for r in results if "content" in r)
            await ctx.info(f"Successfully read {successful}/{len(paths)} files")
            if len(paths) > 3:
                await ctx.report_progress(progress=len(paths), total=len(paths))
        
        return results
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to read multiple files: {str(e)}")
        raise

@mcp.tool()
async def write_file(path: str, content: str, ctx: Optional[Context] = None) -> Dict[str, Any]:
    """
    Create a new file or completely overwrite an existing file with new content.
    
    Args:
        path: The path where the file should be created/overwritten
        content: The content to write to the file
        ctx: Optional context for logging and progress
        
    Returns:
        Result object with success status and file info
    """
    if ctx:
        await ctx.info(f"Writing file: {path} ({len(content)} characters)")
    
    try:
        result = await filesystem.write_file(path, content)
        if ctx:
            await ctx.debug(f"Successfully wrote file: {path}")
        return result
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to write file {path}: {str(e)}")
        raise

@mcp.tool()
async def edit_file(path: str, edits: List[Dict[str, str]], dry_run: bool = False, ctx: Optional[Context] = None) -> Dict[str, Any]:
    """
    Make line-based edits to a text file.
    
    Args:
        path: Path to the file to edit
        edits: List of edit operations, each with 'oldText' and 'newText'
        dry_run: If true, preview changes without actually editing the file
        ctx: Optional context for logging and progress
        
    Returns:
        Result of the edit operation with applied changes
    """
    if ctx:
        mode = "dry run" if dry_run else "edit"
        await ctx.info(f"Performing {mode} on file: {path} ({len(edits)} edits)")
    
    try:
        if ctx and len(edits) > 5:
            for idx, edit in enumerate(edits):
                await ctx.report_progress(progress=idx, total=len(edits))
        
        result = await filesystem.edit_file(path, edits, dry_run)
        
        if ctx:
            if dry_run:
                await ctx.info(f"Dry run completed: {len(edits)} edits would be applied")
            else:
                await ctx.info(f"Successfully applied {len(edits)} edits to {path}")
            if len(edits) > 5:
                await ctx.report_progress(progress=len(edits), total=len(edits))
        
        return result
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to edit file {path}: {str(e)}")
        raise

@mcp.tool()
async def create_directory(path: str, ctx: Optional[Context] = None) -> Dict[str, Any]:
    """
    Create a new directory or ensure a directory exists.
    
    Args:
        path: The path of the directory to create
        ctx: Optional context for logging and progress
        
    Returns:
        Result object with success status and directory path
    """
    if ctx:
        await ctx.info(f"Creating directory: {path}")
    
    try:
        result = await filesystem.create_directory(path)
        if ctx:
            await ctx.debug(f"Successfully created/ensured directory: {path}")
        return result
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to create directory {path}: {str(e)}")
        raise

@mcp.tool()
async def list_directory(path: str, ctx: Optional[Context] = None) -> List[Dict[str, Any]]:
    """
    Get a detailed listing of all files and directories in a specified path.
    
    Args:
        path: The directory path to list
        ctx: Optional context for logging and progress
        
    Returns:
        List of items in the directory with metadata
    """
    if ctx:
        await ctx.info(f"Listing directory: {path}")
    
    try:
        items = await filesystem.list_directory(path)
        if ctx:
            await ctx.debug(f"Found {len(items)} items in {path}")
        return items
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to list directory {path}: {str(e)}")
        raise

@mcp.tool()
async def move_file(source: str, destination: str, ctx: Optional[Context] = None) -> Dict[str, Any]:
    """
    Move or rename files and directories.
    
    Args:
        source: The current path of the file/directory
        destination: The new path for the file/directory
        ctx: Optional context for logging and progress
        
    Returns:
        Result object with success status and new path
    """
    if ctx:
        await ctx.info(f"Moving {source} to {destination}")
    
    try:
        result = await filesystem.move_file(source, destination)
        if ctx:
            await ctx.debug(f"Successfully moved {source} to {destination}")
        return result
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to move file from {source} to {destination}: {str(e)}")
        raise

@mcp.tool()
async def search_files(path: str, pattern: str, exclude_patterns: Optional[List[str]] = None, ctx: Optional[Context] = None) -> List[Dict[str, Any]]:
    """
    Recursively search for files and directories matching a pattern.
    
    Args:
        path: The directory to search in
        pattern: The search pattern (supports wildcards)
        exclude_patterns: Optional list of patterns to exclude
        ctx: Optional context for logging and progress
        
    Returns:
        List of matching files and directories
    """
    if ctx:
        await ctx.info(f"Searching for '{pattern}' in {path}")
        if exclude_patterns:
            await ctx.debug(f"Excluding patterns: {exclude_patterns}")
    
    try:
        results = await filesystem.search_files(path, pattern, exclude_patterns or [])
        if ctx:
            await ctx.info(f"Found {len(results)} matches for '{pattern}'")
        return results
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to search files: {str(e)}")
        raise

@mcp.tool()
async def get_file_info(path: str, ctx: Optional[Context] = None) -> Dict[str, Any]:
    """
    Retrieve detailed metadata about a file or directory.
    
    Args:
        path: The path to get information about
        ctx: Optional context for logging and progress
        
    Returns:
        Detailed metadata including size, permissions, timestamps
    """
    if ctx:
        await ctx.info(f"Getting file info for: {path}")
    
    try:
        info = await filesystem.get_file_info(path)
        if ctx:
            file_type = "directory" if info.get("isDirectory") else "file"
            size = info.get("size", 0)
            await ctx.debug(f"Retrieved info for {file_type}: {path} (size: {size} bytes)")
        return info
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to get file info for {path}: {str(e)}")
        raise

# ===================================================================
# REMOTE AGENT FILESYSTEM TOOLS
# ===================================================================

@mcp.tool()
async def read_file_remote(
    path: str,
    agent_id: str,
    workspace_type: str = "worktree",
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Read a file from agent's remote workspace
    
    Args:
        path: File path (relative to agent's workspace)
        agent_id: Agent identifier for workspace isolation
        workspace_type: 'worktree' or 'shared'
        ctx: Optional context for logging and progress
    
    Returns:
        File content and metadata
    """
    if ctx:
        await ctx.info(f"Reading remote file: {path} for agent: {agent_id}")
    
    try:
        # Resolve path within agent's workspace
        full_path = validate_agent_path(agent_id, path, workspace_type)
        
        # Use existing filesystem read method
        content = await filesystem.read_file(full_path)
        
        file_path = Path(full_path)
        return {
            "success": True,
            "content": content,
            "path": path,  # Return original relative path
            "agent_id": agent_id,
            "workspace_type": workspace_type,
            "size": file_path.stat().st_size,
            "modified": file_path.stat().st_mtime
        }
        
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to read remote file {path} for agent {agent_id}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "agent_id": agent_id,
            "path": path
        }

@mcp.tool()
async def write_file_remote(
    path: str,
    content: str,
    agent_id: str,
    workspace_type: str = "worktree",
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Write a file to agent's remote workspace
    
    Args:
        path: File path (relative to agent's workspace)
        content: File content to write
        agent_id: Agent identifier for workspace isolation
        workspace_type: 'worktree' or 'shared'
        ctx: Optional context for logging and progress
    
    Returns:
        Operation result with metadata
    """
    if ctx:
        await ctx.info(f"Writing remote file: {path} for agent: {agent_id}")
    
    try:
        # Resolve path within agent's workspace
        full_path = validate_agent_path(agent_id, path, workspace_type)
        
        # Use existing filesystem write method
        result = await filesystem.write_file(full_path, content)
        
        return {
            "success": True,
            "path": path,  # Return original relative path
            "agent_id": agent_id,
            "workspace_type": workspace_type,
            "size": result["size"]
        }
        
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to write remote file {path} for agent {agent_id}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "agent_id": agent_id,
            "path": path
        }

@mcp.tool()
async def list_directory_remote(
    path: str,
    agent_id: str,
    workspace_type: str = "worktree", 
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    List directory contents in agent's remote workspace
    
    Args:
        path: Directory path (relative to agent's workspace)
        agent_id: Agent identifier for workspace isolation
        workspace_type: 'worktree' or 'shared'
        ctx: Optional context for logging and progress
    
    Returns:
        Directory listing with metadata
    """
    if ctx:
        await ctx.info(f"Listing remote directory: {path} for agent: {agent_id}")
    
    try:
        # Resolve path within agent's workspace
        full_path = validate_agent_path(agent_id, path, workspace_type)
        
        # Use existing filesystem list method
        items = await filesystem.list_directory(full_path)
        
        return {
            "success": True,
            "path": path,  # Return original relative path
            "agent_id": agent_id,
            "workspace_type": workspace_type,
            "items": items,
            "count": len(items)
        }
        
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to list remote directory {path} for agent {agent_id}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "agent_id": agent_id,
            "path": path
        }

@mcp.tool()
async def get_workspace_info(
    agent_id: str,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Get information about an agent's workspace
    
    Args:
        agent_id: Agent identifier
        ctx: Optional context for logging and progress
    
    Returns:
        Workspace information and statistics
    """
    if ctx:
        await ctx.info(f"Getting workspace info for agent: {agent_id}")
    
    try:
        worktree_path = get_agent_workspace_path(agent_id, "worktree")
        shared_path = get_agent_workspace_path(agent_id, "shared")
        
        # Calculate workspace sizes
        def get_dir_size(path: Path) -> int:
            total = 0
            if path.exists():
                for item in path.rglob('*'):
                    if item.is_file():
                        try:
                            total += item.stat().st_size
                        except (OSError, PermissionError):
                            pass
            return total
        
        return {
            "success": True,
            "agent_id": agent_id,
            "workspaces": {
                "worktree": {
                    "path": str(worktree_path),
                    "exists": worktree_path.exists(),
                    "size": get_dir_size(worktree_path)
                },
                "shared": {
                    "path": str(shared_path),
                    "exists": shared_path.exists(),
                    "size": get_dir_size(shared_path)
                }
            }
        }
        
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to get workspace info for agent {agent_id}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "agent_id": agent_id
        }

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv('FILESYSTEM_MCP_PORT', '8001'))
    
    logger.info(f"Starting Filesystem MCP Server on port {port}")
    logger.info(f"Allowed directories: {allowed_dirs}")
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")