#!/bin/bash

# This script sets up the runtime environment for the Security Onion–Assemblyline middleware project (so-mcp). 
# Specifically, it performs the following tasks:
#
#    Checks for Python 3
#    Verifies that Python 3 is installed on the system.
#
#    Ensures the venv module is available
#    If the Python venv module is missing, it installs it via apt.
#
#    Creates a Python virtual environment
#    Sets up an isolated Python environment in the .venv/ directory to avoid polluting the global Python environment.
#
#    Activates the virtual environment and upgrades pip
#    Ensures pip is up to date inside the virtual environment.
#
#    Installs Python dependencies
#    Installs packages listed in requirements.txt (if it exists).
#
#    Initializes the configuration file
#    Runs config.py, which ensures that a configuration file is created at ~/.so-mcp/config.ini with the correct structure and secure file permissions (read/write only for the user). If the file is missing or incomplete, config.py prompts the user to enter the necessary values for Elasticsearch connection.
#
#    Makes key project files executable
#    Ensures server.py and run.sh are marked as executable so they can be run directly.

VENV_DIR=".venv"

echo "[Installer] Checking for Python 3..."
if ! command -v python3 &>/dev/null; then
    echo "Python3 not found. Please install it."
    exit 1
fi

echo "[Installer] Checking for venv module..."
if ! python3 -m venv --help &>/dev/null; then
    echo "python3-venv not found. Installing..."
    sudo apt update && sudo apt install -y python3-venv
fi

echo "[Installer] Creating virtual environment at $VENV_DIR..."
python3 -m venv "$VENV_DIR"


echo "[Installer] Activating virtual environment..."
#shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "[Installer] Upgrading pip..."
pip install --upgrade pip

echo "[Installer] Installing requirements..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping pip install."
fi

echo ""
echo ""
echo "[Installer] Running config.py to create ~/.so-mcp/config.ini"
python3 config.py
echo ""
echo ""

chmod +x server.py run.sh

echo
echo "[Setup complete]"
echo "Run 'source $VENV_DIR/bin/activate' to activate your environment."