#!/bin/bash
set -e

echo ""
echo "[*] Instagram Profile Card Service - Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "[!] uv not found. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi
echo "[+] uv installed ✓"

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "[!] Python 3.10+ required. Found: $PYTHON_VERSION"
    exit 1
fi
echo "[+] Python version: $PYTHON_VERSION ✓"

# Sync dependencies with uv
echo "[*] Syncing dependencies with uv..."
uv sync
echo "[+] Dependencies synced ✓"

# Create .env from example if not exists
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "[+] Created .env from .env.example"
        echo "[!] Please edit .env with your configuration"
    fi
else
    echo "[+] .env file exists ✓"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[+] Setup complete!"
echo ""
echo "  Next steps:"
echo "    1. Edit .env with your proxy credentials"
echo "    2. Run ./start.sh to start the service"
echo ""
echo "  Commands:"
echo "    ./start.sh   - Start service"
echo "    ./stop.sh    - Stop service"
echo "    ./setup.sh   - Re-run setup"
echo ""
