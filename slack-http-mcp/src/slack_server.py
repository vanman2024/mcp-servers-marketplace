#!/usr/bin/env python3
"""
Slack MCP Server - HTTP Implementation
Slack workspace messaging and user management via Slack Web API

Converted from official MCP TypeScript stdio server to FastMCP HTTP server
"""

import os
import logging
from typing import Dict, Any, Optional, List
import httpx
from datetime import datetime

# FastMCP for HTTP serving
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("slack-http-mcp")

# Get Slack credentials from environment
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
SLACK_TEAM_ID = os.getenv("SLACK_TEAM_ID", "")

if not SLACK_BOT_TOKEN:
    logger.warning("SLACK_BOT_TOKEN not set. Slack operations will fail.")

# Base URL for Slack API
SLACK_API_BASE = "https://slack.com/api"

# Common headers for Slack API requests
def get_headers():
    """Get common headers for Slack API requests"""
    return {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }

# Channel Operations

@mcp.tool()
async def slack_list_channels(
    cursor: Optional[str] = None,
    limit: Optional[int] = 100
) -> Dict[str, Any]:
    """
    List public or pre-defined channels in the workspace with pagination
    
    Args:
        cursor: Pagination cursor for next page of results
        limit: Maximum number of channels to return (default 100, max 200)
    
    Returns:
        Channel list with pagination info
    """
    try:
        # Validate limit
        limit = min(limit or 100, 200)
        
        params = {
            "limit": limit,
            "types": "public_channel",
            "exclude_archived": True
        }
        
        if cursor:
            params["cursor"] = cursor
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SLACK_API_BASE}/conversations.list",
                headers=get_headers(),
                params=params
            )
            
        data = response.json()
        
        if not data.get("ok"):
            raise ValueError(f"Slack API error: {data.get('error', 'Unknown error')}")
        
        return {
            "success": True,
            "channels": data.get("channels", []),
            "cursor": data.get("response_metadata", {}).get("next_cursor"),
            "has_more": bool(data.get("response_metadata", {}).get("next_cursor"))
        }
        
    except Exception as e:
        logger.error(f"Failed to list channels: {e}")
        raise ValueError(f"Failed to list channels: {str(e)}")

