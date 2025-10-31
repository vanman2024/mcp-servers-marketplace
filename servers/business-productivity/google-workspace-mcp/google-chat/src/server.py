#!/usr/bin/env python3
"""Google Chat MCP Server - FastMCP for chat bot integration using Service Account"""

import os
from fastmcp import FastMCP
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import Optional, List
import json

# Service account scopes for Google Chat bot
SCOPES = ['https://www.googleapis.com/auth/chat.bot']

mcp = FastMCP("Google Chat", dependencies=["google-auth", "google-api-python-client"])

_creds: Optional[service_account.Credentials] = None


def get_credentials():
    """Get service account credentials for Google Chat bot"""
    global _creds
    if _creds:
        return _creds

    creds_dir = os.getenv('GDRIVE_CREDS_DIR', os.path.expanduser('~/.config/mcp-gdrive'))
    service_account_file = os.path.join(creds_dir, 'service-account.json')

    if not os.path.exists(service_account_file):
        raise FileNotFoundError(
            f"Service account file not found: {service_account_file}\n"
            "Please download service account JSON from Google Cloud Console:\n"
            "https://console.cloud.google.com/iam-admin/serviceaccounts?project=drive-mcp-460321"
        )

    creds = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=SCOPES
    )

    _creds = creds
    return creds


# ============================================================================
# SPACES - Manage chat spaces/rooms
# ============================================================================

@mcp.tool()
def chat_list_spaces(max_results: int = 100) -> str:
    """List all Google Chat spaces the bot has access to"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    results = service.spaces().list(pageSize=max_results).execute()
    spaces = results.get('spaces', [])

    space_list = []
    for space in spaces:
        space_list.append({
            'name': space.get('name'),
            'spaceType': space.get('spaceType'),
            'displayName': space.get('displayName'),
            'threaded': space.get('spaceThreadingState') == 'THREADED_MESSAGES'
        })

    return json.dumps(space_list, indent=2)


@mcp.tool()
def chat_get_space(space_name: str) -> str:
    """Get details about a specific space"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    space = service.spaces().get(name=space_name).execute()

    return json.dumps({
        'name': space.get('name'),
        'spaceType': space.get('spaceType'),
        'displayName': space.get('displayName'),
        'threaded': space.get('spaceThreadingState') == 'THREADED_MESSAGES',
        'singleUserBotDm': space.get('singleUserBotDm', False)
    }, indent=2)


@mcp.tool()
def chat_create_space(display_name: str, space_type: str = 'SPACE') -> str:
    """Create a new chat space
    space_type: SPACE (group) or DM (direct message)"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    space = {
        'displayName': display_name,
        'spaceType': space_type
    }

    result = service.spaces().create(body=space).execute()

    return json.dumps({
        'name': result.get('name'),
        'displayName': result.get('displayName'),
        'spaceType': result.get('spaceType')
    }, indent=2)


@mcp.tool()
def chat_delete_space(space_name: str) -> str:
    """Delete a chat space"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    service.spaces().delete(name=space_name).execute()

    return json.dumps({
        'success': True,
        'message': f'Deleted space {space_name}'
    }, indent=2)


# ============================================================================
# MESSAGES - Send and manage messages
# ============================================================================

@mcp.tool()
def chat_send_message(space_name: str, text: str, thread_key: Optional[str] = None) -> str:
    """Send a message to a space or thread
    thread_key: Optional thread identifier to reply in thread"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    message = {'text': text}

    # If thread_key provided, send to thread
    if thread_key:
        message['thread'] = {'threadKey': thread_key}

    result = service.spaces().messages().create(
        parent=space_name,
        body=message
    ).execute()

    return json.dumps({
        'name': result.get('name'),
        'text': result.get('text'),
        'sender': result.get('sender', {}).get('displayName'),
        'createTime': result.get('createTime')
    }, indent=2)


@mcp.tool()
def chat_send_card_message(space_name: str, header_title: str, sections: List[dict]) -> str:
    """Send a rich card message with formatted content
    sections: List of card sections with widgets"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    message = {
        'cardsV2': [{
            'cardId': 'taskhub-card',
            'card': {
                'header': {
                    'title': header_title
                },
                'sections': sections
            }
        }]
    }

    result = service.spaces().messages().create(
        parent=space_name,
        body=message
    ).execute()

    return json.dumps({
        'name': result.get('name'),
        'createTime': result.get('createTime')
    }, indent=2)


@mcp.tool()
def chat_list_messages(space_name: str, max_results: int = 50) -> str:
    """List messages in a space"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    results = service.spaces().messages().list(
        parent=space_name,
        pageSize=max_results
    ).execute()

    messages = results.get('messages', [])

    message_list = []
    for msg in messages:
        message_list.append({
            'name': msg.get('name'),
            'text': msg.get('text'),
            'sender': msg.get('sender', {}).get('displayName'),
            'senderEmail': msg.get('sender', {}).get('email'),
            'createTime': msg.get('createTime'),
            'thread': msg.get('thread', {}).get('name')
        })

    return json.dumps(message_list, indent=2)


@mcp.tool()
def chat_get_message(message_name: str) -> str:
    """Get details about a specific message"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    message = service.spaces().messages().get(name=message_name).execute()

    return json.dumps({
        'name': message.get('name'),
        'text': message.get('text'),
        'sender': message.get('sender', {}).get('displayName'),
        'senderEmail': message.get('sender', {}).get('email'),
        'createTime': message.get('createTime'),
        'thread': message.get('thread', {}).get('name'),
        'annotations': message.get('annotations', [])
    }, indent=2)


