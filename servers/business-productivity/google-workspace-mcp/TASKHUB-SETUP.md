# TaskHub - Google Tasks ↔ Sheets Sync System

## Overview
TaskHub automatically syncs tasks between Google Tasks and a Google Spreadsheet every 5 minutes.

**Spreadsheet**: https://docs.google.com/spreadsheets/d/1ikSNPgrKKkqYZV1C3HyqjAY7kOCgDQWHK7f25cnimio

## Architecture

### Components
1. **Google Spreadsheet** (TaskHub)
   - Sheets: Clients, Projects, Tasks, Categories, Dashboard, Sync Log
   - Tasks sheet tracks: TaskID, GoogleTaskID, ProjectID, ClientID, Title, Status, Due, Notes, Category, etc.
   - Categories sheet: Controlled list of 10 categories for task classification

2. **Container-Bound Apps Script** (Task Hub Sync Engine)
   - Script ID: `1lAlA8aJPWPSD3VWW7__XXKYBnFBIz0YDWikdpEJHkVEBbkjvymSMrrt2`
   - Location: Attached to the spreadsheet (Extensions → Apps Script)
   - GCP Project: `drive-mcp-460321` (Project Number: `77394755564`)

3. **Time-Based Trigger**
   - Runs `runScheduledSync()` every 5 minutes
   - Automatically syncs Google Tasks ↔ Spreadsheet

4. **MCP Server** (google-apps-script)
   - Monitors sync executions
   - Can update script code programmatically
   - **Cannot** execute functions remotely (Google limitation for container-bound scripts)

## Setup Steps (Already Completed)

### 1. Create Spreadsheet Structure
```
Created 4 sheets:
- Clients (ClientID, ClientName, Type, Status, Notes, Created, Updated)
- Projects (ProjectID, ClientID, ClientName, ProjectName, Stage, Owner, Created, Updated)
- Tasks (TaskID, GoogleTaskID, ProjectID, ProjectName, ClientID, ClientName, Title, Status, Due, Notes, ParentTaskID, Created, Updated, LastSync, SyncStatus)
- Dashboard (for metrics/summaries)
- Sync Log (created automatically by sync, shows execution history)
```

### 2. Create Container-Bound Apps Script
- Opened spreadsheet → Extensions → Apps Script
- Created `Combined.js` with sync logic
- Functions:
  - `syncTasksToSheets()` - Pull from Google Tasks
  - `syncSheetsToTasks()` - Push to Google Tasks
  - `syncBidirectional()` - Run both directions
  - `runScheduledSync()` - Called by trigger
  - `writeSyncLog()` - Logs to Sync Log sheet

### 3. Enable Google Tasks API
In Apps Script editor:
- Services → Add a service → Google Tasks API v1

### 4. Link to GCP Project
**IMPORTANT**: This allows monitoring via MCP
- Apps Script editor → ⚙️ Project Settings
- Google Cloud Platform (GCP) Project → Change project
- Enter project number: `77394755564`
- Click Set project

### 5. Set Up Trigger
Ran `setupTrigger()` function to create:
- Time-based trigger
- Runs every 5 minutes
- Function: `runScheduledSync`

### 6. Configure MCP Authentication
```bash
cd /home/gotime2022/Projects/Extracted/MCP-Servers/servers/stdio/google-workspace-mcp/google-apps-script
venv/bin/python -c "from src.server import get_credentials; creds = get_credentials(); print('Token valid:', creds.valid)"
```
This creates: `~/.config/mcp-gdrive/apps-script-token.json`

Required scopes:
- `https://www.googleapis.com/auth/script.projects`
- `https://www.googleapis.com/auth/script.deployments`
- `https://www.googleapis.com/auth/script.processes`
- `https://www.googleapis.com/auth/script.scriptapp`
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/spreadsheets`
- `https://www.googleapis.com/auth/tasks`

## How It Works

### Automatic Sync Flow
```
Every 5 minutes:
1. Trigger fires → runScheduledSync()
2. syncBidirectional() runs:
   a. syncTasksToSheets() - Pull from Google Tasks
      - Get all task lists
      - For each task, check if exists in sheet
      - Create new or update existing
   b. syncSheetsToTasks() - Push to Google Tasks
      - Get all tasks from sheet
      - If task modified since last sync, update Google Task
      - If no GoogleTaskID, create new Google Task
3. writeSyncLog() - Record results to Sync Log sheet
```

### Monitoring via MCP

