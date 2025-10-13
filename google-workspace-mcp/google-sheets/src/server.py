#!/usr/bin/env python3
"""Google Sheets MCP Server - FastMCP with formulas, formatting, charts, validation"""

import os
from fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Optional, List, Dict, Any
import json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

mcp = FastMCP("Google Sheets", dependencies=["google-auth", "google-api-python-client"])

_creds: Optional[Credentials] = None


def get_credentials():
    """Get or refresh Google OAuth credentials"""
    global _creds
    if _creds:
        return _creds

    creds_dir = os.getenv('GDRIVE_CREDS_DIR', os.path.expanduser('~/.config/mcp-gdrive'))
    token_file = os.path.join(creds_dir, 'sheets-token.json')
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


# ============================================================================
# BASIC DATA OPERATIONS
# ============================================================================

@mcp.tool()
def sheets_create(title: str, sheet_titles: Optional[List[str]] = None) -> str:
    """Create a new spreadsheet"""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    if not sheet_titles:
        sheet_titles = ["Sheet1"]

    spreadsheet = {
        'properties': {'title': title},
        'sheets': [{'properties': {'title': sheet}} for sheet in sheet_titles]
    }

    result = service.spreadsheets().create(body=spreadsheet).execute()
    return json.dumps({
        'spreadsheetId': result['spreadsheetId'],
        'spreadsheetUrl': result['spreadsheetUrl']
    }, indent=2)


@mcp.tool()
def sheets_read(spreadsheet_id: str, range: str) -> str:
    """Read data from a range"""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range
    ).execute()
    return json.dumps(result.get('values', []), indent=2)


@mcp.tool()
def sheets_write(spreadsheet_id: str, range: str, values: List[List[str]]) -> str:
    """Write data (supports formulas like =SUM(A1:A10))"""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range,
        valueInputOption='USER_ENTERED',  # Formulas work
        body={'values': values}
    ).execute()

    return json.dumps({'updatedCells': result.get('updatedCells')}, indent=2)


@mcp.tool()
def sheets_append(spreadsheet_id: str, range: str, values: List[List[str]]) -> str:
    """Append rows to end of sheet"""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range,
        valueInputOption='USER_ENTERED',
        body={'values': values}
    ).execute()

    return json.dumps({'updatedCells': result.get('updates', {}).get('updatedCells')}, indent=2)


@mcp.tool()
def sheets_get_sheet_id(spreadsheet_id: str, sheet_name: str) -> str:
    """Get the sheet ID for a given sheet name (needed for delete/insert operations)"""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

    for sheet in spreadsheet.get('sheets', []):
        if sheet['properties']['title'] == sheet_name:
            return json.dumps({
                'sheetId': sheet['properties']['sheetId'],
                'sheetName': sheet_name
            }, indent=2)

    return json.dumps({'error': f'Sheet "{sheet_name}" not found'}, indent=2)


@mcp.tool()
def sheets_delete_rows(
    spreadsheet_id: str,
    sheet_id: int,
    start_row: int,
    end_row: int
) -> str:
    """
    Delete rows from sheet.
    Row indices are 0-based (row 2 in UI = index 1).
    Deletes rows from start_row (inclusive) to end_row (exclusive).
    Example: start_row=1, end_row=3 deletes rows 2-3 in UI.
    """
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    requests = [{
        'deleteDimension': {
            'range': {
                'sheetId': sheet_id,
                'dimension': 'ROWS',
                'startIndex': start_row,
                'endIndex': end_row
            }
        }
    }]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    deleted_count = end_row - start_row
    return json.dumps({
        'success': True,
        'deletedRows': deleted_count,
        'message': f'Deleted {deleted_count} row(s)'
    }, indent=2)


@mcp.tool()
def sheets_insert_rows(
    spreadsheet_id: str,
    sheet_id: int,
    start_row: int,
    num_rows: int = 1
) -> str:
    """
    Insert blank rows into sheet.
    Row indices are 0-based (row 2 in UI = index 1).
    Inserts num_rows blank rows starting at start_row.
    """
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    requests = [{
        'insertDimension': {
            'range': {
                'sheetId': sheet_id,
                'dimension': 'ROWS',
                'startIndex': start_row,
                'endIndex': start_row + num_rows
            },
            'inheritFromBefore': False
        }
    }]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    return json.dumps({
        'success': True,
        'insertedRows': num_rows,
        'message': f'Inserted {num_rows} row(s) at row {start_row + 1}'
    }, indent=2)