@mcp.tool()
def chat_update_message(message_name: str, text: str) -> str:
    """Update an existing message"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    message = {'text': text}

    result = service.spaces().messages().update(
        name=message_name,
        updateMask='text',
        body=message
    ).execute()

    return json.dumps({
        'name': result.get('name'),
        'text': result.get('text'),
        'lastUpdateTime': result.get('lastUpdateTime')
    }, indent=2)


@mcp.tool()
def chat_delete_message(message_name: str) -> str:
    """Delete a message"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    service.spaces().messages().delete(name=message_name).execute()

    return json.dumps({
        'success': True,
        'message': f'Deleted message {message_name}'
    }, indent=2)


# ============================================================================
# MEMBERS - Manage space membership
# ============================================================================

@mcp.tool()
def chat_list_members(space_name: str) -> str:
    """List members of a space"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    results = service.spaces().members().list(parent=space_name).execute()
    members = results.get('memberships', [])

    member_list = []
    for member in members:
        member_data = member.get('member', {})
        member_list.append({
            'name': member.get('name'),
            'displayName': member_data.get('displayName'),
            'email': member_data.get('name', '').split('/')[-1] if 'users/' in member_data.get('name', '') else None,
            'type': member_data.get('type'),
            'role': member.get('role'),
            'createTime': member.get('createTime')
        })

    return json.dumps(member_list, indent=2)


@mcp.tool()
def chat_get_member(member_name: str) -> str:
    """Get details about a specific member"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    member = service.spaces().members().get(name=member_name).execute()
    member_data = member.get('member', {})

    return json.dumps({
        'name': member.get('name'),
        'displayName': member_data.get('displayName'),
        'email': member_data.get('name', '').split('/')[-1] if 'users/' in member_data.get('name', '') else None,
        'type': member_data.get('type'),
        'role': member.get('role'),
        'createTime': member.get('createTime')
    }, indent=2)


# ============================================================================
# REACTIONS - Message reactions (emojis)
# ============================================================================

@mcp.tool()
def chat_create_reaction(message_name: str, emoji: str) -> str:
    """Add emoji reaction to a message
    emoji: Unicode emoji or custom emoji ID"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    reaction = {
        'emoji': {'unicode': emoji}
    }

    result = service.spaces().messages().reactions().create(
        parent=message_name,
        body=reaction
    ).execute()

    return json.dumps({
        'name': result.get('name'),
        'emoji': result.get('emoji', {}).get('unicode'),
        'user': result.get('user', {}).get('displayName')
    }, indent=2)


@mcp.tool()
def chat_list_reactions(message_name: str) -> str:
    """List all reactions on a message"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    results = service.spaces().messages().reactions().list(parent=message_name).execute()
    reactions = results.get('reactions', [])

    reaction_list = []
    for reaction in reactions:
        reaction_list.append({
            'name': reaction.get('name'),
            'emoji': reaction.get('emoji', {}).get('unicode'),
            'user': reaction.get('user', {}).get('displayName')
        })

    return json.dumps(reaction_list, indent=2)


@mcp.tool()
def chat_delete_reaction(reaction_name: str) -> str:
    """Delete a reaction from a message"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    service.spaces().messages().reactions().delete(name=reaction_name).execute()

    return json.dumps({
        'success': True,
        'message': f'Deleted reaction {reaction_name}'
    }, indent=2)


# ============================================================================
# ATTACHMENTS - Handle file attachments
# ============================================================================

@mcp.tool()
def chat_get_attachment(attachment_name: str) -> str:
    """Get attachment metadata and download URL"""
    creds = get_credentials()
    service = build('chat', 'v1', credentials=creds)

    attachment = service.spaces().messages().attachments().get(name=attachment_name).execute()

    return json.dumps({
        'name': attachment.get('name'),
        'contentName': attachment.get('contentName'),
        'contentType': attachment.get('contentType'),
        'downloadUri': attachment.get('downloadUri'),
        'thumbnailUri': attachment.get('thumbnailUri')
    }, indent=2)


# ============================================================================
# UTILITY - Bot helpers
# ============================================================================

@mcp.tool()
def chat_parse_mention(message_text: str, bot_user_id: str) -> str:
    """Check if message mentions the bot and extract command
    Returns: JSON with isMentioned and commandText"""
    mention_pattern = f'@{bot_user_id}'
    is_mentioned = mention_pattern in message_text

    command_text = ''
    if is_mentioned:
        # Extract text after @mention
        parts = message_text.split(mention_pattern, 1)
        if len(parts) > 1:
            command_text = parts[1].strip()

    return json.dumps({
        'isMentioned': is_mentioned,
        'commandText': command_text,
        'fullText': message_text
    }, indent=2)


if __name__ == "__main__":
    mcp.run()
