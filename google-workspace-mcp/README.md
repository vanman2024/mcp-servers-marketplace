# Google Workspace MCP Servers

Comprehensive Model Context Protocol servers for Google Workspace integration.

## Structure

```
google-workspace-mcp/
├── google-drive/        # 7 tools - File & folder management
├── google-sheets/       # 10 tools - Spreadsheets with formulas, charts, formatting
├── google-docs/         # 7 tools - Document creation & editing
├── google-tasks/        # 10 tools - Task management with subtasks
├── google-gmail/        # 7 tools - Email management
├── google-calendar/     # 7 tools - Calendar & event management
├── ENHANCEMENTS.md      # Future feature roadmap
└── README.md           # This file
```

## Currently Implemented (48 tools total)

### Google Drive (7 tools)
- `drive_search` - Search files by name
- `drive_list_folder` - List folder contents
- `drive_get_file` - Get file metadata
- `drive_create_folder` - Create new folder
- `drive_move_file` - Move file to folder
- `drive_rename_file` - Rename file/folder
- `drive_delete_file` - Delete/trash file

### Google Sheets (10 tools)
- `sheets_create` - Create new spreadsheet
- `sheets_read` - Read cell data
- `sheets_write` - Write data with formulas (=SUM, etc.)
- `sheets_append` - Append rows
- `sheets_format_cells` - Bold, colors, fonts
- `sheets_add_borders` - Cell borders
- `sheets_add_chart` - Charts (column, bar, line, pie)
- `sheets_add_dropdown` - Data validation dropdowns
- `sheets_conditional_format` - Conditional formatting
- `sheets_sort_range` - Sort data

### Google Docs (7 tools)
- `docs_create` - Create new document
- `docs_read` - Read document content
- `docs_insert_text` - Insert text at position
- `docs_append_text` - Append to end
- `docs_format_text` - Bold, italic, font size
- `docs_find_replace` - Find & replace text
- `docs_insert_table` - Add tables

### Google Tasks (10 tools)
- `tasks_list_tasklists` - List all task lists
- `tasks_create_tasklist` - Create new list
- `tasks_list_tasks` - List tasks
- `tasks_create` - Create new task
- `tasks_update` - Update task
- `tasks_complete` - Mark as completed
- `tasks_delete` - Delete task
- `tasks_add_subtask` - Add subtask to parent ⭐ NEW
- `tasks_list_subtasks` - List subtasks ⭐ NEW
- `tasks_move_task` - Reorder/move tasks ⭐ NEW

### Google Gmail (7 tools) ⭐ NEW
- `gmail_list_messages` - List emails with filters
- `gmail_get_message` - Read full email
- `gmail_send_message` - Send new email
- `gmail_reply_message` - Reply to email
- `gmail_delete_message` - Delete/trash email
- `gmail_modify_labels` - Add/remove labels
- `gmail_search_messages` - Advanced Gmail search

### Google Calendar (7 tools) ⭐ NEW
- `calendar_list_calendars` - List all calendars
- `calendar_list_events` - List events with date filters
- `calendar_get_event` - Get event details
- `calendar_create_event` - Create event with attendees
- `calendar_update_event` - Update event
- `calendar_delete_event` - Delete event
- `calendar_check_availability` - Find free/busy slots

## Authentication & Configuration Storage

All servers use OAuth 2.0 with token caching. Configuration files are stored in:

**`~/.config/mcp-gdrive/`** (Created automatically on first run)

### Files in this directory:
- **`gcp-oauth.keys.json`** - OAuth credentials from Google Cloud Console (reusable across computers)
- **`drive-token.json`** - Google Drive OAuth token (machine-specific)
- **`sheets-token.json`** - Google Sheets OAuth token (machine-specific)
- **`docs-token.json`** - Google Docs OAuth token (machine-specific)
- **`tasks-token.json`** - Google Tasks OAuth token (machine-specific)
- **`gmail-token.json`** - Gmail OAuth token (machine-specific)
- **`calendar-token.json`** - Google Calendar OAuth token (machine-specific)

### Important Notes:
- **Credentials file (`gcp-oauth.keys.json`)**: Can be copied to new computers ✅
- **Token files (`*-token.json`)**: Must be regenerated on each computer via OAuth browser flow ⚠️
- **Scopes**: Each service requests only the minimum required permissions
- **Auto-refresh**: Tokens refresh automatically when expired

## Configuration

### MCP Server Setup (`~/.claude.json`)
```json
{
  "mcpServers": {
    "google-drive": {...},
    "google-sheets": {...},
    "google-docs": {...},
    "google-tasks": {...},
    "google-gmail": {...},
    "google-calendar": {...}
  }
}
```

### Permissions (`~/.claude/settings.local.json`)
All 48 tools are pre-approved in the allow list to avoid permission prompts.

## Usage Examples

### Create Workout Tracker
```python
# Create spreadsheet with formulas
sheets_create(title="Workout Tracker 2025")
sheets_write(range="A1:F10", values=[
    ["Date", "Exercise", "Sets", "Reps", "Weight", "Total Volume"],
    ["2025-10-01", "Bench Press", "3", "10", "185", "=C2*D2*E2"]
])
```

### Manage Email
```python
# List unread emails
gmail_list_messages(query="is:unread", max_results=10)

# Send email
gmail_send_message(
    to="user@example.com",
    subject="Meeting Tomorrow",
    body="Let's meet at 10am"
)
```

### Schedule Events
```python
# Create calendar event
calendar_create_event(
    calendar_id="primary",
    summary="Team Meeting",
    start_time="2025-10-05T10:00:00-07:00",
    end_time="2025-10-05T11:00:00-07:00",
    attendees=["team@example.com"]
)
```

### Organize Tasks
```python
# Create task with subtasks
task = tasks_create(tasklist_id="...", title="Project Launch")
tasks_add_subtask(tasklist_id="...", parent_task_id=task.id, title="Design mockups")
tasks_add_subtask(tasklist_id="...", parent_task_id=task.id, title="Write copy")
```

## Next Steps

See `ENHANCEMENTS.md` for planned features including:
- Google Forms
- Google Slides
- Advanced Drive permissions
- Apps Script support
- And more!
