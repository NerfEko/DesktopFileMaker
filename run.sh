#!/bin/bash
# Desktop File Maker - Run Script for Arch Linux

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Add the project directory to Python path
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Run the application
python -m src.main "$@"
