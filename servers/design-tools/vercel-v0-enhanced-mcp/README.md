# Vercel v0 MCP Server

An MCP (Model Context Protocol) server that provides UI component generation capabilities using Vercel's v0 API. This server enables Claude Code instances to generate professional UI components, overcoming Claude's native UI design limitations.

## Features

- **Component Generation**: Generate React/TypeScript components with customizable tech stacks
- **Page Generation**: Create complete Next.js pages with optional API routes
- **Data-Driven UI**: Generate UI components based on data structures
- **Component Improvement**: Enhance existing components with v0's capabilities
- **Design-to-Code**: Convert design descriptions into working components
- **HTTP API**: FastMCP-based HTTP server for easy integration

## Prerequisites

- Python 3.10+
- Vercel API token (for v0 access)
- FastMCP and dependencies

## Installation

```bash
cd servers/vercel-v0-mcp
pip install -e .
```

## Configuration

Set your Vercel API token as an environment variable:

```bash
export V0_API_KEY="your-vercel-token"
# or
export VERCEL_TOKEN="your-vercel-token"
```

Optional: Set custom port (default: 8010)
```bash
export V0_MCP_PORT=8010
```

## Running the Server

```bash
python src/vercel_v0_server.py
```

The server will start on `http://localhost:8010` (or your configured port).

## Available Tools

### 1. generate_component

Generate a UI component using v0.

**Parameters:**
- `prompt` (required): Description of the component to generate
- `component_name`: Name for the component
- `framework`: Frontend framework (default: "Next.js 14 App Router")
- `styling`: CSS framework (default: "Tailwind CSS")
- `ui_library`: UI component library (default: "shadcn/ui")
- `output_format`: "single_file" or "multi_file"

**Example:**
```json
{
  "tool": "generate_component",
  "arguments": {
    "prompt": "Create a user profile card with avatar, name, bio, and social links",
    "component_name": "UserProfileCard",
    "framework": "Next.js 14 App Router",
    "styling": "Tailwind CSS",
    "ui_library": "shadcn/ui"
  }
}
```

### 2. generate_page

Generate a complete Next.js page.

**Parameters:**
- `page_description` (required): Description of the page functionality
- `page_name` (required): Name for the page
- `include_layout`: Whether to include layout wrapper (default: true)
- `include_api_route`: Whether to generate API route (default: false)

**Example:**
```json
{
  "tool": "generate_page",
  "arguments": {
    "page_description": "User dashboard showing stats, recent activity, and quick actions",
    "page_name": "dashboard",
    "include_layout": true,
    "include_api_route": true
  }
}
```

### 3. generate_ui_from_data

Generate UI component based on data structure.

**Parameters:**
- `data_structure` (required): JSON or description of data
- `ui_type`: Type of UI - "table", "cards", "list", "chart", "form" (default: "table")
- `interactions`: Description of user interactions needed

**Example:**
```json
{
  "tool": "generate_ui_from_data",
  "arguments": {
    "data_structure": "{\"products\": [{\"id\": 1, \"name\": \"Product 1\", \"price\": 99.99, \"stock\": 10}]}",
    "ui_type": "cards",
    "interactions": "Add to cart button, quantity selector"
  }
}
```

### 4. improve_component

Improve an existing component.

**Parameters:**
- `existing_code` (required): Current component code
- `improvements` (required): Description of improvements
- `maintain_structure`: Keep the same structure (default: true)

**Example:**
```json
{
  "tool": "improve_component",
  "arguments": {
    "existing_code": "export const Button = ({children}) => <button>{children}</button>",
    "improvements": "Add proper TypeScript types, loading state, disabled state, and variants (primary, secondary, danger)",
    "maintain_structure": true
  }
}
```

### 5. convert_design_to_code

Convert design description to component code.

**Parameters:**
- `design_description` (required): Detailed design description
- `design_system`: Design system to use (default: "shadcn/ui")
- `responsive_breakpoints`: Responsive strategy (default: "mobile-first")

**Example:**
```json
{
  "tool": "convert_design_to_code",
  "arguments": {
    "design_description": "A pricing card with gradient border, title at top, price in large text, feature list with checkmarks, and CTA button at bottom",
    "design_system": "shadcn/ui",
    "responsive_breakpoints": "mobile-first"
  }
}
```

## Integration with Claude Code

Claude Code instances can use this server via MCP to generate UI components:

```python
# Example usage in Claude Code
result = await mcp_call(
    server="http://localhost:8010",
    tool="generate_component",
    params={
        "prompt": "Create a modern navigation header with logo, menu items, and user dropdown",
        "component_name": "NavigationHeader"
    }
)

# Write the generated component
if result["success"]:
    await write_file(
        path="src/components/NavigationHeader.tsx",
        content=result["code"]
    )
```

## Testing

Run the test suite:

```bash
cd servers/vercel-v0-mcp
pytest tests/ -v
```

## Error Handling

The server provides structured error responses:

```json
{
  "success": false,
  "error": "Detailed error message"
}
```

Common errors:
- Missing API key: Set `V0_API_KEY` or `VERCEL_TOKEN`
- API rate limits: Check Vercel account limits
- Invalid prompts: Ensure clear component descriptions

## Tech Stack Support

Default tech stack:
- Framework: Next.js 14 App Router
- Language: TypeScript
- Styling: Tailwind CSS
- UI Library: shadcn/ui
- State: React hooks

All components are generated with:
- Accessibility best practices
- Responsive design
- TypeScript types
- Modern React patterns
- Helpful comments

## Development

The server uses:
- FastMCP for HTTP API
- OpenAI SDK (configured for v0)
- Async Python for performance
- Comprehensive error handling

## License

Part of the MCP Kernel project.