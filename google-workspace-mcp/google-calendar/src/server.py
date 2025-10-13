#!/usr/bin/env python3
"""Google Calendar MCP Server - FastMCP for calendar management"""

import os
from fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Optional, List
import json
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar']

mcp = FastMCP("Google Calendar", dependencies=["google-auth", "google-api-python-client"])

_creds: Optional[Credentials] = None


def get_credentials():
    """Get or refresh Google OAuth credentials"""
    global _creds
    if _creds:
        return _creds

    creds_dir = os.getenv('GDRIVE_CREDS_DIR', os.path.expanduser('~/.config/mcp-gdrive'))
    token_file = os.path.join(creds_dir, 'calendar-token.json')
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
def calendar_list_calendars() -> str:
    """List all calendars"""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    calendars = service.calendarList().list().execute()

    calendar_list = []
    for cal in calendars.get('items', []):
        calendar_list.append({
            'id': cal['id'],
            'summary': cal.get('summary'),
            'description': cal.get('description'),
            'timeZone': cal.get('timeZone'),
            'primary': cal.get('primary', False),
            'accessRole': cal.get('accessRole')
        })

    return json.dumps(calendar_list, indent=2)


@mcp.tool()
def calendar_list_events(
    calendar_id: str = 'primary',
    time_min: Optional[str] = None,
    time_max: Optional[str] = None,
    max_results: int = 10,
    single_events: bool = True
) -> str:
    """
    List events with date range filter
    time_min/time_max: RFC3339 timestamp (e.g., '2025-10-01T00:00:00Z')
    """
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    kwargs = {
        'calendarId': calendar_id,
        'maxResults': max_results,
        'singleEvents': single_events,
        'orderBy': 'startTime' if single_events else None
    }

    if time_min:
        kwargs['timeMin'] = time_min
    if time_max:
        kwargs['timeMax'] = time_max

    events = service.events().list(**kwargs).execute()

    event_list = []
    for event in events.get('items', []):
        start = event.get('start', {})
        end = event.get('end', {})
        event_list.append({
            'id': event['id'],
            'summary': event.get('summary'),
            'description': event.get('description'),
            'location': event.get('location'),
            'start': start.get('dateTime', start.get('date')),
            'end': end.get('dateTime', end.get('date')),
            'attendees': [a.get('email') for a in event.get('attendees', [])],
            'htmlLink': event.get('htmlLink')
        })

    return json.dumps(event_list, indent=2)


@mcp.tool()
def calendar_get_event(calendar_id: str, event_id: str) -> str:
    """Get event details by ID"""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

    start = event.get('start', {})
    end = event.get('end', {})

    return json.dumps({
        'id': event['id'],
        'summary': event.get('summary'),
        'description': event.get('description'),
        'location': event.get('location'),
        'start': start.get('dateTime', start.get('date')),
        'end': end.get('dateTime', end.get('date')),
        'attendees': event.get('attendees', []),
        'reminders': event.get('reminders'),
        'htmlLink': event.get('htmlLink'),
        'hangoutLink': event.get('hangoutLink')
    }, indent=2)


@mcp.tool()
def calendar_create_event(
    calendar_id: str,
    summary: str,
    start_time: str,
    end_time: str,
    description: Optional[str] = None,
    location: Optional[str] = None,
    attendees: Optional[List[str]] = None,
    reminders_minutes: Optional[List[int]] = None
) -> str:
    """
    Create new event
    start_time/end_time: RFC3339 timestamp (e.g., '2025-10-01T10:00:00-07:00')
    attendees: List of email addresses
    reminders_minutes: List of minutes before event (e.g., [10, 60] for 10min and 1hr reminders)
    """
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'start': {'dateTime': start_time},
        'end': {'dateTime': end_time}
    }

    if description:
        event['description'] = description
    if location:
        event['location'] = location
    if attendees:
        event['attendees'] = [{'email': email} for email in attendees]

    if reminders_minutes:
        event['reminders'] = {
            'useDefault': False,
            'overrides': [{'method': 'popup', 'minutes': m} for m in reminders_minutes]
        }

    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

    return json.dumps({
        'id': created_event['id'],
        'summary': created_event.get('summary'),
        'htmlLink': created_event.get('htmlLink')
    }, indent=2)


@mcp.tool()
def calendar_update_event(
    calendar_id: str,
    event_id: str,
    summary: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None
) -> str:
    """Update existing event"""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    # Get existing event
    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

    # Update fields
    if summary:
        event['summary'] = summary
    if start_time:
        event['start'] = {'dateTime': start_time}
    if end_time:
        event['end'] = {'dateTime': end_time}
    if description is not None:
        event['description'] = description
    if location is not None:
        event['location'] = location

    updated_event = service.events().update(
        calendarId=calendar_id,
        eventId=event_id,
        body=event
    ).execute()

    return json.dumps({
        'id': updated_event['id'],
        'summary': updated_event.get('summary'),
        'htmlLink': updated_event.get('htmlLink')
    }, indent=2)


