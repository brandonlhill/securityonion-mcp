#!/bin/bash

# ------------------------------------------------------------------------------
# Builder script using Nuitka to compile a fully standalone Python 3.10 binary.
# Ensures patchelf is installed and includes .dist-info for packages that rely
# on importlib.metadata (e.g., urllib3, elastic_transport).
# ------------------------------------------------------------------------------

set -e

# Ensure virtual environment exists
if [ ! -f ".venv/bin/activate" ]; then
    echo "[ERROR] Virtual environment not found at .venv/bin/activate"
    echo "        Please run ./install.sh first to create the environment."
    exit 1
fi

# Activate virtualenv (assumes Python 3.10 inside)
source .venv/bin/activate

# Configuration
SCRIPT_PATH="server.py"
EXEC_NAME="server"
BUILD_DIR="build"
DIST_DIR="dist"

# Ensure source script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "[ERROR] Could not find script: $SCRIPT_PATH"
    exit 1
fi

# Ensure Nuitka and ccache are installed
if ! command -v nuitka &> /dev/null; then
    echo "[INFO] Installing Nuitka and ccache into virtualenv..."
    pip install nuitka ccache
fi

# Ensure patchelf is installed
if ! command -v patchelf &> /dev/null; then
    echo "[INFO] Installing patchelf..."
    if command -v apt &> /dev/null; then
        sudo apt install -y patchelf
    else
        echo "[ERROR] Could not install patchelf automatically (non-Debian system)."
        echo "Please install patchelf manually and re-run this script."
        exit 1
    fi
fi

# Clean previous builds
echo "[INFO] Cleaning old build artifacts..."
rm -rf "$BUILD_DIR" "$DIST_DIR" __pycache__ ./*.build ./*.dist ./*.onefile-build ./*.onefile-dist

mkdir -p "$DIST_DIR"

# Locate .dist-info metadata directories
SITE_PACKAGES=$(python -c "import site; print(site.getsitepackages()[0])")

DIST_INFO_FLAGS=()
for pkg in urllib3 elastic_transport certifi setuptools; do
    info_dir=$(find "$SITE_PACKAGES" -maxdepth 1 -name "${pkg}-*.dist-info" | head -n 1)
    if [ -n "$info_dir" ]; then
        DIST_INFO_FLAGS+=("--include-data-dir=${info_dir}=$(basename "$info_dir")")
    else
        echo "[WARN] Could not find dist-info for $pkg"
    fi
done

# Build the standalone binary
echo "[INFO] Building with Nuitka..."

nuitka \
    --standalone \
    --include-package=urllib3,elastic_transport,certifi,setuptools \
    --include-package-data=urllib3,elastic_transport,certifi,setuptools \
    --nofollow-import-to=tkinter \
    --remove-output \
    --output-dir="$DIST_DIR" \
    --output-filename="$EXEC_NAME" \
    --jobs=$(nproc) \
    "$SCRIPT_PATH"

echo "[INFO] Build complete: $DIST_DIR/$EXEC_NAME"
