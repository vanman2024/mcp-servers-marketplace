#!/usr/bin/env python3
"""
Sequential Thinking MCP Server (HTTP)

A server for processing sequential thinking steps with support for revisions,
branching, and dynamic thought management.
"""

import os
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from fastmcp import FastMCP, Context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastMCP server
mcp = FastMCP("sequential-thinking")

# Configure server
PORT = int(os.getenv("SEQUENTIAL_THINKING_MCP_PORT", "8015"))

# In-memory storage for thinking sessions (in production, use persistent storage)
thinking_sessions: Dict[str, List[Dict[str, Any]]] = {}


@mcp.tool()
async def sequentialthinking(
    thought: str,
    nextThoughtNeeded: bool,
    thoughtNumber: int,
    totalThoughts: int,
    isRevision: Optional[bool] = False,
    revisesThought: Optional[int] = None,
    branchFromThought: Optional[int] = None,
    branchId: Optional[str] = None,
    needsMoreThoughts: Optional[bool] = False,
    sessionId: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Process sequential thinking steps with support for revisions and branching.
    
    This tool helps analyze problems through a flexible thinking process that can
    adapt and evolve. Each thought can build on, question, or revise previous
    insights as understanding deepens.
    
    Args:
        thought: Current thinking step content
        nextThoughtNeeded: Whether another thought step is needed
        thoughtNumber: Current number in sequence
        totalThoughts: Current estimate of thoughts needed (can be adjusted)
        isRevision: Whether this thought revises previous thinking
        revisesThought: Which thought number is being reconsidered
        branchFromThought: If branching, which thought is the branching point
        branchId: Identifier for the current branch
        needsMoreThoughts: If reaching end but realizing more thoughts needed
        sessionId: Optional session identifier for tracking thought sequences
        
    Returns:
        Dict containing thought details and session information
    """
    try:
        # Generate session ID if not provided
        if not sessionId:
            sessionId = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if ctx:
            mode = "revision" if isRevision else "branch" if branchFromThought else "sequential"
            await ctx.info(f"Processing {mode} thought {thoughtNumber}/{totalThoughts} in session {sessionId}")
        
        # Initialize session if new
        if sessionId not in thinking_sessions:
            thinking_sessions[sessionId] = []
            if ctx:
                await ctx.debug(f"Initialized new thinking session: {sessionId}")
        
        # Create thought record
        thought_record = {
            "thoughtNumber": thoughtNumber,
            "thought": thought,
            "timestamp": datetime.now().isoformat(),
            "nextThoughtNeeded": nextThoughtNeeded,
            "totalThoughts": totalThoughts,
            "isRevision": isRevision,
            "revisesThought": revisesThought,
            "branchFromThought": branchFromThought,
            "branchId": branchId,
            "needsMoreThoughts": needsMoreThoughts
        }
        
        # Add to session
        thinking_sessions[sessionId].append(thought_record)
        
        # Prepare response
        response = {
            "thoughtNumber": thoughtNumber,
            "thought": thought,
            "nextThoughtNeeded": nextThoughtNeeded,
            "totalThoughts": totalThoughts,
            "sessionId": sessionId,
            "sessionThoughtCount": len(thinking_sessions[sessionId])
        }
        
        # Add optional fields if present
        if isRevision:
            response["isRevision"] = isRevision
            if revisesThought:
                response["revisesThought"] = revisesThought
        
        if branchFromThought:
            response["branchFromThought"] = branchFromThought
            if branchId:
                response["branchId"] = branchId
        
        if needsMoreThoughts:
            response["needsMoreThoughts"] = needsMoreThoughts
            
        # Add session summary if this is the final thought
        if not nextThoughtNeeded:
            response["sessionSummary"] = {
                "totalThoughts": len(thinking_sessions[sessionId]),
                "revisionCount": sum(1 for t in thinking_sessions[sessionId] if t.get("isRevision", False)),
                "branches": len(set(t.get("branchId", "main") for t in thinking_sessions[sessionId])),
                "completed": True
            }
        
        return response
        
    except Exception as e:
        return {
            "error": f"Failed to process thought: {str(e)}",
            "thoughtNumber": thoughtNumber,
            "nextThoughtNeeded": False,
            "totalThoughts": totalThoughts
        }


@mcp.tool()
async def get_thinking_session(sessionId: str) -> Dict[str, Any]:
    """
    Retrieve a complete thinking session by ID.
    
    Args:
        sessionId: The session identifier
        
    Returns:
        Dict containing all thoughts in the session
    """
    try:
        if sessionId not in thinking_sessions:
            return {
                "error": f"Session {sessionId} not found",
                "availableSessions": list(thinking_sessions.keys())
            }
        
        thoughts = thinking_sessions[sessionId]
        
        return {
            "sessionId": sessionId,
            "thoughts": thoughts,
            "totalThoughts": len(thoughts),
            "revisionCount": sum(1 for t in thoughts if t.get("isRevision", False)),
            "branches": list(set(t.get("branchId", "main") for t in thoughts)),
            "startTime": thoughts[0]["timestamp"] if thoughts else None,
            "endTime": thoughts[-1]["timestamp"] if thoughts else None,
            "completed": not thoughts[-1]["nextThoughtNeeded"] if thoughts else False
        }
        
    except Exception as e:
        return {
            "error": f"Failed to retrieve session: {str(e)}"
        }


@mcp.tool()
async def list_thinking_sessions() -> Dict[str, Any]:
    """
    List all available thinking sessions.
    
    Returns:
        Dict containing session summaries
    """
    try:
        sessions = []
        
        for session_id, thoughts in thinking_sessions.items():
            if thoughts:
                sessions.append({
                    "sessionId": session_id,
                    "thoughtCount": len(thoughts),
                    "startTime": thoughts[0]["timestamp"],
                    "endTime": thoughts[-1]["timestamp"],
                    "completed": not thoughts[-1]["nextThoughtNeeded"],
                    "hasRevisions": any(t.get("isRevision", False) for t in thoughts),
                    "branchCount": len(set(t.get("branchId", "main") for t in thoughts))
                })
        
        return {
            "sessions": sessions,
            "totalSessions": len(sessions)
        }
        
    except Exception as e:
        return {
            "error": f"Failed to list sessions: {str(e)}"
        }


@mcp.tool()
async def clear_thinking_sessions() -> Dict[str, Any]:
    """
    Clear all thinking sessions from memory.
    
    Returns:
        Dict confirming the operation
    """
    try:
        session_count = len(thinking_sessions)
        thought_count = sum(len(thoughts) for thoughts in thinking_sessions.values())
        
        thinking_sessions.clear()
        
        return {
            "message": "All thinking sessions cleared",
            "sessionsCleared": session_count,
            "thoughtsCleared": thought_count
        }
        
    except Exception as e:
        return {
            "error": f"Failed to clear sessions: {str(e)}"
        }


# Health check endpoint (automatically provided by FastMCP)
@mcp.tool()
async def health_check() -> Dict[str, Any]:
    """Check server health and status."""
    return {
        "status": "healthy",
        "server": "sequential-thinking-http",
        "transport": "streamable-http",
        "port": PORT,
        "activeSessions": len(thinking_sessions),
        "totalThoughts": sum(len(thoughts) for thoughts in thinking_sessions.values()),
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    print(f"Starting Sequential Thinking MCP Server on port {PORT}")
    print(f"Server: sequential-thinking")
    print(f"Transport: streamable-http")
    print(f"Health check: http://localhost:{PORT}/health")
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=PORT, path="/")