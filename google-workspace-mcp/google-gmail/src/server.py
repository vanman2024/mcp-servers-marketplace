#!/usr/bin/env python3
"""Google Gmail MCP Server - FastMCP for email management"""

import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Optional, List
import json

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

mcp = FastMCP("Google Gmail", dependencies=["google-auth", "google-api-python-client"])

_creds: Optional[Credentials] = None


def get_credentials():
    """Get or refresh Google OAuth credentials"""
    global _creds
    if _creds:
        return _creds

    creds_dir = os.getenv('GDRIVE_CREDS_DIR', os.path.expanduser('~/.config/mcp-gdrive'))
    token_file = os.path.join(creds_dir, 'gmail-token.json')
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
def gmail_list_messages(max_results: int = 10, query: Optional[str] = None, label_ids: Optional[List[str]] = None) -> str:
    """
    List emails with filters
    query examples: 'is:unread', 'from:user@example.com', 'subject:important', 'after:2025/01/01'
    label_ids: ['INBOX', 'UNREAD', 'STARRED', 'IMPORTANT', 'SENT', 'DRAFT']
    """
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    kwargs = {'userId': 'me', 'maxResults': max_results}
    if query:
        kwargs['q'] = query
    if label_ids:
        kwargs['labelIds'] = label_ids

    results = service.users().messages().list(**kwargs).execute()
    messages = results.get('messages', [])

    # Get basic info for each message
    message_list = []
    for msg in messages:
        full_msg = service.users().messages().get(userId='me', id=msg['id'], format='metadata',
                                                   metadataHeaders=['From', 'Subject', 'Date']).execute()
        headers = {h['name']: h['value'] for h in full_msg.get('payload', {}).get('headers', [])}
        message_list.append({
            'id': msg['id'],
            'threadId': msg['threadId'],
            'snippet': full_msg.get('snippet'),
            'from': headers.get('From'),
            'subject': headers.get('Subject'),
            'date': headers.get('Date')
        })

    return json.dumps(message_list, indent=2)


@mcp.tool()
def gmail_get_message(message_id: str) -> str:
    """Read full email content by ID"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    msg = service.users().messages().get(userId='me', id=message_id, format='full').execute()

    payload = msg.get('payload', {})
    headers = {h['name']: h['value'] for h in payload.get('headers', [])}

    # Extract body
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
    elif 'data' in payload.get('body', {}):
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

    return json.dumps({
        'id': msg['id'],
        'threadId': msg['threadId'],
        'labelIds': msg.get('labelIds', []),
        'snippet': msg.get('snippet'),
        'from': headers.get('From'),
        'to': headers.get('To'),
        'subject': headers.get('Subject'),
        'date': headers.get('Date'),
        'body': body
    }, indent=2)


@mcp.tool()
def gmail_send_message(to: str, subject: str, body: str, cc: Optional[str] = None, bcc: Optional[str] = None) -> str:
    """Send new email"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEMultipart()
    message['To'] = to
    message['Subject'] = subject
    if cc:
        message['Cc'] = cc
    if bcc:
        message['Bcc'] = bcc

    message.attach(MIMEText(body, 'plain'))

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    result = service.users().messages().send(userId='me', body={'raw': raw}).execute()

    return json.dumps({'id': result['id'], 'threadId': result['threadId']}, indent=2)


@mcp.tool()
def gmail_reply_message(message_id: str, body: str) -> str:
    """Reply to existing email"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    # Get original message
    original = service.users().messages().get(userId='me', id=message_id, format='metadata',
                                               metadataHeaders=['From', 'To', 'Subject', 'Message-ID']).execute()
    headers = {h['name']: h['value'] for h in original['payload']['headers']}

    message = MIMEText(body)
    message['To'] = headers.get('From')
    message['Subject'] = 'Re: ' + headers.get('Subject', '').replace('Re: ', '')
    message['In-Reply-To'] = headers.get('Message-ID')
    message['References'] = headers.get('Message-ID')

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    result = service.users().messages().send(userId='me', body={'raw': raw, 'threadId': original['threadId']}).execute()

    return json.dumps({'id': result['id'], 'threadId': result['threadId']}, indent=2)


@mcp.tool()
def gmail_delete_message(message_id: str, permanent: bool = False) -> str:
    """Delete/trash email. Set permanent=True to permanently delete (bypass trash)"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    if permanent:
        service.users().messages().delete(userId='me', id=message_id).execute()
    else:
        service.users().messages().trash(userId='me', id=message_id).execute()

    return json.dumps({'success': True, 'messageId': message_id, 'permanent': permanent}, indent=2)