**What you CAN do:**
```bash
# View recent sync executions
mcp__google-apps-script__list_script_processes(
  script_id="1lAlA8aJPWPSD3VWW7__XXKYBnFBIz0YDWikdpEJHkVEBbkjvymSMrrt2"
)

# Get script metadata
mcp__google-apps-script__get_script_project(
  script_id="1lAlA8aJPWPSD3VWW7__XXKYBnFBIz0YDWikdpEJHkVEBbkjvymSMrrt2"
)

# Read sync log from spreadsheet
mcp__google-sheets__sheets_read(
  spreadsheet_id="1ikSNPgrKKkqYZV1C3HyqjAY7kOCgDQWHK7f25cnimio",
  range="Sync Log!A1:C50"
)
```

**What you CANNOT do:**
- Execute functions remotely via `scripts.run` API
- This is a Google limitation for container-bound scripts
- Manual execution must be done in Apps Script UI

## Sync Log Sheet

The "Sync Log" sheet is automatically created on first sync and contains:
- **Timestamp**: When sync ran
- **Message**: "Sync completed" or "Sync failed"
- **Details**: JSON with sync stats
  ```json
  {
    "duration": "45.2s",
    "tasksToSheets": {
      "success": true,
      "synced": 4,
      "created": 1,
      "updated": 3
    },
    "sheetsToTasks": {
      "success": true,
      "updated": 0,
      "created": 0
    }
  }
  ```

## Troubleshooting

### Sync Not Running
1. Check trigger exists: Apps Script → Triggers (clock icon)
2. Check executions: Apps Script → Executions tab
3. View errors in execution logs

### MCP Authentication Issues
If MCP tools return authentication errors:

**Re-authenticate:**
```bash
cd /home/gotime2022/Projects/Extracted/MCP-Servers/servers/stdio/google-workspace-mcp/google-apps-script
trash ~/.config/mcp-gdrive/apps-script-token.json
venv/bin/python -c "from src.server import get_credentials; creds = get_credentials(); print('Token valid:', creds.valid)"
```

This will:
1. Open browser to Google OAuth
2. Show all required scopes
3. Save new token after approval

### Viewing Sync Results
1. Open spreadsheet: https://docs.google.com/spreadsheets/d/1ikSNPgrKKkqYZV1C3HyqjAY7kOCgDQWHK7f25cnimio
2. Go to "Sync Log" sheet
3. See recent executions with timestamps and results

## File Locations

### Local Files
- Code: `/home/gotime2022/Projects/TaskHub/Combined.js`
- MCP Server: `/home/gotime2022/Projects/Extracted/MCP-Servers/servers/stdio/google-workspace-mcp/google-apps-script/`
- Token: `~/.config/mcp-gdrive/apps-script-token.json`
- OAuth Keys: `~/.config/mcp-gdrive/gcp-oauth.keys.json`
- MCP Config: `~/.claude.json` (all Google MCP servers)

### Google Cloud
- GCP Project ID: `drive-mcp-460321`
- GCP Project Number: `77394755564`
- Script ID (container-bound): `1lAlA8aJPWPSD3VWW7__XXKYBnFBIz0YDWikdpEJHkVEBbkjvymSMrrt2`
- Spreadsheet ID: `1ikSNPgrKKkqYZV1C3HyqjAY7kOCgDQWHK7f25cnimio`

## Quick Reference

### Access Points
- **Spreadsheet**: https://docs.google.com/spreadsheets/d/1ikSNPgrKKkqYZV1C3HyqjAY7kOCgDQWHK7f25cnimio
- **Apps Script**: Open spreadsheet → Extensions → Apps Script
- **GCP Console**: https://console.cloud.google.com/home/dashboard?project=drive-mcp-460321

### Common Tasks
```bash
# Monitor sync executions
claude code
> Use mcp__google-apps-script__list_script_processes tool

# View sync logs
# Open spreadsheet → "Sync Log" sheet

# Update sync code
# Edit /home/gotime2022/Projects/TaskHub/Combined.js
# Then deploy via MCP or paste into Apps Script editor

# Re-authenticate MCP
cd /home/gotime2022/Projects/Extracted/MCP-Servers/servers/stdio/google-workspace-mcp/google-apps-script
venv/bin/python -c "from src.server import get_credentials; creds = get_credentials(); print('Token valid:', creds.valid)"
```

## Status
✅ **OPERATIONAL** - Sync running automatically every 5 minutes since 2025-10-02
