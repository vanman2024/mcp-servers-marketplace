# Miro HTTP MCP Server

A comprehensive MCP server for creating and managing Miro boards for visual workflow diagrams, agent orchestration planning, and collaborative design processes.

## Features

- **Board Management**: Create and manage Miro boards programmatically
- **Visual Elements**: Add sticky notes, shapes, and connectors
- **Workflow Visualization**: Create agent workflow diagrams automatically
- **Kanban Boards**: Build task management boards with columns

## Prerequisites

- Python 3.8+
- Miro API access token
- FastMCP framework

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Set the following environment variables:

```bash
export MIRO_ACCESS_TOKEN="your-miro-api-token"
export MIRO_MCP_PORT="8021"  # Optional, defaults to 8021
```

## Running the Server

```bash
cd src
python miro_server.py
```

The server will start on port 8021 by default.

## Available Tools

### 1. create_board
Create a new Miro board.

**Parameters:**
- `name` (required): Board name
- `description` (optional): Board description

### 2. create_sticky_note
Add a sticky note to a board.

**Parameters:**
- `board_id` (required): Target board ID
- `content` (required): Note content
- `x` (optional): X position (default: 0)
- `y` (optional): Y position (default: 0)
- `color` (optional): Note color hex (default: #FFF9B1)

### 3. create_shape
Create a shape on a board.

**Parameters:**
- `board_id` (required): Target board ID
- `shape_type` (required): Shape type (rectangle, circle, triangle, etc.)
- `content` (optional): Shape text
- `x` (optional): X position
- `y` (optional): Y position
- `width` (optional): Shape width
- `height` (optional): Shape height
- `color` (optional): Fill color hex

### 4. create_connector
Create a connector between two items.

**Parameters:**
- `board_id` (required): Target board ID
- `start_item_id` (required): Source item ID
- `end_item_id` (required): Target item ID
- `label` (optional): Connector label
- `style` (optional): Connector style (elbowed, curved, straight)

### 5. create_agent_workflow_board
Create a complete agent workflow visualization.

**Parameters:**
- `workflow_name` (required): Workflow name
- `agents` (required): List of agent definitions
- `connections` (optional): Connections between agents
- `mcp_servers` (optional): MCP servers to include

### 6. create_kanban_board
Create a kanban-style task board.

**Parameters:**
- `board_name` (required): Board name
- `columns` (required): List of column names
- `tasks` (optional): Initial tasks with column assignments

## Testing

The server includes comprehensive tests using the FastMCP Client pattern with both direct function testing and HTTP protocol compliance validation.

### Recent Test Results (August 4, 2025)

**Overall Test Status: ⚠️ NEEDS ATTENTION (86% pass rate)**

#### Phase 2: Direct Function Testing ✅ EXCELLENT
- **Success Rate:** 100% (31/31 tests passed)
- **Duration:** 10.2 seconds
- **Status:** PRODUCTION READY

**Coverage:**
- ✅ 6 Tools: All functional with proper error handling
- ✅ 5 Resources: All return valid structured data
- ✅ 5 Prompts: All generate appropriate guidance content
- ✅ 7 Error Scenarios: Comprehensive validation coverage
- ✅ 8 Performance Tests: Sub-second response times

#### Phase 3: Protocol Compliance Testing ⚠️ PARTIAL
- **Success Rate:** 50% (6/12 tests passed)
- **Duration:** 5 minutes
- **Status:** NEEDS IMPROVEMENT

**Category Results:**
- ✅ Basic Connectivity: 100% (1/1)
- ✅ JSON-RPC Format: 100% (3/3)
- ✅ Concurrent Sessions: 100% (1/1)
- ✅ Stress Testing: 100% (1/1) - 100/100 requests successful
- ❌ Session Management: 0% (0/5) - Critical compatibility issue
- ❌ Header Requirements: 0% (0/1) - Overly restrictive validation

### Running Tests

```bash
# Interactive testing with detailed output
python test_direct.py

# CI/CD testing with JSON output
python test_ci.py

# Protocol compliance testing
python test_protocol.py

# Comprehensive multi-phase testing
python test_comprehensive.py
```

### Performance Metrics

- **Average Response Time:** 33ms under load
- **Stress Test Performance:** 100/100 requests at 100% success rate
- **Concurrent Handling:** 5 simultaneous sessions managed effectively
- **Server Stability:** Excellent - no crashes or timeouts during testing

### Known Issues and Limitations

#### 🚨 Critical Issues (Require Immediate Attention)
1. **Session Management Compatibility**: Session ID validation is overly restrictive
   - Standard session header formats not accepted (`x-session-id`, `Session-ID`)
   - Query parameter variations not supported (`session_id`, `sessionId`)
   - May not work with standard MCP clients (Claude Desktop, etc.)

#### ⚠️ Minor Issues
1. **Header Validation**: Too strict, prevents standard MCP client connections
2. **Protocol Documentation**: Limited documentation of session requirements
3. **Client Compatibility**: Needs testing with real MCP clients

### Recommendations for Production Deployment

#### Before Production Use:
1. **Fix Session ID Handling** (High Priority)
   - Accept standard session header formats
   - Support common query parameter patterns
   - Test with real MCP clients (Claude Desktop, etc.)

2. **Improve Header Compatibility** (Medium Priority)
   - Implement graceful header validation
   - Add backwards compatibility options

3. **Documentation Updates** (Low Priority)
   - Document session requirements clearly
   - Provide client integration examples

## Contributing

1. Add tests for any new tools
2. Ensure all tests pass before submitting PR
3. Update this README with new features

## License

[License information]