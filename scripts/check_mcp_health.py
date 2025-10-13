#!/usr/bin/env python3
"""
Quick health check for all MCP HTTP servers
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from pathlib import Path

async def check_server(session, name, url):
    """Check health of a single server"""
    health_urls = [
        f"{url}/health",
        f"{url}/",
        f"{url}/mcp/health"
    ]
    
    # Try with different headers
    headers_list = [
        {},  # Default headers
        {"Accept": "text/event-stream"},  # MCP servers expect this
        {"Accept": "application/json"}
    ]
    
    for headers in headers_list:
        for health_url in health_urls:
            try:
                async with session.get(health_url, headers=headers, timeout=aiohttp.ClientTimeout(total=3)) as response:
                    # Consider any response as healthy if server is responding
                    if response.status < 500:
                        return {
                            'name': name,
                            'url': url,
                            'status': 'healthy',
                            'response_code': response.status,
                            'checked_at': datetime.now().isoformat()
                        }
            except:
                continue
    
    return {
        'name': name,
        'url': url,
        'status': 'unhealthy',
        'response_code': None,
        'checked_at': datetime.now().isoformat()
    }

async def main():
    """Check all servers"""
    # Load config
    config_path = Path("/home/gotime2022/mcp-kernel-new/.claude/mcp_master_config.json")
    with open(config_path) as f:
        config = json.load(f)
    
    # Get HTTP servers
    http_servers = {
        name: info['url'] 
        for name, info in config.get('mcpServers', {}).items() 
        if info.get('transport') == 'http'
    }
    
    print(f"🔍 Checking {len(http_servers)} MCP HTTP servers...")
    print("=" * 60)
    
    # Check all servers
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[
            check_server(session, name, url) 
            for name, url in http_servers.items()
        ])
    
    # Display results
    healthy_count = 0
    for result in sorted(results, key=lambda x: x['name']):
        status_icon = "✅" if result['status'] == 'healthy' else "❌"
        print(f"{status_icon} {result['name']:<30} {result['url']:<40} {result['status']}")
        if result['status'] == 'healthy':
            healthy_count += 1
    
    print("=" * 60)
    print(f"Summary: {healthy_count}/{len(http_servers)} servers healthy")
    
    # Save results
    results_file = Path("/home/gotime2022/.mcp-persistent/health-check-results.json")
    results_file.parent.mkdir(exist_ok=True)
    with open(results_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'summary': f"{healthy_count}/{len(http_servers)} healthy",
            'servers': results
        }, f, indent=2)
    
    print(f"\n📊 Results saved to: {results_file}")

if __name__ == "__main__":
    asyncio.run(main())