@mcp.tool()
def sheets_clear_range(spreadsheet_id: str, range: str) -> str:
    """
    Clear values from a range (keeps formatting).
    Range in A1 notation (e.g., 'Sheet1!A1:B10').
    """
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=range
    ).execute()

    return json.dumps({
        'success': True,
        'message': f'Cleared range: {range}'
    }, indent=2)


@mcp.tool()
def sheets_find_replace(
    spreadsheet_id: str,
    find: str,
    replacement: str,
    sheet_id: Optional[int] = None,
    match_case: bool = False,
    match_entire_cell: bool = False
) -> str:
    """
    Find and replace text across sheet(s).
    If sheet_id not provided, searches entire spreadsheet.
    """
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    find_replace_spec = {
        'find': find,
        'replacement': replacement,
        'matchCase': match_case,
        'matchEntireCell': match_entire_cell
    }

    if sheet_id is not None:
        find_replace_spec['sheetId'] = sheet_id

    requests = [{'findReplace': find_replace_spec}]

    result = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    occurrences = result.get('replies', [{}])[0].get('findReplace', {}).get('occurrencesChanged', 0)

    return json.dumps({
        'success': True,
        'replacements': occurrences,
        'message': f'Replaced {occurrences} occurrence(s)'
    }, indent=2)


@mcp.tool()
def sheets_duplicate_sheet(
    spreadsheet_id: str,
    source_sheet_id: int,
    new_sheet_name: str
) -> str:
    """
    Duplicate an entire sheet within the same spreadsheet.
    """
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    requests = [{
        'duplicateSheet': {
            'sourceSheetId': source_sheet_id,
            'newSheetName': new_sheet_name
        }
    }]

    result = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    new_sheet = result.get('replies', [{}])[0].get('duplicateSheet', {}).get('properties', {})

    return json.dumps({
        'success': True,
        'newSheetId': new_sheet.get('sheetId'),
        'newSheetName': new_sheet.get('title'),
        'message': f'Duplicated sheet to "{new_sheet_name}"'
    }, indent=2)


@mcp.tool()
def sheets_delete_duplicates(
    spreadsheet_id: str,
    sheet_id: int,
    start_row: int,
    end_row: int,
    start_col: int,
    end_col: int,
    comparison_columns: Optional[List[int]] = None
) -> str:
    """
    Delete duplicate rows based on column values.
    comparison_columns: List of column indices to check for duplicates (0-based).
    If not provided, checks all columns in range.
    """
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    delete_duplicates_spec = {
        'range': {
            'sheetId': sheet_id,
            'startRowIndex': start_row,
            'endRowIndex': end_row,
            'startColumnIndex': start_col,
            'endColumnIndex': end_col
        }
    }

    if comparison_columns:
        delete_duplicates_spec['comparisonColumns'] = [
            {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': col, 'endIndex': col + 1}
            for col in comparison_columns
        ]

    requests = [{'deleteDuplicates': delete_duplicates_spec}]

    result = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    duplicates = result.get('replies', [{}])[0].get('deleteDuplicates', {}).get('duplicatesRemovedCount', 0)

    return json.dumps({
        'success': True,
        'duplicatesRemoved': duplicates,
        'message': f'Removed {duplicates} duplicate row(s)'
    }, indent=2)


@mcp.tool()
def sheets_trim_whitespace(
    spreadsheet_id: str,
    sheet_id: int,
    start_row: int,
    end_row: int,
    start_col: int,
    end_col: int
) -> str:
    """
    Trim leading/trailing whitespace from all cells in range.
    """
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    requests = [{
        'trimWhitespace': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': start_row,
                'endRowIndex': end_row,
                'startColumnIndex': start_col,
                'endColumnIndex': end_col
            }
        }
    }]

    result = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    cells_trimmed = result.get('replies', [{}])[0].get('trimWhitespace', {}).get('cellsChangedCount', 0)

    return json.dumps({
        'success': True,
        'cellsTrimmed': cells_trimmed,
        'message': f'Trimmed whitespace from {cells_trimmed} cell(s)'
    }, indent=2)


