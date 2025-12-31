#!/bin/bash

# Local test script for HuggingFace Space
# Loads environment variables from .env and runs the app

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create a .env file with your HF_TOKEN"
    echo "Example:"
    echo "  HF_TOKEN=hf_your_token_here"
    exit 1
fi

# Load environment variables from .env
echo "Loading environment variables from .env..."
export $(grep -v '^#' .env | xargs)

# Verify HF_TOKEN is set
if [ -z "$HF_TOKEN" ]; then
    echo "Warning: HF_TOKEN not found in .env file"
    echo "Please add: HF_TOKEN=hf_your_token_here"
    exit 1
fi

echo "Environment loaded successfully"
echo "Starting application..."

# Run the app with uv
uv run app.py
