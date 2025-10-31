#!/usr/bin/env python3
"""Google Tasks MCP Server - FastMCP for task management"""

import os
from fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Optional
import json

SCOPES = ['https://www.googleapis.com/auth/tasks']

mcp = FastMCP("Google Tasks", dependencies=["google-auth", "google-api-python-client"])

_creds: Optional[Credentials] = None


def get_credentials():
    """Get or refresh Google OAuth credentials"""
    global _creds
    if _creds:
        return _creds

    creds_dir = os.getenv('GDRIVE_CREDS_DIR', os.path.expanduser('~/.config/mcp-gdrive'))
    token_file = os.path.join(creds_dir, 'tasks-token.json')
    credentials_file = os.path.join(creds_dir, 'gcp-oauth.keys.json')

    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)

        os.makedirs(creds_dir, exist_ok=True)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    _creds = creds
    return creds


@mcp.tool()
def tasks_list_tasklists() -> str:
    """List all task lists"""
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    results = service.tasklists().list().execute()
    items = results.get('items', [])

    return json.dumps(items, indent=2)


@mcp.tool()
def tasks_create_tasklist(title: str) -> str:
    """Create a new task list"""
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    tasklist = service.tasklists().insert(body={'title': title}).execute()

    return json.dumps({
        'id': tasklist['id'],
        'title': tasklist['title']
    }, indent=2)


@mcp.tool()
def tasks_list_tasks(tasklist_id: str, show_completed: bool = False) -> str:
    """List tasks in a task list"""
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    results = service.tasks().list(
        tasklist=tasklist_id,
        showCompleted=show_completed
    ).execute()

    items = results.get('items', [])

    return json.dumps(items, indent=2)


@mcp.tool()
def tasks_create(tasklist_id: str, title: str, notes: Optional[str] = None, due: Optional[str] = None) -> str:
    """Create a new task (due date as RFC 3339 timestamp like 2025-12-31T00:00:00Z)"""
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    task = {'title': title}
    if notes:
        task['notes'] = notes
    if due:
        task['due'] = due

    result = service.tasks().insert(tasklist=tasklist_id, body=task).execute()

    return json.dumps(result, indent=2)


@mcp.tool()
def tasks_update(tasklist_id: str, task_id: str, title: Optional[str] = None, notes: Optional[str] = None, status: Optional[str] = None) -> str:
    """Update a task (status: needsAction or completed)"""
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    # Get current task
    task = service.tasks().get(tasklist=tasklist_id, task=task_id).execute()

    # Update fields
    if title:
        task['title'] = title
    if notes is not None:
        task['notes'] = notes
    if status:
        task['status'] = status

    result = service.tasks().update(
        tasklist=tasklist_id,
        task=task_id,
        body=task
    ).execute()

    return json.dumps(result, indent=2)


@mcp.tool()
def tasks_complete(tasklist_id: str, task_id: str) -> str:
    """Mark a task as completed"""
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    task = service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
    task['status'] = 'completed'

    result = service.tasks().update(
        tasklist=tasklist_id,
        task=task_id,
        body=task
    ).execute()

    return json.dumps({'success': True, 'taskId': task_id}, indent=2)


@mcp.tool()
def tasks_delete(tasklist_id: str, task_id: str) -> str:
    """Delete a task"""
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    service.tasks().delete(tasklist=tasklist_id, task=task_id).execute()

    return json.dumps({'success': True, 'taskId': task_id}, indent=2)


@mcp.tool()
def tasks_add_subtask(tasklist_id: str, parent_task_id: str, title: str, notes: Optional[str] = None) -> str:
    """Add subtask to parent task"""
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    task = {'title': title, 'parent': parent_task_id}
    if notes:
        task['notes'] = notes

    result = service.tasks().insert(tasklist=tasklist_id, body=task, parent=parent_task_id).execute()

    return json.dumps(result, indent=2)


@mcp.tool()
def tasks_list_subtasks(tasklist_id: str, parent_task_id: str) -> str:
    """List subtasks for a task"""
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    # Get all tasks and filter by parent
    results = service.tasks().list(tasklist=tasklist_id, showCompleted=True).execute()

    subtasks = [task for task in results.get('items', []) if task.get('parent') == parent_task_id]

    return json.dumps(subtasks, indent=2)


@mcp.tool()
def tasks_move_task(tasklist_id: str, task_id: str, previous: Optional[str] = None, parent: Optional[str] = None) -> str:
    """
    Move task to different position or list
    previous: Task ID to place this task after (for reordering)
    parent: Parent task ID (to make this a subtask)
    """
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    kwargs = {'tasklist': tasklist_id, 'task': task_id}
    if previous:
        kwargs['previous'] = previous
    if parent:
        kwargs['parent'] = parent

    result = service.tasks().move(**kwargs).execute()

    return json.dumps(result, indent=2)


@mcp.tool()
def tasks_clear_completed(tasklist_id: str) -> str:
    """Clear all completed tasks from the specified task list (bulk cleanup)"""
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    service.tasks().clear(tasklist=tasklist_id).execute()

    return json.dumps({
        'success': True,
        'message': f'Cleared all completed tasks from list {tasklist_id}'
    }, indent=2)


@mcp.tool()
def tasks_patch(tasklist_id: str, task_id: str, title: Optional[str] = None, notes: Optional[str] = None, status: Optional[str] = None, due: Optional[str] = None) -> str:
    """
    Partial update of a task (more efficient than full update).
    Only updates fields that are provided.
    """
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    updates = {}
    if title is not None:
        updates['title'] = title
    if notes is not None:
        updates['notes'] = notes
    if status is not None:
        updates['status'] = status
    if due is not None:
        updates['due'] = due

    result = service.tasks().patch(
        tasklist=tasklist_id,
        task=task_id,
        body=updates
    ).execute()

    return json.dumps(result, indent=2)


@mcp.tool()
def tasklists_delete(tasklist_id: str) -> str:
    """Delete an entire task list"""
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    service.tasklists().delete(tasklist=tasklist_id).execute()

    return json.dumps({
        'success': True,
        'message': f'Deleted task list {tasklist_id}'
    }, indent=2)


@mcp.tool()
def tasklists_update(tasklist_id: str, title: str) -> str:
    """Update (rename) a task list"""
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    result = service.tasklists().update(
        tasklist=tasklist_id,
        body={'id': tasklist_id, 'title': title}
    ).execute()

    return json.dumps({
        'success': True,
        'id': result['id'],
        'title': result['title']
    }, indent=2)


@mcp.tool()
def tasklists_patch(tasklist_id: str, title: str) -> str:
    """Partial update (rename) a task list"""
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)

    result = service.tasklists().patch(
        tasklist=tasklist_id,
        body={'title': title}
    ).execute()

    return json.dumps({
        'success': True,
        'id': result['id'],
        'title': result['title']
    }, indent=2)


if __name__ == "__main__":
    mcp.run()