@mcp.tool()
def gmail_modify_labels(message_id: str, add_labels: Optional[List[str]] = None, remove_labels: Optional[List[str]] = None) -> str:
    """
    Add/remove labels from email
    Common labels: INBOX, UNREAD, STARRED, IMPORTANT, TRASH, SPAM, SENT, DRAFT
    """
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    body = {}
    if add_labels:
        body['addLabelIds'] = add_labels
    if remove_labels:
        body['removeLabelIds'] = remove_labels

    result = service.users().messages().modify(userId='me', id=message_id, body=body).execute()

    return json.dumps({'id': result['id'], 'labelIds': result.get('labelIds', [])}, indent=2)


@mcp.tool()
def gmail_search_messages(query: str, max_results: int = 10) -> str:
    """
    Advanced search with Gmail query syntax
    Examples:
    - 'from:user@example.com subject:meeting'
    - 'is:unread after:2025/01/01'
    - 'has:attachment larger:10M'
    - 'in:inbox is:important'
    """
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
    messages = results.get('messages', [])

    # Get basic info for each message
    message_list = []
    for msg in messages:
        full_msg = service.users().messages().get(userId='me', id=msg['id'], format='metadata',
                                                   metadataHeaders=['From', 'Subject', 'Date']).execute()
        headers = {h['name']: h['value'] for h in full_msg.get('payload', {}).get('headers', [])}
        message_list.append({
            'id': msg['id'],
            'threadId': msg['threadId'],
            'snippet': full_msg.get('snippet'),
            'from': headers.get('From'),
            'subject': headers.get('Subject'),
            'date': headers.get('Date')
        })

    return json.dumps(message_list, indent=2)


@mcp.tool()
def gmail_batch_delete(message_ids: List[str]) -> str:
    """Delete multiple messages at once"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    service.users().messages().batchDelete(userId='me', body={'ids': message_ids}).execute()

    return json.dumps({'success': True, 'deleted_count': len(message_ids)}, indent=2)


@mcp.tool()
def gmail_batch_modify(message_ids: List[str], add_labels: Optional[List[str]] = None, remove_labels: Optional[List[str]] = None) -> str:
    """Modify labels on multiple messages at once"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    body = {'ids': message_ids}
    if add_labels:
        body['addLabelIds'] = add_labels
    if remove_labels:
        body['removeLabelIds'] = remove_labels

    service.users().messages().batchModify(userId='me', body=body).execute()

    return json.dumps({'success': True, 'modified_count': len(message_ids)}, indent=2)


@mcp.tool()
def gmail_untrash(message_id: str) -> str:
    """Restore message from trash"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    result = service.users().messages().untrash(userId='me', id=message_id).execute()

    return json.dumps({'success': True, 'messageId': result['id']}, indent=2)


@mcp.tool()
def gmail_get_attachment(message_id: str, attachment_id: str) -> str:
    """Download attachment (returns base64 encoded data)"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    attachment = service.users().messages().attachments().get(
        userId='me',
        messageId=message_id,
        id=attachment_id
    ).execute()

    return json.dumps({
        'attachmentId': attachment_id,
        'size': attachment.get('size'),
        'data': attachment.get('data')  # base64 encoded
    }, indent=2)


