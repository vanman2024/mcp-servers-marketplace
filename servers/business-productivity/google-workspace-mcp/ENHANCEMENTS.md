# Google Workspace MCP Server Enhancements

## Current Services
- ✅ Google Drive (7 tools)
- ✅ Google Sheets (10 tools)
- ✅ Google Docs (7 tools)
- ✅ Google Tasks (7 tools)

## Planned Additions

### Priority 1 - Immediate

#### Google Gmail MCP Server (7 tools)
**Scope**: `https://www.googleapis.com/auth/gmail.modify`

1. `gmail_list_messages` - List emails with filters (unread, from, subject, date range)
2. `gmail_get_message` - Read full email content by ID
3. `gmail_send_message` - Send new email with attachments
4. `gmail_reply_message` - Reply to existing email
5. `gmail_delete_message` - Delete/trash email
6. `gmail_modify_labels` - Add/remove labels (read/unread, starred, etc.)
7. `gmail_search_messages` - Advanced search with Gmail query syntax

#### Google Calendar MCP Server (7 tools)
**Scope**: `https://www.googleapis.com/auth/calendar`

1. `calendar_list_calendars` - List all calendars
2. `calendar_list_events` - List events with date range filter
3. `calendar_get_event` - Get event details by ID
4. `calendar_create_event` - Create new event with attendees, reminders
5. `calendar_update_event` - Update existing event
6. `calendar_delete_event` - Delete event
7. `calendar_check_availability` - Find free/busy time slots

#### Google Tasks Enhancements (3 new tools)
Add to existing Google Tasks MCP Server:

8. `tasks_add_subtask` - Add subtask to parent task
9. `tasks_list_subtasks` - List subtasks for a task
10. `tasks_move_task` - Move task to different position or list

### Priority 2 - Near Future

#### Google Sheets Advanced
- Pivot tables
- Named ranges
- Protected ranges
- Filters & filter views
- Merge cells
- Cell notes & comments
- Freeze rows/columns
- Sheet copying

#### Google Docs Advanced
- Headers/footers
- Page breaks
- Images
- Lists (bulleted/numbered)
- Bookmarks & links
- Table of contents

#### Google Drive Advanced
- Permissions management (sharing)
- Comments & replies
- Revisions/version history
- Export files (PDF, DOCX, XLSX)
- Copy files
- Star/unstar files
- Trash management

#### Google Apps Script
**Scope**: `https://www.googleapis.com/auth/script.projects`

1. `sheets_add_script` - Add custom function to spreadsheet
2. `sheets_run_script` - Execute Apps Script function
3. `sheets_create_trigger` - Set up time-based or event-driven automation

### Priority 3 - Future Expansion

#### Google Forms MCP Server
- Create forms
- Add questions
- Get responses
- Analyze results

#### Google Slides MCP Server
- Create presentations
- Add/edit slides
- Insert images/charts
- Export as PDF

#### Google Meet MCP Server
- Create meetings
- Get meeting details
- List scheduled meetings

## Notes
- All services use OAuth 2.0 with separate token files
- Credentials stored in `~/.config/mcp-gdrive/`
- Permissions configured in `~/.claude/settings.local.json`
- Each service uses appropriate Google API scope for security
