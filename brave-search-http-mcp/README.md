# Brave Search MCP Server (HTTP)

Web and local search capabilities using Brave Search API via FastMCP with HTTP transport.

Converted from the official MCP TypeScript stdio server to Python HTTP implementation.

## Features

- **Web search** with pagination and result filtering
- **Local search** for businesses and places
- **Automatic fallback** from local to web search
- **Rate limiting** enforcement (1 req/sec, 15k/month)
- **HTTP transport** using FastMCP with streamable-http
- **Comprehensive error handling** with clear messages

## Tools

### Search Operations
- `brave_web_search(query, count?, offset?)` - General web search
- `brave_local_search(query, count?)` - Local business/place search

## API Features

### Web Search
- General queries, news, articles, online content
- Maximum 20 results per request
- Pagination support with offset (max 9)
- Returns title, URL, description, age, language

### Local Search
- Physical locations, businesses, restaurants, services
- Returns detailed business information:
  - Name, address, phone
  - Ratings and review counts
  - Operating hours
  - Geographic coordinates
- Automatically falls back to web search if no local results

## Configuration

### Environment Variables

```bash
# Brave Search API key (required)
BRAVE_API_KEY=your_api_key_here

# Server port
BRAVE_SEARCH_MCP_PORT=8003
```

### Default Settings
- **Default port**: 8003
- **Transport**: streamable-http
- **Rate limit**: 1 request/second
- **Monthly limit**: 15,000 requests

## Installation

```bash
# Install dependencies
pip install fastmcp python-dotenv uvicorn httpx

# Run server
python src/brave_search_server.py
```

## Usage Examples

### Web Search
```python
# Basic web search
{
    "name": "brave_web_search",
    "arguments": {
        "query": "MCP protocol documentation",
        "count": 10
    }
}

# Paginated search
{
    "name": "brave_web_search",
    "arguments": {
        "query": "latest AI developments",
        "count": 20,
        "offset": 5
    }
}
```

### Local Search
```python
# Find nearby restaurants
{
    "name": "brave_local_search",
    "arguments": {
        "query": "pizza near Times Square NYC",
        "count": 5
    }
}

# Search for services
{
    "name": "brave_local_search",
    "arguments": {
        "query": "car repair shops in Seattle"
    }
}
```

## HTTP Endpoints

The server runs on `http://localhost:8003` with MCP tools available at:
- `POST /tools/call` - Execute MCP tools
- `GET /tools/list` - List available tools
- `GET /health` - Health check

## Rate Limiting

The Brave Search API enforces:
- **1 request per second** rate limit
- **15,000 requests per month** quota

The server automatically handles rate limiting by:
- Tracking request timestamps
- Enforcing minimum 1-second intervals
- Sleeping when necessary to comply

## Error Handling

Common errors and their meanings:
- **401**: Invalid API key
- **429**: Rate limit exceeded
- **400**: Invalid query parameters

## Conversion Notes

This server maintains 100% API compatibility with the original TypeScript stdio version while adding:

- **HTTP transport** for web integration
- **Async/await** throughout for performance
- **Better error messages** with specific causes
- **Fallback logic** for local→web search
- **Rate limit enforcement** built-in

## Getting an API Key

1. Visit [Brave Search API](https://brave.com/search/api/)
2. Sign up for an account
3. Get your API key from the dashboard
4. Set the `BRAVE_API_KEY` environment variable

## Testing

```bash
# Test web search
curl -X POST http://localhost:8003/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "brave_web_search",
    "arguments": {
        "query": "test search",
        "count": 5
    }
  }'

# Test local search
curl -X POST http://localhost:8003/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "brave_local_search",
    "arguments": {
        "query": "coffee shops near me"
    }
  }'
```