@mcp.tool()
def sheets_merge_cells(
    spreadsheet_id: str,
    sheet_id: int,
    start_row: int,
    end_row: int,
    start_col: int,
    end_col: int,
    merge_type: str = 'MERGE_ALL'
) -> str:
    """
    Merge cells in range.
    merge_type: MERGE_ALL, MERGE_COLUMNS, MERGE_ROWS
    """
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    requests = [{
        'mergeCells': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': start_row,
                'endRowIndex': end_row,
                'startColumnIndex': start_col,
                'endColumnIndex': end_col
            },
            'mergeType': merge_type
        }
    }]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    return json.dumps({
        'success': True,
        'message': f'Merged cells with type: {merge_type}'
    }, indent=2)


@mcp.tool()
def sheets_copy_paste(
    spreadsheet_id: str,
    source_sheet_id: int,
    source_start_row: int,
    source_end_row: int,
    source_start_col: int,
    source_end_col: int,
    dest_sheet_id: int,
    dest_start_row: int,
    dest_start_col: int,
    paste_type: str = 'NORMAL'
) -> str:
    """
    Copy and paste range. paste_type: NORMAL, VALUES, FORMAT, FORMULA, etc.
    """
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    requests = [{
        'copyPaste': {
            'source': {
                'sheetId': source_sheet_id,
                'startRowIndex': source_start_row,
                'endRowIndex': source_end_row,
                'startColumnIndex': source_start_col,
                'endColumnIndex': source_end_col
            },
            'destination': {
                'sheetId': dest_sheet_id,
                'startRowIndex': dest_start_row,
                'startColumnIndex': dest_start_col
            },
            'pasteType': paste_type
        }
    }]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    return json.dumps({
        'success': True,
        'message': f'Copied range with paste type: {paste_type}'
    }, indent=2)


# ============================================================================
# FORMATTING
# ============================================================================

@mcp.tool()
def sheets_format_cells(
    spreadsheet_id: str,
    sheet_id: int,
    start_row: int,
    end_row: int,
    start_col: int,
    end_col: int,
    bold: Optional[bool] = None,
    italic: Optional[bool] = None,
    font_size: Optional[int] = None,
    bg_color: Optional[str] = None,
    text_color: Optional[str] = None
) -> str:
    """Format cells (bold, italic, font size, colors). Colors as hex like #FF0000"""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    cell_format = {}
    text_format = {}

    if bold is not None:
        text_format['bold'] = bold
    if italic is not None:
        text_format['italic'] = italic
    if font_size is not None:
        text_format['fontSize'] = font_size

    if text_color:
        color = text_color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) / 255 for i in (0, 2, 4))
        text_format['foregroundColor'] = {'red': r, 'green': g, 'blue': b}

    if text_format:
        cell_format['textFormat'] = text_format

    if bg_color:
        color = bg_color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) / 255 for i in (0, 2, 4))
        cell_format['backgroundColor'] = {'red': r, 'green': g, 'blue': b}

    requests = [{
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': start_row,
                'endRowIndex': end_row,
                'startColumnIndex': start_col,
                'endColumnIndex': end_col
            },
            'cell': {'userEnteredFormat': cell_format},
            'fields': 'userEnteredFormat'
        }
    }]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    return json.dumps({'success': True}, indent=2)


@mcp.tool()
def sheets_add_borders(
    spreadsheet_id: str,
    sheet_id: int,
    start_row: int,
    end_row: int,
    start_col: int,
    end_col: int,
    style: str = "SOLID",
    color: str = "#000000"
) -> str:
    """Add borders to cells. Style: SOLID, DASHED, DOTTED"""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    hex_color = color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))

    border_style = {
        'style': style,
        'color': {'red': r, 'green': g, 'blue': b}
    }

    requests = [{
        'updateBorders': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': start_row,
                'endRowIndex': end_row,
                'startColumnIndex': start_col,
                'endColumnIndex': end_col
            },
            'top': border_style,
            'bottom': border_style,
            'left': border_style,
            'right': border_style,
            'innerHorizontal': border_style,
            'innerVertical': border_style
        }
    }]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    return json.dumps({'success': True}, indent=2)


