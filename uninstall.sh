#!/bin/bash

VENV_DIR=".venv"
CONFIG_DIR="$HOME/.so-mcp"
CONFIG_FILE="$CONFIG_DIR/config.ini"

echo "[Uninstaller] Starting cleanup..."

# Deactivate venv if active
if [[ "$VIRTUAL_ENV" == "$(pwd)/$VENV_DIR" ]]; then
    echo "[Uninstaller] Deactivating virtual environment..."
    deactivate
fi

# Remove virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "[Uninstaller] Removing virtual environment: $VENV_DIR"
    rm -rf "$VENV_DIR"
else
    echo "[Uninstaller] No virtual environment found at $VENV_DIR"
fi

# Remove config file
if [ -f "$CONFIG_FILE" ]; then
    echo "[Uninstaller] Removing config file: $CONFIG_FILE"
    rm -f "$CONFIG_FILE"
else
    echo "[Uninstaller] No config file found at $CONFIG_FILE"
fi

# Remove config directory if empty
if [ -d "$CONFIG_DIR" ] && [ -z "$(ls -A "$CONFIG_DIR")" ]; then
    echo "[Uninstaller] Removing empty config directory: $CONFIG_DIR"
    rmdir "$CONFIG_DIR"
fi

echo "[Uninstaller] Cleanup complete."
