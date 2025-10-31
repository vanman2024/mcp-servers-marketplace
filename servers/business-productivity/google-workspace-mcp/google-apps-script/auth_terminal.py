#!/usr/bin/env python3
"""Terminal-based OAuth for Apps Script - no browser required"""

import os
import json
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/script.projects',
    'https://www.googleapis.com/auth/script.deployments',
    'https://www.googleapis.com/auth/script.processes',
    'https://www.googleapis.com/auth/script.scriptapp',  # Required for scripts.run
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/tasks'  # Required for Tasks API in script
]

creds_dir = os.path.expanduser('~/.config/mcp-gdrive')
credentials_file = os.path.join(creds_dir, 'gcp-oauth.keys.json')
token_file = os.path.join(creds_dir, 'apps-script-token.json')

# Load client config
with open(credentials_file) as f:
    client_config = json.load(f)

# Create OOB flow (Out Of Band - manual code entry)
flow = Flow.from_client_config(
    client_config,
    scopes=SCOPES,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
)

# Generate authorization URL
auth_url, state = flow.authorization_url(
    access_type='offline',
    prompt='consent'
)

print("\n" + "="*80)
print("GOOGLE APPS SCRIPT AUTHENTICATION")
print("="*80)
print("\n1. Visit this URL in your browser:\n")
print(f"   {auth_url}\n")
print("2. Grant permissions")
print("3. Copy the authorization code")
print("4. Paste it below\n")
print("-"*80)

# Get code from user
code = input("Enter authorization code: ").strip()

# Exchange code for token
flow.fetch_token(code=code)
creds = flow.credentials

# Save token
os.makedirs(creds_dir, exist_ok=True)
with open(token_file, 'w') as f:
    f.write(creds.to_json())

print("\n" + "="*80)
print("SUCCESS! Token saved to:")
print(f"   {token_file}")
print("="*80 + "\n")
