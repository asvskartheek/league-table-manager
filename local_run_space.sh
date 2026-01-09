#!/bin/bash

# Local test script for HuggingFace Space
# Loads environment variables from .env and runs the app

# Check if .env.local file exists
if [ ! -f .env.local ]; then
    echo "Error: .env file not found!"
    echo "Please create a .env.local file with your HF_TOKEN"
    echo "Example:"
    echo "  HF_TOKEN=hf_your_token_here"
    exit 1
fi

# Load environment variables from .env.local
echo "Loading environment variables from .env.local..."
export $(grep -v '^#' .env.local | xargs)

echo "Environment loaded successfully"
echo "Starting application..."

# Run the app with uv
uv run app.py
