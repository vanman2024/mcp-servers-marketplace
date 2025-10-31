#!/usr/bin/env python3
"""
Figma Marketing MCP Server Startup Script
Enterprise-grade startup with comprehensive configuration and monitoring
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / "src"))

from figma_marketing_server import mcp as app

def setup_logging():
    """Configure enterprise logging"""
    log_dir = current_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "marketing_server.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def load_config():
    """Load server configuration"""
    config_path = current_dir / "configs" / "server_config.json"
    with open(config_path) as f:
        return json.load(f)

def validate_environment():
    """Validate required environment variables"""
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_SERVICE_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {missing_vars}")

async def health_check():
    """Perform startup health check"""
    try:
        # Basic health check - server imports work
        logging.info("✅ Server imports validated")
        return True
    except Exception as e:
        logging.error(f"❌ Health check failed: {e}")
        return False

def main():
    """Main startup function"""
    setup_logging()
    config = load_config()
    
    logging.info(f"🚀 Starting {config['server']['name']} v{config['server']['version']}")
    
    try:
        validate_environment()
        logging.info("✅ Environment validation passed")
        
        # Run health check
        if not asyncio.run(health_check()):
            sys.exit(1)
        
        # Start server
        port = config['server']['port']
        host = config['server']['host']
        
        logging.info(f"🌐 Server starting on {host}:{port}")
        logging.info(f"📊 Specialized for: {config['specialization']['focus']}")
        logging.info(f"🎯 Primary categories: {', '.join(config['specialization']['primary_categories'][:3])}...")
        
        import uvicorn
        uvicorn.run(
            "figma_marketing_server:mcp",
            host=host,
            port=port,
            reload=True,
            log_level="info"
        )
        
    except Exception as e:
        logging.error(f"💥 Startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()