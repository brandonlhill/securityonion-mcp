#!/bin/bash

# This script sets up the runtime environment for the Security Onion–Assemblyline middleware project (so-mcp).
# It dynamically selects a Python 3.10+ interpreter, sets up a venv, installs dependencies, runs config.py, and sets permissions.

VENV_DIR=".venv"

# === Step 1: Find Python >= 3.10 ===
echo "[Installer] Searching for Python ≥ 3.10..."
PYTHON=""
for BIN in python3.12 python3.11 python3.10; do
    if command -v "$BIN" &>/dev/null; then
        VERSION=$($BIN -c 'import sys; print(sys.version_info >= (3, 10))')
        if [[ "$VERSION" == "True" ]]; then
            PYTHON="$BIN"
            break
        fi
    fi
done

if [[ -z "$PYTHON" ]]; then
    echo "[Error] No compatible Python (>=3.10) found."
    exit 1
fi

echo "[Installer] Using Python interpreter: $PYTHON"

# === Step 2: Ensure venv module is available ===
echo "[Installer] Checking for venv support..."
if ! "$PYTHON" -m venv --help &>/dev/null; then
    echo "[Installer] Missing venv module. Installing python3-venv..."
    sudo apt update && sudo apt install -y python3-venv
fi

# === Step 3: Create virtual environment ===
echo "[Installer] Creating virtual environment at $VENV_DIR..."
"$PYTHON" -m venv "$VENV_DIR"

# === Step 4: Activate venv ===
echo "[Installer] Activating virtual environment..."
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# === Step 5: Upgrade pip ===
echo "[Installer] Upgrading pip..."
pip install --upgrade pip

# === Step 6: Install dependencies ===
echo "[Installer] Installing requirements..."
if [[ -f requirements.txt ]]; then
    pip install -r requirements.txt
else
    echo "[Installer] No requirements.txt found. Skipping."
fi

# === Step 7: Initialize config ===
echo
echo "[Installer] Running config.py to create ~/.so-mcp/config.ini..."
"$PYTHON" config.py
echo

# === Step 8: Set executable permissions ===
echo "[Installer] Marking project scripts executable..."
chmod +x server.py run.sh

# === Done ===
echo
echo "[Setup complete]"
echo "Run 'source $VENV_DIR/bin/activate' to activate your environment."
