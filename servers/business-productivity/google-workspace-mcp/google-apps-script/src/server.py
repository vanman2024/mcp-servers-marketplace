#!/usr/bin/env python3
"""Google Apps Script MCP Server - FastMCP for Apps Script management"""

import os
from fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Optional, List, Dict, Any
import json

SCOPES = [
    'https://www.googleapis.com/auth/script.projects',
    'https://www.googleapis.com/auth/script.deployments',
    'https://www.googleapis.com/auth/script.processes',
    'https://www.googleapis.com/auth/script.scriptapp',  # Required for scripts.run
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/tasks'  # Required for Tasks API in script
]

mcp = FastMCP("Google Apps Script", dependencies=["google-auth", "google-api-python-client"])

_creds: Optional[Credentials] = None


def get_credentials():
    """Get or refresh Google OAuth credentials"""
    global _creds
    if _creds:
        return _creds

    creds_dir = os.getenv('GDRIVE_CREDS_DIR', os.path.expanduser('~/.config/mcp-gdrive'))
    token_file = os.path.join(creds_dir, 'apps-script-token.json')
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
def authenticate() -> str:
    """Manually trigger OAuth authentication for Apps Script"""
    global _creds
    _creds = None  # Clear cached credentials

    # Remove existing token to force fresh auth
    creds_dir = os.getenv('GDRIVE_CREDS_DIR', os.path.expanduser('~/.config/mcp-gdrive'))
    token_file = os.path.join(creds_dir, 'apps-script-token.json')
    if os.path.exists(token_file):
        os.remove(token_file)

    # Trigger OAuth flow
    creds = get_credentials()

    return json.dumps({
        "success": True,
        "message": "Authentication successful! Apps Script token saved.",
        "token_valid": creds.valid
    }, indent=2)


@mcp.tool()
def run_script_function(script_id: str, function_name: str, parameters: Optional[List[Any]] = None, dev_mode: bool = True) -> str:
    """
    Execute a function in Apps Script project

    Args:
        script_id: The script project ID
        function_name: Name of function to execute
        parameters: Optional list of parameters to pass
        dev_mode: If True, run latest code instead of deployed version (default: True)
    """
    creds = get_credentials()
    service = build('script', 'v1', credentials=creds)

    request_body = {
        "function": function_name,
        "devMode": dev_mode
    }

    if parameters:
        request_body["parameters"] = parameters

    response = service.scripts().run(
        scriptId=script_id,
        body=request_body
    ).execute()

    if 'error' in response:
        return json.dumps({
            "success": False,
            "error": response['error']
        }, indent=2)

    return json.dumps({
        "success": True,
        "response": response.get('response', {}),
        "result": response.get('response', {}).get('result')
    }, indent=2)


@mcp.tool()
def get_script_project(script_id: str) -> str:
    """Get Apps Script project details"""
    creds = get_credentials()
    service = build('script', 'v1', credentials=creds)

    project = service.projects().get(scriptId=script_id).execute()

    return json.dumps(project, indent=2)


@mcp.tool()
def list_script_processes(script_id: str, page_size: int = 10) -> str:
    """
    List processes for a specific script

    Args:
        script_id: The script project ID
        page_size: Number of processes to return (max 100)
    """
    creds = get_credentials()
    service = build('script', 'v1', credentials=creds)

    processes = service.processes().listScriptProcesses(
        scriptId=script_id,
        pageSize=min(page_size, 100)
    ).execute()

    return json.dumps(processes.get('processes', []), indent=2)


@mcp.tool()
def get_project_metrics(script_id: str) -> str:
    """Get metrics data for script project (executions, active users, etc.)"""
    creds = get_credentials()
    service = build('script', 'v1', credentials=creds)

    metrics = service.projects().getMetrics(
        scriptId=script_id
    ).execute()

    return json.dumps(metrics, indent=2)


@mcp.tool()
def create_version(script_id: str, description: str) -> str:
    """
    Create a new immutable version of the script

    Args:
        script_id: The script project ID
        description: Version description
    """
    creds = get_credentials()
    service = build('script', 'v1', credentials=creds)

    version = service.projects().versions().create(
        scriptId=script_id,
        body={'description': description}
    ).execute()

    return json.dumps(version, indent=2)


@mcp.tool()
def list_versions(script_id: str, page_size: int = 10) -> str:
    """List all versions of a script project"""
    creds = get_credentials()
    service = build('script', 'v1', credentials=creds)

    versions = service.projects().versions().list(
        scriptId=script_id,
        pageSize=min(page_size, 200)
    ).execute()

    return json.dumps(versions.get('versions', []), indent=2)


@mcp.tool()
def create_deployment(script_id: str, version_number: int, description: str) -> str:
    """
    Create a deployment for Apps Script project

    Args:
        script_id: The script project ID
        version_number: Version number to deploy
        description: Deployment description
    """
    creds = get_credentials()
    service = build('script', 'v1', credentials=creds)

    deployment_config = {
        "versionNumber": version_number,
        "manifestFileName": "appsscript",
        "description": description
    }

    deployment = service.projects().deployments().create(
        scriptId=script_id,
        body={"deploymentConfig": deployment_config}
    ).execute()

    return json.dumps(deployment, indent=2)


@mcp.tool()
def list_deployments(script_id: str) -> str:
    """List all deployments for a script project"""
    creds = get_credentials()
    service = build('script', 'v1', credentials=creds)

    deployments = service.projects().deployments().list(
        scriptId=script_id
    ).execute()

    return json.dumps(deployments.get('deployments', []), indent=2)


if __name__ == "__main__":
    mcp.run()
