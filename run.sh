#!/bin/bash

# Find a Python 3.10+ interpreter
PYTHON=""
for BIN in python3.12 python3.11 python3.10; do
    if command -v $BIN >/dev/null 2>&1; then
        VERSION=$($BIN -c 'import sys; print(sys.version_info[:2] >= (3, 10))')
        if [ "$VERSION" = "True" ]; then
            PYTHON=$BIN
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "Error: No Python interpreter >= 3.10 found."
    exit 1
fi

echo "Using Python interpreter: $PYTHON"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    $PYTHON -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Run the server
$PYTHON ./server.py