# ============================================================================
# CHARTS
# ============================================================================

@mcp.tool()
def sheets_add_chart(
    spreadsheet_id: str,
    sheet_id: int,
    chart_type: str,
    data_range: str,
    title: str,
    row: int = 0,
    col: int = 0
) -> str:
    """
    Add a chart. Types: COLUMN, BAR, LINE, PIE, SCATTER
    data_range like 'Sheet1!A1:B10'
    """
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    requests = [{
        'addChart': {
            'chart': {
                'spec': {
                    'title': title,
                    'basicChart': {
                        'chartType': chart_type,
                        'legendPosition': 'RIGHT_LEGEND',
                        'axis': [
                            {'position': 'BOTTOM_AXIS'},
                            {'position': 'LEFT_AXIS'}
                        ],
                        'domains': [{
                            'domain': {
                                'sourceRange': {
                                    'sources': [{'sheetId': sheet_id, 'startRowIndex': 0, 'startColumnIndex': 0}]
                                }
                            }
                        }],
                        'series': [{
                            'series': {
                                'sourceRange': {
                                    'sources': [{'sheetId': sheet_id}]
                                }
                            }
                        }]
                    }
                },
                'position': {
                    'overlayPosition': {
                        'anchorCell': {
                            'sheetId': sheet_id,
                            'rowIndex': row,
                            'columnIndex': col
                        }
                    }
                }
            }
        }
    }]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    return json.dumps({'success': True}, indent=2)


# ============================================================================
# DATA VALIDATION & CONDITIONAL FORMATTING
# ============================================================================

@mcp.tool()
def sheets_add_dropdown(
    spreadsheet_id: str,
    sheet_id: int,
    start_row: int,
    end_row: int,
    start_col: int,
    end_col: int,
    values: List[str]
) -> str:
    """Add dropdown list validation to cells"""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    requests = [{
        'setDataValidation': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': start_row,
                'endRowIndex': end_row,
                'startColumnIndex': start_col,
                'endColumnIndex': end_col
            },
            'rule': {
                'condition': {
                    'type': 'ONE_OF_LIST',
                    'values': [{'userEnteredValue': v} for v in values]
                },
                'showCustomUi': True
            }
        }
    }]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    return json.dumps({'success': True}, indent=2)


@mcp.tool()
def sheets_conditional_format(
    spreadsheet_id: str,
    sheet_id: int,
    start_row: int,
    end_row: int,
    start_col: int,
    end_col: int,
    condition_type: str,
    condition_value: str,
    bg_color: str
) -> str:
    """
    Add conditional formatting.
    condition_type: NUMBER_GREATER, NUMBER_LESS, TEXT_CONTAINS, etc.
    condition_value: value to compare
    bg_color: hex color like #00FF00
    """
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    hex_color = bg_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))

    requests = [{
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{
                    'sheetId': sheet_id,
                    'startRowIndex': start_row,
                    'endRowIndex': end_row,
                    'startColumnIndex': start_col,
                    'endColumnIndex': end_col
                }],
                'booleanRule': {
                    'condition': {
                        'type': condition_type,
                        'values': [{'userEnteredValue': condition_value}]
                    },
                    'format': {
                        'backgroundColor': {'red': r, 'green': g, 'blue': b}
                    }
                }
            },
            'index': 0
        }
    }]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    return json.dumps({'success': True}, indent=2)


# ============================================================================
# SORT & FILTER
# ============================================================================

@mcp.tool()
def sheets_sort_range(
    spreadsheet_id: str,
    sheet_id: int,
    start_row: int,
    end_row: int,
    start_col: int,
    end_col: int,
    sort_column: int,
    ascending: bool = True
) -> str:
    """Sort a range by a column"""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    requests = [{
        'sortRange': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': start_row,
                'endRowIndex': end_row,
                'startColumnIndex': start_col,
                'endColumnIndex': end_col
            },
            'sortSpecs': [{
                'dimensionIndex': sort_column,
                'sortOrder': 'ASCENDING' if ascending else 'DESCENDING'
            }]
        }
    }]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    return json.dumps({'success': True}, indent=2)


if __name__ == "__main__":
    mcp.run()
