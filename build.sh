#!/bin/bash

# NOTE: This is a builder script that leverages pyinstaller to build a python standalone binary

# Exit on error
set -e

# Ensure virtual environment is available
if [ ! -f ".venv/bin/activate" ]; then
    echo "[ERROR] Virtual environment not found at .venv/bin/activate"
    echo "        Please run ./install.sh first to create the environment."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Configuration
SCRIPT_PATH="server.py"
EXEC_NAME="server"
DIST_DIR="dist"
BUILD_DIR="build"

# Check for PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing it..."
    pip install pyinstaller
fi

# Check if script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Could not find script: $SCRIPT_PATH"
    exit 1
fi

# Clean old build artifacts
echo "Cleaning old build artifacts..."
rm -rf "$DIST_DIR" "$BUILD_DIR" *.spec __pycache__

# Build executable
echo "Building executable from $SCRIPT_PATH..."
pyinstaller \
  --onefile \
  --name "$EXEC_NAME" \
  --distpath "$DIST_DIR" \
  --workpath "$BUILD_DIR" \
  "$SCRIPT_PATH"

# Done
echo "Build complete."
echo "Executable located at: $DIST_DIR/$EXEC_NAME"