@mcp.tool()
def gmail_create_draft(to: str, subject: str, body: str) -> str:
    """Create draft email"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(body)
    message['To'] = to
    message['Subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    draft = service.users().drafts().create(userId='me', body={'message': {'raw': raw}}).execute()

    return json.dumps({'draftId': draft['id'], 'messageId': draft['message']['id']}, indent=2)


@mcp.tool()
def gmail_list_drafts(max_results: int = 10) -> str:
    """List all draft emails"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().drafts().list(userId='me', maxResults=max_results).execute()
    drafts = results.get('drafts', [])

    draft_list = []
    for draft in drafts:
        full_draft = service.users().drafts().get(userId='me', id=draft['id'], format='metadata',
                                                   metadataHeaders=['To', 'Subject', 'Date']).execute()
        headers = {h['name']: h['value'] for h in full_draft['message']['payload'].get('headers', [])}
        draft_list.append({
            'draftId': draft['id'],
            'messageId': draft['message']['id'],
            'to': headers.get('To'),
            'subject': headers.get('Subject'),
            'snippet': full_draft['message'].get('snippet')
        })

    return json.dumps(draft_list, indent=2)


@mcp.tool()
def gmail_send_draft(draft_id: str) -> str:
    """Send existing draft"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    result = service.users().drafts().send(userId='me', body={'id': draft_id}).execute()

    return json.dumps({'messageId': result['id'], 'threadId': result['threadId']}, indent=2)


@mcp.tool()
def gmail_delete_draft(draft_id: str) -> str:
    """Delete draft"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    service.users().drafts().delete(userId='me', id=draft_id).execute()

    return json.dumps({'success': True, 'draftId': draft_id}, indent=2)


@mcp.tool()
def gmail_list_labels() -> str:
    """List all Gmail labels"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    label_list = []
    for label in labels:
        label_list.append({
            'id': label['id'],
            'name': label.get('name'),
            'type': label.get('type'),
            'messageListVisibility': label.get('messageListVisibility'),
            'labelListVisibility': label.get('labelListVisibility')
        })

    return json.dumps(label_list, indent=2)


@mcp.tool()
def gmail_create_label(name: str, label_list_visibility: str = 'labelShow', message_list_visibility: str = 'show') -> str:
    """Create custom label"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    label = {
        'name': name,
        'labelListVisibility': label_list_visibility,
        'messageListVisibility': message_list_visibility
    }

    result = service.users().labels().create(userId='me', body=label).execute()

    return json.dumps({
        'id': result['id'],
        'name': result.get('name')
    }, indent=2)


@mcp.tool()
def gmail_delete_label(label_id: str) -> str:
    """Delete custom label"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    service.users().labels().delete(userId='me', id=label_id).execute()

    return json.dumps({'success': True, 'labelId': label_id}, indent=2)


@mcp.tool()
def gmail_mark_as_read(message_id: str) -> str:
    """Mark message as read (shortcut for removing UNREAD label)"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    result = service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()

    return json.dumps({'success': True, 'messageId': result['id']}, indent=2)


@mcp.tool()
def gmail_mark_as_unread(message_id: str) -> str:
    """Mark message as unread (shortcut for adding UNREAD label)"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    result = service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'addLabelIds': ['UNREAD']}
    ).execute()

    return json.dumps({'success': True, 'messageId': result['id']}, indent=2)


@mcp.tool()
def gmail_star(message_id: str) -> str:
    """Star message (shortcut)"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    result = service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'addLabelIds': ['STARRED']}
    ).execute()

    return json.dumps({'success': True, 'messageId': result['id']}, indent=2)


@mcp.tool()
def gmail_unstar(message_id: str) -> str:
    """Unstar message (shortcut)"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    result = service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'removeLabelIds': ['STARRED']}
    ).execute()

    return json.dumps({'success': True, 'messageId': result['id']}, indent=2)


@mcp.tool()
def gmail_archive(message_id: str) -> str:
    """Archive message (remove from INBOX)"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    result = service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'removeLabelIds': ['INBOX']}
    ).execute()

    return json.dumps({'success': True, 'messageId': result['id']}, indent=2)


@mcp.tool()
def gmail_get_profile() -> str:
    """Get user's Gmail profile info"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    profile = service.users().getProfile(userId='me').execute()

    return json.dumps({
        'emailAddress': profile.get('emailAddress'),
        'messagesTotal': profile.get('messagesTotal'),
        'threadsTotal': profile.get('threadsTotal'),
        'historyId': profile.get('historyId')
    }, indent=2)


if __name__ == "__main__":
    mcp.run()
