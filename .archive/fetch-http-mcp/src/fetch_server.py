#!/usr/bin/env python3
"""
Fetch HTTP MCP Server
Web content fetching and conversion for efficient LLM usage.
Based on the official Fetch MCP server pattern with FastMCP HTTP transport.
"""

import os
import re
import asyncio
import aiohttp
from typing import Any, Dict, Optional
from urllib.parse import urlparse, urljoin
from fastmcp import FastMCP
import html2text

# Initialize the MCP server
mcp = FastMCP("Fetch HTTP Server")

# Initialize HTML to text converter
h2t = html2text.HTML2Text()
h2t.ignore_links = False
h2t.ignore_images = False
h2t.body_width = 0  # Don't wrap text

async def fetch_url(url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Helper function to fetch URL content"""
    try:
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers) as response:
                content = await response.text()
                
                return {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "content": content,
                    "url": str(response.url),
                    "content_type": response.content_type
                }
    except asyncio.TimeoutError:
        return {"error": "Request timed out after 30 seconds"}
    except Exception as e:
        return {"error": str(e)}

def clean_markdown(content: str) -> str:
    """Clean up markdown content"""
    # Remove excessive blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    # Remove trailing whitespace
    content = '\n'.join(line.rstrip() for line in content.split('\n'))
    return content.strip()

@mcp.tool()
async def fetch(
    url: str,
    start_index: int = 0,
    max_length: int = 50000,
    raw: bool = False,
    ignore_robots_txt: bool = False,
    user_agent: Optional[str] = None
) -> Dict[str, Any]:
    """Fetch a URL and extract its contents as markdown"""
    try:
        # Validate URL
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return {
                "success": False,
                "error": "Invalid URL format"
            }
        
        # Security check for local/internal IPs
        if parsed.hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
            return {
                "success": False,
                "error": "Access to localhost is restricted for security reasons"
            }
        
        # Set headers
        headers = {
            "User-Agent": user_agent or "Mozilla/5.0 (compatible; MCP-Fetch/1.0)"
        }
        
        # Check robots.txt if not ignored
        if not ignore_robots_txt:
            robots_url = urljoin(url, '/robots.txt')
            robots_response = await fetch_url(robots_url, headers)
            
            if robots_response.get('status') == 200:
                # Basic robots.txt parsing (simplified)
                robots_content = robots_response.get('content', '')
                if 'User-agent: *' in robots_content and 'Disallow: /' in robots_content:
                    return {
                        "success": False,
                        "error": "Access forbidden by robots.txt"
                    }
        
        # Fetch the actual URL
        response = await fetch_url(url, headers)
        
        if 'error' in response:
            return {
                "success": False,
                "error": response['error']
            }
        
        if response['status'] != 200:
            return {
                "success": False,
                "error": f"HTTP {response['status']} error",
                "status": response['status']
            }
        
        content = response['content']
        
        # Convert HTML to markdown if not raw
        if not raw and 'text/html' in response.get('content_type', ''):
            content = h2t.handle(content)
            content = clean_markdown(content)
        
        # Apply start_index and max_length
        if start_index > 0:
            content = content[start_index:]
        
        if len(content) > max_length:
            content = content[:max_length]
            truncated = True
        else:
            truncated = False
        
        return {
            "success": True,
            "url": url,
            "content": content,
            "content_type": response.get('content_type', 'text/plain'),
            "length": len(content),
            "truncated": truncated,
            "start_index": start_index,
            "headers": response.get('headers', {}),
            "action": "fetch"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def fetch_batch(
    urls: list[str],
    max_concurrent: int = 5,
    ignore_errors: bool = True
) -> Dict[str, Any]:
    """Fetch multiple URLs concurrently"""
    try:
        results = []
        errors = 0
        
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def fetch_with_semaphore(url: str, index: int):
            async with semaphore:
                result = await fetch(url)
                return {"index": index, "url": url, "result": result}
        
        # Create tasks for all URLs
        tasks = [
            fetch_with_semaphore(url, i) 
            for i, url in enumerate(urls)
        ]
        
        # Execute tasks concurrently
        completed = await asyncio.gather(*tasks, return_exceptions=True)
        
        for item in completed:
            if isinstance(item, Exception):
                errors += 1
                if not ignore_errors:
                    return {
                        "success": False,
                        "error": str(item),
                        "action": "fetch_batch"
                    }
                results.append({
                    "success": False,
                    "error": str(item)
                })
            else:
                results.append(item)
                if not item['result']['success']:
                    errors += 1
        
        return {
            "success": errors == 0 or ignore_errors,
            "total_urls": len(urls),
            "successful": len(urls) - errors,
            "errors": errors,
            "results": results,
            "action": "fetch_batch"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def fetch_extract(
    url: str,
    selectors: Optional[list[str]] = None,
    extract_links: bool = True,
    extract_images: bool = True,
    extract_metadata: bool = True
) -> Dict[str, Any]:
    """Fetch a URL and extract specific elements"""
    try:
        # First fetch the URL
        fetch_result = await fetch(url, raw=True)
        
        if not fetch_result['success']:
            return fetch_result
        
        content = fetch_result['content']
        extracted = {
            "url": url,
            "title": None,
            "description": None,
            "links": [],
            "images": [],
            "metadata": {}
        }
        
        # Basic HTML parsing for extraction
        if extract_metadata:
            # Extract title
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
            if title_match:
                extracted['title'] = title_match.group(1).strip()
            
            # Extract meta description
            desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
            if desc_match:
                extracted['description'] = desc_match.group(1).strip()
            
            # Extract other meta tags
            meta_matches = re.findall(r'<meta\s+([^>]+)>', content, re.IGNORECASE)
            for meta in meta_matches[:10]:  # Limit to first 10
                name_match = re.search(r'name=["\']([^"\']+)["\']', meta)
                content_match = re.search(r'content=["\']([^"\']+)["\']', meta)
                if name_match and content_match:
                    extracted['metadata'][name_match.group(1)] = content_match.group(1)
        
        if extract_links:
            # Extract links
            link_matches = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>', content, re.IGNORECASE)
            for href, text in link_matches[:50]:  # Limit to first 50
                absolute_url = urljoin(url, href)
                extracted['links'].append({
                    "url": absolute_url,
                    "text": text.strip(),
                    "relative": not href.startswith(('http://', 'https://'))
                })
        
        if extract_images:
            # Extract images
            img_matches = re.findall(r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>', content, re.IGNORECASE)
            for src in img_matches[:30]:  # Limit to first 30
                absolute_url = urljoin(url, src)
                alt_match = re.search(r'alt=["\']([^"\']+)["\']', src)
                alt_text = alt_match.group(1) if alt_match else ""
                extracted['images'].append({
                    "url": absolute_url,
                    "alt": alt_text,
                    "relative": not src.startswith(('http://', 'https://'))
                })
        
        return {
            "success": True,
            "extracted": extracted,
            "content_length": len(content),
            "action": "fetch_extract"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def fetch_sitemap(url: str, max_urls: int = 100) -> Dict[str, Any]:
    """Fetch and parse a sitemap.xml file"""
    try:
        # Try common sitemap locations
        sitemap_urls = [
            url if url.endswith('sitemap.xml') else urljoin(url, '/sitemap.xml'),
            urljoin(url, '/sitemap_index.xml'),
            urljoin(url, '/sitemap.xml.gz')
        ]
        
        sitemap_content = None
        used_url = None
        
        for sitemap_url in sitemap_urls:
            result = await fetch(sitemap_url, raw=True)
            if result['success']:
                sitemap_content = result['content']
                used_url = sitemap_url
                break
        
        if not sitemap_content:
            return {
                "success": False,
                "error": "Could not find sitemap at common locations",
                "tried_urls": sitemap_urls
            }
        
        # Parse sitemap
        urls = []
        url_matches = re.findall(r'<loc>([^<]+)</loc>', sitemap_content)
        
        for match in url_matches[:max_urls]:
            lastmod_match = re.search(r'<lastmod>([^<]+)</lastmod>', sitemap_content[sitemap_content.find(match):])
            urls.append({
                "url": match.strip(),
                "lastmod": lastmod_match.group(1).strip() if lastmod_match else None
            })
        
        return {
            "success": True,
            "sitemap_url": used_url,
            "total_urls": len(url_matches),
            "returned_urls": len(urls),
            "urls": urls,
            "truncated": len(url_matches) > max_urls,
            "action": "fetch_sitemap"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def fetch_rss(url: str, max_items: int = 20) -> Dict[str, Any]:
    """Fetch and parse an RSS/Atom feed"""
    try:
        result = await fetch(url, raw=True)
        
        if not result['success']:
            return result
        
        content = result['content']
        
        # Detect feed type
        is_atom = '<feed' in content and 'xmlns' in content
        is_rss = '<rss' in content or '<channel>' in content
        
        if not is_atom and not is_rss:
            return {
                "success": False,
                "error": "Content does not appear to be a valid RSS or Atom feed"
            }
        
        feed_info = {
            "type": "atom" if is_atom else "rss",
            "title": None,
            "description": None,
            "link": None,
            "items": []
        }
        
        # Extract feed metadata
        if is_rss:
            title_match = re.search(r'<channel>.*?<title>([^<]+)</title>', content, re.DOTALL)
            desc_match = re.search(r'<channel>.*?<description>([^<]+)</description>', content, re.DOTALL)
            link_match = re.search(r'<channel>.*?<link>([^<]+)</link>', content, re.DOTALL)
        else:
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
            desc_match = re.search(r'<subtitle[^>]*>([^<]+)</subtitle>', content)
            link_match = re.search(r'<link[^>]+href=["\']([^"\']+)["\'][^>]*/?>', content)
        
        if title_match:
            feed_info['title'] = title_match.group(1).strip()
        if desc_match:
            feed_info['description'] = desc_match.group(1).strip()
        if link_match:
            feed_info['link'] = link_match.group(1).strip()
        
        # Extract items
        if is_rss:
            items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
        else:
            items = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
        
        for item in items[:max_items]:
            item_data = {
                "title": None,
                "link": None,
                "description": None,
                "pubDate": None
            }
            
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', item)
            if title_match:
                item_data['title'] = title_match.group(1).strip()
            
            if is_rss:
                link_match = re.search(r'<link>([^<]+)</link>', item)
                desc_match = re.search(r'<description>(<!\[CDATA\[)?([^<\]]+)(\]\]>)?</description>', item)
                date_match = re.search(r'<pubDate>([^<]+)</pubDate>', item)
            else:
                link_match = re.search(r'<link[^>]+href=["\']([^"\']+)["\']', item)
                desc_match = re.search(r'<(content|summary)[^>]*>(<!\[CDATA\[)?([^<\]]+)(\]\]>)?</(content|summary)>', item)
                date_match = re.search(r'<(published|updated)>([^<]+)</(published|updated)>', item)
            
            if link_match:
                item_data['link'] = link_match.group(1).strip()
            if desc_match:
                item_data['description'] = desc_match.group(2).strip() if is_rss else desc_match.group(3).strip()
            if date_match:
                item_data['pubDate'] = date_match.group(1).strip() if is_rss else date_match.group(2).strip()
            
            feed_info['items'].append(item_data)
        
        return {
            "success": True,
            "feed": feed_info,
            "total_items": len(items),
            "returned_items": len(feed_info['items']),
            "truncated": len(items) > max_items,
            "action": "fetch_rss"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Get port from environment variable
    port = int(os.getenv('FETCH_MCP_PORT', '8022'))
    
    print(f"Fetch server initializing...")
    print(f"Starting Fetch HTTP MCP Server on port {port}")
    print("Web content fetching and conversion for efficient LLM usage")
    
    # Run the server
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")