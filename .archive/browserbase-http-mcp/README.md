# Browserbase HTTP MCP Server

Cloud-based browser automation server providing comprehensive web interaction tools via HTTP.

## Features

- **Cloud Browser Management**: Session creation, context management
- **Page Interaction**: Click, type, hover, drag & drop operations  
- **Navigation**: URL navigation, back/forward controls
- **Content Extraction**: Screenshots, text extraction, accessibility snapshots
- **Form Handling**: Input filling, dropdown selection
- **Keyboard Control**: Key press simulation

## Tools Available

### Session Management
- `browserbase_session_create` - Create/reuse browser sessions
- `browserbase_session_close` - Close browser sessions
- `browserbase_context_create` - Create persistent contexts
- `browserbase_context_delete` - Remove contexts

### Page Navigation
- `browserbase_navigate` - Navigate to URLs
- `browserbase_navigate_back` - Go back in history
- `browserbase_navigate_forward` - Go forward in history

### Element Interaction
- `browserbase_click` - Click elements using refs
- `browserbase_type` - Type text into inputs
- `browserbase_hover` - Hover over elements
- `browserbase_drag` - Drag and drop between elements
- `browserbase_select_option` - Select dropdown options

### Content Capture
- `browserbase_take_screenshot` - Capture page/element screenshots
- `browserbase_get_text` - Extract text content
- `browserbase_snapshot` - Create accessibility snapshots

### Controls
- `browserbase_press_key` - Simulate keyboard input
- `browserbase_wait` - Add delays between actions
- `browserbase_resize` - Resize browser window
- `browserbase_close` - Close current page

## Configuration

Required environment variables:
```bash
BROWSERBASE_API_KEY=your_browserbase_api_key
BROWSERBASE_PROJECT_ID=your_browserbase_project_id
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Start Server
```bash
python browserbase_server.py
```

Server runs on http://localhost:8020

### Claude Integration
```bash
claude mcp add --transport sse browserbase-http http://localhost:8020
```

## Example Usage

1. **Create Session**:
   ```json
   {
     "tool": "browserbase_session_create",
     "arguments": {}
   }
   ```

2. **Navigate to URL**:
   ```json
   {
     "tool": "browserbase_navigate", 
     "arguments": {"url": "https://example.com"}
   }
   ```

3. **Take Screenshot**:
   ```json
   {
     "tool": "browserbase_take_screenshot",
     "arguments": {}
   }
   ```

4. **Click Element**:
   ```json
   {
     "tool": "browserbase_click",
     "arguments": {
       "element": "Submit Button",
       "ref": "button#submit"
     }
   }
   ```

Perfect for autonomous web automation in DevLoop3 workflows!