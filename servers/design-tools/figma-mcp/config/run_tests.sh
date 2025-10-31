#!/bin/bash
# Run tests for Figma MCP Server

set -e

# Navigate to script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install test dependencies
echo "Installing test dependencies..."
pip install -q pytest pytest-asyncio pytest-mock pytest-cov

# Run tests with coverage
echo "Running tests..."
if [ "$1" = "--coverage" ]; then
    python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term
    echo "Coverage report generated in htmlcov/index.html"
else
    python -m pytest tests/ -v
fi

# Run specific auth tests if requested
if [ "$1" = "--auth" ]; then
    python -m pytest tests/test_auth_validation.py -v
fi