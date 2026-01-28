#!/bin/bash
# Desktop File Maker - Test Script for Arch Linux

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Run tests
python -m pytest tests/ "$@"
