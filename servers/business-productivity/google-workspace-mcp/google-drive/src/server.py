#!/usr/bin/env python3
"""Google Drive MCP Server - FastMCP with full Drive access"""

import os
from fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaInMemoryUpload
from typing import Optional
import json

SCOPES = ['https://www.googleapis.com/auth/drive']

mcp = FastMCP("Google Drive", dependencies=["google-auth", "google-api-python-client"])

_creds: Optional[Credentials] = None


def get_credentials():
    """Get or refresh Google OAuth credentials"""
    global _creds
    if _creds:
        return _creds

    creds_dir = os.getenv('GDRIVE_CREDS_DIR', os.path.expanduser('~/.config/mcp-gdrive'))
    token_file = os.path.join(creds_dir, 'drive-token.json')
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
def drive_search(query: str, page_size: int = 10) -> str:
    """Search for files in Google Drive"""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    search_query = f"name contains '{query}' and trashed = false"
    results = service.files().list(
        q=search_query,
        pageSize=page_size,
        fields="files(id, name, mimeType, modifiedTime, webViewLink)"
    ).execute()

    return json.dumps(results.get('files', []), indent=2)


@mcp.tool()
def drive_get_file(file_id: str) -> str:
    """Get file metadata by ID"""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    file = service.files().get(
        fileId=file_id,
        fields="id, name, mimeType, parents, modifiedTime, webViewLink"
    ).execute()

    return json.dumps(file, indent=2)


@mcp.tool()
def drive_create_folder(name: str, parent_id: Optional[str] = None) -> str:
    """Create a new folder in Google Drive"""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]

    folder = service.files().create(body=file_metadata, fields='id, name, webViewLink').execute()
    return json.dumps(folder, indent=2)


@mcp.tool()
def drive_move_file(file_id: str, new_parent_id: str) -> str:
    """Move a file to a different folder"""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    # Get current parents
    file = service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ','.join(file.get('parents', []))

    file = service.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=previous_parents,
        fields='id, name, parents'
    ).execute()

    return json.dumps(file, indent=2)


@mcp.tool()
def drive_rename_file(file_id: str, new_name: str) -> str:
    """Rename a file or folder"""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    file = service.files().update(
        fileId=file_id,
        body={'name': new_name},
        fields='id, name'
    ).execute()

    return json.dumps(file, indent=2)


@mcp.tool()
def drive_delete_file(file_id: str) -> str:
    """Delete a file (move to trash)"""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    service.files().delete(fileId=file_id).execute()
    return json.dumps({'success': True, 'fileId': file_id}, indent=2)


@mcp.tool()
def drive_list_folder(folder_id: Optional[str] = None, page_size: int = 100) -> str:
    """List files in a folder (root if folder_id not provided)"""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    query = "trashed = false"
    if folder_id:
        query = f"'{folder_id}' in parents and trashed = false"
    else:
        query = "'root' in parents and trashed = false"

    results = service.files().list(
        q=query,
        pageSize=page_size,
        fields="files(id, name, mimeType, modifiedTime)"
    ).execute()

    return json.dumps(results.get('files', []), indent=2)


@mcp.tool()
def drive_create_text_file(name: str, content: str, parent_id: Optional[str] = None, mime_type: str = 'text/plain') -> str:
    """Create a text/markdown file in Google Drive.
    mime_type options: 'text/plain', 'text/markdown'"""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': name}
    if parent_id:
        file_metadata['parents'] = [parent_id]

    media = MediaInMemoryUpload(content.encode('utf-8'), mimetype=mime_type, resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink, mimeType'
    ).execute()

    return json.dumps(file, indent=2)


@mcp.tool()
def drive_read_text_file(file_id: str) -> str:
    """Read content from a text file in Google Drive"""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    request = service.files().get_media(fileId=file_id)
    content = request.execute()

    return content.decode('utf-8')


@mcp.tool()
def drive_update_text_file(file_id: str, content: str, mime_type: str = 'text/plain') -> str:
    """Update content of a text file in Google Drive"""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    media = MediaInMemoryUpload(content.encode('utf-8'), mimetype=mime_type, resumable=True)

    file = service.files().update(
        fileId=file_id,
        media_body=media,
        fields='id, name, modifiedTime'
    ).execute()

    return json.dumps(file, indent=2)


if __name__ == "__main__":
    mcp.run()
