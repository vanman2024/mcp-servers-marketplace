# Sequential Thinking MCP Server (HTTP)

A Model Context Protocol (MCP) server that provides sequential thinking capabilities with support for revisions, branching, and dynamic thought management.

## Features

- **Sequential Thinking**: Process thoughts in ordered sequences
- **Revision Support**: Ability to revise previous thoughts
- **Branching**: Create alternative thought branches for exploration
- **Session Management**: Track complete thinking sessions
- **Dynamic Adjustment**: Adjust total thought estimates as needed
- **HTTP Transport**: FastMCP with streamable-http for web integration

## Tools

### Core Thinking Tool
- `sequentialthinking` - Process sequential thinking steps with full revision and branching support

### Session Management Tools
- `get_thinking_session` - Retrieve a complete thinking session by ID
- `list_thinking_sessions` - List all available thinking sessions
- `clear_thinking_sessions` - Clear all sessions from memory
- `health_check` - Check server health and status

## Installation

```bash
# Install dependencies
pip install fastmcp python-dotenv uvicorn httpx

# Or using the project file
pip install -e .
```

## Configuration

### Environment Variables

```bash
# Server port (optional, defaults to 8015)
SEQUENTIAL_THINKING_MCP_PORT=8015
```

## Usage

### Starting the Server

```bash
# From the server directory
python src/sequential_thinking_server.py

# Or if installed
sequential-thinking-server
```

The server will start on port 8015 by default.

### Integration with Claude Desktop

Add to your Claude configuration:

```bash
claude mcp add --transport sse sequential-thinking http://localhost:8015
```

### Example Usage

#### Basic Sequential Thinking
```json
{
  "name": "sequentialthinking",
  "arguments": {
    "thought": "First, I need to understand the problem statement clearly.",
    "nextThoughtNeeded": true,
    "thoughtNumber": 1,
    "totalThoughts": 5
  }
}
```

#### Revising a Previous Thought
```json
{
  "name": "sequentialthinking",
  "arguments": {
    "thought": "Actually, I need to reconsider my understanding from thought 2.",
    "nextThoughtNeeded": true,
    "thoughtNumber": 4,
    "totalThoughts": 6,
    "isRevision": true,
    "revisesThought": 2
  }
}
```

#### Creating a Branch
```json
{
  "name": "sequentialthinking",
  "arguments": {
    "thought": "Let me explore an alternative approach from thought 3.",
    "nextThoughtNeeded": true,
    "thoughtNumber": 5,
    "totalThoughts": 7,
    "branchFromThought": 3,
    "branchId": "alternative-approach"
  }
}
```

#### Final Thought with Summary
```json
{
  "name": "sequentialthinking",
  "arguments": {
    "thought": "Based on all the analysis, the solution is to implement a caching layer.",
    "nextThoughtNeeded": false,
    "thoughtNumber": 8,
    "totalThoughts": 8
  }
}
```

### Session Management

#### Retrieve a Session
```json
{
  "name": "get_thinking_session",
  "arguments": {
    "sessionId": "session_20240126_143022"
  }
}
```

#### List All Sessions
```json
{
  "name": "list_thinking_sessions",
  "arguments": {}
}
```

## Thought Parameters

### Required Parameters
- `thought`: The content of the current thinking step
- `nextThoughtNeeded`: Whether another thought is needed (boolean)
- `thoughtNumber`: Current thought number in sequence
- `totalThoughts`: Estimated total thoughts needed (can be adjusted)

### Optional Parameters
- `isRevision`: Whether this thought revises previous thinking
- `revisesThought`: Which thought number is being revised
- `branchFromThought`: Thought number to branch from
- `branchId`: Identifier for the branch
- `needsMoreThoughts`: Indicates more thoughts needed than originally estimated
- `sessionId`: Custom session identifier (auto-generated if not provided)

## Response Format

### Successful Thought Response
```json
{
  "thoughtNumber": 3,
  "thought": "The problem requires a distributed approach.",
  "nextThoughtNeeded": true,
  "totalThoughts": 5,
  "sessionId": "session_20240126_143022",
  "sessionThoughtCount": 3
}
```

### Final Thought Response with Summary
```json
{
  "thoughtNumber": 5,
  "thought": "Final conclusion reached.",
  "nextThoughtNeeded": false,
  "totalThoughts": 5,
  "sessionId": "session_20240126_143022",
  "sessionThoughtCount": 5,
  "sessionSummary": {
    "totalThoughts": 5,
    "revisionCount": 1,
    "branches": 2,
    "completed": true
  }
}
```

## Session Storage

Currently uses in-memory storage. In production, consider:
- SQLite for persistence
- Redis for distributed sessions
- PostgreSQL for complex queries

## HTTP Endpoints

The server runs on `http://localhost:8015` with MCP tools available at:
- `POST /tools/call` - Execute MCP tools
- `GET /tools/list` - List available tools
- `GET /health` - Health check

## Use Cases

### Problem Solving
- Break down complex problems into steps
- Explore multiple solution paths
- Revise understanding as new information emerges

### Planning and Design
- Create detailed plans with flexibility
- Branch into alternative approaches
- Adjust scope as requirements clarify

### Analysis and Research
- Systematic exploration of topics
- Document thought evolution
- Track hypothesis changes

### Learning and Understanding
- Step-by-step comprehension building
- Identify and correct misconceptions
- Build on previous insights

## Best Practices

1. **Start Simple**: Begin with an estimated thought count, adjust as needed
2. **Use Revisions**: Don't hesitate to revise earlier thoughts
3. **Branch Exploration**: Create branches for alternative approaches
4. **Clear Conclusions**: Mark final thoughts clearly with `nextThoughtNeeded: false`
5. **Session Management**: Use session IDs for related thought sequences

## Error Handling

The server handles:
- Invalid parameters gracefully
- Missing sessions with helpful messages
- Memory limits (consider implementing max session count)
- Concurrent session access

## Testing

```bash
# Test basic thinking
curl -X POST http://localhost:8015/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "sequentialthinking",
    "arguments": {
      "thought": "Testing sequential thinking",
      "nextThoughtNeeded": true,
      "thoughtNumber": 1,
      "totalThoughts": 3
    }
  }'

# Check health
curl http://localhost:8015/health
```

## Security Notes

- No authentication required (add if needed)
- Sessions are ephemeral (cleared on restart)
- No sensitive data should be stored in thoughts
- Consider rate limiting for production use