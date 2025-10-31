#!/usr/bin/env python3
"""
Redis MCP Server - HTTP Implementation
Key-value storage operations via Redis API

Converted from official MCP TypeScript stdio server to FastMCP HTTP server
"""

import os
import logging
from typing import Dict, Any, Optional, List, Union
import redis
import json
from datetime import datetime

# FastMCP for HTTP serving
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("redis-http-mcp")

# Get Redis connection from environment
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Initialize Redis client
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    # Test connection
    redis_client.ping()
    logger.info(f"Connected to Redis at {REDIS_URL}")
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_client = None

@mcp.tool()
async def set(
    key: str,
    value: str,
    expire_seconds: Optional[int] = None
) -> Dict[str, Any]:
    """
    Set a Redis key-value pair with optional expiration
    
    Args:
        key: Redis key
        value: Value to store
        expire_seconds: Optional expiration time in seconds
    
    Returns:
        Success status and key details
    """
    try:
        if not redis_client:
            raise ValueError("Redis client not connected")
        
        if not key:
            raise ValueError("Key cannot be empty")
        
        # Set the key-value pair
        result = redis_client.set(key, value)
        
        if not result:
            raise ValueError("Failed to set key")
        
        # Set expiration if provided
        if expire_seconds:
            redis_client.expire(key, expire_seconds)
        
        # Get key info for response
        ttl = redis_client.ttl(key) if expire_seconds else -1
        
        return {
            "success": True,
            "key": key,
            "value": value,
            "expires_in": ttl if ttl > 0 else None,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to set key '{key}': {e}")
        raise ValueError(f"Failed to set key: {str(e)}")

@mcp.tool()
async def get(key: str) -> Dict[str, Any]:
    """
    Get value by key from Redis
    
    Args:
        key: Redis key to retrieve
    
    Returns:
        Value and key metadata
    """
    try:
        if not redis_client:
            raise ValueError("Redis client not connected")
        
        if not key:
            raise ValueError("Key cannot be empty")
        
        # Get the value
        value = redis_client.get(key)
        
        if value is None:
            return {
                "success": True,
                "key": key,
                "value": None,
                "exists": False,
                "message": "Key not found"
            }
        
        # Get key metadata
        ttl = redis_client.ttl(key)
        key_type = redis_client.type(key)
        
        return {
            "success": True,
            "key": key,
            "value": value,
            "exists": True,
            "type": key_type,
            "ttl": ttl if ttl >= 0 else None,
            "expires_in": ttl if ttl > 0 else None
        }
        
    except Exception as e:
        logger.error(f"Failed to get key '{key}': {e}")
        raise ValueError(f"Failed to get key: {str(e)}")

@mcp.tool()
async def delete(key: Union[str, List[str]]) -> Dict[str, Any]:
    """
    Delete one or more keys from Redis
    
    Args:
        key: Key or array of keys to delete
    
    Returns:
        Deletion results
    """
    try:
        if not redis_client:
            raise ValueError("Redis client not connected")
        
        # Normalize to list
        keys_to_delete = key if isinstance(key, list) else [key]
        
        if not keys_to_delete:
            raise ValueError("At least one key must be provided")
        
        # Check which keys exist before deletion
        existing_keys = []
        for k in keys_to_delete:
            if redis_client.exists(k):
                existing_keys.append(k)
        
        # Delete the keys
        deleted_count = redis_client.delete(*keys_to_delete) if keys_to_delete else 0
        
        return {
            "success": True,
            "requested_keys": keys_to_delete,
            "existing_keys": existing_keys,
            "deleted_count": deleted_count,
            "not_found_count": len(keys_to_delete) - deleted_count
        }
        
    except Exception as e:
        logger.error(f"Failed to delete keys: {e}")
        raise ValueError(f"Failed to delete keys: {str(e)}")

@mcp.tool()
async def list(pattern: Optional[str] = "*") -> Dict[str, Any]:
    """
    List Redis keys matching a pattern
    
    Args:
        pattern: Pattern to match keys (default: *)
    
    Returns:
        List of matching keys with metadata
    """
    try:
        if not redis_client:
            raise ValueError("Redis client not connected")
        
        # Use default pattern if none provided
        search_pattern = pattern or "*"
        
        # Get matching keys
        keys = redis_client.keys(search_pattern)
        
        # Get metadata for each key
        key_details = []
        for key in keys[:100]:  # Limit to 100 keys for performance
            try:
                key_type = redis_client.type(key)
                ttl = redis_client.ttl(key)
                size = redis_client.memory_usage(key) if hasattr(redis_client, 'memory_usage') else None
                
                key_details.append({
                    "key": key,
                    "type": key_type,
                    "ttl": ttl if ttl >= 0 else None,
                    "expires_in": ttl if ttl > 0 else None,
                    "memory_usage": size
                })
            except Exception as e:
                # Skip keys that cause errors (might be deleted concurrently)
                logger.warning(f"Skipping key '{key}': {e}")
                continue
        
        return {
            "success": True,
            "pattern": search_pattern,
            "total_matches": len(keys),
            "returned_count": len(key_details),
            "keys": key_details,
            "truncated": len(keys) > 100
        }
        
    except Exception as e:
        logger.error(f"Failed to list keys with pattern '{pattern}': {e}")
        raise ValueError(f"Failed to list keys: {str(e)}")

@mcp.tool()
async def redis_info() -> Dict[str, Any]:
    """
    Get Redis server information and statistics
    
    Returns:
        Redis server info and connection status
    """
    try:
        if not redis_client:
            raise ValueError("Redis client not connected")
        
        # Get Redis info
        info = redis_client.info()
        
        # Extract key metrics
        server_info = {
            "redis_version": info.get("redis_version"),
            "used_memory_human": info.get("used_memory_human"),
            "connected_clients": info.get("connected_clients"),
            "total_commands_processed": info.get("total_commands_processed"),
            "keyspace_hits": info.get("keyspace_hits"),
            "keyspace_misses": info.get("keyspace_misses"),
            "uptime_in_seconds": info.get("uptime_in_seconds")
        }
        
        # Get database info
        databases = {}
        for key, value in info.items():
            if key.startswith("db"):
                databases[key] = value
        
        return {
            "success": True,
            "connection_url": REDIS_URL.split("@")[-1] if "@" in REDIS_URL else REDIS_URL,
            "server_info": server_info,
            "databases": databases,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get Redis info: {e}")
        raise ValueError(f"Failed to get Redis info: {str(e)}")

@mcp.tool()
async def exists(key: str) -> Dict[str, Any]:
    """
    Check if a key exists in Redis
    
    Args:
        key: Key to check
    
    Returns:
        Existence status and key metadata
    """
    try:
        if not redis_client:
            raise ValueError("Redis client not connected")
        
        if not key:
            raise ValueError("Key cannot be empty")
        
        # Check if key exists
        exists_count = redis_client.exists(key)
        key_exists = exists_count > 0
        
        result = {
            "success": True,
            "key": key,
            "exists": key_exists
        }
        
        # If key exists, get additional metadata
        if key_exists:
            key_type = redis_client.type(key)
            ttl = redis_client.ttl(key)
            
            result.update({
                "type": key_type,
                "ttl": ttl if ttl >= 0 else None,
                "expires_in": ttl if ttl > 0 else None
            })
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to check key existence '{key}': {e}")
        raise ValueError(f"Failed to check key existence: {str(e)}")

@mcp.tool()
async def flush_database(database: Optional[int] = None) -> Dict[str, Any]:
    """
    Flush (clear) a Redis database or all databases
    
    Args:
        database: Database number to flush (None for current database)
    
    Returns:
        Flush operation results
    """
    try:
        if not redis_client:
            raise ValueError("Redis client not connected")
        
        # Get current database info before flushing
        current_db = redis_client.connection_pool.connection_kwargs.get('db', 0)
        
        if database is not None:
            # Select specific database
            redis_client.select(database)
            db_to_flush = database
        else:
            db_to_flush = current_db
        
        # Count keys before flushing
        keys_before = len(redis_client.keys("*"))
        
        # Flush the database
        redis_client.flushdb()
        
        # Restore original database selection if we changed it
        if database is not None and database != current_db:
            redis_client.select(current_db)
        
        return {
            "success": True,
            "database_flushed": db_to_flush,
            "keys_deleted": keys_before,
            "timestamp": datetime.utcnow().isoformat(),
            "warning": "All keys in the specified database have been permanently deleted"
        }
        
    except Exception as e:
        logger.error(f"Failed to flush database: {e}")
        raise ValueError(f"Failed to flush database: {str(e)}")

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv('REDIS_MCP_PORT', '8018'))
    
    logger.info(f"Starting Redis MCP Server on port {port}")
    logger.info(f"Redis URL: {REDIS_URL.split('@')[-1] if '@' in REDIS_URL else REDIS_URL}")
    
    if redis_client:
        try:
            info = redis_client.info()
            logger.info(f"Redis version: {info.get('redis_version')}")
            logger.info(f"Connected clients: {info.get('connected_clients')}")
        except Exception as e:
            logger.warning(f"Could not get Redis info: {e}")
    else:
        logger.warning("Redis client not connected - operations will fail")
    
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")