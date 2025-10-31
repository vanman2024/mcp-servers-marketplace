#!/bin/bash
# Startup script for Figma Marketing MCP Server

echo "Starting Figma Marketing MCP Server on port 8032..."

# Change to the server directory
cd "$(dirname "$0")"

# Kill any existing server on port 8032
echo "Checking for existing server on port 8032..."
lsof -ti:8032 | xargs kill -9 2>/dev/null || true

# Start the server
echo "Starting server..."
python src/figma_marketing_server.py

# Keep the script running
wait