@mcp.tool()
async def slack_post_message(
    channel_id: str,
    text: str
) -> Dict[str, Any]:
    """
    Post a new message to a Slack channel
    
    Args:
        channel_id: The ID of the channel to post to
        text: The message text to post
    
    Returns:
        Posted message details
    """
    try:
        if not channel_id or not text:
            raise ValueError("channel_id and text are required")
        
        payload = {
            "channel": channel_id,
            "text": text
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SLACK_API_BASE}/chat.postMessage",
                headers=get_headers(),
                json=payload
            )
            
        data = response.json()
        
        if not data.get("ok"):
            raise ValueError(f"Slack API error: {data.get('error', 'Unknown error')}")
        
        return {
            "success": True,
            "channel": data.get("channel"),
            "timestamp": data.get("ts"),
            "message": {
                "text": data.get("message", {}).get("text"),
                "user": data.get("message", {}).get("user"),
                "ts": data.get("ts")
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to post message: {e}")
        raise ValueError(f"Failed to post message: {str(e)}")

@mcp.tool()
async def slack_reply_to_thread(
    channel_id: str,
    thread_ts: str,
    text: str
) -> Dict[str, Any]:
    """
    Reply to a specific message thread in Slack
    
    Args:
        channel_id: The ID of the channel containing the thread
        thread_ts: The timestamp of the parent message in the format '1234567890.123456'
        text: The reply text
    
    Returns:
        Posted reply details
    """
    try:
        if not all([channel_id, thread_ts, text]):
            raise ValueError("channel_id, thread_ts, and text are required")
        
        # Ensure timestamp has correct format
        if '.' not in thread_ts:
            # Convert format if needed (add period with 6 decimal places)
            if len(thread_ts) > 10:
                thread_ts = f"{thread_ts[:10]}.{thread_ts[10:].ljust(6, '0')[:6]}"
            else:
                thread_ts = f"{thread_ts}.000000"
        
        payload = {
            "channel": channel_id,
            "text": text,
            "thread_ts": thread_ts
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SLACK_API_BASE}/chat.postMessage",
                headers=get_headers(),
                json=payload
            )
            
        data = response.json()
        
        if not data.get("ok"):
            raise ValueError(f"Slack API error: {data.get('error', 'Unknown error')}")
        
        return {
            "success": True,
            "channel": data.get("channel"),
            "timestamp": data.get("ts"),
            "thread_ts": thread_ts,
            "message": {
                "text": data.get("message", {}).get("text"),
                "user": data.get("message", {}).get("user"),
                "ts": data.get("ts")
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to reply to thread: {e}")
        raise ValueError(f"Failed to reply to thread: {str(e)}")

@mcp.tool()
async def slack_add_reaction(
    channel_id: str,
    timestamp: str,
    reaction: str
) -> Dict[str, Any]:
    """
    Add a reaction emoji to a message
    
    Args:
        channel_id: The ID of the channel containing the message
        timestamp: The timestamp of the message to react to
        reaction: The name of the emoji reaction (without ::)
    
    Returns:
        Success status
    """
    try:
        if not all([channel_id, timestamp, reaction]):
            raise ValueError("channel_id, timestamp, and reaction are required")
        
        # Remove colons if provided
        reaction = reaction.strip(':')
        
        payload = {
            "channel": channel_id,
            "timestamp": timestamp,
            "name": reaction
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SLACK_API_BASE}/reactions.add",
                headers=get_headers(),
                json=payload
            )
            
        data = response.json()
        
        if not data.get("ok"):
            # Check if already reacted
            if data.get("error") == "already_reacted":
                return {
                    "success": True,
                    "already_reacted": True,
                    "message": "Reaction already exists"
                }
            raise ValueError(f"Slack API error: {data.get('error', 'Unknown error')}")
        
        return {
            "success": True,
            "channel": channel_id,
            "timestamp": timestamp,
            "reaction": reaction
        }
        
    except Exception as e:
        logger.error(f"Failed to add reaction: {e}")
        raise ValueError(f"Failed to add reaction: {str(e)}")

# Message History Operations

@mcp.tool()
async def slack_get_channel_history(
    channel_id: str,
    limit: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Get recent messages from a channel
    
    Args:
        channel_id: The ID of the channel
        limit: Number of messages to retrieve (default 10)
    
    Returns:
        List of recent messages
    """
    try:
        if not channel_id:
            raise ValueError("channel_id is required")
        
        # Limit to reasonable number
        limit = min(limit or 10, 100)
        
        params = {
            "channel": channel_id,
            "limit": limit
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SLACK_API_BASE}/conversations.history",
                headers=get_headers(),
                params=params
            )
            
        data = response.json()
        
        if not data.get("ok"):
            raise ValueError(f"Slack API error: {data.get('error', 'Unknown error')}")
        
        # Format messages
        messages = []
        for msg in data.get("messages", []):
            messages.append({
                "text": msg.get("text"),
                "user": msg.get("user"),
                "timestamp": msg.get("ts"),
                "type": msg.get("type"),
                "thread_ts": msg.get("thread_ts"),
                "reply_count": msg.get("reply_count", 0),
                "reactions": [
                    {
                        "name": r.get("name"),
                        "count": r.get("count"),
                        "users": r.get("users", [])
                    }
                    for r in msg.get("reactions", [])
                ]
            })
        
        return {
            "success": True,
            "channel": channel_id,
            "messages": messages,
            "has_more": data.get("has_more", False)
        }
        
    except Exception as e:
        logger.error(f"Failed to get channel history: {e}")
        raise ValueError(f"Failed to get channel history: {str(e)}")

@mcp.tool()
async def slack_get_thread_replies(
    channel_id: str,
    thread_ts: str
) -> Dict[str, Any]:
    """
    Get all replies in a message thread
    
    Args:
        channel_id: The ID of the channel containing the thread
        thread_ts: The timestamp of the parent message
    
    Returns:
        Thread messages including parent and all replies
    """
    try:
        if not channel_id or not thread_ts:
            raise ValueError("channel_id and thread_ts are required")
        
        # Ensure timestamp has correct format
        if '.' not in thread_ts:
            if len(thread_ts) > 10:
                thread_ts = f"{thread_ts[:10]}.{thread_ts[10:].ljust(6, '0')[:6]}"
            else:
                thread_ts = f"{thread_ts}.000000"
        
        params = {
            "channel": channel_id,
            "ts": thread_ts
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SLACK_API_BASE}/conversations.replies",
                headers=get_headers(),
                params=params
            )
            
        data = response.json()
        
        if not data.get("ok"):
            raise ValueError(f"Slack API error: {data.get('error', 'Unknown error')}")
        
        # Format messages
        messages = []
        for msg in data.get("messages", []):
            messages.append({
                "text": msg.get("text"),
                "user": msg.get("user"),
                "timestamp": msg.get("ts"),
                "type": msg.get("type"),
                "thread_ts": msg.get("thread_ts"),
                "parent_user_id": msg.get("parent_user_id")
            })
        
        return {
            "success": True,
            "channel": channel_id,
            "thread_ts": thread_ts,
            "messages": messages,
            "message_count": len(messages)
        }
        
    except Exception as e:
        logger.error(f"Failed to get thread replies: {e}")
        raise ValueError(f"Failed to get thread replies: {str(e)}")

# User Operations

@mcp.tool()
async def slack_get_users(
    cursor: Optional[str] = None,
    limit: Optional[int] = 100
) -> Dict[str, Any]:
    """
    Get a list of all users in the workspace with their basic profile information
    
    Args:
        cursor: Pagination cursor for next page of results
        limit: Maximum number of users to return (default 100, max 200)
    
    Returns:
        List of users with basic profile info
    """
    try:
        # Validate limit
        limit = min(limit or 100, 200)
        
        params = {
            "limit": limit
        }
        
        if cursor:
            params["cursor"] = cursor
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SLACK_API_BASE}/users.list",
                headers=get_headers(),
                params=params
            )
            
        data = response.json()
        
        if not data.get("ok"):
            raise ValueError(f"Slack API error: {data.get('error', 'Unknown error')}")
        
        # Format users
        users = []
        for user in data.get("members", []):
            if not user.get("deleted") and not user.get("is_bot"):
                users.append({
                    "id": user.get("id"),
                    "name": user.get("name"),
                    "real_name": user.get("real_name"),
                    "display_name": user.get("profile", {}).get("display_name"),
                    "email": user.get("profile", {}).get("email"),
                    "is_admin": user.get("is_admin", False),
                    "is_owner": user.get("is_owner", False),
                    "status": user.get("profile", {}).get("status_text"),
                    "timezone": user.get("tz")
                })
        
        return {
            "success": True,
            "users": users,
            "cursor": data.get("response_metadata", {}).get("next_cursor"),
            "has_more": bool(data.get("response_metadata", {}).get("next_cursor")),
            "total_count": len(users)
        }
        
    except Exception as e:
        logger.error(f"Failed to get users: {e}")
        raise ValueError(f"Failed to get users: {str(e)}")

@mcp.tool()
async def slack_get_user_profile(
    user_id: str
) -> Dict[str, Any]:
    """
    Get detailed profile information for a specific user
    
    Args:
        user_id: The ID of the user
    
    Returns:
        Detailed user profile information
    """
    try:
        if not user_id:
            raise ValueError("user_id is required")
        
        params = {
            "user": user_id
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SLACK_API_BASE}/users.profile.get",
                headers=get_headers(),
                params=params
            )
            
        data = response.json()
        
        if not data.get("ok"):
            raise ValueError(f"Slack API error: {data.get('error', 'Unknown error')}")
        
        profile = data.get("profile", {})
        
        return {
            "success": True,
            "user_id": user_id,
            "profile": {
                "real_name": profile.get("real_name"),
                "display_name": profile.get("display_name"),
                "email": profile.get("email"),
                "phone": profile.get("phone"),
                "title": profile.get("title"),
                "status_text": profile.get("status_text"),
                "status_emoji": profile.get("status_emoji"),
                "avatar_url": profile.get("image_512"),
                "first_name": profile.get("first_name"),
                "last_name": profile.get("last_name"),
                "pronouns": profile.get("pronouns"),
                "fields": profile.get("fields", {})
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get user profile: {e}")
        raise ValueError(f"Failed to get user profile: {str(e)}")

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv('SLACK_MCP_PORT', '8017'))
    
    logger.info(f"Starting Slack MCP Server on port {port}")
    logger.info(f"Team ID: {SLACK_TEAM_ID[:10]}..." if SLACK_TEAM_ID else "No team ID set")
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")