@mcp.tool()
def calendar_delete_event(calendar_id: str, event_id: str) -> str:
    """Delete event"""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()

    return json.dumps({'success': True, 'eventId': event_id}, indent=2)


@mcp.tool()
def calendar_check_availability(
    calendar_id: str,
    time_min: str,
    time_max: str
) -> str:
    """
    Find free/busy time slots
    time_min/time_max: RFC3339 timestamp (e.g., '2025-10-01T09:00:00-07:00')
    """
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    body = {
        'timeMin': time_min,
        'timeMax': time_max,
        'items': [{'id': calendar_id}]
    }

    result = service.freebusy().query(body=body).execute()

    busy_times = result['calendars'].get(calendar_id, {}).get('busy', [])

    return json.dumps({
        'calendar': calendar_id,
        'timeMin': time_min,
        'timeMax': time_max,
        'busySlots': busy_times,
        'busyCount': len(busy_times)
    }, indent=2)


@mcp.tool()
def calendar_patch(
    calendar_id: str,
    event_id: str,
    summary: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None
) -> str:
    """Partial update of event (more efficient than full update)"""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    updates = {}
    if summary is not None:
        updates['summary'] = summary
    if start_time is not None:
        updates['start'] = {'dateTime': start_time}
    if end_time is not None:
        updates['end'] = {'dateTime': end_time}
    if description is not None:
        updates['description'] = description
    if location is not None:
        updates['location'] = location

    result = service.events().patch(
        calendarId=calendar_id,
        eventId=event_id,
        body=updates
    ).execute()

    return json.dumps({
        'id': result['id'],
        'summary': result.get('summary'),
        'htmlLink': result.get('htmlLink')
    }, indent=2)


@mcp.tool()
def calendar_quick_add(calendar_id: str, text: str) -> str:
    """
    Create event using natural language
    Examples: 'Dinner with John tomorrow 7pm', 'Team meeting next Monday 2-3pm', 'Coffee at Starbucks on Friday 10am'
    """
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    result = service.events().quickAdd(calendarId=calendar_id, text=text).execute()

    start = result.get('start', {})
    end = result.get('end', {})

    return json.dumps({
        'id': result['id'],
        'summary': result.get('summary'),
        'start': start.get('dateTime', start.get('date')),
        'end': end.get('dateTime', end.get('date')),
        'htmlLink': result.get('htmlLink')
    }, indent=2)


@mcp.tool()
def calendar_move(
    source_calendar_id: str,
    event_id: str,
    destination_calendar_id: str
) -> str:
    """Move event to different calendar"""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    result = service.events().move(
        calendarId=source_calendar_id,
        eventId=event_id,
        destination=destination_calendar_id
    ).execute()

    return json.dumps({
        'id': result['id'],
        'summary': result.get('summary'),
        'calendar': destination_calendar_id,
        'htmlLink': result.get('htmlLink')
    }, indent=2)


@mcp.tool()
def calendar_list_instances(
    calendar_id: str,
    event_id: str,
    time_min: Optional[str] = None,
    time_max: Optional[str] = None
) -> str:
    """List instances of a recurring event"""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    kwargs = {'calendarId': calendar_id, 'eventId': event_id}
    if time_min:
        kwargs['timeMin'] = time_min
    if time_max:
        kwargs['timeMax'] = time_max

    result = service.events().instances(**kwargs).execute()

    instances = []
    for event in result.get('items', []):
        start = event.get('start', {})
        end = event.get('end', {})
        instances.append({
            'id': event['id'],
            'summary': event.get('summary'),
            'start': start.get('dateTime', start.get('date')),
            'end': end.get('dateTime', end.get('date')),
            'status': event.get('status')
        })

    return json.dumps(instances, indent=2)


@mcp.tool()
def calendar_create_calendar(summary: str, description: Optional[str] = None, timezone: str = 'America/Toronto') -> str:
    """Create a new calendar"""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    calendar = {
        'summary': summary,
        'timeZone': timezone
    }
    if description:
        calendar['description'] = description

    result = service.calendars().insert(body=calendar).execute()

    return json.dumps({
        'id': result['id'],
        'summary': result.get('summary'),
        'description': result.get('description'),
        'timeZone': result.get('timeZone')
    }, indent=2)


@mcp.tool()
def calendar_delete_calendar(calendar_id: str) -> str:
    """Delete a calendar (WARNING: Permanent!)"""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    service.calendars().delete(calendarId=calendar_id).execute()

    return json.dumps({
        'success': True,
        'message': f'Deleted calendar {calendar_id}'
    }, indent=2)


if __name__ == "__main__":
    mcp.run()
