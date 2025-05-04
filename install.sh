#!/bin/bash

ENV_FILE=".env"
VENV_DIR=".venv"
REQUIRED_VARS=("ELASTICSEARCH_HOST" "ELASTICSEARCH_USERNAME" "ELASTICSEARCH_PASSWORD")

echo "[ENV_FILE Installer]"

# Ensure .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "📄 Creating $ENV_FILE..."
    touch "$ENV_FILE"
fi

# Read existing values from .env into a map (no export)
declare -A env_values
while IFS='=' read -r key value; do
    [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
    # Remove surrounding quotes if present
    value="${value%\"}"
    value="${value#\"}"
    env_values["$key"]="$value"
done < "$ENV_FILE"

# Prompt user for any missing values (no shell export)
for VAR in "${REQUIRED_VARS[@]}"; do
    CURRENT_VALUE="${env_values[$VAR]}"
    if [ -z "$CURRENT_VALUE" ]; then
        if [[ "$VAR" == "ELASTICSEARCH_PASSWORD" ]]; then
            read -rsp "🔐 Enter value for $VAR: " INPUT
            echo
        else
            read -rp "📝 Enter value for $VAR: " INPUT
        fi
        # Escape `&` only, not slashes
        INPUT_ESCAPED=$(printf '%s\n' "$INPUT" | sed 's/[&]/\\&/g')
        # Remove existing entry if present
        sed -i "/^$VAR=/d" "$ENV_FILE"
        # Add quoted value to .env
        echo "$VAR=\"$INPUT_ESCAPED\"" >> "$ENV_FILE"
    else
        echo "✅ $VAR already present in .env"
    fi
done

echo "[PYTHON Installer]"
echo "Checking for Python 3..."
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 not found. Please install it and try again."
    exit 1
fi

echo "[INFO] Checking for venv module..."
if ! python3 -m venv --help &>/dev/null; then
    echo "⚠️ python3-venv not found. Installing with apt..."
    sudo apt update && sudo apt install -y python3-venv
fi

echo "[VENV_DIR Installer]"
echo "[INFO] Creating virtual environment in $VENV_DIR..."
python3 -m venv "$VENV_DIR"

echo "[INFO] Activating virtual environment..."
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "[INFO] Upgrading pip..."
pip install --upgrade pip

echo "[INFO] Installing dependencies from requirements.txt..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found!"
    deactivate
    exit 1
fi

# Helper
chmod +x server.py run.sh

echo "[NOTICE - README]"
echo "✅ Setup complete."
echo "✅ Virtual environment is now active."
echo "📌 To activate it in the future, run:"
echo "    source $VENV_DIR/bin/activate"
echo "📌 Run your software only while the virtual environment is active."
