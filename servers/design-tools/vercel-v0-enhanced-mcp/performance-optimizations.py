#\!/usr/bin/env python3
"""
Performance Optimizations for Enhanced V0 MCP Server
Production-ready enhancements for concurrent request handling
"""

import asyncio
import aiohttp
import logging
from typing import Dict, Any
import time
from functools import wraps
import json
from pathlib import Path

# Performance Configuration
PERFORMANCE_CONFIG = {
    "max_concurrent_requests": 50,
    "request_timeout": 300,  # 5 minutes
    "connection_pool_size": 100,
    "connection_pool_ttl": 30,
    "memory_cache_size": 1000,
    "cache_ttl": 3600,  # 1 hour
    "rate_limit_per_minute": 60,
    "burst_limit": 10,
    "worker_processes": 4,
    "thread_pool_size": 20
}

class PerformanceOptimizer:
    """Enhanced performance optimization for production deployment"""
    
    def __init__(self):
        self.request_cache = {}
        self.rate_limits = {}
        self.connection_pool = None
        self.metrics = {
            "requests_processed": 0,
            "average_response_time": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors": 0,
            "active_connections": 0
        }
        
    async def initialize(self):
        """Initialize performance optimizations"""
        # Create optimized HTTP client session
        connector = aiohttp.TCPConnector(
            limit=PERFORMANCE_CONFIG["connection_pool_size"],
            limit_per_host=20,
            ttl_dns_cache=300,
            use_dns_cache=True,
            keepalive_timeout=30,
            enable_cleanup_closed=True
        )
        
        timeout = aiohttp.ClientTimeout(
            total=PERFORMANCE_CONFIG["request_timeout"],
            connect=30,
            sock_read=60
        )
        
        self.connection_pool = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={"User-Agent": "Enhanced-V0-MCP-Server/1.0"}
        )
        
        logging.info("✅ Performance optimizer initialized")
    
    def performance_monitor(self, func):
        """Decorator to monitor function performance"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                self.metrics["requests_processed"] += 1
                
                # Update average response time
                response_time = time.time() - start_time
                if self.metrics["average_response_time"] == 0:
                    self.metrics["average_response_time"] = response_time
                else:
                    self.metrics["average_response_time"] = (
                        self.metrics["average_response_time"] * 0.9 + 
                        response_time * 0.1
                    )
                
                return result
            except Exception as e:
                self.metrics["errors"] += 1
                raise e
        return wrapper
    
    def cache_response(self, cache_key: str, response: Any, ttl: int = None):
        """Cache response with TTL"""
        if ttl is None:
            ttl = PERFORMANCE_CONFIG["cache_ttl"]
        
        self.request_cache[cache_key] = {
            "data": response,
            "timestamp": time.time(),
            "ttl": ttl
        }
        
        # Cleanup old cache entries
        current_time = time.time()
        expired_keys = [
            key for key, value in self.request_cache.items()
            if current_time - value["timestamp"] > value["ttl"]
        ]
        for key in expired_keys:
            del self.request_cache[key]
    
    def get_cached_response(self, cache_key: str):
        """Get cached response if valid"""
        if cache_key not in self.request_cache:
            self.metrics["cache_misses"] += 1
            return None
        
        cached = self.request_cache[cache_key]
        if time.time() - cached["timestamp"] > cached["ttl"]:
            del self.request_cache[cache_key]
            self.metrics["cache_misses"] += 1
            return None
        
        self.metrics["cache_hits"] += 1
        return cached["data"]
    
    def rate_limit_check(self, client_id: str) -> bool:
        """Check if request is within rate limits"""
        current_time = time.time()
        minute_window = int(current_time // 60)
        
        if client_id not in self.rate_limits:
            self.rate_limits[client_id] = {}
        
        client_limits = self.rate_limits[client_id]
        
        # Clean old windows
        old_windows = [w for w in client_limits.keys() if w < minute_window - 1]
        for window in old_windows:
            del client_limits[window]
        
        # Check current window
        if minute_window not in client_limits:
            client_limits[minute_window] = 0
        
        if client_limits[minute_window] >= PERFORMANCE_CONFIG["rate_limit_per_minute"]:
            return False
        
        client_limits[minute_window] += 1
        return True
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        cache_hit_rate = 0
        if self.metrics["cache_hits"] + self.metrics["cache_misses"] > 0:
            cache_hit_rate = self.metrics["cache_hits"] / (
                self.metrics["cache_hits"] + self.metrics["cache_misses"]
            )
        
        return {
            **self.metrics,
            "cache_hit_rate": cache_hit_rate,
            "cache_size": len(self.request_cache),
            "rate_limit_clients": len(self.rate_limits)
        }
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.connection_pool:
            await self.connection_pool.close()
        logging.info("✅ Performance optimizer cleanup completed")

# Production Server Configuration
PRODUCTION_SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8015,
    "workers": PERFORMANCE_CONFIG["worker_processes"],
    "loop": "uvloop",  # Faster event loop
    "http": "httptools",  # Faster HTTP parser
    "access_log": True,
    "access_log_format": '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s',
    "log_config": {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S %z"
            }
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "/var/log/mcp/v0-enhanced.log",
                "maxBytes": 104857600,  # 100MB
                "backupCount": 5
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["default"]
        }
    }
}

# Health Check Configuration
async def health_check():
    """Production health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "server": "vercel-v0-enhanced-mcp",
        "uptime": time.time() - start_time,
        "tools_available": 20,
        "performance": optimizer.get_metrics()
    }

# Global optimizer instance
optimizer = PerformanceOptimizer()
start_time = time.time()

# Production startup script
async def production_startup():
    """Production server startup sequence"""
    logging.info("🚀 Starting Enhanced V0 MCP Server in production mode")
    
    # Initialize performance optimizations
    await optimizer.initialize()
    
    # Verify all required environment variables
    required_vars = ["V0_API_KEY", "VERCEL_TOKEN"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {missing_vars}")
    
    # Create necessary directories
    Path("/var/log/mcp").mkdir(parents=True, exist_ok=True)
    Path("/var/mcp-data").mkdir(parents=True, exist_ok=True)
    
    logging.info("✅ Production startup completed successfully")

# Production shutdown sequence
async def production_shutdown():
    """Production server shutdown sequence"""
    logging.info("🛑 Shutting down Enhanced V0 MCP Server")
    await optimizer.cleanup()
    logging.info("✅ Production shutdown completed")

if __name__ == "__main__":
    import uvicorn
    
    # Run with production configuration
    uvicorn.run(
        "vercel_v0_server:mcp",
        **PRODUCTION_SERVER_CONFIG
    )

EOF < /dev/null
